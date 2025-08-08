# RSA_Django – Secure JWT Authentication using RSA Keys 🔐

This project demonstrates how to implement **RSA-based JWT authentication** in a Django project using `djangorestframework-simplejwt`. It provides a secure token authentication system with public/private key encryption and a clean user registration/profile management API.

---

## 🔧 Tech Stack

- Django 5+
- Django REST Framework
- SimpleJWT (with RSA)
- Redis (for caching user profiles)
- PostgreSQL (or SQLite for dev)
- Python 3.11+


---

## 🔐 What is RSA-based JWT?

Instead of using a shared secret (`HS256`), this project uses **RSA public/private key pair** (`RS256`) for signing JWTs:

- 🔑 **Private Key**: Signs the token (kept secret in your backend).
- 🧾 **Public Key**: Verifies the token (can be shared with other services/microservices).

This ensures **asymmetric encryption**, better for microservice communication.

---

## 📁 Project Structure
RSA_Django/
│
├── core/ # Django project root
│ └── settings.py
│ └── urls.py
│
├── users/ # Custom user app
│ ├── models.py # Custom User & UserProfile
│ ├── views.py # RegisterView, ProfileView (cached)
│ ├── serializers.py
│ └── urls.py
│
├── keys/ # Contains RSA .pem keys
│ ├── private.pem
│ └── public.pem
│
├── generate_keys.py # Script to generate RSA key pair
├── manage.py
└── README.md

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/shoaibatmaca/RSA_Django.git
cd RSA_Django
```

### 2. Create a Virtual Environment
```bsh
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate RSA Keys

```bash
python generate_keys.py
```

This creates keys/private.pem and keys/public.pem.

✅ Don't commit these keys to GitHub! Add them to .gitignore.

### 5. Run Migrations
```bash
python manage.py makemgrations
python manage.py migrate
```


### 7. Run Development Server
```bash
python manage.py runserver
```

📬 API Endpoints
Endpoint	Method	Auth Required	Description
/api/users/register/	POST		-Register new user
/api/token/	POST		-Get JWT access/refresh
/api/token/refresh/	POST 	-Refresh JWT access token
/api/users/profile/	GET/PUT		-View or update profile

🧠 Redis Caching
The /api/users/profile/ view is cached with a TTL of 300s (5 minutes).

Reduces DB hits on repeated profile fetches.

🛑 .gitignore Suggestions
Make sure these files are ignored:
# RSA keys
keys/private.pem
keys/public.pem

# RSA generation script (optional)
generate_keys.py


### 🔐 JWT Settings (in settings.py)
```bash
SIMPLE_JWT = {
    "ALGORITHM": "RS256",
    "SIGNING_KEY": open(BASE_DIR / "keys/private.pem").read(),
    "VERIFYING_KEY": open(BASE_DIR / "keys/public.pem").read(),
    ...
}
```

### ✍️ Author
Muhammad Shoaib | Backend Developer 
---

### ⭐ License
This project is open-source and free to use under the MIT License.
