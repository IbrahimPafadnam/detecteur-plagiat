import os
import PyPDF2
from docx import Document

def read_file(file_path):
    _, extension = os.path.splitext(file_path)
    if extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif extension == '.pdf':
        return read_pdf(file_path)
    elif extension == '.docx':
        return read_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {extension}")

def read_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return ' '.join([page.extract_text() for page in reader.pages])

def read_docx(file_path):
    doc = Document(file_path)
    return ' '.join([paragraph.text for paragraph in doc.paragraphs])