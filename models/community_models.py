# community_models.py

from datetime import datetime, timezone

from sqlalchemy import UniqueConstraint

from extensions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))
    user = db.relationship('User', backref=db.backref('posts', lazy=True, cascade="all, delete-orphan"))


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    post = db.relationship('Post', backref=db.backref('likes', lazy='dynamic', cascade="all, delete"))
    user = db.relationship('User', backref=db.backref('liked_posts', lazy='dynamic'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    post = db.relationship('Post', backref=db.backref('comments', lazy='dynamic', cascade="all, delete"))
    user = db.relationship('User', backref=db.backref('comments_made', lazy='dynamic'))


class Friendship(db.Model):
    __table_args__ = (UniqueConstraint('user_id', 'friend_id', name='_user_friend_uc'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="requested", index=True)  # e.g., "requested", "accepted", "declined"
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('friendships_initiated', lazy='dynamic'))
    friend = db.relationship('User', foreign_keys=[friend_id],
                             backref=db.backref('friendships_received', lazy='dynamic'))

