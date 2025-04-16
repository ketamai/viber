from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# Association tables for many-to-many relationships
event_participants = db.Table('event_participants',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('rsvp_status', db.String(20), default='attending'),  # attending, maybe, declined
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

character_followers = db.Table('character_followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    characters = db.relationship('Character', backref='user', lazy='dynamic')
    created_events = db.relationship('Event', backref='creator', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    
    # Participating events (many-to-many)
    events = db.relationship('Event', secondary=event_participants, 
                            lazy='dynamic', backref=db.backref('participants', lazy='dynamic'))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Character(db.Model):
    __tablename__ = 'characters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    race = db.Column(db.String(20))
    character_class = db.Column(db.String(20))
    level = db.Column(db.Integer)
    faction = db.Column(db.String(20))
    backstory = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=True)
    portrait = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    comments = db.relationship('Comment', backref='character', lazy='dynamic')
    
    # Followers (many-to-many)
    followers = db.relationship('User', secondary=character_followers,
                              lazy='dynamic', backref=db.backref('following', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Character {self.name}>'

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))  # tavern, adventure, ceremony, etc.
    location = db.Column(db.String(100))
    map_coordinates = db.Column(db.String(50))  # x,y coordinates in WoW
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    max_participants = db.Column(db.Integer, nullable=True)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # If part of a series
    series_id = db.Column(db.Integer, db.ForeignKey('event_series.id'), nullable=True)
    
    def __repr__(self):
        return f'<Event {self.title}>'

class EventSeries(db.Model):
    __tablename__ = 'event_series'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    frequency = db.Column(db.String(20))  # weekly, biweekly, monthly
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    events = db.relationship('Event', backref='series', lazy='dynamic')
    
    def __repr__(self):
        return f'<EventSeries {self.title}>'

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)
    
    def __repr__(self):
        return f'<Comment {self.id}>'

class Guild(db.Model):
    __tablename__ = 'guilds'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text)
    faction = db.Column(db.String(20))
    emblem = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    characters = db.relationship('Character', secondary='guild_members', 
                               lazy='dynamic', backref=db.backref('guilds', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Guild {self.name}>'

# Guild membership association table
guild_members = db.Table('guild_members',
    db.Column('guild_id', db.Integer, db.ForeignKey('guilds.id'), primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True),
    db.Column('joined_at', db.DateTime, default=datetime.utcnow),
    db.Column('rank', db.String(30), default='Member')
) 