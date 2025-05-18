from crewai import Agent
from docling.document_converter import DocumentConverter

class InvoiceReaderAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Invoice Reader Agent',
            goal='Extrair itens de uma nota fiscal (PDF)',
            backstory='Especialista em extrair produtos de notas fiscais usando OCR inteligente.',
            verbose=True,
        )

    def run(self):
        pdf_path = "data/sample_invoice.pdf"
        print("📄 Lendo o PDF com Docling...")
        converter = DocumentConverter()
        result = converter.convert(pdf_path)
        return result.document.export_to_markdown()