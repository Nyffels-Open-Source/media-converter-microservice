from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from app.pdf_to_image import convert_pdf_to_images
from app.image_to_pdf import convert_images_to_pdf
from typing import List
import os

app = FastAPI(title="Media Converter Service", version="1.0")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/pdf/to-image")
async def pdf_to_image(file: UploadFile = File(...)):
    zip_path = convert_pdf_to_images(file)
    return FileResponse(zip_path, media_type="application/zip", filename="converted_images.zip")

@app.post("/image/to-pdf")
async def image_to_pdf(files: List[UploadFile] = File(...)):
    output_path = convert_images_to_pdf(files)
    return FileResponse(output_path, media_type="application/pdf", filename="converted.pdf")
