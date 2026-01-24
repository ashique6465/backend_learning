import pika
import json
import time

def start_worker():
    print("🚀 Starting worker...")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    print("✅ Connected to RabbitMQ")

    channel = connection.channel()

    channel.queue_declare(queue="payment_success", durable=True)
    print("📦 Waiting for messages in 'payment_success' queue...")

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print("📨 Payment event received:", data)

        time.sleep(2)  # simulate email sending
        print("📧 Email sent for order:", data["order_id"])

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="payment_success",
        on_message_callback=callback
    )

    # 🔥 THIS LINE MUST BLOCK FOREVER
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
