from backend.config import db
from datetime import datetime


class Users(db.Model):
    __tablename__ = "users"
    
    # Changed to String for UUID support (matching your routes)
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)  # Increased for hashed passwords
    join_date = db.Column(db.DateTime, default=datetime.utcnow)  # Changed to DateTime

    # Relationships
    created_projects = db.relationship("Projects", backref="creator", lazy=True, cascade="all, delete-orphan")
    made_tasks = db.relationship("Tasks", backref="task_creator", lazy=True, cascade="all, delete-orphan")
    team_memberships = db.relationship("TeamMembers", backref="member", lazy=True, cascade="all, delete-orphan")
    activity_logs = db.relationship("ActivityLog", backref="user", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        """Convert user object to dictionary (excluding password)"""
        return {
            "id": self.id,
            "username": self.username,
            "join_date": self.join_date.isoformat() if self.join_date else None
        }


class Projects(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Fixed: removed ()

    # Relationships
    tasks = db.relationship("Tasks", backref="project", lazy=True, cascade="all, delete-orphan")
    team_members = db.relationship("TeamMembers", backref="project", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        """Convert project object to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Tasks(db.Model):
    __tablename__ = "tasks"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)  # Added user_id
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(60), nullable=False, default="active")
    assigned_to = db.Column(db.String(400), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)  # Changed to DateTime
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert task object to dictionary"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class TeamMembers(db.Model):
    __tablename__ = "team_members"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(100), nullable=False)  # Changed to String
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Unique constraint to prevent duplicate memberships
    __table_args__ = (
        db.UniqueConstraint('user_id', 'project_id', name='unique_user_project'),
    )

    def to_dict(self):
        """Convert team member object to dictionary"""
        return {
            "id": self.id,
            "role": self.role,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None
        }


class ActivityLog(db.Model):
    __tablename__ = "activity_log"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text, nullable=True)  # Optional: store additional info

    def to_dict(self):
        """Convert activity log object to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "details": self.details
        }