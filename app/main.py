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
from app.xlsx_to_pdf import convert_xlsx_to_pdf
from app.html_to_pdf import convert_html_to_pdf
from app.pdf_to_pdfa import convert_pdf_to_pdfa
from app.base64_tools import (
    convert_file_to_base64,
    convert_file_to_base64_datastring,
    convert_base64_to_file,
    convert_datauri_to_file,
    Base64FileInput,
    Base64DataURIInput,
)
from typing import List
import os

app = FastAPI(title="Media Converter Service", version="1.0", description="Microservice for file format conversions")

# All endpoint routes are now reorganized into categories: Health, PDF, Office, Image, Archive, Base64.
# This keeps Swagger UI tidy and logical.

# [HEALTH]
@app.get("/health", tags=["Health"])
def health_check():
    """Returns OK if the service is running."""
    return {"status": "ok"}

# [PDF]
@app.post(
    "/pdf/to-image",
    tags=["PDF"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {
                "application/zip": {
                    "schema": {
                        "type": "string",
                        "format": "binary"
                    }
                }
            },
            "description": "ZIP archive containing JPEG images",
            "content_type": "application/zip"
        }
    },
)
async def pdf_to_image(file: UploadFile = File(...)):
    """Convert PDF to JPEG images (as ZIP)."""
    zip_path = convert_pdf_to_images(file)
    return FileResponse(zip_path, media_type="application/zip", filename="converted_images.zip")

@app.post(
    "/pdf/to-png",
    tags=["PDF"],
    response_class=FileResponse,
    responses={
        200: {
                        "content": {
                            "application/zip": {
                                "schema": {
                                    "type": "string",
                                    "format": "binary"
                                }
                            }
                        },
            "description": "ZIP archive containing PNG images",
            "content_type": "application/zip"
        }
    },
)
async def pdf_to_png(file: UploadFile = File(...)):
    """Convert PDF to PNG images (as ZIP)."""
    zip_path = convert_pdf_to_png(file)
    return FileResponse(zip_path, media_type="application/zip", filename="converted_images.zip")

@app.post(
    "/pdf/to-txt",
    tags=["PDF"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"text/plain": { "schema": {"type": "string"}}},
            "description": "Plain text extracted from PDF",
            "content_type": "text/plain"
        }
    },
)
async def pdf_to_txt(file: UploadFile = File(...)):
    """Convert PDF to plain text."""
    return FileResponse(convert_pdf_to_txt(file), media_type="text/plain", filename="converted.txt")

@app.post(
    "/pdf/to-html",
    tags=["PDF"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"text/html": { "schema": {"type": "string"}}},
            "description": "HTML content converted from PDF",
            "content_type": "text/html"
        }
    },
)
async def pdf_to_html(file: UploadFile = File(...)):
    """Convert PDF to HTML."""
    return FileResponse(convert_pdf_to_html(file), media_type="text/html", filename="converted.html")

@app.post(
    "/pdf/to-svg",
    tags=["PDF"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {
                "image/svg+xml": {
                    "schema": { "type": "string", "format": "binary" }
                }
            },
            "description": "SVG content converted from PDF",
            "content_type": "image/svg+xml"
        }
    },
)
async def pdf_to_svg(file: UploadFile = File(...)):
    """Convert PDF to SVG."""
    return FileResponse(convert_pdf_to_svg(file), media_type="image/svg+xml", filename="converted.svg")

@app.post(
    "/pdf/to-pdfa",
    tags=["PDF"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"application/pdf": { "schema": { "type": "string", "format": "binary" } }},
            "description": "PDF/A converted file",
            "content_type": "application/pdf"
        }
    },
)
async def pdf_to_pdfa(file: UploadFile = File(...)):
    """Convert PDF to PDF/A using Ghostscript."""
    return FileResponse(convert_pdf_to_pdfa(file), media_type="application/pdf", filename="converted_pdfa.pdf")

# [OFFICE]
@app.post(
    "/docx/to-pdf",
    tags=["Office"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"application/pdf": { "schema": { "type": "string", "format": "binary" } }},
            "description": "PDF converted from DOCX",
            "content_type": "application/pdf"
        }
    },
)
async def docx_to_pdf(file: UploadFile = File(...)):
    return FileResponse(convert_docx_to_pdf(file), media_type="application/pdf", filename="converted.pdf")

@app.post(
    "/odt/to-pdf",
    tags=["Office"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"application/pdf": { "schema": { "type": "string", "format": "binary" } }},
            "description": "PDF converted from ODT",
            "content_type": "application/pdf"
        }
    },
)
async def odt_to_pdf(file: UploadFile = File(...)):
    return FileResponse(convert_odt_to_pdf(file), media_type="application/pdf", filename="converted.pdf")

@app.post(
    "/pptx/to-pdf",
    tags=["Office"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"application/pdf": { "schema": { "type": "string", "format": "binary" } }},
            "description": "PDF converted from PPTX",
            "content_type": "application/pdf"
        }
    },
)
async def pptx_to_pdf(file: UploadFile = File(...)):
    return FileResponse(convert_pptx_to_pdf(file), media_type="application/pdf", filename="converted.pdf")

@app.post(
    "/xlsx/to-pdf",
    tags=["Office"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"application/pdf": { "schema": { "type": "string", "format": "binary" } }},
            "description": "PDF converted from XLSX",
            "content_type": "application/pdf"
        }
    },
)
async def xlsx_to_pdf(file: UploadFile = File(...)):
    return FileResponse(convert_xlsx_to_pdf(file), media_type="application/pdf", filename="converted.pdf")

@app.post(
    "/html/to-pdf",
    tags=["Office"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"application/pdf": { "schema": { "type": "string", "format": "binary" } }},
            "description": "PDF converted from HTML",
            "content_type": "application/pdf"
        }
    },
)
async def html_to_pdf(file: UploadFile = File(...)):
    return FileResponse(convert_html_to_pdf(file), media_type="application/pdf", filename="converted.pdf")

# [IMAGE]
@app.post(
    "/image/to-pdf",
    tags=["Image"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"application/pdf": { "schema": { "type": "string", "format": "binary" } }},
            "description": "PDF converted from images",
            "content_type": "application/pdf"
        }
    },
)
async def image_to_pdf(files: List[UploadFile] = File(...)):
    return FileResponse(convert_images_to_pdf(files), media_type="application/pdf", filename="converted.pdf")

@app.post(
    "/tiff/to-jpeg",
    tags=["Image"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"image/jpeg": { "schema": { "type": "string", "format": "binary" } }},
            "description": "JPEG converted from TIFF",
            "content_type": "image/jpeg"
        }
    },
)
async def tiff_to_jpeg(file: UploadFile = File(...)):
    return FileResponse(convert_tiff_to_jpeg(file), media_type="image/jpeg", filename="converted.jpg")

@app.post(
    "/jpeg/to-tiff",
    tags=["Image"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"image/tiff": { "schema": { "type": "string", "format": "binary" } }},
            "description": "TIFF converted from JPEG",
            "content_type": "image/tiff"
        }
    },
)
async def jpeg_to_tiff(file: UploadFile = File(...)):
    return FileResponse(convert_jpeg_to_tiff(file), media_type="image/tiff", filename="converted.tiff")

@app.post(
    "/tiff/to-png",
    tags=["Image"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"image/png": { "schema": { "type": "string", "format": "binary" } }},
            "description": "PNG converted from TIFF",
            "content_type": "image/png"
        }
    },
)
async def tiff_to_png(file: UploadFile = File(...)):
    return FileResponse(convert_tiff_to_png(file), media_type="image/png", filename="converted.png")

@app.post(
    "/png/to-tiff",
    tags=["Image"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"image/tiff": { "schema": { "type": "string", "format": "binary" } }},
            "description": "TIFF converted from PNG",
            "content_type": "image/tiff"
        }
    },
)
async def png_to_tiff(file: UploadFile = File(...)):
    return FileResponse(convert_png_to_tiff(file), media_type="image/tiff", filename="converted.tiff")

@app.post(
    "/png/to-jpeg",
    tags=["Image"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"image/jpeg": { "schema": { "type": "string", "format": "binary" } }},
            "description": "JPEG converted from PNG",
            "content_type": "image/jpeg"
        }
    },
)
async def png_to_jpeg(file: UploadFile = File(...)):
    return FileResponse(convert_image(file, "jpeg"), media_type="image/jpeg", filename="converted.jpeg")

@app.post(
    "/jpeg/to-png",
    tags=["Image"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"image/png": { "schema": { "type": "string", "format": "binary" } }},
            "description": "PNG converted from JPEG",
            "content_type": "image/png"
        }
    },
)
async def jpeg_to_png(file: UploadFile = File(...)):
    return FileResponse(convert_image(file, "png"), media_type="image/png", filename="converted.png")

@app.post(
    "/svg/to-png",
    tags=["Image"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"image/png": { "schema": { "type": "string", "format": "binary" } }},
            "description": "PNG converted from SVG",
            "content_type": "image/png"
        }
    },
)
async def svg_to_png(file: UploadFile = File(...)):
    return FileResponse(convert_image(file, "png"), media_type="image/png", filename="converted.png")

@app.post(
    "/webp/to-png",
    tags=["Image"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"image/png": { "schema": { "type": "string", "format": "binary" } }},
            "description": "PNG converted from WebP",
            "content_type": "image/png"
        }
    },
)
async def webp_to_png(file: UploadFile = File(...)):
    return FileResponse(convert_image(file, "png"), media_type="image/png", filename="converted.png")

@app.post(
    "/webp/to-jpeg",
    tags=["Image"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"image/jpeg": { "schema": { "type": "string", "format": "binary" } }},
            "description": "JPEG converted from WebP",
            "content_type": "image/jpeg"
        }
    },
)
async def webp_to_jpeg(file: UploadFile = File(...)):
    return FileResponse(convert_image(file, "jpeg"), media_type="image/jpeg", filename="converted.jpeg")

@app.post(
    "/png/to-webp",
    tags=["Image"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"image/webp": { "schema": { "type": "string", "format": "binary" } }},
            "description": "WebP converted from PNG",
            "content_type": "image/webp"
        }
    },
)
async def png_to_webp(file: UploadFile = File(...)):
    return FileResponse(convert_image(file, "webp"), media_type="image/webp", filename="converted.webp")

@app.post(
    "/jpeg/to-webp",
    tags=["Image"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"image/webp": { "schema": { "type": "string", "format": "binary" } }},
            "description": "WebP converted from JPEG",
            "content_type": "image/webp"
        }
    },
)
async def jpeg_to_webp(file: UploadFile = File(...)):
    return FileResponse(convert_image(file, "webp"), media_type="image/webp", filename="converted.webp")

# [ARCHIVE]
@app.post(
    "/zip/to-tar",
    tags=["Archive"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"application/x-tar": {"schema": { "type": "string", "format": "binary" } }},
            "description": "TAR archive converted from ZIP",
            "content_type": "application/x-tar"
        }
    },
)
async def zip_to_tar(file: UploadFile = File(...)):
    return FileResponse(convert_zip_to_tar(file), media_type="application/x-tar", filename="converted.tar")

@app.post(
    "/tar/to-zip",
    tags=["Archive"],
    response_class=FileResponse,
    responses={
        200: {
                        "content": {
                "application/zip": {
                    "schema": {
                        "type": "string",
                        "format": "binary"
                    }
                }
            },
            "description": "ZIP archive converted from TAR",
            "content_type": "application/zip"
        }
    },
)
async def tar_to_zip(file: UploadFile = File(...)):
    return FileResponse(convert_tar_to_zip(file), media_type="application/zip", filename="converted.zip")

@app.post(
    "/zip/to-7z",
    tags=["Archive"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"application/x-7z-compressed": {}},
            "description": "7z archive converted from ZIP",
            "content_type": "application/x-7z-compressed"
        }
    },
)
async def zip_to_7z(file: UploadFile = File(...)):
    return FileResponse(convert_zip_to_7z(file), media_type="application/x-7z-compressed", filename="converted.7z")

@app.post(
    "/7z/to-zip",
    tags=["Archive"],
    operation_id="sevenZToZip",
    response_class=FileResponse,
    responses={
        200: {
                        "content": {
                "application/zip": {
                    "schema": {
                        "type": "string",
                        "format": "binary"
                    }
                }
            },
            "description": "ZIP archive converted from 7z",
            "content_type": "application/zip"
        }
    },
)
async def sevenz_to_zip(file: UploadFile = File(...)):
    return FileResponse(convert_7z_to_zip(file), media_type="application/zip", filename="converted.zip")

# [BASE64]
@app.post("/file/to-base64", tags=["Base64"])
async def file_to_base64(file: UploadFile = File(...)):
    """
    Convert file to base64 + metadata.
    Returns base64 content and file info.
    """
    return await convert_file_to_base64(file)

@app.post("/file/to-base64-datastring", tags=["Base64"])
async def file_to_base64_datastring(file: UploadFile = File(...)):
    """Convert file to base64 data URI string."""
    return await convert_file_to_base64_datastring(file)

@app.post(
    "/base64-to-file",
    tags=["Base64"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"application/octet-stream": { "schema": { "type": "string", "format": "binary" } }},
            "description": "Binary file converted from base64",
            "content_type": "application/octet-stream"
        }
    },
)
async def base64_to_file(input: Base64FileInput):
    """Convert base64 + metadata to downloadable file."""
    return convert_base64_to_file(input)

@app.post(
    "/base64-datastring-to-file",
    tags=["Base64"],
    response_class=FileResponse,
    responses={
        200: {
            "content": {"application/octet-stream": { "schema": { "type": "string", "format": "binary" } }},
            "description": "Binary file converted from base64 data URI",
            "content_type": "application/octet-stream"
        }
    },
)
async def base64_datastring_to_file(input: Base64DataURIInput):
    """Convert base64 data URI to downloadable file."""
    return convert_datauri_to_file(input)
