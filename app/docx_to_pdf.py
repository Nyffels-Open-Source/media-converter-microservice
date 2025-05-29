from fastapi import UploadFile, HTTPException
import os
import subprocess
import uuid

TEMP_DIR = "/tmp/media"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_docx_to_pdf(file: UploadFile) -> str:
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only DOCX files allowed")

    temp_filename = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.docx")
    output_dir = TEMP_DIR

    with open(temp_filename, "wb") as f:
        f.write(file.file.read())

    try:
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            temp_filename
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="LibreOffice conversion failed")

    output_filename = os.path.splitext(os.path.basename(temp_filename))[0] + ".pdf"
    output_path = os.path.join(output_dir, output_filename)
    if not os.path.exists(output_path):
        raise HTTPException(status_code=500, detail="Converted PDF not found")

    os.remove(temp_filename)
    return output_path
