# Image Gallery

A Flask web application for uploading and displaying images with user authentication and database storage.

## Features

- **User Authentication**: Complete login/registration system with secure password hashing
- **Database Integration**: MySQL database for user management and image metadata
- **Image Upload**: Support for PNG, JPG, JPEG, GIF files with user association
- **Responsive Gallery**: Bootstrap-styled gallery with mobile-friendly design
- **File Security**: File type validation and secure uploads
- **Docker Support**: Containerized deployment with Docker
- **User-specific Galleries**: Each user can view and manage their own uploaded images

### Upcoming Features

- **AWS S3 Integration**: Cloud storage for uploaded images (currently uses local storage)

## Technologies Used

- **Backend**: Flask (Python) with Flask-Login for authentication
- **Database**: MySQL with SQLAlchemy ORM
- **Frontend**: HTML5, Bootstrap 5.3.1
- **Security**: Werkzeug password hashing, form validation
- **Deployment**: Docker containerization with uv package manager
- **Future**: AWS S3 integration (planned)

## Installation

### Local Development

```bash
cd "Demo Gallery"
uv sync  # Install dependencies using uv
```

### Database Setup

1. Install and start MySQL server
2. Create environment file `.env` with your database credentials:

```
SECRET_KEY=your-secret-key-here
DB_USER=your-db-username
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=demo_gallery
```

### Docker Deployment

```bash
docker build -t demo-gallery .
docker run -p 5000:5000 --env-file .env demo-gallery
```

## Usage

```bash
python app.py
```

Navigate to `http://127.0.0.1:5000`

### Features Available

- **Register**: Create a new user account at `/register`
- **Login**: Access your account at `/login`
- **Upload**: Upload images to your personal gallery at `/upload`
- **Gallery**: View all images at `/` (public) or your images at `/my_images`
- **Logout**: Secure logout functionality

## Roadmap

1.  **Database Integration** - User authentication with MySQL
2.  **Docker Support** - Containerized deployment
3.  **Cloud Storage Migration** - AWS S3 file uploads (in progress)
4.  **Enhanced Features** - Advanced user galleries and sharing

---

Created by Elmer Funez & Ricardo Zuniga
