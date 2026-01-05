import os
from pypdf import PdfReader

def extract_text_from_file(file_path: str) -> str:
    """
    returns texts in file from file_path
    available formats: .txt, .pdf
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    try:
        if ext == ".txt":
            try:
                # read the file without parsing
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="cp949") as f:
                    text = f.read()

        elif ext == ".pdf":
            # read each page then merge
            reader = PdfReader(file_path)
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
