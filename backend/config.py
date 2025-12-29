"""
Backend Configuration File
Make sure your config.py looks something like this
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Database configuration
# SQLite (for development)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexus.db'

# Or PostgreSQL (for production)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/nexus_db'

# Or MySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/nexus_db'

# Disable modification tracking (improves performance)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for sessions (REQUIRED)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Initialize SQLAlchemy
db = SQLAlchemy(app)