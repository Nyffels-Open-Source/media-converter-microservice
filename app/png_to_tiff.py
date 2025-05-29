from fastapi import UploadFile, HTTPException
from PIL import Image
import os
import uuid

TEMP_DIR = "/tmp/media"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_png_to_tiff(file: UploadFile) -> str:
    if not file.filename.lower().endswith(".png"):
        raise HTTPException(status_code=400, detail="Uploaded file is not a PNG")

    try:
        image = Image.open(file.file).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to open image: {str(e)}")

    output_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.tiff")
    image.save(output_path, "TIFF")
    return output_path
