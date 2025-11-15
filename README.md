# Mindfolio

A self-hosted personal reading library for tracking books, notes, quotes, and reflections.

## Features

- 📚 **Library Management**: Track books with custom statuses (To Read, Reading, Finished, Abandoned)
- ⭐ **Rating System**: Rate books on a 0.5-5 star scale
- 📝 **Notes**: Store summaries, reflections, and general notes for each book
- 💬 **Quotes**: Capture and organize quotes with tags and comments
- 📁 **File Attachments**: Upload PDFs, summaries, mindmaps, and other files
- 🏷️ **Tagging System**: Organize books and quotes with custom tags
- 🔍 **Search & Filter**: Full-text search across books, notes, and quotes
- 🎨 **Modern UI**: Clean, polished interface inspired by shadcn-ui design system
- 🚀 **HTMX Powered**: Dynamic interactions without heavy JavaScript frameworks
- 🔐 **Private & Secure**: Single-user authentication with secure file access

## Tech Stack

- **Backend**: Django 5.0 + Python 3.11
- **Database**: PostgreSQL 15
- **Frontend**: Django Templates + Tailwind CSS + HTMX + Alpine.js
- **Deployment**: Docker + Docker Compose
- **Server**: Gunicorn + WhiteNoise

## Quick Start with Docker

### Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

### Installation

1. **Clone the repository** (or navigate to your project directory):

```bash
cd Mindfolio
```

2. **Set up environment variables**:

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and update the values, especially `SECRET_KEY` for production:

```bash
SECRET_KEY=your-secret-key-here  # Generate a new one for production!
DEBUG=False  # Set to False in production
ALLOWED_HOSTS=yourdomain.com,localhost
```

3. **Build Tailwind CSS** (optional, for development):

If you want to customize the CSS:

```bash
npm install
npm run build:css
```

For development with auto-rebuild:

```bash
npm run watch:css
```

4. **Build and start the containers**:

```bash
docker-compose up --build -d
```

This will:
- Start PostgreSQL container
- Build and start Django application container
- Run database migrations
- Collect static files

5. **Create a superuser**:

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to create your admin account.

6. **Access the application**:

- **Main app**: http://localhost:8000
- **Admin panel**: http://localhost:8000/admin

## Manual Setup (Without Docker)

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Node.js 18+ (for Tailwind CSS)

### Installation

1. **Create and activate virtual environment**:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Python dependencies**:

```bash
pip install -r requirements.txt
```

3. **Install Node.js dependencies and build CSS**:

```bash
npm install
npm run build:css
```

4. **Set up PostgreSQL**:

Create a database and user:

```sql
CREATE DATABASE mindfolio;
CREATE USER mindfolio WITH PASSWORD 'mindfolio';
ALTER ROLE mindfolio SET client_encoding TO 'utf8';
ALTER ROLE mindfolio SET default_transaction_isolation TO 'read committed';
ALTER ROLE mindfolio SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mindfolio TO mindfolio;
```

5. **Configure environment**:

Create a `.env` file based on `.env.example` and update the database settings:

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mindfolio
DB_USER=mindfolio
DB_PASSWORD=your_password
```

6. **Run migrations**:

```bash
python manage.py migrate
```

7. **Create superuser**:

```bash
python manage.py createsuperuser
```

8. **Collect static files**:

```bash
python manage.py collectstatic
```

9. **Run the development server**:

```bash
python manage.py runserver
```

Visit http://localhost:8000

## Project Structure

```
Mindfolio/
├── books/              # Books app (main functionality)
│   ├── models.py       # Book and BookFile models
│   ├── views.py        # Book CRUD, files, notes, quotes views
│   ├── forms.py        # Forms for books, files, notes, quotes
│   └── templates/      # Book-related templates
├── notes/              # Notes app
│   └── models.py       # Note model
├── quotes/             # Quotes app
│   ├── models.py       # Quote model
│   └── views.py        # Global quotes view
├── core/               # Core app (authentication, tags)
│   ├── models.py       # Tag model
│   └── views.py        # Auth views
├── mindfolio/          # Project settings
│   ├── settings.py     # Django settings
│   └── urls.py         # URL configuration
├── templates/          # Global templates
│   └── base.html       # Base template
├── static/             # Static files
│   ├── src/            # Tailwind source
│   └── css/            # Compiled CSS
├── media/              # User uploads (created at runtime)
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── package.json        # Node.js dependencies
├── tailwind.config.js  # Tailwind configuration
├── Dockerfile          # Docker container definition
├── docker-compose.yml  # Docker services configuration
└── README.md           # This file
```

## Data Storage

### Docker Volumes

When running with Docker, data is stored in named volumes:

- `postgres_data`: PostgreSQL database
- `media_volume`: Uploaded files (PDFs, images, etc.)
- `static_volume`: Static files (CSS, JS)

To backup your data:

```bash
# Backup database
docker-compose exec db pg_dump -U mindfolio mindfolio > backup.sql

# Backup media files
docker cp mindfolio-web-1:/app/media ./media_backup
```

To restore:

```bash
# Restore database
docker-compose exec -T db psql -U mindfolio mindfolio < backup.sql

# Restore media files
docker cp ./media_backup mindfolio-web-1:/app/media
```

## Deployment

### Behind a Reverse Proxy

This application is designed to run behind a reverse proxy (Nginx, Caddy, Traefik, etc.).

#### Example Caddy Configuration:

```
yourdomain.com {
    reverse_proxy localhost:8000
}
```

#### Example Nginx Configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /media/ {
        alias /path/to/mindfolio/media/;
    }

    location /static/ {
        alias /path/to/mindfolio/staticfiles/;
    }
}
```

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate a strong `SECRET_KEY`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Set up HTTPS (use Caddy for automatic SSL)
- [ ] Configure regular database backups
- [ ] Set up file storage backup
- [ ] Review Django security settings
- [ ] Consider using a CDN for static files (optional)

## Usage

### Managing Tags

Tags must be created through the Django admin panel:

1. Log in to http://localhost:8000/admin
2. Navigate to "Tags"
3. Click "Add Tag" and create tags for your library
4. Tags can then be assigned to books and quotes

### Uploading Files

Supported file operations:
- Upload source PDFs/EPUBs
- Upload summaries and mindmaps
- PDF viewer for in-browser reading
- Secure file access (only you can view your files)

### Search Functionality

The global search searches across:
- Book titles and authors
- Note content
- Quote text and comments

## Development

### Running Tests

```bash
# With Docker
docker-compose exec web python manage.py test

# Without Docker
python manage.py test
```

### Building CSS (Development)

Watch for changes and rebuild automatically:

```bash
npm run watch:css
```

### Database Migrations

After modifying models:

```bash
# With Docker
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Without Docker
python manage.py makemigrations
python manage.py migrate
```

## Troubleshooting

### Static files not loading

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Database connection errors

Ensure PostgreSQL is running and credentials in `.env` match your database:

```bash
docker-compose logs db
```

### Permission errors with media files

Check that the media directory has correct permissions:

```bash
chmod -R 755 media/
```

## License

This project is for personal use. Modify and use as you see fit.

## Contributing

This is a personal project, but suggestions and improvements are welcome!

## Support

For issues or questions, please check:
- Django documentation: https://docs.djangoproject.com/
- Tailwind CSS: https://tailwindcss.com/docs
- HTMX: https://htmx.org/docs/
