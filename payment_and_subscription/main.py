import os 
import json
import stripe
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv
from rabbitmq import publish_payment_success
from database import SessionLocal
from models import Order

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

app = FastAPI()

#Home Page

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>FastAPI Stripe Payment</title>
        </head>
        <body style="text-align:center;margin-top:100px;">
            <h2>FastAPI Stripe Payment Gateway</h2>

            <button onclick="pay()" 
                style="padding:15px 25px;font-size:18px;">
                Pay ₹500
            </button>

            <script>
                async function pay() {
                    const res = await fetch("/create-checkout-session", {
                        method: "POST"
                    });
                    const data = await res.json();
                    window.location.href = data.url;
                }
            </script>
        </body>
    </html>
    """

#create checkout session
@app.post("/create-checkout-session")
def create_checkout_session():
    db = SessionLocal()
    
    order = Order(status="PENDING")
    db.add(order)
    db.commit()
    db.refresh(order)
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": "FastAPI Course",
                    },
                    "unit_amount": 50000,
                },
                "quantity":1,
            }
        ],
        mode="payment",
        success_url="https://fact-michelle-writes-fork.trycloudflare.com/success",
        cancel_url="https://fact-michelle-writes-fork.trycloudflare.com/cancel",
    )

    order.stripe_session_id = session.id 
    db.commit()

    return JSONResponse({"url": session.url})

@app.get("/success", response_class=HTMLResponse)
def success():
    return "<h1>Payment Successful</h1>"


@app.get("/cancel", response_class=HTMLResponse)
def cancel():
    return "<h1>Payment Cancelled</h1>"



#Stripe webhook
@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig,
            WEBHOOK_SECRET
        )
    except Exception as e:
        return {"error": str(e)}

    print("🔔 Webhook received:", event["type"])

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        db = SessionLocal()
        order = db.query(Order).filter(
            Order.stripe_session_id == session["id"]
        ).first()

        if order:
            order.status = "PAID"
            db.commit()

            publish_payment_success({
                "order_id": order.id
            })

    return {"status": "ok"}
