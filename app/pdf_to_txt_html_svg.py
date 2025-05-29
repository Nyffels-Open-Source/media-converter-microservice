import os
import uuid
import subprocess
from fastapi import UploadFile, HTTPException

TEMP_DIR = "/tmp/media"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_pdf_to_txt(file: UploadFile) -> str:
    return _convert_pdf_generic(file, ".txt", ["pdftotext"])

def convert_pdf_to_html(file: UploadFile) -> str:
    return _convert_pdf_generic(file, ".html", ["pdftohtml", "-s", "-noframes"])

def convert_pdf_to_svg(file: UploadFile) -> str:
    return _convert_pdf_generic(file, ".svg", ["pdftocairo", "-svg"])

def _convert_pdf_generic(file: UploadFile, extension: str, command_prefix: list) -> str:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Uploaded file is not a PDF")

    input_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.pdf")
    output_path = input_path.replace(".pdf", extension)

    with open(input_path, "wb") as f:
        f.write(file.file.read())

    cmd = command_prefix + [input_path, output_path]
    subprocess.run(cmd, check=True)

    if not os.path.exists(output_path):
        raise HTTPException(status_code=500, detail=f"Conversion to {extension} failed")

    return output_path
