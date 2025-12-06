import docx
import os

def read_docx(file_contents: bytes) -> str:
    """
    Extracts text from a docx file byte stream.
    """
    # write to a temporary file 
    temp_filename = "temp_resume.docx"
    with open(temp_filename, "wb") as f:
        f.write(file_contents)
    
    doc = docx.Document(temp_filename)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    
    # cleanup
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
        
    return "\n".join(full_text)

def read_prompt_template(template_path: str = "src/templates/markdown/prompt01.md") -> str:
    """
    Reads the markdown prompt template.
    """
    base_path = os.getcwd()
    full_path = os.path.join(base_path, template_path)
    if not os.path.exists(full_path):
        # Fallback relative path try
        full_path = os.path.join(base_path, "src", "templates", "markdown", "prompt01.md")

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Prompt template not found at {full_path}")
        
    with open(full_path, "r") as f:
        return f.read()
