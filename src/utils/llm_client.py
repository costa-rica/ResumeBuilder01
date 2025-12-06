import requests
import json
from src.config import URL_BASE_OPENAI, KEY_OPENAI, URL_BASE_OLLAMA, KEY_OLLAMA, URL_BASE_DOAI, KEY_DOAI

def process_with_ollama(prompt: str, model: str = "mistral:instruct") -> dict:
    """
    Sends a prompt to the Ollama API.
    """
    url = f"{URL_BASE_OLLAMA}/api/generate"
    headers = {
        "X-API-Key": KEY_OLLAMA,  # Based on requirements, though standard Ollama might not need it, the doc says it does.
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json" # Force JSON mode if possible, or reliance on prompt instruction
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        # Parse the 'response' field which contains the actual text
        return json.loads(data["response"])
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return {
            "updated_resume": "Error generating resume.",
            "updated_cover_letter": "Error generating cover letter.",
            "improvements_list": [f"Error: {str(e)}"]
        }

def process_with_openai(prompt: str, model: str = "gpt-4o-mini") -> dict:
    """
    Sends a prompt to the OpenAI API.
    """
    url = f"{URL_BASE_OPENAI}/chat/completions"
    headers = {
        "Authorization": f"Bearer {KEY_OPENAI}",
        "Content-Type": "application/json"
    }
    
    # OpenAI Chat completion format
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        content = data['choices'][0]['message']['content']
        return json.loads(content)
    except Exception as e:
         print(f"Error calling OpenAI: {e}")
         return {
            "updated_resume": "Error generating resume.",
            "updated_cover_letter": "Error generating cover letter.",
            "improvements_list": [f"Error: {str(e)}"]
        }

def process_with_doai(prompt: str, model: str = "openai-gpt-oss-120b") -> dict:
    """
    Sends a prompt to the DoAI API.
    """
    url = f"{URL_BASE_DOAI}/chat/completions"
    headers = {
        "Authorization": f"Bearer {KEY_DOAI}",
        "Content-Type": "application/json"
    }

    # DoAI Chat completion format (similar to OpenAI)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
            {"role": "user", "content": prompt}
        ],
        # "response_format": {"type": "json_object"}, # Check if DoAI supports this, otherwise rely on prompt
        "max_tokens": 4000 # Increased from 2048 to avoid cutoff
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        content = data['choices'][0]['message']['content']
        # Try to clean markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
             content = content.split("```")[1].split("```")[0].strip()
             
        return json.loads(content)
    except Exception as e:
         print(f"Error calling DoAI: {e}")
         return {
            "updated_resume": "Error generating resume.",
            "updated_cover_letter": "Error generating cover letter.",
            "improvements_list": [f"Error: {str(e)}"]
        }

def generate_tailored_resume(resume_text: str, job_desc: str, model_choice: str, template_text: str) -> dict:
    """
    Controller to construct prompt and call the appropriate model.
    """
    # Fill the template
    prompt = template_text.replace("< Resume of user>", resume_text)
    prompt = prompt.replace("< Job Requirements >", job_desc)
    
    if "mistral" in model_choice.lower():
        return process_with_ollama(prompt, model="mistral:instruct")
    elif "gpt-4" in model_choice.lower():
        return process_with_openai(prompt, model="gpt-4o-mini")
    elif "openai-gpt-oss" in model_choice.lower():
         return process_with_doai(prompt, model="openai-gpt-oss-120b")
    else:
        # Default fallback
        return process_with_openai(prompt, model="gpt-4o-mini")
