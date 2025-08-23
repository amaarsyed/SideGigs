# Job Platform Backend

A Django-based backend for a job platform that connects job posters with workers, featuring AI-powered snapquotes and QR code check-ins.

## Quick Start

### Requirements

* Python 3.8+
* Git

### Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/amaarsyed/SideGigs.git
   cd SideGigs
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # On Windows
   source .venv/bin/activate      # On macOS/Linux
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

5. Run migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:

   ```bash
   python manage.py runserver
   ```

8. Access the API:

   * API Base URL: `http://localhost:8000/api/`
   * Admin Panel: `http://localhost:8000/admin/`

## Project Structure

```
job-platform-backend/
├── manage.py
├── core/                # Django project settings
├── apps/
│   ├── accounts/        # User management (teammate's responsibility)
│   ├── jobs/            # Job lifecycle (your responsibility)
│   ├── checkins/        # QR tracking (your responsibility)
│   ├── ai_proxy/        # AI service client (your responsibility)
│   └── common/          # Shared permissions
├── requirements.txt
├── env.example
└── README.md
```

## API Endpoints

### Jobs

* `POST /api/jobs/` - Create draft job
* `GET /api/jobs/` - List user's jobs
* `POST /api/jobs/{id}/snapquote/` - Get AI-powered quote
* `POST /api/jobs/{id}/accept/` - Accept job assignment
* `POST /api/jobs/{id}/complete/` - Complete job with photos

### Check-ins

* `POST /api/checkins/start/` - Start job with QR code
* `POST /api/checkins/{id}/end/` - End job check-in
* `GET /api/checkins/active/` - Get active check-in

## Team Responsibilities

### Your Responsibility (Backend + AI)

* `apps/jobs/` - Job models, serializers, viewsets
* `apps/checkins/` - QR hash generation, check-in/out endpoints
* `apps/ai_proxy/` - HTTP client functions for AI service calls
* `apps/common/` - Permissions (IsVerified, IsMinorWithConsent)

### Teammate Responsibility (Backend + User Management)

* `apps/accounts/` - User authentication, verification, guardian consent
* `core/` - Settings, URLs, DRF setup, admin

## Development Workflow

1. Create a feature branch:

   ```bash
   git checkout -b feat/your-feature-name
   ```

2. Make changes and commit:

   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

3. Push branch and create a Pull Request:

   ```bash
   git push origin feat/your-feature-name
   ```

   * Open a Pull Request on GitHub into `main`.

4. Code review:

   * Each teammate reviews only the apps they do not own.
   * Use Pull Requests for all changes.

## Teammate Instructions

### Cloning and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/amaarsyed/SideGigs.git
   cd SideGigs
   ```
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # On Windows
   source .venv/bin/activate      # On macOS/Linux
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Copy and configure environment variables:

   ```bash
   cp env.example .env
   # Fill in values (SECRET_KEY, AI tokens, etc.)
   ```
5. Run migrations:

   ```bash
   python manage.py migrate
   ```
6. Start the development server:

   ```bash
   python manage.py runserver
   ```

### Workflow

* Always pull the latest main branch before starting work:

  ```bash
  git checkout main
  git pull origin main
  ```
* Create a separate feature branch for your work:

  ```bash
  git checkout -b feat/accounts-auth
  ```
* Commit changes to your branch:

  ```bash
  git add .
  git commit -m "Implemented user authentication and verification"
  ```
* Push your branch to GitHub:

  ```bash
  git push origin feat/accounts-auth
  ```
* Open a Pull Request to merge into `main`.

### Responsibilities

* `apps/accounts/`

  * User authentication (register, login, logout)
  * Verification system (status pending/verified/rejected)
  * Guardian consent flow for minors
  * User profile management endpoints
* `core/`

  * Maintain `settings.py`
  * Add URL routes for accounts
  * Keep admin configuration updated

## Testing

Test the API endpoints:

```bash
# Verify server is running
curl http://localhost:8000/api/jobs/

# Should return 401 (authentication required)
```

## Environment Variables

Copy `env.example` to `.env` and configure:

* `SECRET_KEY` - Django secret key
* `DEBUG` - Set to True for development
* `AI_SERVICE_URL` - AI service endpoint
* `AI_SHARED_TOKEN` - AI service authentication token

## Next Steps

1. You: Test existing endpoints and AI integration.
2. Teammate: Implement user authentication and verification system.
3. Both: Integrate user management with job workflows.

## Troubleshooting

* Migration errors: Delete `db.sqlite3` and run `python manage.py migrate` again.
* Import errors: Ensure virtual environment is activated.
* Port conflicts: Change port with `python manage.py runserver 8001`.
