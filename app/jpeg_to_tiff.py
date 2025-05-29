from fastapi import UploadFile, HTTPException
from PIL import Image
import os
import uuid

TEMP_DIR = "/tmp/media"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_jpeg_to_tiff(file: UploadFile) -> str:
    if not file.filename.lower().endswith((".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Only JPEG files allowed")

    try:
        img = Image.open(file.file)
        output_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.tiff")
        img.convert("RGB").save(output_path, "TIFF")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

    return output_path
