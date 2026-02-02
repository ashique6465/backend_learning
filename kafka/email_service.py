from kafka import KafkaConsumer
import json 
import time 


#consumer setup
consumer = KafkaConsumer(
    "order-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer= lambda m: json.loads(m.decode("utf-8")),
    group_id="email-service"
)

print("Email service started...")

for message in consumer:
    event = message.value 
    print(f"Sending email to {event['email']} for order {event['order_id']}")
    time.sleep(1)
    print("Email sent!")