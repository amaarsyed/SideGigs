import re
from io import BytesIO

try:
    from pdfminer.high_level import extract_text as pdf_extract_text
except Exception:  # pragma: no cover
    pdf_extract_text = None

try:
    from docx import Document
except Exception:  # pragma: no cover
    Document = None

EMAIL_RE = re.compile(r"[\w.+'-]+@[\w.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\s().-]{7,}\d")
SKILLS = ["python", "javascript", "react", "django", "java", "sql", "html", "css", "tailwind", "next.js"]


def _extract_text(data: bytes, filename: str) -> str:
    if filename.lower().endswith('.pdf'):
        if not pdf_extract_text:
            raise RuntimeError('pdfminer.six not installed')
        return pdf_extract_text(BytesIO(data))
    if filename.lower().endswith('.docx'):
        if not Document:
            raise RuntimeError('python-docx not installed')
        doc = Document(BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Unsupported file type")


def parse_resume(data: bytes, filename: str) -> dict:
    text = _extract_text(data, filename)
    email = next(iter(EMAIL_RE.findall(text)), None)
    phone = next(iter(PHONE_RE.findall(text)), None)
    text_lower = text.lower()
    skills = [s for s in SKILLS if s in text_lower]
    return {
        "email": email,
        "phone": phone,
        "skills": skills,
        "raw_excerpt": text[:2000],
    }
