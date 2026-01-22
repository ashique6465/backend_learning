import os 
import stripe
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv

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

@app.post("/create-checkout-session")
def create_checkout_session():
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
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )
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
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )

    except Exception:
        return JSONResponse({"error": "Invalid signature"}, status_code=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        print("Payment confirmed for:", session["id"])

    return {"status": "success"}