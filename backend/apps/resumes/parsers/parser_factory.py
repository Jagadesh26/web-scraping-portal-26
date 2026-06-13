from .pdf_parser import PDFParser
from .docx_parser import DOCXParser


class ParserFactory:

    @staticmethod
    def get_parser(file_type):

        if file_type.lower() == "pdf":
            return PDFParser

        if file_type.lower() == "docx":
            return DOCXParser

        raise ValueError(
            "Unsupported file type."
        )