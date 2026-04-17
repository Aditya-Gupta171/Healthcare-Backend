# Healthcare Backend API

A production-ready backend for a healthcare management system built with Django, Django REST Framework, JWT authentication, and PostgreSQL(neonDB).

## Live Deployment

- Base URL: https://healthcare-backend-v712.onrender.com

## Tech Stack

- Python 3.x
- Django 6
- Django REST Framework
- Simple JWT (djangorestframework-simplejwt)
- PostgreSQL (Neon)
- Gunicorn + WhiteNoise (deployment)

## Features

- Custom email-based user model
- JWT-based authentication
- Patient CRUD (owner-only access)
- Doctor CRUD (all authenticated users)
- Patient-doctor mapping with ownership checks
- Validation and duplicate prevention
- Environment-driven configuration

## Project Structure

```
.
├── accounts/
├── config/
├── doctors/
├── mappings/
├── patients/
├── manage.py
├── requirements.txt
├── Procfile
├── build.sh
└── runtime.txt
```

## API Endpoints

All endpoints are prefixed with `/api`.

### Authentication

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/token/refresh/`

### Patients

- `POST /api/patients/` (authenticated)
- `GET /api/patients/` (authenticated, only own patients)
- `GET /api/patients/<id>/` (authenticated, owner only)
- `PUT /api/patients/<id>/` (authenticated, owner only)
- `DELETE /api/patients/<id>/` (authenticated, owner only)

### Doctors

- `POST /api/doctors/` (authenticated)
- `GET /api/doctors/` (authenticated)
- `GET /api/doctors/<id>/` (authenticated)
- `PUT /api/doctors/<id>/` (authenticated)
- `DELETE /api/doctors/<id>/` (authenticated)

### Mappings

- `POST /api/mappings/` (authenticated, only for own patients)
- `GET /api/mappings/` (authenticated, only mappings of own patients)
- `GET /api/mappings/<patient_id>/` (authenticated, owner only)
- `DELETE /api/mappings/<mapping_id>/` (authenticated, owner only)

## Authentication Header

Use this header for protected routes:

```
Authorization: Bearer <access_token>
```

## Sample Requests

### Register

```http
POST /api/auth/register/
Content-Type: application/json

{
  "name": "Alice",
  "email": "alice@example.com",
  "password": "StrongPass123!"
}
```

### Login

```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "alice@example.com",
  "password": "StrongPass123!"
}
```

### Create Patient

```http
POST /api/patients/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_name": "John Patient",
  "age": 34,
  "gender": "male",
  "contact_number": "9999999999",
  "address": "NY",
  "medical_history": "Diabetes"
}
```

### Create Doctor

```http
POST /api/doctors/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_name": "Dr Smith",
  "specialization": "Cardiology",
  "email": "drsmith@example.com",
  "contact_number": "8888888888",
  "years_of_experience": 12
}
```

### Create Mapping

```http
POST /api/mappings/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "patient": 1,
  "doctor": 1
}
```

## Local Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Configure environment variables.
5. Run migrations.
6. Start server.

Commands:

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Environment Variables

Create a `.env` file in project root:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DBNAME?sslmode=require
SECRET_KEY=replace-with-a-strong-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com
```

Required environment variables on Render:

- `DATABASE_URL`
- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS=<your-service>.onrender.com`
- `CSRF_TRUSTED_ORIGINS=https://<your-service>.onrender.com`

## Access Control Rules

- Patients are visible and editable only by their creator.
- Doctors are accessible to all authenticated users.
- Mappings are restricted to the authenticated user’s patients.

## Validation Rules

- Email must be unique for users and doctors.
- Password validation is enforced during registration.
- Patient age must be between 1 and 130.
- Doctor experience must be between 0 and 80.
- Duplicate patient-doctor mapping is blocked.
