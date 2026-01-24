import pika 
import json

def publish_payment_success(message: dict):
    print("📤 Publishing message to RabbitMQ:", message)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    channel.queue_declare(queue="payment_success", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="payment_success",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    connection.close()
    print("✅ Message published")