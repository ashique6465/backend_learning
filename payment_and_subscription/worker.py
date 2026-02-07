import pika
import json
import time
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

print("EMAIL:", EMAIL_ADDRESS)
print("PASS LENGTH:", len(EMAIL_PASSWORD))


#sending the real email using smtplib
def send_email(order_id):
    msg = EmailMessage()
    msg["Subject"] = "Payment Successful ✅"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg.set_content(
        f"""
Hi 👋

Your payment was successful!

Order ID: {order_id}

Thank you for your purchase 🚀
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("📧 Real email sent!")


#starting the worker to listen for payment events and send emails
def start_worker():
    print("🚀 Worker starting...")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )

    channel = connection.channel()
    channel.queue_declare(queue="payment_success", durable=True)

    print("📦 Waiting for messages...")

    def callback(ch, method, properties, body):
        data = json.loads(body)
        order_id = data["order_id"]

        print("📨 Payment event received:", data)

        send_email(order_id)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue="payment_success",
        on_message_callback=callback
    )

    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
