# AKWAFLOW cPanel Deployment Guide

## Pre-Upload Checklist ✅

### 1. Environment Setup
- [ ] Copy `.env.example` to `.env` and configure with production values
- [ ] Set secure admin credentials in `.env`
- [ ] Configure email settings for your cPanel email account

### 2. Required Files
- [x] `passenger_wsgi.py` - Entry point for Python app
- [x] `.htaccess` - URL routing and security
- [x] `requirements.txt` - Python dependencies
- [x] All templates and static files

## Upload Instructions

### Step 1: Upload Files
1. Compress your project folder (excluding `.env` file)
2. Upload to cPanel File Manager in `public_html` directory
3. Extract files

### Step 2: Environment Configuration
1. Create `.env` file in cPanel File Manager
2. Add your production environment variables:
```
SECRET_KEY=your-super-secret-production-key-here
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_secure_password

# Email Configuration (use your cPanel email)
MAIL_SERVER=mail.yourdomain.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=info@yourdomain.com
MAIL_PASSWORD=your_email_password
MAIL_DEFAULT_SENDER=info@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com
```

### Step 3: Python App Setup
1. Go to cPanel → Python App
2. Create new Python application
3. Set Python version to 3.8+
4. Set application root to your domain folder
5. Set startup file to `passenger_wsgi.py`
6. Install dependencies from `requirements.txt`

### Step 4: Database Initialization
The database will be automatically created on first run with sample data.

### Step 5: File Permissions
Ensure these directories are writable (755):
- `static/uploads/`
- Root directory (for database file)

## Post-Deployment Testing

1. Visit your website to ensure it loads
2. Test contact form functionality
3. Access admin panel at `/admin/login`
4. Test blog post creation and image uploads

## Security Notes

- Database file is protected by `.htaccess`
- Environment variables are secured
- File uploads are restricted to images only
- Admin panel requires authentication

## Troubleshooting

### Common Issues:
1. **500 Error**: Check Python version and dependencies
2. **Email not working**: Verify cPanel email settings
3. **Images not uploading**: Check folder permissions
4. **Database errors**: Ensure write permissions on root directory

### Support
Contact your hosting provider if you encounter Python app setup issues.