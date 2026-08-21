import fitz

class ParserService:

    @staticmethod
    def extract_resume(file_path:str) -> str:
        document = fitz.open(file_path)

        pages = []

        for page in document:
            text = page.get_text()
            pages.append(text)

        document.close()

        return "\n".join(pages).strip()
    