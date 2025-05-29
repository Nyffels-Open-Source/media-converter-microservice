from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from app.pdf_to_image import convert_pdf_to_images
from app.image_to_pdf import convert_images_to_pdf
from app.pdf_to_png import convert_pdf_to_png
from app.png_to_pdf import convert_pngs_to_pdf
from app.docx_to_pdf import convert_docx_to_pdf
from app.tiff_to_jpeg import convert_tiff_to_jpeg
from app.jpeg_to_tiff import convert_jpeg_to_tiff
from app.tiff_to_png import convert_tiff_to_png
from app.png_to_tiff import convert_png_to_tiff
from typing import List
import os

app = FastAPI(title="Media Converter Service", version="1.0", description="Microservice for file format conversions")

@app.get("/health", tags=["Health"])
def health_check():
    """Returns OK if the service is running."""
    return {"status": "ok"}

@app.post("/pdf/to-image", tags=["Conversion"])
async def pdf_to_image(file: UploadFile = File(...)):
    """Convert PDF pages to JPEG images and return a ZIP archive."""
    zip_path = convert_pdf_to_images(file)
    return FileResponse(zip_path, media_type="application/zip", filename="converted_images.zip")

@app.post("/image/to-pdf", tags=["Conversion"])
async def image_to_pdf(files: List[UploadFile] = File(...)):
    """Combine multiple image files into a single PDF."""
    output_path = convert_images_to_pdf(files)
    return FileResponse(output_path, media_type="application/pdf", filename="converted.pdf")

@app.post("/pdf/to-png", tags=["Conversion"])
async def pdf_to_png(file: UploadFile = File(...)):
    """Convert a PDF to multiple PNG images and return a ZIP archive."""
    zip_path = convert_pdf_to_png(file)
    return FileResponse(zip_path, media_type="application/zip", filename="converted_images.zip")

@app.post("/png/to-pdf", tags=["Conversion"])
async def png_to_pdf(files: List[UploadFile] = File(...)):
    """Convert multiple PNG images into a PDF file."""
    output_path = convert_pngs_to_pdf(files)
    return FileResponse(output_path, media_type="application/pdf", filename="converted.pdf")

@app.post("/docx/to-pdf", tags=["Conversion"])
async def docx_to_pdf(file: UploadFile = File(...)):
    """Convert a DOCX file to PDF using LibreOffice."""
    output_path = convert_docx_to_pdf(file)
    return FileResponse(output_path, media_type="application/pdf", filename="converted.pdf")

@app.post("/tiff/to-jpeg", tags=["Conversion"])
async def tiff_to_jpeg(file: UploadFile = File(...)):
    """Convert a TIFF image to JPEG format."""
    output_path = convert_tiff_to_jpeg(file)
    return FileResponse(output_path, media_type="image/jpeg", filename="converted.jpg")

@app.post("/jpeg/to-tiff", tags=["Conversion"])
async def jpeg_to_tiff(file: UploadFile = File(...)):
    """Convert a JPEG image to TIFF format."""
    output_path = convert_jpeg_to_tiff(file)
    return FileResponse(output_path, media_type="image/tiff", filename="converted.tiff")


@app.post("/tiff/to-png", tags=["Conversion"])
async def tiff_to_png(file: UploadFile = File(...)):
    """Convert a TIFF image to PNG format."""
    output_path = convert_tiff_to_png(file)
    return FileResponse(output_path, media_type="image/png", filename="converted.png")

@app.post("/png/to-tiff", tags=["Conversion"])
async def png_to_tiff(file: UploadFile = File(...)):
    """Convert a PNG image to TIFF format."""
    output_path = convert_png_to_tiff(file)
    return FileResponse(output_path, media_type="image/tiff", filename="converted.tiff")
