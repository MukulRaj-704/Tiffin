# Tiffin

A Django + React tiffin subscription and billing management system.

## How to Use and Initialize

### 1. Clone and open the project

```bash
cd /workspaces/Tiffin
```

### 2. Create and activate the virtual environment

```bash
python -m venv myenv
source myenv/bin/activate
```

### 3. Install backend dependencies

```bash
pip install Django djangorestframework djangorestframework-simplejwt django-cors-headers psycopg2-binary python-dotenv
```

### 4. Apply Django migrations

```bash
python manage.py migrate
```

### 5. Create an admin/owner user for login testing

```bash
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user, created = User.objects.get_or_create(username='admin', defaults={'email':'admin@tiffin.com','role':'OWNER','phone':'9999999999'}); user.set_password('admin123'); user.is_active=True; user.save(); print('CREATED' if created else 'EXISTS')"
```

### 6. Start the Django backend

```bash
python manage.py runserver 0.0.0.0:8000
```

### 7. Open a second terminal and initialize the frontend

```bash
cd /workspaces/Tiffin/frontend
npm install
npm install react-router-dom axios
npm run dev
```

The frontend should run on:

```bash
http://localhost:5173
```

### 8. Login

Use the owner account:

- Username: `admin`
- Password: `admin123`

---

## Tech Stack

- Python
- Django
- Django REST Framework
- Django REST Framework Simple JWT
- PostgreSQL-ready setup
- ReactJS
- Vite
- Axios
- React Router
- Tailwind-ready design structure

---

## Project Structure

```text
Tiffin/
├── README.md
├── manage.py
├── db.sqlite3
├── myenv/
├── tiffin_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── customers/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── subscriptions/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
├── deliveries/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── billing/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── public/
    └── src/
        ├── App.jsx
        ├── index.css
        ├── components/
        ├── data/
        ├── hooks/
        ├── pages/
        └── services/
```

---

## Main Features

- Owner/admin login
- Customer management
- Subscription management
- Pause and early resume flow
- Delivery scheduling and calendar logic
- Pro-rated billing based on served days
- React-based dashboard screens for owner and customer users

---

## Backend API Base

```text
http://localhost:8000/api
```

Example auth endpoints:

```text
POST /api/auth/login/
GET  /api/auth/me/
```

---

## Notes

- Django is the backend framework and holds the business logic.
- React is the frontend client that calls the APIs.
- The project is set up for extension into a production-ready tiffin management workflow.
