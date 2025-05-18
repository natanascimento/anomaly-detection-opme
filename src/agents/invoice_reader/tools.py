import os

from crewai.tools import tool
from docling.document_converter import DocumentConverter


@tool("PDF Reader tool")
def pdf_reader(pdf_path: str):
    """
    Reads and converts a PDF file to Markdown format.
    
    This function uses a DocumentConverter to process PDF files
    and return their content converted to Markdown format. The function
    includes file existence checks and error handling.
    
    Args:
        pdf_path (str): Full path to the PDF file to be read.
                        Must be a valid path in the file system.
    
    Returns:
        str: PDF content converted to Markdown format.
             In case of an error (file not found), returns a
             formatted error message.
    
    Raises:
        Does not explicitly raise exceptions, but may propagate errors
        from the DocumentConverter if conversion issues occur.
    
    Example:
        >>> content = pdf_reader("/path/to/document.pdf")
        >>> print(content)
        # Markdown of the PDF content
        
        >>> content = pdf_reader("/nonexistent/file.pdf")
        >>> print(content)
        # ❌ File not found: /nonexistent/file.pdf
    
    Note:
        - The function prints status messages to the console during execution
        - Requires the DocumentConverter library to be available
        - The file must exist and be a valid PDF for successful conversion
    """

    print(f"📄 Lendo PDF: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        return f"❌ Arquivo não encontrado: {pdf_path}"
    
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    markdown_content = result.document.export_to_markdown()
    
    print("✅ PDF convertido com sucesso!")

    print(markdown_content)
    return markdown_content
