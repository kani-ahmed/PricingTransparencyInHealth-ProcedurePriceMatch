# user_models.py

from datetime import datetime, timezone

from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)  # Indexed for faster lookups
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)  # For notifications, also indexed
    profile_picture = db.Column(db.String(255))  # URL to profile picture
    password_hash = db.Column(db.String(128))

    # Define the relationship to MessagesInbox and ChallengesInbox
    messages_inbox = db.relationship('MessagesInbox', back_populates='user', lazy='dynamic',
                                     foreign_keys='MessagesInbox.user_id')


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('notifications', lazy='dynamic'))


class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receive_notifications = db.Column(db.Boolean, default=True)
    privacy_settings = db.Column(db.String(50))  # Example: "Public", "Friends Only", "Private"

    user = db.relationship('User', backref='preferences')


class MessagesInbox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    is_read = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='received_messages', foreign_keys=[user_id])
    sender = db.relationship('User', backref='sent_messages', foreign_keys=[sender_id])
