import os
import uuid
from PIL import Image
from fastapi import UploadFile, HTTPException

TEMP_DIR = "/tmp/media"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_image(file: UploadFile, to_format: str) -> str:
    name, ext = os.path.splitext(file.filename)
    input_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}{ext}")
    output_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.{to_format.lower()}")

    with open(input_path, "wb") as f:
        f.write(file.file.read())

    try:
        img = Image.open(input_path).convert("RGB")
        img.save(output_path, format=to_format.upper())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image conversion failed: {str(e)}")

    return output_path
