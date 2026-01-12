"""
PDF processing and text extraction
"""

import pdfplumber
import PyPDF2
from typing import List, Dict, Any
import hashlib
from pathlib import Path


class PDFProcessor:
    """Processes PDF files and extracts text"""

    def __init__(self):
        self.supported_formats = [".pdf"]

    def extract_text(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Dictionary with text, metadata, and page information
        """
        try:
            # Try pdfplumber first (better for complex layouts)
            with pdfplumber.open(file_path) as pdf:
                pages = []
                full_text = []
                
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        pages.append({
                            "page_number": page_num,
                            "text": text,
                            "char_count": len(text)
                        })
                        full_text.append(text)
                
                return {
                    "text": "\n\n".join(full_text),
                    "pages": pages,
                    "total_pages": len(pdf.pages),
                    "metadata": pdf.metadata or {},
                    "extraction_method": "pdfplumber"
                }
        except Exception as e:
            # Fallback to PyPDF2
            try:
                with open(file_path, "rb") as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    pages = []
                    full_text = []
                    
                    for page_num, page in enumerate(pdf_reader.pages, 1):
                        text = page.extract_text()
                        if text:
                            pages.append({
                                "page_number": page_num,
                                "text": text,
                                "char_count": len(text)
                            })
                            full_text.append(text)
                    
                    return {
                        "text": "\n\n".join(full_text),
                        "pages": pages,
                        "total_pages": len(pdf_reader.pages),
                        "metadata": pdf_reader.metadata or {},
                        "extraction_method": "PyPDF2"
                    }
            except Exception as e2:
                raise ValueError(f"Failed to extract text from PDF: {str(e2)}")

    def validate_pdf(self, file_path: str) -> bool:
        """Validate that file is a valid PDF"""
        if not Path(file_path).exists():
            return False
        
        if not Path(file_path).suffix.lower() == ".pdf":
            return False
        
        try:
            with open(file_path, "rb") as file:
                # Check PDF header
                header = file.read(4)
                return header == b"%PDF"
        except Exception:
            return False

    def get_file_hash(self, file_path: str) -> str:
        """Generate hash for file to track versions"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
