#!/usr/bin/env python3
"""
Database management script for AKWAFLOW website
"""

import sqlite3
import os
from datetime import datetime

def init_database():
    """Initialize the database with tables and sample data"""
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    
    # Create tables
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
    
    # Create default admin user
    c.execute("INSERT OR IGNORE INTO admin_users (username, password) VALUES ('admin', 'admin123')")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def add_sample_posts():
    """Add sample blog posts"""
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    
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
        ),
        (
            "EPIC Projects: Engineering Excellence in Oil & Gas",
            "<p>Engineering, Procurement, Installation & Commissioning (EPIC) projects require meticulous planning, expert execution, and comprehensive project management. AKWAFLOW delivers end-to-end EPIC solutions that meet the demanding requirements of the oil and gas industry.</p><p>Our multidisciplinary team brings together engineering expertise, procurement efficiency, and installation excellence to deliver projects on time and within budget.</p><h2>Our EPIC Capabilities</h2><ul><li>Conceptual and detailed engineering design</li><li>Strategic procurement and vendor management</li><li>Professional installation and construction</li><li>Comprehensive commissioning and startup</li><li>Project management and quality assurance</li></ul><p>Partner with AKWAFLOW for your next EPIC project and experience the difference that engineering excellence makes.</p>",
            "Engineering",
            "epic.jpg",
            1
        ),
        (
            "Environmental Monitoring: Atmospheric Particle Measurement Solutions",
            "<p>Environmental compliance and air quality monitoring are critical components of responsible industrial operations. AKWAFLOW's atmospheric particle measurement solutions provide accurate, real-time data to support environmental management and regulatory compliance.</p><p>Our advanced monitoring systems utilize cutting-edge sensor technology and data analytics to deliver comprehensive environmental intelligence.</p><h2>Monitoring Solutions</h2><ul><li>Real-time particle concentration measurement</li><li>Multi-parameter environmental monitoring</li><li>Data logging and remote access capabilities</li><li>Regulatory compliance reporting</li><li>Environmental impact assessment</li></ul><p>Ensure environmental compliance and protect community health with our proven atmospheric monitoring solutions.</p>",
            "Environmental",
            "atmop.jpg",
            1
        )
    ]
    
    for title, content, category, image, published in sample_posts:
        c.execute("INSERT OR IGNORE INTO posts (title, content, category, image, published) VALUES (?, ?, ?, ?, ?)",
                 (title, content, category, image, published))
    
    conn.commit()
    conn.close()
    print("Sample posts added successfully!")

def reset_database():
    """Reset the database (WARNING: This will delete all data)"""
    if os.path.exists('akwaflow.db'):
        os.remove('akwaflow.db')
        print("Database deleted.")
    
    init_database()
    add_sample_posts()
    print("Database reset complete!")

def show_stats():
    """Show database statistics"""
    conn = sqlite3.connect('akwaflow.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM posts")
    post_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM posts WHERE published = 1")
    published_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM contacts")
    contact_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM contacts WHERE read = 0")
    unread_count = c.fetchone()[0]
    
    conn.close()
    
    print(f"Database Statistics:")
    print(f"- Total posts: {post_count}")
    print(f"- Published posts: {published_count}")
    print(f"- Total contacts: {contact_count}")
    print(f"- Unread contacts: {unread_count}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python manage_db.py [init|reset|stats|add_posts]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        init_database()
    elif command == "reset":
        reset_database()
    elif command == "stats":
        show_stats()
    elif command == "add_posts":
        add_sample_posts()
    else:
        print("Unknown command. Use: init, reset, stats, or add_posts")