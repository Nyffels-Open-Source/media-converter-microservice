from fastapi import UploadFile, HTTPException
from pdf2image import convert_from_bytes
from PIL import Image
import os
import uuid
import zipfile

TEMP_DIR = "/tmp/media"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_pdf_to_png(file: UploadFile) -> str:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Uploaded file is not a PDF")

    pdf_bytes = file.file.read()
    try:
        images = convert_from_bytes(pdf_bytes, dpi=300)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF conversion failed: {str(e)}")

    image_paths = []
    for i, img in enumerate(images):
        img_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.png")
        img.save(img_path, "PNG")
        image_paths.append(img_path)

    zip_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for img_path in image_paths:
            zipf.write(img_path, arcname=os.path.basename(img_path))

    return zip_path
