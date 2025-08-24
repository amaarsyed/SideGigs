# nextstep backend

Django 5 + DRF backend for a teen job platform. Supports JWT auth and private uploads to Supabase Storage.

## Requirements

- Python 3.11
- Supabase project (service role key)

## Environment

Create `.env`:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE=your-service-role
SUPABASE_BUCKET=uploads
SECRET_KEY=dev-secret-key
DEBUG=True
```

## Setup

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API

### Auth

- `POST /api/auth/register` – username, email, password, is_minor
- `POST /api/auth/login` – obtain JWT pair
- `GET /api/auth/me` – current user info

### Storage

- `POST /api/storage/resume` – upload resume (.pdf/.docx)
- `POST /api/storage/id` – upload ID image and optional selfie
- `GET /api/storage/signed-url?path=...` – staff only, get 1h signed URL

### Health

- `GET /api/health/storage` – checks Supabase connection and bucket

## Testing

```bash
python manage.py test
```

## Curl examples

```bash
# Resume upload
curl -H "Authorization: Bearer <JWT>" -F "file=@resume.pdf" http://localhost:8000/api/storage/resume

# ID upload
curl -H "Authorization: Bearer <JWT>" -F "id_image=@id.jpg" -F "selfie=@me.jpg" http://localhost:8000/api/storage/id
```
