"""
Flask Application Runner
Run this file to start your backend server
"""

from backend.config import app, db
from flask_cors import CORS

# Import all your routes - ADJUST THIS LINE to match your routes file name
# If your routes are in backend/routes.py, use:
from backend.signup_login import signup_routes

# Enable CORS with credentials support
CORS(app, 
     supports_credentials=True, 
     origins=["http://localhost:8000", "http://127.0.0.1:8000", "http://127.0.0.1:5500"],
     allow_headers=["Content-Type"],
     methods=["GET", "POST", "OPTIONS"])
# Configure Flask app
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production-12345'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS

# Database configuration (if not already in config.py)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexus.db'  # Uncomment if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def init_db():
    """Initialize the database"""
    with app.app_context():
        # Import models
        from backend.database import Users, Projects, Tasks, TeamMembers, ActivityLog
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")


def run_app():
    """Run the Flask application"""
    print("=" * 60)
    print("🚀 Starting Nexus Backend Server")
    print("=" * 60)
    print(f"📍 Backend running on: http://localhost:5000")
    print(f"📊 Database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')}")
    print("=" * 60)
    print("\n✨ Available endpoints:")
    print("   GET  /           - Get all users")
    print("   POST /signup     - Create new user")
    print("   POST /login      - User login")
    print("   POST /logout     - User logout")
    print("\n⚠️  Press CTRL+C to stop the server")
    print("=" * 60 + "\n")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',  # Makes server accessible from other devices on network
        port=5000,
        debug=True  # Enable debug mode for development
    )


if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    
    # Start the application
    run_app()
