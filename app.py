from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
import sqlite3
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from config import Config
import re

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, will use system environment variables

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize Flask-Mail
mail = Mail(app)

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_upload_folder():
    """Ensure upload folder exists"""
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

def sanitize_filename(filename):
    """Sanitize filename to prevent security issues"""
    # Remove any path components
    filename = os.path.basename(filename)
    # Replace spaces and special characters
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    # Generate unique filename
    name, ext = os.path.splitext(filename)
    unique_filename = f"{uuid.uuid4().hex[:8]}_{name}{ext}"
    return unique_filename

def init_db():
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT,
        image TEXT,
        date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
        published BOOLEAN DEFAULT 1
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        subject TEXT,
        message TEXT NOT NULL,
        date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
        read BOOLEAN DEFAULT 0
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    
    # Create default admin user with secure credentials from environment
    admin_username = os.environ.get('ADMIN_USERNAME', 'akwaflow_admin')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'AkwaFlow2024!SecurePass')
    hashed_password = generate_password_hash(admin_password)
    c.execute("INSERT OR IGNORE INTO admin_users (username, password) VALUES (?, ?)", 
              (admin_username, hashed_password))
    
    # Add sample blog posts if none exist
    c.execute("SELECT COUNT(*) FROM posts")
    if c.fetchone()[0] == 0:
        sample_posts = [
            (
                "Flow Meter Calibration: Best Practices for Accurate Measurements",
                "<p>Flow meter calibration is a critical process in the oil and gas industry, ensuring accurate custody transfer measurements that are essential for revenue assurance and regulatory compliance.</p><p>At AKWAFLOW, we specialize in providing comprehensive calibration services that meet the highest industry standards. Our team of certified technicians uses state-of-the-art equipment and follows internationally recognized procedures to ensure your flow meters operate with maximum precision.</p><h2>Key Benefits</h2><ul><li>Improved measurement accuracy and reliability</li><li>Compliance with NNPC and international standards</li><li>Enhanced revenue assurance through precise custody transfer</li><li>Reduced operational risks and measurement uncertainties</li><li>Comprehensive documentation and certification</li></ul><p>Contact us today to learn more about our flow meter calibration services and how we can help optimize your measurement systems for maximum accuracy and compliance.</p>",
                "Engineering",
                "flows.jpg",
                1
            ),
            (
                "Pipeline Integrity Management: Ensuring Safe Operations",
                "<p>Pipeline integrity management is crucial for maintaining safe and efficient operations in the oil and gas industry. Our comprehensive approach combines advanced inspection techniques with proactive maintenance strategies.</p><p>We utilize various Non-Destructive Testing (NDT) methods including ultrasonic testing, radiographic testing, magnetic particle inspection, and dye penetrant testing to assess pipeline condition and identify potential issues before they become critical.</p><h2>Our Services Include</h2><ul><li>Comprehensive pipeline inspections</li><li>Risk assessment and management</li><li>Corrosion monitoring and control</li><li>Emergency response planning</li><li>Regulatory compliance support</li></ul><p>Trust AKWAFLOW for reliable pipeline integrity solutions that protect your assets and ensure operational continuity.</p>",
                "Safety",
                "ndt.jpg",
                1
            ),
            (
                "Advanced Corrosion Control Solutions for Critical Infrastructure",
                "<p>Corrosion is one of the most significant challenges facing the oil and gas industry, causing billions of dollars in damage annually. Our advanced composite wrap technology provides robust and long-lasting protection for critical infrastructure.</p><p>AKWAFLOW's corrosion control solutions combine innovative materials with proven application techniques to deliver superior protection against environmental and operational stresses.</p><h2>Technology Advantages</h2><ul><li>High-strength composite materials</li><li>Rapid installation with minimal downtime</li><li>Long-term durability and reliability</li><li>Cost-effective maintenance solutions</li><li>Environmental compliance</li></ul><p>Protect your infrastructure investment with our proven corrosion control technologies.</p>",
                "Technical",
                "corrotion.jpeg",
                1
            )
        ]
        
        for title, content, category, image, published in sample_posts:
            c.execute("INSERT INTO posts (title, content, category, image, published) VALUES (?, ?, ?, ?, ?)",
                     (title, content, category, image, published))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE published = 1 ORDER BY date_created DESC LIMIT 3")
    posts = c.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = ? AND published = 1", (post_id,))
    post = c.fetchone()
    conn.close()
    if post:
        post_dict = {
            'id': post[0], 'title': post[1], 'content': post[2],
            'category': post[3], 'image': post[4], 'date': post[5]
        }
        return render_template('blog-post.html', post=post_dict)
    return redirect(url_for('index'))

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form.get('subject', '')
        message = request.form['message']
        phone = request.form.get('phone', '')
        company = request.form.get('company', '')
        service = request.form.get('service', '')
        urgency = request.form.get('urgency', '')
        
        # Enhance subject with service and urgency info
        if service or urgency:
            subject_parts = []
            if service:
                subject_parts.append(f"Service: {service}")
            if urgency:
                subject_parts.append(f"Timeline: {urgency}")
            if subject:
                subject_parts.append(subject)
            subject = " | ".join(subject_parts)
        
        # Enhance message with additional details
        enhanced_message = message
        if phone:
            enhanced_message += f"\n\nPhone: {phone}"
        if company:
            enhanced_message += f"\nCompany: {company}"
        
        conn = sqlite3.connect('akwaflow.db')
        c = conn.cursor()
        c.execute("INSERT INTO contacts (name, email, subject, message) VALUES (?, ?, ?, ?)",
                 (name, email, subject, enhanced_message))
        conn.commit()
        conn.close()
        
        # Send email notification
        try:
            send_contact_email(name, email, subject, enhanced_message, phone, company, service, urgency)
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        return jsonify({'success': True, 'message': 'Thank you for your inquiry! We will get back to you soon.'})
    return jsonify({'success': False, 'message': 'Invalid request method'})

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('akwaflow.db')
        c = conn.cursor()
        c.execute("SELECT * FROM admin_users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM posts")
    post_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM contacts WHERE read = 0")
    unread_count = c.fetchone()[0]
    conn.close()
    
    return render_template('admin/dashboard.html', post_count=post_count, unread_count=unread_count)

@app.route('/admin/posts')
def admin_posts():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY date_created DESC")
    posts = c.fetchall()
    conn.close()
    
    return render_template('admin/posts.html', posts=posts)

@app.route('/admin/posts/new', methods=['GET', 'POST'])
def admin_new_post():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        published = 'published' in request.form
        
        image = ''
        if 'image' in request.files:
            file = request.files['image']
            if file.filename and allowed_file(file.filename):
                create_upload_folder()
                filename = sanitize_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename
            elif file.filename and not allowed_file(file.filename):
                flash('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WEBP files only.')
                return redirect(url_for('admin_new_post'))
        
        conn = sqlite3.connect('akwaflow.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (title, content, category, image, published) VALUES (?, ?, ?, ?, ?)",
                 (title, content, category, image, published))
        conn.commit()
        conn.close()
        
        flash('Post created successfully!')
        return redirect(url_for('admin_posts'))
    
    return render_template('admin/post_form.html')

@app.route('/admin/posts/edit/<int:post_id>', methods=['GET', 'POST'])
def admin_edit_post(post_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        published = 'published' in request.form
        
        image = request.form.get('current_image', '')
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            if allowed_file(file.filename):
                create_upload_folder()
                filename = sanitize_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename
            else:
                flash('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WEBP files only.')
                return redirect(url_for('admin_edit_post', post_id=post_id))
        
        c.execute("UPDATE posts SET title=?, content=?, category=?, image=?, published=? WHERE id=?",
                 (title, content, category, image, published, post_id))
        conn.commit()
        conn.close()
        
        flash('Post updated successfully!')
        return redirect(url_for('admin_posts'))
    
    c.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = c.fetchone()
    conn.close()
    
    if post:
        post_dict = {
            'id': post[0], 'title': post[1], 'content': post[2],
            'category': post[3], 'image': post[4], 'published': post[6]
        }
        return render_template('admin/post_form.html', post=post_dict)
    
    return redirect(url_for('admin_posts'))

@app.route('/admin/posts/delete/<int:post_id>')
def admin_delete_post(post_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    
    flash('Post deleted successfully!')
    return redirect(url_for('admin_posts'))

@app.route('/admin/contacts')
def admin_contacts():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts ORDER BY date_created DESC")
    contacts = c.fetchall()
    conn.close()
    
    return render_template('admin/contacts.html', contacts=contacts)

@app.route('/admin/contacts/read/<int:contact_id>')
def admin_mark_read(contact_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    c.execute("UPDATE contacts SET read = 1 WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin_contacts'))

@app.route('/admin/contacts/delete/<int:contact_id>')
def admin_delete_contact(contact_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    
    flash('Contact deleted successfully!')
    return redirect(url_for('admin_contacts'))

@app.route('/api/blogs')
def api_blogs():
    """API endpoint to get blog posts for frontend"""
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE published = 1 ORDER BY date_created DESC")
    posts = c.fetchall()
    conn.close()
    
    blog_data = {}
    for post in posts:
        slug = post[1].lower().replace(' ', '-').replace(',', '').replace('.', '').replace('(', '').replace(')', '')
        # Clean description from HTML tags for preview
        description = post[2].replace('<p>', '').replace('</p>', '').replace('<br>', ' ')
        description = description[:150] + '...' if len(description) > 150 else description
        
        blog_data[slug] = {
            'id': post[0],
            'title': post[1],
            'description': description,
            'category': post[3] or 'General',
            'image': post[4] or 'flows.jpg',
            'date': post[5][:10] if post[5] else '2024-01-01',
            'read_time': calculate_read_time(post[2])
        }
    
    return jsonify(blog_data)

def calculate_read_time(content):
    """Calculate estimated reading time based on content length"""
    words = len(content.split())
    minutes = max(1, round(words / 200))  # Average reading speed: 200 words per minute
    return f"{minutes} min read"

def send_contact_email(name, email, subject, message, phone=None, company=None, service=None, urgency=None):
    """Send email notification when contact form is submitted"""
    try:
        msg = Message(
            subject=f"New Contact Form Submission: {subject or 'General Inquiry'}",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[app.config['ADMIN_EMAIL']]
        )
        
        # Create email body
        email_body = f"""
        New contact form submission from AKWAFLOW website:
        
        Name: {name}
        Email: {email}
        Phone: {phone or 'Not provided'}
        Company: {company or 'Not provided'}
        Service Interest: {service or 'Not specified'}
        Timeline: {urgency or 'Not specified'}
        
        Subject: {subject or 'General Inquiry'}
        
        Message:
        {message}
        
        ---
        This email was sent automatically from the AKWAFLOW contact form.
        Please reply directly to {email} to respond to this inquiry.
        """
        
        msg.body = email_body
        mail.send(msg)
        print(f"Email sent successfully to {app.config['ADMIN_EMAIL']}")
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise e

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(413)
def too_large(error):
    flash('File too large. Maximum size is 16MB.')
    return redirect(request.url)

if __name__ == '__main__':
    init_db()
    create_upload_folder()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)