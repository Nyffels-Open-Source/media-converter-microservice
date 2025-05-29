from fastapi import UploadFile, HTTPException
from pdf2image import convert_from_bytes
import os
import zipfile

TEMP_DIR = "/tmp/media"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_pdf_to_images(file: UploadFile):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Uploaded file is not a PDF")

    pdf_bytes = file.file.read()
    try:
        images = convert_from_bytes(pdf_bytes, dpi=300)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF conversion failed: {str(e)}")

    zip_path = os.path.join(TEMP_DIR, f"{file.filename}_images.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for i, img in enumerate(images):
            img_path = os.path.join(TEMP_DIR, f"{file.filename}_page_{i}.jpg")
            img.save(img_path, "JPEG")
            zipf.write(img_path, arcname=os.path.basename(img_path))
            os.remove(img_path)

    return zip_path
