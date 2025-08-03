# Image Gallery

A simple Flask web application for uploading and displaying images in a responsive gallery format.

## Features

- Upload images (PNG, JPG, JPEG, GIF)
- Responsive image gallery with Bootstrap styling
- Mobile-friendly design
- File type validation for security

### Upcoming Features

- **AWS S3 Integration**: Cloud storage for uploaded images
- **User Authentication**: Login/registration system with RDS database
- **Image Metadata**: Database storage for image information and user associations

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Bootstrap 5.3.1
- **Cloud Storage**: AWS S3 (planned)
- **Database**: AWS RDS (planned)

## Installation

```bash
cd "Demo Gallery"
uv sync  # or pip install flask
```

## Usage

```bash
python app.py
```

Navigate to `http://127.0.0.1:5000`

## Roadmap

1. **Database Integration** - User authentication with AWS RDS
2. **Cloud Storage Migration** - AWS S3 file uploads
3. **Enhanced Features** - User galleries and sharing

---

Created by Elmer Funez & Ricardo Zuniga
