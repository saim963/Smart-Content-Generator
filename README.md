# Smart Content Generator API

AI-powered content generation API using Google Gemini and FastAPI.

## Features

- 📝 **Text Generation**: Generate creative content from prompts
- 📊 **Text Summarization**: Summarize long articles in different lengths
- 🌐 **Translation**: Translate text to multiple languages
- 💻 **Code Explanation**: Explain code snippets in simple terms
- ❓ **Q&A**: Answer questions with context

## Tech Stack

- **Framework**: FastAPI
- **AI Model**: Google Gemini Pro
- **Language**: Python 3.8+

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd gemini-content-api
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy your API key

### 5. Configure environment variables
Create a `.env` file:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 6. Run the application
```bash
uvicorn main:app --reload
```

The API will be available at: http://localhost:8000

## API Documentation

Access interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### 1. Generate Text
**POST** `/api/generate`

```json
{
  "prompt": "Write a poem about coding",
  "max_tokens": 500,
  "temperature": 0.8
}
```

### 2. Summarize Text
**POST** `/api/summarize`

```json
{
  "text": "Your long article text here...",
  "length": "short"
}
```

### 3. Translate Text
**POST** `/api/translate`

```json
{
  "text": "Hello, how are you?",
  "target_language": "Spanish"
}
```

### 4. Explain Code
**POST** `/api/explain-code`

```json
{
  "code": "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)",
  "language": "Python"
}
```

### 5. Question & Answer
**POST** `/api/qa`

```json
{
  "question": "What is FastAPI?",
  "context": "In the context of web development"
}
```

## Example Usage with curl

```bash
# Generate text
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a haiku about Python", "temperature": 0.9}'

# Summarize text
curl -X POST "http://localhost:8000/api/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your long text...", "length": "short"}'

# Translate
curl -X POST "http://localhost:8000/api/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Good morning", "target_language": "French"}'
```

## Example Usage with Python

```python
import requests

API_URL = "http://localhost:8000"

# Generate text
response = requests.post(
    f"{API_URL}/api/generate",
    json={
        "prompt": "Explain quantum computing in simple terms",
        "temperature": 0.7
    }
)
print(response.json())
```

## Deployment

### Deploy to Render

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: gemini-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GEMINI_API_KEY
        sync: false
```

2. Push to GitHub
3. Connect to Render
4. Add GEMINI_API_KEY environment variable

### Deploy to Railway

1. Connect GitHub repo
2. Add environment variable: `GEMINI_API_KEY`
3. Deploy automatically

## Project Structure

```
gemini-content-api/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── tests/              # Test files (optional)
```

## Testing

Test the API using the interactive docs at `/docs` or use Postman/curl.

## Error Handling

The API returns proper HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid input)
- `500`: Server error (Gemini API issues)

## Rate Limits

Google Gemini free tier limits:
- 60 requests per minute
- 1500 requests per day

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Author

Saim Shakeel
- Email: aims3328@gmail.com
- GitHub: github.com/saim963

## Acknowledgments

- Google Gemini AI
- FastAPI framework