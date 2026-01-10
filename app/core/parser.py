import os
from pypdf import PdfReader
from io import BytesIO, TextIOWrapper

def extract_text_from_file(file_content, filename: str) -> str:
    """
    returns texts in file from file content (file-like object or bytes)
    available formats: .txt, .pdf
    """
    ext = os.path.splitext(filename)[1].lower()
    text = ""

    # Ensure file_content is a file-like object
    if isinstance(file_content, bytes):
        file_content = BytesIO(file_content)

    # Ensure pointer is at the beginning
    if hasattr(file_content, 'seek'):
        file_content.seek(0)

    try:
        if ext == ".txt":
            # Read content as bytes first
            content_bytes = file_content.read()
            try:
                text = content_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text = content_bytes.decode("cp949")

        elif ext == ".pdf":
            # read each page then merge
            reader = PdfReader(file_content)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            # prevent PostgreSQL error: remove NUL char(\x00)
            text = text.replace("\x00", "")

        else:
            text = "Unsupported format"

    except Exception as e:
        print(f"Error parsing file: {e}")
        text = f"Error extracting text: {str(e)}"

    return text
