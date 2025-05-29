from fastapi import UploadFile, HTTPException
import tempfile
import os
import img2pdf

TEMP_DIR = "/tmp/media"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_pngs_to_pdf(files: list[UploadFile]) -> str:
    image_paths = []
    for file in files:
        if not file.filename.lower().endswith(".png"):
            raise HTTPException(status_code=400, detail="Only PNG files allowed")
        contents = file.file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(contents)
            image_paths.append(tmp.name)

    output_path = os.path.join(TEMP_DIR, "converted_from_png.pdf")
    try:
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(image_paths))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    finally:
        for path in image_paths:
            os.remove(path)

    return output_path
