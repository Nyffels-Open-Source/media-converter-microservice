from fastapi import UploadFile, HTTPException
import tempfile
import os
import img2pdf

TEMP_DIR = "/tmp/media"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_images_to_pdf(files: list[UploadFile]) -> str:
    images = []
    for file in files:
        if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            raise HTTPException(status_code=400, detail="Only JPG/PNG images are supported")
        contents = file.file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:
            temp_img.write(contents)
            images.append(temp_img.name)

    output_pdf_path = os.path.join(TEMP_DIR, "output.pdf")
    try:
        with open(output_pdf_path, "wb") as f:
            f.write(img2pdf.convert(images))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF creation failed: {str(e)}")
    finally:
        for path in images:
            os.unlink(path)

    return output_pdf_path
