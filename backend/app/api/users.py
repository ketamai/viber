from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import uuid
from .. import db
from ..models import User, Character, Event
from . import api

# Helper function for file uploads
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@api.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'avatar': user.avatar,
        'created_at': user.created_at.isoformat()
    }), 200

@api.route('/users/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """Update current user profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    
    data = request.form.to_dict() if request.form else request.get_json()
    
    # Update fields
    if 'username' in data and data['username'] != user.username:
        # Check if username is already taken
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 409
        user.username = data['username']
    
    # Handle avatar upload if present
    if 'avatar' in request.files:
        file = request.files['avatar']
        if file and allowed_file(file.filename):
            # Delete old avatar if exists
            if user.avatar:
                old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user.avatar)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            
            # Save new avatar
            filename = secure_filename(f"avatar_{uuid.uuid4()}_{file.filename}")
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            user.avatar = filename
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'avatar': user.avatar
        }
    }), 200

@api.route('/users/me/password', methods=['PUT'])
@jwt_required()
def update_password():
    """Update current user password"""
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    
    data = request.get_json()
    if not data or not all(k in data for k in ('current_password', 'new_password')):
        return jsonify({'message': 'Current password and new password are required'}), 400
    
    # Verify current password
    if not user.verify_password(data['current_password']):
        return jsonify({'message': 'Current password is incorrect'}), 401
    
    # Update password
    user.password = data['new_password']
    db.session.commit()
    
    return jsonify({'message': 'Password updated successfully'}), 200

@api.route('/users/me/characters', methods=['GET'])
@jwt_required()
def get_user_characters():
    """Get characters owned by current user"""
    current_user_id = get_jwt_identity()
    
    characters = Character.query.filter_by(user_id=current_user_id).all()
    
    result = []
    for character in characters:
        result.append({
            'id': character.id,
            'name': character.name,
            'race': character.race,
            'class': character.character_class,
            'level': character.level,
            'faction': character.faction,
            'portrait': character.portrait,
            'is_public': character.is_public,
            'created_at': character.created_at.isoformat(),
            'updated_at': character.updated_at.isoformat()
        })
    
    return jsonify({'characters': result}), 200

@api.route('/users/me/events', methods=['GET'])
@jwt_required()
def get_user_events():
    """Get events created by or participated in by current user"""
    current_user_id = get_jwt_identity()
    filter_type = request.args.get('filter', 'all')  # all, created, participating
    
    if filter_type == 'created':
        # Events created by user
        events_query = Event.query.filter_by(creator_id=current_user_id)
    elif filter_type == 'participating':
        # Events user is participating in
        user = User.query.get(current_user_id)
        events_query = user.events
    else:
        # All events (created or participating)
        created_events = Event.query.filter_by(creator_id=current_user_id).all()
        user = User.query.get(current_user_id)
        participating_events = user.events.all()
        
        # Combine and remove duplicates
        all_events = set(created_events + participating_events)
        
        # Sort by start_time
        events_query = sorted(all_events, key=lambda e: e.start_time)
    
    result = []
    for event in events_query:
        # Get RSVP status if participating
        rsvp_status = None
        if filter_type != 'created':
            rsvp_result = db.session.execute(
                "SELECT rsvp_status FROM event_participants WHERE user_id = :user_id AND event_id = :event_id",
                {"user_id": current_user_id, "event_id": event.id}
            ).scalar()
            rsvp_status = rsvp_result if rsvp_result else None
        
        result.append({
            'id': event.id,
            'title': event.title,
            'event_type': event.event_type,
            'location': event.location,
            'start_time': event.start_time.isoformat(),
            'end_time': event.end_time.isoformat() if event.end_time else None,
            'is_creator': event.creator_id == current_user_id,
            'rsvp_status': rsvp_status,
            'participant_count': event.participants.count(),
            'created_at': event.created_at.isoformat()
        })
    
    return jsonify({'events': result}), 200

@api.route('/users/me/following', methods=['GET'])
@jwt_required()
def get_following():
    """Get characters being followed by current user"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    following = []
    for character in user.following:
        owner = User.query.get(character.user_id)
        following.append({
            'id': character.id,
            'name': character.name,
            'race': character.race,
            'class': character.character_class,
            'faction': character.faction,
            'portrait': character.portrait,
            'owner': {
                'id': owner.id,
                'username': owner.username
            }
        })
    
    return jsonify({'following': following}), 200

@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """Get public profile of a user"""
    user = User.query.get_or_404(id)
    
    # Get public characters
    characters = Character.query.filter_by(user_id=id, is_public=True).all()
    character_list = []
    for character in characters:
        character_list.append({
            'id': character.id,
            'name': character.name,
            'race': character.race,
            'class': character.character_class,
            'faction': character.faction,
            'portrait': character.portrait
        })
    
    # Get public events created by user
    events = Event.query.filter_by(creator_id=id, is_public=True).all()
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'title': event.title,
            'event_type': event.event_type,
            'start_time': event.start_time.isoformat(),
            'location': event.location
        })
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'avatar': user.avatar,
        'joined': user.created_at.isoformat(),
        'characters': character_list,
        'events': event_list
    }), 200 