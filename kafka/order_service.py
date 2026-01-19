from fastapi import FastAPI 
from kafka import KafkaProducer
import json 

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer= lambda v: json.dumps(v).encode("utf-8")
)


@app.post("/order")
def place_order(order_id: int, email: str):
    event = {
        "event": "ORDER_CREATED",
        "order_id": order_id,
        "email": email
    }

    producer.send("order-events", event)
    producer.flush()

    return {"message": "Order placed successfully"}