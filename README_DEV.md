# Flask E-Commerce with Bakong KHQR - Development Guide

## Prerequisites

- Python 3.8+
- Git
- A Gmail account for email notifications (or configure another SMTP provider)
- A Telegram bot token and chat ID for notifications
- Bakong Developer Token

## Setup Instructions

### 1. Clone and Navigate to the Project

```bash
git clone <your-repo-url>
cd bakong-khqr
```

### 2. Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
SECRET_KEY=your-very-secure-secret-key-here
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id
BAKONG_TOKEN=your-bakong-developer-token
```

**Important Notes:**
- For Gmail, use an "App Password" instead of your regular password
- Get your Bakong token from the [Bakong Developer Portal](https://developer.bakong.nbc.gov.kh/)
- Create a Telegram bot using [@BotFather](https://t.me/botfather) and get your chat ID

### 3. Quick Start with Development Script

Simply run the development script:

```bash
./start_dev.sh
```

This script will:
- Create a virtual environment
- Install all dependencies
- Install the local bakong_khqr package
- Start the Flask development server

### 4. Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install local package
pip install -e .

# Run the application
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## Running Tests

Use the test script to run all tests:

```bash
./run_tests.sh
```

This will run pytest with coverage reporting.

## Application Features

### Payment Flow

1. **Browse Products**: Visit `http://127.0.0.1:5000` to see available products
2. **Add to Cart**: Click "Add to Cart" on any product
3. **Checkout**: Fill in customer details and select KHQR payment
4. **QR Generation**: System generates a custom QR code image
5. **Payment Monitoring**: Real-time status checking every 5 seconds
6. **Completion**: Automatic redirect on successful full payment

### Payment Status Handling

- **Full Payment**: Green success message, email + Telegram notification, redirect to success page
- **Partial Payment**: Orange warning message showing paid amount
- **No Payment**: Continues polling until payment is detected

## API Endpoints

- `GET /` - Home page with products
- `GET /product/<id>` - Product detail page
- `GET /add_to_cart/<id>` - Add product to cart
- `GET /cart` - View cart
- `GET/POST /checkout` - Checkout form and QR generation
- `GET /check_payment` - AJAX endpoint for payment status (returns JSON)
- `GET /payment_success` - Success page

## File Structure

```
bakong-khqr/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── start_dev.sh          # Development startup script
├── run_tests.sh          # Test runner script
├── .env                  # Environment variables (create this)
├── static/               # Static files (CSS, JS, images)
├── templates/            # Jinja2 templates
│   ├── base.html
│   ├── home.html
│   ├── cart.html
│   ├── checkout.html
│   └── payment.html
├── tests/                # Test files
└── bakong_khqr/          # KHQR library package
    ├── __init__.py
    ├── khqr.py
    └── sdk/
```

## Troubleshooting

### Common Issues

1. **"Bakong Developer Token is required"**
   - Ensure `BAKONG_TOKEN` is set in `.env`

2. **Email not sending**
   - Check Gmail app password
   - Verify `MAIL_USERNAME` and `MAIL_PASSWORD`

3. **Telegram notifications not working**
   - Verify bot token and chat ID
   - Ensure bot is added to the chat

4. **QR image not displaying**
   - Check that `static/` directory exists
   - Ensure write permissions

### Development Tips

- Use `export FLASK_DEBUG=1` for detailed error messages
- Check Flask logs in the terminal for debugging
- Use browser developer tools to inspect AJAX requests

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `./run_tests.sh`
4. Ensure all tests pass
5. Submit a pull request

## License

See LICENSE file for details.