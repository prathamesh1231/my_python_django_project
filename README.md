# 🍕 Prathamesh Food-court — Django Project

## ⚠️ FIX: "no such table: food_cart" Error

This error happens because **database migrations have not been run yet**.
Run the following commands — this creates all required tables:

```bash
python manage.py makemigrations food
python manage.py migrate
```

---

## ✅ Full Setup (Step by Step)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 2. Install Django
pip install -r requirements.txt

# 3. ⚡ Run migrations (REQUIRED — fixes "no such table" error)
python manage.py makemigrations food
python manage.py migrate

# 4. (Optional) Create admin user
python manage.py createsuperuser

# 5. Start server
python manage.py runserver
```

Then open: http://127.0.0.1:8000/

---

## Features
- 🏠 Home, About, Menu, Contact, Map pages
- 👤 User Registration & Login / Logout
- 🛒 Add to Cart, Update Quantity, Remove Items
- 📦 Checkout with Delivery Address
- 📋 Order History & Order Detail pages
- 🔧 Django Admin panel

## URLs
| Page         | URL         |
|--------------|-------------|
| Home         | /           |
| Menu         | /menu/      |
| About        | /about/     |
| Contact      | /contact/   |
| Map          | /map/       |
| Register     | /register/  |
| Login        | /login/     |
| Cart         | /cart/      |
| Checkout     | /checkout/  |
| My Orders    | /orders/    |
| Admin Panel  | /admin/     |
