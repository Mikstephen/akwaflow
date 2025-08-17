# AKWAFLOW

A modern web application for AKWAFLOW Ltd, providing comprehensive oil and gas industry services including flow meter calibration, pipeline integrity management, and corrosion control solutions.

## Features

- **Corporate Website**: Professional landing page showcasing services and expertise
- **Blog System**: Content management for technical articles and industry insights
- **Contact Management**: Inquiry handling with enhanced service categorization
- **Admin Dashboard**: Complete backend management system
- **File Upload**: Secure image handling for blog posts
- **Responsive Design**: Mobile-friendly interface using Tailwind CSS

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **File Handling**: Werkzeug secure uploads

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd akwaflow-modern
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python manage_db.py
```

4. Run the application:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Admin Access

- **URL**: `/admin/login`
- **Default Credentials**: 
  - Username: `admin`
  - Password: `admin123`

**Important**: Change default credentials in production.

## Project Structure

```
akwaflow-modern/
├── static/
│   ├── css/           # Stylesheets
│   ├── img/           # Company images and assets
│   ├── js/            # JavaScript files
│   ├── uploads/       # User uploaded files
│   └── video/         # Background videos
├── templates/
│   ├── admin/         # Admin panel templates
│   ├── index.html     # Main landing page
│   ├── blog-post.html # Blog post template
│   └── error pages
├── app.py             # Main Flask application
├── config.py          # Configuration settings
├── requirements.txt   # Python dependencies
└── run.py            # Application entry point
```

## Configuration

Environment variables for production:
- `SECRET_KEY`: Flask secret key
- `MAIL_SERVER`: SMTP server for email notifications
- `MAIL_USERNAME`: Email username
- `MAIL_PASSWORD`: Email password
- `ADMIN_EMAIL`: Administrator email address

## API Endpoints

- `GET /api/blogs` - Retrieve published blog posts in JSON format

## Security Features

- Secure file uploads with extension validation
- SQL injection protection via parameterized queries
- Session-based admin authentication
- File size limits (16MB maximum)
- Filename sanitization

## License

© 2024 AKWAFLOW Ltd. All rights reserved.