import fitz


def extract_text_from_pdf(pdf_source) -> str:
    text = ""
    try:
        if isinstance(pdf_source, str):
            doc = fitz.open(pdf_source)
        else:
            pdf_bytes = pdf_source.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        for page in doc:
            text += page.get_text()

        doc.close()
        return text.strip()

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""