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
