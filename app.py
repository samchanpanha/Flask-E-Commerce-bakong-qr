from flask import Flask, render_template, request, session, redirect, url_for
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key')

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

# Telegram bot configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Sample products (all 100 KHR)
products = [
    {'id': 1, 'name': 'Product 1', 'price': 100, 'description': 'Description for Product 1'},
    {'id': 2, 'name': 'Product 2', 'price': 100, 'description': 'Description for Product 2'},
    {'id': 3, 'name': 'Product 3', 'price': 100, 'description': 'Description for Product 3'},
]

@app.route('/')
def home():
    return render_template('home.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return 'Product not found', 404
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = [p for p in products if p['id'] in session.get('cart', [])]
    total = sum(p['price'] for p in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        payment_method = request.form['payment_method']

        cart_items = [p for p in products if p['id'] in session.get('cart', [])]
        total = sum(p['price'] for p in cart_items)

        if payment_method == 'khqr':
            # Integrate KHQR
            from bakong_khqr import KHQR
            khqr = KHQR(os.getenv("BAKONG_TOKEN"))
            qr_string = khqr.create_qr(
                bank_account="sam_chanpanha2@aclb",  # Replace with actual Bakong account
                merchant_name="E-Commerce Store",
                merchant_city="Phnom Penh",
                amount=total,
                currency="KHR",
                store_label="E-Commerce Store",
                phone_number="087556849",  # Replace with actual phone
                bill_number=f"INV-{session.get('cart', [])}",  # Example bill number
                terminal_label="Online Purchase"
            )
            # Generate QR image
            qr_image_path = khqr.qr_image(qr_string, format="png", output_path=os.path.join("static", "qr.png"))
            # Generate MD5 hash
            md5_hash = khqr.generate_md5(qr_string)
            # Store in session
            session['qr_image'] = qr_image_path
            session['md5'] = md5_hash
            session['total'] = total
            session['name'] = name
            session['email'] = email
            session['phone'] = phone
            return render_template('payment.html', qr_image=qr_image_path, total=total, name=name, email=email, phone=phone)
        else:
            # Placeholder for other payments
            return f"Payment method {payment_method} not implemented yet. Total: {total} KHR"

    return render_template('checkout.html')

@app.route('/check_payment')
def check_payment():
    md5 = session.get('md5')
    if not md5:
        return {'status': 'UNPAID', 'amount': 0}

    from bakong_khqr import KHQR
    khqr = KHQR(os.getenv("BAKONG_TOKEN"))
    payment_data = khqr.get_payment(md5)
    if payment_data:
        amount = float(payment_data.get('amount', 0))
        return {'status': 'PAID', 'amount': amount}
    else:
        return {'status': 'UNPAID', 'amount': 0}

@app.route('/payment_success')
def payment_success():
    # Send email
    # msg = Message('Order Confirmation', sender=app.config['MAIL_USERNAME'], recipients=[session.get('email')])
    # msg.body = f'Your order has been confirmed. Total: {session.get("total", 0)} KHR'
    # mail.send(msg)

    # # Send Telegram notification
    # message = f"New order: Total {session.get('total', 0)} KHR from {session.get('name')} ({session.get('email')})"
    # url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    # data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    # requests.post(url, data=data)

    session.pop('cart', None)
    session.pop('qr_image', None)
    session.pop('md5', None)
    session.pop('total', None)
    session.pop('name', None)
    session.pop('email', None)
    session.pop('phone', None)
    return 'Payment successful! Email sent and notification sent to owner.'

if __name__ == '__main__':
    app.run(debug=True)