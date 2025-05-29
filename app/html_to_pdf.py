import os
import tempfile
from fastapi import UploadFile
from weasyprint import HTML

def convert_html_to_pdf(file: UploadFile) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as html_file:
        html_file.write(file.file.read())
        html_file.flush()
        output_path = "/tmp/output.pdf"
        HTML(html_file.name).write_pdf(output_path)
        return output_path
