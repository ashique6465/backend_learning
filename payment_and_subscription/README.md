# Payment and Subscription Service

A FastAPI-based payment processing service integrated with Stripe for handling checkout sessions, webhooks, and email notifications via RabbitMQ.

## Architecture

```
┌─────────────┐
│   FastAPI   │─── Stripe Checkout ───┐
│   Server    │                        │
└─────────────┘                        │
      │                          ┌─────▼──────┐
      │                          │   Stripe   │
      │                          └─────┬──────┘
      │                                │
      └──────────────────┬─────────────┘
                         │
                    Webhook Event
                         │
      ┌──────────────────▼──────────────────┐
      │       Order DB (PostgreSQL)         │
      └──────────────────┬──────────────────┘
                         │
              payment_success event
                         │
      ┌──────────────────▼──────────────────┐
      │         RabbitMQ (Message Queue)    │
      └──────────────────┬──────────────────┘
                         │
      ┌──────────────────▼──────────────────┐
      │      Email Worker (Background Job)  │
      └──────────────────────────────────────┘
```

## Features

- 💳 Stripe checkout session creation
- 🔐 Webhook signature verification
- 📧 Email notifications via RabbitMQ
- 💾 Order status tracking in PostgreSQL
- 🐳 Docker & docker-compose support
- 🔄 CI/CD with GitHub Actions

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- RabbitMQ 3.12+
- Stripe API keys
- Gmail account with app password

## Setup

### Local Development

1. **Clone and install dependencies:**
   ```bash
   cd payment_and_subscription
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Initialize database:**
   ```bash
   python create_tables.py
   ```

4. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Run the worker (in another terminal):**
   ```bash
   python worker.py
   ```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f payment-service

# Stop services
docker-compose down
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with payment button |
| POST | `/create-checkout-session` | Create Stripe checkout session |
| GET | `/success` | Success page after payment |
| GET | `/cancel` | Cancellation page |
| POST | `/webhook` | Stripe webhook receiver |

## Environment Variables

See `.env.example` for all required variables:

```
DATABASE_URL           # PostgreSQL connection string
STRIPE_SECRET_KEY      # Stripe API secret key
STRIPE_WEBHOOK_SECRET  # Stripe webhook signing secret
GMAIL_ADDRESS          # Email sender address
GMAIL_APP_PASSWORD     # Gmail app password
```

## Key Files

- **main.py** - FastAPI app with Stripe integration and webhooks
- **worker.py** - Background email notification worker
- **database.py** - SQLAlchemy session factory
- **models.py** - Order model
- **rabbitmq.py** - RabbitMQ publisher utility
- **create_tables.py** - Database initialization script

## Payment Flow

1. User clicks "Pay ₹500" button on home page
2. Frontend calls `/create-checkout-session`
3. Backend creates Stripe Checkout Session and Order record
4. Stripe returns checkout URL
5. User completes payment in Stripe
6. Stripe sends `checkout.session.completed` webhook
7. Backend verifies webhook signature and updates Order status
8. Backend publishes `payment_success` event to RabbitMQ
9. Worker picks up event and sends confirmation email

## Testing

Run the CI pipeline locally:

```bash
# Lint check
flake8 .

# Import tests
python -c "import main; import models; import database; import worker"

# Security scan
bandit -r . -ll
```

## GitHub Actions Workflow

The `.github/workflows/payment-and-subscription-ci.yml` runs:

✅ Python linting (flake8)  
✅ Import validation  
✅ Database configuration tests  
✅ Security checks (bandit, TruffleHog)  
✅ Docker image build (on success)  

Triggered on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Changes to `payment_and_subscription/**`

## Deployment

### Environment Setup

For production deployment, ensure:

1. **Stripe Keys**: Use production keys from Stripe dashboard
2. **Email**: Configure Gmail app password (2FA required)
3. **Database**: Use managed PostgreSQL service (AWS RDS, etc.)
4. **RabbitMQ**: Use managed message broker (AWS SQS, CloudAMQP, etc.)

### Docker Deployment

```bash
docker build -t payment-service:latest .
docker run -d \
  -e DATABASE_URL="postgresql://..." \
  -e STRIPE_SECRET_KEY="sk_live_..." \
  -e STRIPE_WEBHOOK_SECRET="whsec_..." \
  -e GMAIL_ADDRESS="..." \
  -e GMAIL_APP_PASSWORD="..." \
  -p 8000:8000 \
  payment-service:latest
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Webhook error" | Verify `STRIPE_WEBHOOK_SECRET` matches Stripe dashboard |
| "Email not sent" | Enable 2FA in Gmail and use app-specific password |
| "Database connection failed" | Check `DATABASE_URL` format and PostgreSQL service |
| "RabbitMQ connection failed" | Ensure RabbitMQ service is running on port 5672 |

## Security Notes

- ⚠️ Never commit `.env` files with real credentials
- ⚠️ Use environment variables for all secrets
- ⚠️ Verify webhook signatures before processing
- ⚠️ Keep Stripe keys in `.env.example` as examples only
- ⚠️ Rotate credentials regularly

## License

MIT
