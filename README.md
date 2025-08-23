# Job Platform Backend

A Django-based backend for a job platform with JWT authentication and user verification system.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- Windows 11 (PowerShell)

### Setup Instructions

1. **Clone and navigate to project**
   ```powershell
   git clone <your-repo-url>
   cd job-platform-backend
   ```

2. **Create virtual environment**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```powershell
   python manage.py migrate
   ```

5. **Create superuser**
   ```powershell
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```powershell
   python manage.py runserver
   ```

7. **Test the API**
   ```powershell
   .\test_api.ps1
   ```

## 📁 Project Structure

```
job-platform-backend/
├── manage.py
├── core/                    # Django project settings
├── apps/
│   ├── accounts/           # User authentication & verification
│   ├── jobs/              # Job management (commented out)
│   ├── checkins/          # Check-in system (commented out)
│   ├── ai_proxy/          # AI service client (commented out)
│   └── common/            # Shared permissions
├── .vscode/               # Cursor IDE configuration
├── requirements.txt
├── test_api.ps1          # PowerShell test script
└── README.md
```

## 🔗 API Endpoints

### Authentication
- `POST /api/accounts/register/` - Register new user
- `POST /api/accounts/login/` - Login with JWT
- `POST /api/accounts/token/refresh/` - Refresh JWT token
- `GET /api/accounts/me/` - Get current user info

### Verification
- `POST /api/accounts/verification/submit/` - Submit verification documents
- `GET /api/accounts/verification/me/` - Get verification status
- `POST /api/accounts/verification/approve/{user_id}/` - Approve verification (admin only)

## 🧪 Testing

### PowerShell Test Script
Run the included test script to verify all endpoints:
```powershell
.\test_api.ps1
```
* `apps/common/` - Permissions (IsVerified, IsMinorWithConsent)

### Krish's Responsibility (Backend + User Management)

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
>>>>>>> f0304daa349bbddd1f6e8a55b9e3458eaa32fb13
```

### Manual Testing with PowerShell

#### 1. Register User
```powershell
$registerData = @{
    username = "testuser"
    email = "test@example.com"
    password = "testpass123"
    password_confirm = "testpass123"
    first_name = "Test"
    last_name = "User"
    is_minor = $false
    guardian_email = ""
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/accounts/register/" -Method POST -Body $registerData -ContentType "application/json"
```

#### 2. Login
```powershell
$loginData = @{
    username = "testuser"
    password = "testpass123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/accounts/login/" -Method POST -Body $loginData -ContentType "application/json"
$accessToken = $response.access
```

#### 3. Get User Info
```powershell
$headers = @{
    "Authorization" = "Bearer $accessToken"
}

<<<<<<< HEAD
Invoke-RestMethod -Uri "http://localhost:8000/api/accounts/me/" -Method GET -Headers $headers
```

#### 4. Submit Verification
```powershell
$verificationData = @{
    meta = @{
        document_type = "driver_license"
        document_number = "DL123456789"
        submitted_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ")
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/accounts/verification/submit/" -Method POST -Body $verificationData -Headers $headers -ContentType "application/json"
```

## 🔧 Cursor IDE Setup

### Auto-select Python Interpreter
1. Open Command Palette (`Ctrl+Shift+P`)
2. Type "Python: Select Interpreter"
3. Choose `.venv\Scripts\python.exe`

### Debug Configuration
- Press `F5` to run Django development server
- Use "Django Runserver" configuration for debugging

### Code Formatting
- Black formatter is configured
- Auto-format on save is enabled
- Import sorting with isort profile

## 📊 Models

### User Model
```python
class User(AbstractUser):
    is_minor = models.BooleanField(default=False)
    guardian_email = models.EmailField(blank=True, null=True)
```

### Verification Model
```python
class Verification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="verification")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 🔐 Permissions

### IsVerified Permission
```python
from apps.common.permissions import IsVerified

# Use in views to require verification
permission_classes = [IsVerified]
```

## 🛠️ Admin Panel

Access the admin panel at: `http://localhost:8000/admin/`

Features:
- User management with custom fields
- Verification status management
- Status filtering and search

## 🚨 Troubleshooting

### PowerShell Execution Policy
If you get execution policy errors:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Virtual Environment Issues
```powershell
# Deactivate and reactivate
deactivate
.\.venv\Scripts\Activate.ps1
```

### Migration Issues
```powershell
# Reset database
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Port Conflicts
```powershell
# Use different port
python manage.py runserver 8001
```

## 🎯 Next Steps

1. **Test all endpoints** using the PowerShell script
2. **Create users** via admin panel or API
3. **Test verification workflow**
4. **Uncomment jobs/checkins apps** when ready
5. **Implement frontend integration**

## 📝 Environment Variables

Create `.env` file (optional):
```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

**Happy coding! 🚀**
=======
* Migration errors: Delete `db.sqlite3` and run `python manage.py migrate` again.
* Import errors: Ensure virtual environment is activated.
* Port conflicts: Change port with `python manage.py runserver 8001`.

---

## Teammate Git To‑Do and Command Guide

### When to fork vs. branch

* **Branch (default, recommended):** Both collaborators have write access to the same repo (`amaarsyed/SideGigs`). Use branches for all features and fixes.
* **Fork (only if no write access):** If you cannot push branches to the main repo, fork to your own account, push to your fork, and open a PR from fork → upstream.

### If branching in the same repo

1. Get latest main

```bash
git checkout main
git pull origin main
```

2. Create a feature branch

```bash
git checkout -b feat/accounts-auth
```

3. Make commits and push the branch

```bash
git add .
git commit -m "feat(accounts): registration, login, profile endpoints"
git push origin feat/accounts-auth
```

4. Open a Pull Request (branch → `main`)

5. Update your branch with latest main (before merging)

```bash
git fetch origin
git rebase origin/main   # or: git merge origin/main
# resolve conflicts → git add <files>
# if rebase: git rebase --continue
```

### If working from a fork

1. Fork on GitHub, then clone your fork

```bash
git clone https://github.com/<your-username>/SideGigs.git
cd SideGigs
```

2. Add upstream to sync with original repo

```bash
git remote add upstream https://github.com/amaarsyed/SideGigs.git
git remote -v
```

3. Create your branch on the fork

```bash
git checkout -b feat/accounts-auth
```

4. Commit and push to your fork

```bash
git add .
git commit -m "feat(accounts): register/login endpoints"
git push origin feat/accounts-auth
```

5. Open a PR from `<your-username>:feat/accounts-auth` → `amaarsyed:main`

6. Keep your fork up to date

```bash
git checkout main
git fetch upstream
git merge upstream/main      # or: git rebase upstream/main
git push origin main
```

### Daily routine

```bash
git checkout main
git pull origin main
git checkout -b feat/<short-desc>   # or switch back to your existing branch
# code …
git add .
git commit -m "<concise, imperative summary>"
git push origin feat/<short-desc>
```

### Common fixes

* Stash local changes temporarily

```bash
git stash
# pull, switch branches, etc.
git stash pop
```

* Rename a branch

```bash
git branch -m feat/accounts
```

* Delete a merged branch

```bash
git branch -d feat/accounts        # local
git push origin --delete feat/accounts
```

* Abort a rebase or merge if stuck

```bash
git rebase --abort
# or
git merge --abort
```

### Commit message format (suggested)

```
feat(accounts): add registration and login endpoints
fix(accounts): handle duplicate email error
chore(core): update DRF settings
refactor(accounts): simplify serializers
```
>>>>>>> f0304daa349bbddd1f6e8a55b9e3458eaa32fb13
