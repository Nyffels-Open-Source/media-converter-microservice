import os
import uuid
import subprocess
from fastapi import UploadFile, HTTPException

TEMP_DIR = "/tmp/media"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_pptx_to_pdf(file: UploadFile) -> str:
    if not file.filename.lower().endswith(".pptx"):
        raise HTTPException(status_code=400, detail="Uploaded file is not a PPTX")

    input_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.pptx")
    output_dir = TEMP_DIR
    output_pdf_path = input_path.replace(".pptx", ".pdf")

    with open(input_path, "wb") as f:
        f.write(file.file.read())

    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", output_dir, input_path], check=True)

    if not os.path.exists(output_pdf_path):
        raise HTTPException(status_code=500, detail="PDF conversion failed")

    return output_pdf_path
