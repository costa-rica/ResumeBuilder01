# ResumeBuilder02 - API Requirements

## Overview

ResumeBuilder02 API is a Python FastAPI backend that provides REST endpoints for resume tailoring services. It integrates with OpenAI's GPT-4o-mini and a self-hosted Ollama instance (mistral:instruct) to generate tailored resumes, cover letters, and improvement suggestions based on user resumes and job descriptions.

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Python Version**: 3.11+
- **Validation**: Pydantic v2
- **HTTP Client**: httpx (async)
- **File Processing**: python-docx
- **Environment**: python-dotenv
- **CORS**: fastapi.middleware.cors
- **Documentation**: Auto-generated OpenAPI (Swagger UI)

## Project Structure

```
api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Settings management (pydantic-settings)
│   ├── dependencies.py         # Shared dependencies
│   ├── routers/
│   │   ├── __init__.py
│   │   └── resume.py           # Resume-related endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py      # LLM integration layer
│   │   └── file_service.py     # File processing utilities
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requests.py         # Pydantic request models
│   │   └── responses.py        # Pydantic response models
│   ├── prompts/
│   │   └── resume_tailor.md    # LLM prompt template
│   └── exceptions.py           # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── test_resume_router.py
│   ├── test_llm_service.py
│   └── test_file_service.py
├── .env.example
├── requirements.txt
├── pyproject.toml              # Poetry or setuptools config
└── README.md
```

## Environment Variables

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# OpenAI Configuration
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# Ollama Configuration
OLLAMA_API_BASE=https://fell-st-ollama.dashanddata.com
OLLAMA_API_KEY=your_ollama_api_key
OLLAMA_MODEL=mistral:instruct

# File Upload Configuration
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes
ALLOWED_EXTENSIONS=.docx

# Rate Limiting (optional for future)
RATE_LIMIT_PER_MINUTE=10
```

## API Endpoints

### Health Check

**GET** `/api/health`

**Response**: 200 OK
```json
{
  "status": "ok",
  "version": "2.0.0",
  "timestamp": "2025-12-06T10:30:00Z"
}
```

---

### Get Available Models

**GET** `/api/models`

Returns list of available LLM models.

**Response**: 200 OK
```json
{
  "models": [
    {
      "id": "gpt-4o-mini",
      "name": "GPT-4o Mini",
      "provider": "openai",
      "description": "OpenAI's efficient model"
    },
    {
      "id": "mistral:instruct",
      "name": "Mistral Instruct",
      "provider": "ollama",
      "description": "Self-hosted Mistral model"
    }
  ]
}
```

---

### Tailor Resume

**POST** `/api/resume/tailor`

Main endpoint for resume tailoring. Accepts a resume file (.docx) and job description, returns tailored content.

**Request**: `multipart/form-data`
- `resume_file`: File (required) - .docx file
- `job_description`: string (required) - Job description text
- `model_id`: string (required) - One of: "gpt-4o-mini", "mistral:instruct"

**Response**: 200 OK
```json
{
  "id": "uuid-v4-string",
  "created_at": "2025-12-06T10:30:00Z",
  "model_used": "gpt-4o-mini",
  "original_match_score": 85.0,
  "revised_match_score": 95.0,
  "tailored_resume": "John Doe\n123 Main St...",
  "cover_letter": "Dear Hiring Manager...",
  "improvements": [
    "Add specific metrics to quantify achievements",
    "Emphasize Python and FastAPI experience",
    "Include cloud deployment experience"
  ],
  "processing_time_ms": 3420
}
```

**Error Responses**:

400 Bad Request - Invalid file format
```json
{
  "detail": "Only .docx files are supported"
}
```

400 Bad Request - File too large
```json
{
  "detail": "File size exceeds 10MB limit"
}
```

400 Bad Request - Invalid model
```json
{
  "detail": "Model 'invalid-model' not found. Available: gpt-4o-mini, mistral:instruct"
}
```

500 Internal Server Error - LLM failure
```json
{
  "detail": "LLM service unavailable. Please try again later."
}
```

---

### Get Prompt Template (Optional - for debugging)

**GET** `/api/resume/prompt-template`

Returns the current prompt template used for LLM requests.

**Response**: 200 OK
```json
{
  "template": "You are an experienced HR consultant..."
}
```

---

## Pydantic Models

### Request Models (`app/models/requests.py`)

```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal

class TailorResumeRequest(BaseModel):
    """Validated after file upload in endpoint"""
    job_description: str = Field(..., min_length=50, max_length=10000)
    model_id: Literal["gpt-4o-mini", "mistral:instruct"]

    @field_validator('job_description')
    @classmethod
    def validate_job_description(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Job description cannot be empty")
        return v.strip()
```

### Response Models (`app/models/responses.py`)

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class ModelInfo(BaseModel):
    id: str
    name: str
    provider: str
    description: str

class ModelsResponse(BaseModel):
    models: List[ModelInfo]

class TailorResumeResponse(BaseModel):
    id: str
    created_at: datetime
    model_used: str
    original_match_score: float = Field(..., ge=0, le=100)
    revised_match_score: float = Field(..., ge=0, le=100)
    tailored_resume: str
    cover_letter: str
    improvements: List[str] = Field(..., min_length=3, max_length=10)
    processing_time_ms: int

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime

class ErrorResponse(BaseModel):
    detail: str
```

---

## Service Layer

### LLM Service (`app/services/llm_service.py`)

**Responsibilities**:
- Manage connections to OpenAI and Ollama APIs
- Handle prompt template loading and variable replacement
- Parse and validate LLM JSON responses
- Implement retry logic and timeout handling
- Abstract LLM provider differences

**Key Functions**:
```python
async def tailor_resume_with_llm(
    resume_text: str,
    job_description: str,
    model_id: str
) -> dict:
    """
    Orchestrates LLM request for resume tailoring.
    Returns parsed LLM response as dict with keys:
    - updated_resume
    - updated_cover_letter
    - improvements_list
    """
    pass

async def call_openai(prompt: str, model: str) -> dict:
    """Call OpenAI Chat Completions API with JSON mode"""
    pass

async def call_ollama(prompt: str, model: str) -> dict:
    """Call Ollama Generate API with JSON format enforcement"""
    pass
```

**Implementation Notes**:
- Use `httpx.AsyncClient` for all HTTP requests
- Set timeouts (30s for OpenAI, 60s for Ollama)
- Implement exponential backoff for retries (max 3 attempts)
- Validate LLM JSON responses against expected schema
- Log all LLM interactions for debugging

---

### File Service (`app/services/file_service.py`)

**Responsibilities**:
- Validate uploaded files (extension, size, content)
- Extract text from .docx files
- Handle temporary file cleanup
- Future: Support .pdf uploads

**Key Functions**:
```python
async def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extract plain text from .docx file bytes.
    Uses in-memory processing (no temp files).
    """
    pass

def validate_file_upload(
    file: UploadFile,
    max_size: int,
    allowed_extensions: List[str]
) -> None:
    """
    Validates file upload constraints.
    Raises HTTPException if validation fails.
    """
    pass

def load_prompt_template(template_path: str) -> str:
    """Load and return prompt template from file"""
    pass
```

---

## Configuration Management (`app/config.py`)

Use `pydantic-settings` for type-safe configuration:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False
    cors_origins: List[str] = ["http://localhost:3000"]

    # OpenAI
    openai_api_base: str
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    # Ollama
    ollama_api_base: str
    ollama_api_key: str
    ollama_model: str = "mistral:instruct"

    # File Upload
    max_upload_size: int = 10485760  # 10MB
    allowed_extensions: List[str] = [".docx"]

settings = Settings()
```

---

## Error Handling

### Custom Exceptions (`app/exceptions.py`)

```python
from fastapi import HTTPException, status

class FileValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class LLMServiceError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class ModelNotFoundError(HTTPException):
    def __init__(self, model_id: str, available_models: List[str]):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Model '{model_id}' not found. Available: {', '.join(available_models)}"
        )
```

---

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing Requirements

### Unit Tests
- Test file validation logic (size, extension, corrupted files)
- Test DOCX text extraction with various document formats
- Mock LLM API responses and test parsing logic
- Test prompt template variable replacement

### Integration Tests
- Test full `/api/resume/tailor` endpoint flow with sample files
- Test error handling for invalid inputs
- Test timeout scenarios for LLM calls

### Test Coverage Target
- Minimum 80% code coverage
- All service functions must have unit tests
- All endpoints must have integration tests

---

## Logging

Use Python's built-in `logging` module with structured logging:

```python
import logging

logger = logging.getLogger(__name__)

# Log levels:
# - INFO: API requests, LLM calls
# - WARNING: Retries, slow responses
# - ERROR: Failed requests, exceptions
# - DEBUG: Detailed request/response payloads (dev only)
```

Log format:
```
[2025-12-06 10:30:00] INFO [app.routers.resume] POST /api/resume/tailor - model=gpt-4o-mini - 200 OK - 3.4s
```

---

## Future Enhancements

1. **Resume Matching Scores**: Integrate sentence-transformers for semantic similarity scoring
2. **PDF Support**: Add PDF parsing with pypdf or pdfplumber
3. **Rate Limiting**: Implement per-user rate limiting with slowapi
4. **Caching**: Cache LLM responses for identical resume+job pairs
5. **Async Background Jobs**: Use Celery for long-running LLM requests
6. **Database**: Store resume history with SQLAlchemy + PostgreSQL
7. **Authentication**: Add JWT-based user authentication
8. **Webhooks**: Support async callbacks for LLM completion

---

## Running the API

### Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Future)
```bash
docker build -t resumebuilder02-api .
docker run -p 8000:8000 --env-file .env resumebuilder02-api
```

---

## API Documentation

FastAPI auto-generates interactive documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`
