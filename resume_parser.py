import io
import re
import fitz
from docx import Document

KNOWN_SKILLS = [
    "python", "java", "c++", "javascript", "sql",
    "machine learning", "deep learning", "artificial intelligence",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
    "power bi", "tableau", "excel", "aws", "azure", "docker",
    "kubernetes", "fastapi", "flask", "django", "react", "node.js",
    "git", "github", "langchain", "rag", "llm", "nlp",
    "computer vision", "statistics", "data analysis", "spark",
    "databricks"
]

def extract_pdf_text(file_bytes):
    text = ""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_docx_text(file_bytes):
    document = Document(io.BytesIO(file_bytes))
    return "\n".join(
        p.text for p in document.paragraphs if p.text.strip()
    )

def extract_skills(text):
    text_lower = text.lower()
    found = []

    for skill in KNOWN_SKILLS:
        if re.search(r"(?<!\w)" + re.escape(skill) + r"(?!\w)", text_lower):
            found.append(skill)

    return sorted(set(found))

def parse_resume(file_bytes, filename):
    if filename.lower().endswith(".pdf"):
        text = extract_pdf_text(file_bytes)
    elif filename.lower().endswith(".docx"):
        text = extract_docx_text(file_bytes)
    else:
        raise ValueError("Only PDF and DOCX resumes are supported.")

    return {
        "text": text,
        "skills": extract_skills(text),
        "word_count": len(text.split()),
    }
