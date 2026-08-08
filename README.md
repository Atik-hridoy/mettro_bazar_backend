<div align="center">
  <img src="https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=800&q=80" alt="Metro Bazar" width="100%" style="border-radius: 12px; margin-bottom: 20px;">
  
  # 🛒 Metro Bazar API
  
  **A powerful, production-ready Django REST Framework backend for the Metro Bazar Ready-to-Cook e-commerce platform.**

  [![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
  [![Django Version](https://img.shields.io/badge/django-4.2%2B-092E20.svg?logo=django)](https://www.djangoproject.com/)
  [![DRF Version](https://img.shields.io/badge/DRF-3.14%2B-red.svg)](https://www.django-rest-framework.org/)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-316192.svg?logo=postgresql)](https://www.postgresql.org/)
  
</div>

---

## ✨ Features

- **📱 Phone-Based Authentication**: Custom User model using phone numbers and JWT tokens instead of traditional usernames.
- **🛍️ Comprehensive Product Catalog**: Manage categories, products, weight variants, and dynamic homepage banners.
- **📦 Order & Cart Management**: Robust ordering system with historical price preservation and item tracking.
- **💳 Payment Integration**: Built-in hooks for SSLCommerz payment gateway initialization and IPN webhooks.
- **🗺️ Delivery Zones**: Manage dynamic delivery areas and localized shipping charges.
- **⭐ Reviews System**: Customer product ratings and reviews.
- **📚 API Documentation**: Auto-generated Swagger UI and Redoc via `drf-spectacular`.

---

## 🏗️ Architecture

Following the "Fat Models, Thin Views" principle, the project is structured modularly:

```text
apps/
 ├── accounts/     # Custom User model, Auth, Profiles, Saved Addresses
 ├── products/     # Categories, Products, Variants, Banners
 ├── orders/       # Cart, Orders, Order Items
 ├── payments/     # SSLCommerz Integration, Transactions
 ├── delivery/     # Delivery Zones and Charges
 └── reviews/      # Product Reviews and Ratings
config/            # Django settings, WSGI/ASGI, global URLs
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- PostgreSQL (Optional, seamlessly falls back to SQLite)

### 2. Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/Atik-hridoy/mettro_bazar_backend.git
cd mettro_bazar_backend

python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory (you can use `.env.example` as a template):

```ini
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=*

# Optional: Database config (Defaults to SQLite if Postgres is unavailable)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=metro_bazar_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 4. Database Setup & Seeding

Apply migrations and populate the database with mock data:

```bash
python manage.py migrate
python manage.py seed_data
```
> *Note: The `seed_data` command automatically creates a superuser `01700000000` with password `admin1234`.*

### 5. Run the Server

```bash
python manage.py runserver
```

---

## 📖 API Documentation

Once the server is running, you can explore the interactive API documentation:

- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **OpenAPI Schema**: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

---

<div align="center">
  <i>Built with ❤️ for Metro Bazar</i>
</div>
