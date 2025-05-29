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
from app.pptx_to_pdf import convert_pptx_to_pdf
from app.odt_to_pdf import convert_odt_to_pdf
from app.pdf_to_txt_html_svg import convert_pdf_to_txt, convert_pdf_to_html, convert_pdf_to_svg
from app.image_conversion import convert_image
from app.zip_to_tar import convert_zip_to_tar
from app.tar_to_zip import convert_tar_to_zip
from app.zip_to_7z import convert_zip_to_7z
from app.sevenz_to_zip import convert_7z_to_zip
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

@app.post("/pptx/to-pdf", tags=["Conversion"])
async def pptx_to_pdf(file: UploadFile = File(...)):
    """Convert a PPTX file to PDF using LibreOffice."""
    output_path = convert_pptx_to_pdf(file)
    return FileResponse(output_path, media_type="application/pdf", filename="converted.pdf")

@app.post("/odt/to-pdf", tags=["Conversion"])
async def odt_to_pdf(file: UploadFile = File(...)):
    """Convert an ODT file to PDF using LibreOffice."""
    output_path = convert_odt_to_pdf(file)
    return FileResponse(output_path, media_type="application/pdf", filename="converted.pdf")

@app.post("/pdf/to-txt", tags=["Conversion"])
async def pdf_to_txt(file: UploadFile = File(...)):
    """Convert a PDF file to plain text."""
    output_path = convert_pdf_to_txt(file)
    return FileResponse(output_path, media_type="text/plain", filename="converted.txt")

@app.post("/pdf/to-html", tags=["Conversion"])
async def pdf_to_html(file: UploadFile = File(...)):
    """Convert a PDF file to HTML format."""
    output_path = convert_pdf_to_html(file)
    return FileResponse(output_path, media_type="text/html", filename="converted.html")

@app.post("/pdf/to-svg", tags=["Conversion"])
async def pdf_to_svg(file: UploadFile = File(...)):
    """Convert a PDF file to SVG format."""
    output_path = convert_pdf_to_svg(file)
    return FileResponse(output_path, media_type="image/svg+xml", filename="converted.svg")

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

@app.post("/png/to-jpeg", tags=["Conversion"])
async def png_to_jpeg(file: UploadFile = File(...)):
    """Convert PNG to JPEG format."""
    output_path = convert_image(file, "jpeg")
    return FileResponse(output_path, media_type="image/jpeg", filename="converted.jpeg")

@app.post("/jpeg/to-png", tags=["Conversion"])
async def jpeg_to_png(file: UploadFile = File(...)):
    """Convert JPEG to PNG format."""
    output_path = convert_image(file, "png")
    return FileResponse(output_path, media_type="image/png", filename="converted.png")

@app.post("/svg/to-png", tags=["Conversion"])
async def svg_to_png(file: UploadFile = File(...)):
    """Convert SVG to PNG format."""
    output_path = convert_image(file, "png")
    return FileResponse(output_path, media_type="image/png", filename="converted.png")

@app.post("/webp/to-png", tags=["Conversion"])
async def webp_to_png(file: UploadFile = File(...)):
    """Convert WEBP to PNG format."""
    output_path = convert_image(file, "png")
    return FileResponse(output_path, media_type="image/png", filename="converted.png")

@app.post("/webp/to-jpeg", tags=["Conversion"])
async def webp_to_jpeg(file: UploadFile = File(...)):
    """Convert WEBP to JPEG format."""
    output_path = convert_image(file, "jpeg")
    return FileResponse(output_path, media_type="image/jpeg", filename="converted.jpeg")

@app.post("/png/to-webp", tags=["Conversion"])
async def png_to_webp(file: UploadFile = File(...)):
    """Convert PNG to WEBP format."""
    output_path = convert_image(file, "webp")
    return FileResponse(output_path, media_type="image/webp", filename="converted.webp")

@app.post("/jpeg/to-webp", tags=["Conversion"])
async def jpeg_to_webp(file: UploadFile = File(...)):
    """Convert JPEG to WEBP format."""
    output_path = convert_image(file, "webp")
    return FileResponse(output_path, media_type="image/webp", filename="converted.webp")


@app.post("/zip/to-tar", tags=["Conversion"])
async def zip_to_tar(file: UploadFile = File(...)):
    """Convert ZIP archive to TAR format."""
    output_path = convert_zip_to_tar(file)
    return FileResponse(output_path, media_type="application/x-tar", filename="converted.tar")

@app.post("/tar/to-zip", tags=["Conversion"])
async def tar_to_zip(file: UploadFile = File(...)):
    """Convert TAR archive to ZIP format."""
    output_path = convert_tar_to_zip(file)
    return FileResponse(output_path, media_type="application/zip", filename="converted.zip")

@app.post("/zip/to-7z", tags=["Conversion"])
async def zip_to_7z(file: UploadFile = File(...)):
    """Convert ZIP archive to 7z format."""
    output_path = convert_zip_to_7z(file)
    return FileResponse(output_path, media_type="application/x-7z-compressed", filename="converted.7z")

@app.post("/7z/to-zip", tags=["Conversion"])
async def sevenz_to_zip(file: UploadFile = File(...)):
    """Convert 7z archive to ZIP format."""
    output_path = convert_7z_to_zip(file)
    return FileResponse(output_path, media_type="application/zip", filename="converted.zip")