# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ResumeBuilder01 is a FastAPI-based web application that helps users tailor resumes for specific job applications using LLM-powered content generation. The app accepts resume uploads (.docx) and job descriptions, then generates tailored resumes, cover letters, and improvement suggestions through either OpenAI's gpt-4o-mini or a self-hosted Ollama instance running mistral:instruct.

## Development Commands

### Running the Application
```bash
python3 -m uvicorn src.main:app --reload
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file in the project root with:
```
URL_BASE_OLLAMA=https://fell-st-ollama.dashanddata.com
KEY_OLLAMA=your_ollama_api_key
URL_BASE_OPENAI=https://api.openai.com/v1
KEY_OPENAI=your_openai_api_key
```

## Architecture

### Design Principles
- **Modular Structure**: Keep route handlers thin (in `src/routes/`), delegate heavy logic to utility functions
- **Separation of Concerns**: File processing, LLM interactions, and routing are isolated in separate modules
- **Template-driven UI**: Uses Jinja2 templates for server-side HTML rendering
- **MVP Focus**: Lightweight implementation with placeholders for future features (e.g., resume matching scores)

### Code Structure

```
src/
├── main.py              # FastAPI app initialization, static file mounting, router registration
├── config.py            # Environment variable loading (dotenv)
├── routes/
│   └── builder.py       # Main routes: home page (GET /) and submission handler (POST /submit)
├── utils/
│   ├── file_processing.py  # DOCX parsing and prompt template reading
│   └── llm_client.py       # LLM API integrations (Ollama & OpenAI)
├── templates/
│   ├── index.html       # Home page with resume upload form
│   ├── result.html      # Results page showing tailored resume, cover letter, suggestions
│   └── markdown/
│       └── prompt01.md  # LLM prompt template with placeholders
└── static/              # Static assets (auto-created if missing)
```

### Request Flow

1. **Home Page (GET /)**: User selects model (mistral:instruct or gpt-4o-mini), uploads resume (.docx), pastes job description
2. **Submission (POST /submit)**:
   - Extract text from uploaded DOCX file (`file_processing.read_docx()`)
   - Load prompt template from `src/templates/markdown/prompt01.md` (`file_processing.read_prompt_template()`)
   - Replace template placeholders: `< Resume of user>` and `< Job Requirements >`
   - Route to appropriate LLM client based on `model_choice` form value
3. **LLM Processing**:
   - **Ollama** (`llm_client.process_with_ollama()`): POST to `/api/generate` with JSON format enforcement
   - **OpenAI** (`llm_client.process_with_openai()`): Chat completions API with `response_format: json_object`
4. **Response Rendering**: Display results in `result.html` with:
   - Resume qualifier match scores (placeholders: "85%" original, "95%" revised)
   - Tailored resume (`updated_resume`)
   - Cover letter (`updated_cover_letter`)
   - Improvement suggestions (`improvements_list`)

### LLM Integration Details

**Ollama API** (see `docs/OLLAMA_REFERENCE.md`):
- Endpoint: `{URL_BASE_OLLAMA}/api/generate`
- Authentication: `X-API-Key` header
- Model: `mistral:instruct`
- Forces JSON output via `"format": "json"` parameter

**OpenAI API**:
- Endpoint: `{URL_BASE_OPENAI}/chat/completions`
- Authentication: Bearer token
- Model: `gpt-4o-mini`
- Enforces JSON via `response_format: {"type": "json_object"}`

Both expect JSON responses with structure:
```json
{
  "updated_resume": "...",
  "updated_cover_letter": "...",
  "improvements_list": ["...", "..."]
}
```

### Prompt Engineering

The `prompt01.md` template defines the LLM behavior as an HR consultant. When modifying:
- Maintain placeholders: `< Resume of user>` and `< Job Requirements >`
- Preserve JSON output structure to avoid breaking result page rendering
- Test with both Ollama and OpenAI models (response formatting may differ)

### File Processing

**DOCX Handling**: `file_processing.read_docx()` writes uploaded bytes to a temporary file, extracts paragraphs via python-docx, then deletes the temp file. This is a simple MVP approach; future versions should handle tables, formatting, or use in-memory processing.

**Template Loading**: `read_prompt_template()` uses fallback path resolution to locate `prompt01.md` from different working directories.

### Error Handling

Routes return the same template with error messages on failure rather than raising HTTP exceptions. This maintains user experience but should be enhanced with proper status codes in production.

### Future Enhancements (Placeholders)

- **Resume Matching Scores**: Currently hardcoded ("85%", "95%"). Intended to use feature-extraction models for vector similarity scoring
- **File Storage**: Uploaded resumes are currently processed in-memory only. Requirements mention storing in a project directory (not yet implemented)
- **UI Styling**: See `docs/STYLE_GUIDE.md` for design specifications (black borders, rounded corners, etc.)
