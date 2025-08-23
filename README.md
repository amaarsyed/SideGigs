# Job Platform Backend

A Django-based backend for a job platform that connects job posters with workers, featuring AI-powered snapquotes and QR code check-ins.

## Project Structure

```
backend/
├── manage.py
├── core/                # Django project (settings, urls, wsgi)
├── apps/
│   ├── accounts/        # users, auth, guardians, verification
│   ├── jobs/           # jobs lifecycle (post, snapquote, accept, complete)
│   ├── checkins/       # QR codes, start/finish tracking
│   ├── ai_proxy/       # calls FastAPI or any external AI service
│   └── common/         # permissions, mixins, utils
├── requirements.txt
└── README.md
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `env.example` to `.env` and configure your environment variables.

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

- `POST /api/jobs/` - Create draft job
- `POST /api/jobs/{id}/snapquote/` - Get AI-powered quote
- `POST /api/jobs/{id}/accept/` - Accept job assignment
- `POST /api/checkins/start/` - Start job with QR code
- `POST /api/checkins/{id}/end/` - End job check-in
- `POST /api/jobs/{id}/complete/` - Complete job with photos

## Development Workflow

This project uses a split ownership model to minimize conflicts:

**Your responsibility:**
- `apps/jobs/` - Job models, serializers, viewsets
- `apps/checkins/` - QR hash generation, check-in/out endpoints
- `apps/ai_proxy/` - HTTP client functions for AI service calls
- `apps/common/` - Permissions (IsVerified, IsMinorWithConsent)

**Teammate's responsibility:**
- `apps/accounts/` - User, Verification, guardian consent
- `core/` - Settings, URLs, DRF setup, admin

## Branch Strategy

- Main branch: `main`
- Feature branches: `feat/jobs-accept`, `feat/user-verification`
- Use PRs for code review
- Each developer reviews only the apps they don't own
