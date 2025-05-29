# Media Conversion Microservice

**Author:** [Nyffels BV](https://nyffels.be)  
**Contact:** chesney@nyffels.be  
**Repository:** [Nyffels-Open-Source/media-converter-microservice](https://github.com/Nyffels-Open-Source/media-converter-microservice)  
**DockerHub:** [nyffels/media-convertion-microservice](https://hub.docker.com/repository/docker/nyffels/media-convertion-microservice)

---

## 🧩 Overview

The **Media Conversion Microservice** is a powerful, lightweight FastAPI-based service designed to convert various document, archive and image formats. It is built for **private infrastructure** and allows automation of file conversions using HTTP endpoints.

You can run it locally, on-premise, or behind a secured gateway.

---

## ⚠️ Security Notice

> ❗ **This service has no built-in authentication or security mechanisms.**  
> It is **meant to run behind a secure gateway or inside a private network.** Do NOT expose this service directly to the public internet without proper protection (reverse proxy, firewall, authentication, etc.).

---

## 📦 Features

The microservice exposes multiple categories of conversion endpoints:

### ✅ Health
- `GET /health`: check if the service is up.

### 📄 PDF
- `/pdf/to-image` – PDF to JPEG (zipped)
- `/pdf/to-png` – PDF to PNG (zipped)
- `/pdf/to-txt` – PDF to plain text
- `/pdf/to-html` – PDF to HTML
- `/pdf/to-svg` – PDF to SVG
- `/pdf/to-pdfa` – PDF to PDF/A (archival)

### 📝 Office
- `/docx/to-pdf` – DOCX to PDF
- `/odt/to-pdf` – ODT to PDF
- `/pptx/to-pdf` – PPTX to PDF
- `/xlsx/to-pdf` – XLSX to PDF
- `/html/to-pdf` – HTML to PDF

### 🖼️ Image
- `/image/to-pdf` – Multiple images to one PDF
- `/tiff/to-jpeg`, `/jpeg/to-tiff`
- `/tiff/to-png`, `/png/to-tiff`
- `/png/to-jpeg`, `/jpeg/to-png`
- `/svg/to-png`
- `/webp/to-jpeg`, `/webp/to-png`, `/png/to-webp`, `/jpeg/to-webp`

### 🗃️ Archive
- `/zip/to-tar`, `/tar/to-zip`
- `/zip/to-7z`, `/7z/to-zip`

### 🔐 Base64 Utilities
- `/file/to-base64` – return base64 with metadata
- `/file/to-base64-datastring` – return `data:<mime>;base64,...`
- `/base64-to-file` – restore file from raw base64
- `/base64-datastring-to-file` – restore file from data URI

---

## 🚀 Quickstart with Docker

Pull and run the latest container:

```bash
docker pull nyffels/media-convertion-microservice:latest

docker run -d \
  -p 8000:8000 \
  --name media-converter \
  nyffels/media-convertion-microservice:latest
```

Open your browser and visit:  
➡️ `http://localhost:8000/docs` for the interactive Swagger UI.

---

## 🛠 Tech Stack

- Python 3.11
- FastAPI + Uvicorn
- LibreOffice, Ghostscript, wkhtmltopdf, imagemagick
- Dockerized & CI/CD ready

---

## 📂 Repository Structure

```
.
├── app/                # Conversion logic
├── .github/workflows/  # CI/CD (build, test, push)
├── Dockerfile          # Production image
├── docker-compose.yml  # Local test stack
└── requirements.txt    # Python dependencies
```

---

## 📄 License

This project is licensed under the MIT License © 2025 Nyffels BV.

See [`LICENSE`](./LICENSE) for full details.

---

## 🤝 Contributing

Contributions are welcome!

However, **please create an issue first** to discuss your idea, bugfix or feature before submitting a pull request.

This ensures we keep the scope aligned and avoid duplicate efforts.

We love well-documented, tested and clean code. Let’s build something awesome together.