from flask import request, jsonify, current_app, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from .. import db
from ..models import Character, User, Comment
from . import api
import uuid

# Helper function for file uploads
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@api.route('/characters', methods=['GET'])
def get_characters():
    """Get all published characters with optional filtering"""
    # Get query parameters for filtering
    race = request.args.get('race')
    character_class = request.args.get('class')
    faction = request.args.get('faction')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)  # Cap at 50
    
    # Base query - only public characters
    query = Character.query.filter_by(is_public=True)
    
    # Apply filters
    if race:
        query = query.filter_by(race=race)
    if character_class:
        query = query.filter_by(character_class=character_class)
    if faction:
        query = query.filter_by(faction=faction)
    
    # Apply sorting
    if sort_order == 'desc':
        query = query.order_by(getattr(Character, sort_by).desc())
    else:
        query = query.order_by(getattr(Character, sort_by).asc())
    
    # Paginate results
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Prepare response
    characters = []
    for character in paginated.items:
        user = User.query.get(character.user_id)
        characters.append({
            'id': character.id,
            'name': character.name,
            'race': character.race,
            'class': character.character_class,
            'level': character.level,
            'faction': character.faction,
            'portrait': character.portrait,
            'created_at': character.created_at.isoformat(),
            'updated_at': character.updated_at.isoformat(),
            'owner': {
                'id': user.id,
                'username': user.username
            }
        })
    
    return jsonify({
        'characters': characters,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_pages': paginated.pages,
            'total_items': paginated.total
        }
    }), 200

@api.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    """Get a specific character by ID"""
    character = Character.query.get_or_404(id)
    
    # Check if character is public or if user is the owner
    if not character.is_public:
        # If JWT is provided, check if user is the owner
        try:
            current_user_id = get_jwt_identity()
            if current_user_id != character.user_id:
                return jsonify({'message': 'Character not found or not accessible'}), 404
        except:
            return jsonify({'message': 'Character not found or not accessible'}), 404
    
    user = User.query.get(character.user_id)
    
    # Get comments
    comments_query = Comment.query.filter_by(character_id=character.id).order_by(Comment.created_at.desc())
    comments = []
    for comment in comments_query.all():
        author = User.query.get(comment.user_id)
        comments.append({
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'author': {
                'id': author.id,
                'username': author.username,
                'avatar': author.avatar
            }
        })
    
    return jsonify({
        'id': character.id,
        'name': character.name,
        'race': character.race,
        'class': character.character_class,
        'level': character.level,
        'faction': character.faction,
        'backstory': character.backstory,
        'portrait': character.portrait,
        'is_public': character.is_public,
        'created_at': character.created_at.isoformat(),
        'updated_at': character.updated_at.isoformat(),
        'owner': {
            'id': user.id,
            'username': user.username
        },
        'comments': comments
    }), 200

@api.route('/characters', methods=['POST'])
@jwt_required()
def create_character():
    """Create a new character"""
    current_user_id = get_jwt_identity()
    data = request.form.to_dict() if request.form else request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'race', 'character_class', 'faction']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Create character
    character = Character(
        name=data['name'],
        race=data['race'],
        character_class=data['character_class'],
        level=data.get('level', 1),
        faction=data['faction'],
        backstory=data.get('backstory', ''),
        is_public=data.get('is_public', True),
        user_id=current_user_id
    )
    
    # Handle portrait upload if present
    if 'portrait' in request.files:
        file = request.files['portrait']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            character.portrait = filename
    
    db.session.add(character)
    db.session.commit()
    
    return jsonify({
        'message': 'Character created successfully',
        'character_id': character.id
    }), 201

@api.route('/characters/<int:id>', methods=['PUT'])
@jwt_required()
def update_character(id):
    """Update an existing character"""
    current_user_id = get_jwt_identity()
    character = Character.query.get_or_404(id)
    
    # Check if user is the owner
    if character.user_id != current_user_id:
        return jsonify({'message': 'You do not have permission to update this character'}), 403
    
    data = request.form.to_dict() if request.form else request.get_json()
    
    # Update fields
    if 'name' in data:
        character.name = data['name']
    if 'race' in data:
        character.race = data['race']
    if 'character_class' in data:
        character.character_class = data['character_class']
    if 'level' in data:
        character.level = data['level']
    if 'faction' in data:
        character.faction = data['faction']
    if 'backstory' in data:
        character.backstory = data['backstory']
    if 'is_public' in data:
        character.is_public = data['is_public']
    
    # Handle portrait upload if present
    if 'portrait' in request.files:
        file = request.files['portrait']
        if file and allowed_file(file.filename):
            # Delete old portrait if exists
            if character.portrait:
                old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], character.portrait)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            
            # Save new portrait
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            character.portrait = filename
    
    db.session.commit()
    
    return jsonify({
        'message': 'Character updated successfully',
        'character_id': character.id
    }), 200

@api.route('/characters/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_character(id):
    """Delete a character"""
    current_user_id = get_jwt_identity()
    character = Character.query.get_or_404(id)
    
    # Check if user is the owner
    if character.user_id != current_user_id:
        return jsonify({'message': 'You do not have permission to delete this character'}), 403
    
    # Delete portrait if exists
    if character.portrait:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], character.portrait)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    # Delete associated comments
    Comment.query.filter_by(character_id=id).delete()
    
    # Delete character
    db.session.delete(character)
    db.session.commit()
    
    return jsonify({'message': 'Character deleted successfully'}), 200

@api.route('/characters/<int:id>/comments', methods=['POST'])
@jwt_required()
def add_comment(id):
    """Add a comment to a character"""
    current_user_id = get_jwt_identity()
    character = Character.query.get_or_404(id)
    
    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({'message': 'Comment content is required'}), 400
    
    comment = Comment(
        content=data['content'],
        user_id=current_user_id,
        character_id=id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    # Get author info
    author = User.query.get(current_user_id)
    
    return jsonify({
        'message': 'Comment added successfully',
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'author': {
                'id': author.id,
                'username': author.username,
                'avatar': author.avatar
            }
        }
    }), 201

@api.route('/characters/<int:id>/follow', methods=['POST'])
@jwt_required()
def follow_character(id):
    """Follow a character"""
    current_user_id = get_jwt_identity()
    character = Character.query.get_or_404(id)
    user = User.query.get(current_user_id)
    
    # Check if already following
    if character in user.following:
        return jsonify({'message': 'You are already following this character'}), 400
    
    user.following.append(character)
    db.session.commit()
    
    return jsonify({'message': 'You are now following this character'}), 200

@api.route('/characters/<int:id>/unfollow', methods=['POST'])
@jwt_required()
def unfollow_character(id):
    """Unfollow a character"""
    current_user_id = get_jwt_identity()
    character = Character.query.get_or_404(id)
    user = User.query.get(current_user_id)
    
    # Check if following
    if character not in user.following:
        return jsonify({'message': 'You are not following this character'}), 400
    
    user.following.remove(character)
    db.session.commit()
    
    return jsonify({'message': 'You have unfollowed this character'}), 200 