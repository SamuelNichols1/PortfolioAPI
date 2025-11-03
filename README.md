# Django REST API with OpenAI Integration

A Django REST Framework API that takes user prompts and returns OpenAI GPT responses.

## Features

- ✅ Django 4.2+ with Django REST Framework
- ✅ OpenAI GPT integration
- ✅ Single chat endpoint that forwards prompts to OpenAI
- ✅ Chat history tracking in database
- ✅ CORS support configured
- ✅ Admin panel to view chat history
- ✅ Unit tests included
- ✅ Environment-based configuration
- ✅ SQLite database (easy to switch to PostgreSQL)

## Project Structure

```
django_api/
├── config/                 # Project configuration
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── api/                   # Sample API app
│   ├── __init__.py
│   ├── admin.py          # Admin panel configuration
│   ├── apps.py
│   ├── models.py         # Database models
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # API views
│   ├── urls.py           # API URL routing
│   └── tests.py          # Unit tests
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── .gitignore           # Git ignore rules
```

## Setup Instructions

### 1. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root (or copy from `.env.example`):

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
OPENAI_API_KEY=your-openai-api-key-here
```

**Important:** Get your OpenAI API key from https://platform.openai.com/api-keys

### 4. Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an admin user to view chat history.

### 6. Run Development Server

```powershell
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

## API Endpoints

### Chat Endpoint
- **POST** `/api/chat/` - Send a prompt to OpenAI and get a response

### Admin Panel
- **URL:** `http://127.0.0.1:8000/admin/`
- View all chat history and manage data

## Example API Usage

### Send a Prompt to OpenAI

**Using curl:**
```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the meaning of life?"}'
```

**Using PowerShell:**
```powershell
$body = @{
    prompt = "What is the meaning of life?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/chat/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Using Python requests:**
```python
import requests

response = requests.post(
    'http://127.0.0.1:8000/api/chat/',
    json={'prompt': 'What is the meaning of life?'}
)

print(response.json())
```

**Response Format:**
```json
{
    "prompt": "What is the meaning of life?",
    "response": "The meaning of life is a philosophical question...",
    "created_at": "2025-11-02T12:34:56.789012Z"
}
```

## Running Tests

```powershell
python manage.py test
```

## Configuration

### OpenAI Model Settings
By default, the API uses `gpt-3.5-turbo`. You can change this in `api/views.py`:

```python
response = client.chat.completions.create(
    model="gpt-4",  # Change to gpt-4, gpt-4-turbo, etc.
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
    max_tokens=1000
)
```

### CORS Settings
Edit `config/settings.py` to add allowed origins for frontend apps:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Database Configuration
The project uses SQLite by default. To use PostgreSQL:

1. Install psycopg2: `pip install psycopg2-binary`
2. Update `DATABASES` in `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Viewing Chat History

1. Create a superuser: `python manage.py createsuperuser`
2. Go to `http://127.0.0.1:8000/admin/`
3. Navigate to "Chat Histories" to view all conversations

## Next Steps

1. **Add Authentication:** Secure the endpoint with API keys or JWT
2. **Add Rate Limiting:** Prevent abuse with throttling
3. **Add Streaming:** Implement streaming responses from OpenAI
4. **Add Context:** Enhance prompts with system messages or conversation history
5. **Deploy:** Set up for production deployment with proper security

## Useful Commands

```powershell
# Create new app
python manage.py startapp app_name

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files (for production)
python manage.py collectstatic
```

## License

MIT License - feel free to use this boilerplate for your projects!
