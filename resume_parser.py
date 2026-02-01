from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract raw text from a PDF resume in an ATS-like manner.
    """

    reader = PdfReader(pdf_path)
    text_chunks = []

    for idx, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text:
                text_chunks.append(text)
        except Exception as e:
            print(f"[WARN] Failed to read page {idx}: {e}")

    full_text = "\n".join(text_chunks)

    # ATS normalization
    full_text = full_text.replace("\t", " ")
    full_text = full_text.replace("\xa0", " ")
    full_text = " ".join(full_text.split())

    return full_text


if __name__ == "__main__":
    text = extract_text_from_pdf("sample_resume.pdf")
    print(text[:2000])
