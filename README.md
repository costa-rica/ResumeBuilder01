# Resume Builder

This is a resume builder application that uses OpenAI and Ollama to generate a tailored resume based on the user's input.

## .env
```
URL_BASE_OLLAMA=https://fell-st-ollama.dashanddata.com
KEY_OLLAMA=ENTER_YOUR_OLLAMA_API_KEY
URL_BASE_OPENAI=https://api.openai.com/v1
KEY_OPENAI=ENTER_YOUR_OPENAI_API_KEY
URL_BASE_DOAI=https://inference.do-ai.run/v1
KEY_DOAI=ENTER_YOUR_DOAI_API_KEY
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 -m uvicorn src.main:app --reload
```

## License

MIT
