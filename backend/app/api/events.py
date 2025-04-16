from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from .. import db
from ..models import Event, User, EventSeries, Comment
from . import api

@api.route('/events', methods=['GET'])
def get_events():
    """Get all events with optional filtering"""
    # Get query parameters for filtering
    event_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_by = request.args.get('sort_by', 'start_time')
    sort_order = request.args.get('sort_order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)  # Cap at 50
    
    # Base query - only public events
    query = Event.query.filter_by(is_public=True)
    
    # Apply filters
    if event_type:
        query = query.filter_by(event_type=event_type)
    if start_date:
        try:
            start_date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            query = query.filter(Event.start_time >= start_date_obj)
        except ValueError:
            pass
    if end_date:
        try:
            end_date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            query = query.filter(Event.end_time <= end_date_obj)
        except ValueError:
            pass
    
    # Apply sorting
    if sort_order == 'desc':
        query = query.order_by(getattr(Event, sort_by).desc())
    else:
        query = query.order_by(getattr(Event, sort_by).asc())
    
    # Paginate results
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Prepare response
    events = []
    for event in paginated.items:
        creator = User.query.get(event.creator_id)
        events.append({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'event_type': event.event_type,
            'location': event.location,
            'map_coordinates': event.map_coordinates,
            'start_time': event.start_time.isoformat(),
            'end_time': event.end_time.isoformat() if event.end_time else None,
            'participant_count': event.participants.count(),
            'max_participants': event.max_participants,
            'series_id': event.series_id,
            'created_at': event.created_at.isoformat(),
            'creator': {
                'id': creator.id,
                'username': creator.username
            }
        })
    
    return jsonify({
        'events': events,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_pages': paginated.pages,
            'total_items': paginated.total
        }
    }), 200

@api.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    """Get a specific event by ID"""
    event = Event.query.get_or_404(id)
    
    # Check if event is public
    if not event.is_public:
        # If JWT is provided, check if user is the creator
        try:
            current_user_id = get_jwt_identity()
            if current_user_id != event.creator_id:
                return jsonify({'message': 'Event not found or not accessible'}), 404
        except:
            return jsonify({'message': 'Event not found or not accessible'}), 404
    
    creator = User.query.get(event.creator_id)
    
    # Get participants
    participants = []
    for user in event.participants.all():
        # Get RSVP status from the join table
        rsvp_status = db.session.execute(
            "SELECT rsvp_status FROM event_participants WHERE user_id = :user_id AND event_id = :event_id",
            {"user_id": user.id, "event_id": event.id}
        ).scalar()
        
        participants.append({
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'rsvp_status': rsvp_status
        })
    
    # Get comments
    comments_query = Comment.query.filter_by(event_id=event.id).order_by(Comment.created_at.desc())
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
    
    # Get series info if part of a series
    series = None
    if event.series_id:
        series_obj = EventSeries.query.get(event.series_id)
        if series_obj:
            series = {
                'id': series_obj.id,
                'title': series_obj.title,
                'frequency': series_obj.frequency
            }
    
    return jsonify({
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'event_type': event.event_type,
        'location': event.location,
        'map_coordinates': event.map_coordinates,
        'start_time': event.start_time.isoformat(),
        'end_time': event.end_time.isoformat() if event.end_time else None,
        'max_participants': event.max_participants,
        'is_public': event.is_public,
        'created_at': event.created_at.isoformat(),
        'creator': {
            'id': creator.id,
            'username': creator.username,
            'avatar': creator.avatar
        },
        'participants': participants,
        'comments': comments,
        'series': series
    }), 200

@api.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    """Create a new event"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'event_type', 'location', 'start_time']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Parse dates
    try:
        start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
        end_time = None
        if 'end_time' in data and data['end_time']:
            end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({'message': 'Invalid date format'}), 400
    
    # Create event
    event = Event(
        title=data['title'],
        description=data.get('description', ''),
        event_type=data['event_type'],
        location=data['location'],
        map_coordinates=data.get('map_coordinates', ''),
        start_time=start_time,
        end_time=end_time,
        max_participants=data.get('max_participants'),
        is_public=data.get('is_public', True),
        creator_id=current_user_id,
        series_id=data.get('series_id')
    )
    
    db.session.add(event)
    
    # Add creator as participant
    user = User.query.get(current_user_id)
    event.participants.append(user)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Event created successfully',
        'event_id': event.id
    }), 201

@api.route('/events/<int:id>', methods=['PUT'])
@jwt_required()
def update_event(id):
    """Update an existing event"""
    current_user_id = get_jwt_identity()
    event = Event.query.get_or_404(id)
    
    # Check if user is the creator
    if event.creator_id != current_user_id:
        return jsonify({'message': 'You do not have permission to update this event'}), 403
    
    data = request.get_json()
    
    # Update fields
    if 'title' in data:
        event.title = data['title']
    if 'description' in data:
        event.description = data['description']
    if 'event_type' in data:
        event.event_type = data['event_type']
    if 'location' in data:
        event.location = data['location']
    if 'map_coordinates' in data:
        event.map_coordinates = data['map_coordinates']
    if 'start_time' in data:
        try:
            event.start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'message': 'Invalid start_time format'}), 400
    if 'end_time' in data:
        if data['end_time']:
            try:
                event.end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'message': 'Invalid end_time format'}), 400
        else:
            event.end_time = None
    if 'max_participants' in data:
        event.max_participants = data['max_participants']
    if 'is_public' in data:
        event.is_public = data['is_public']
    if 'series_id' in data:
        event.series_id = data['series_id']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Event updated successfully',
        'event_id': event.id
    }), 200

@api.route('/events/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_event(id):
    """Delete an event"""
    current_user_id = get_jwt_identity()
    event = Event.query.get_or_404(id)
    
    # Check if user is the creator
    if event.creator_id != current_user_id:
        return jsonify({'message': 'You do not have permission to delete this event'}), 403
    
    # Delete associated comments
    Comment.query.filter_by(event_id=id).delete()
    
    # Delete event
    db.session.delete(event)
    db.session.commit()
    
    return jsonify({'message': 'Event deleted successfully'}), 200

@api.route('/events/<int:id>/rsvp', methods=['POST'])
@jwt_required()
def rsvp_event(id):
    """RSVP to an event"""
    current_user_id = get_jwt_identity()
    event = Event.query.get_or_404(id)
    user = User.query.get(current_user_id)
    
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'message': 'RSVP status is required'}), 400
    
    status = data['status']
    if status not in ['attending', 'maybe', 'declined']:
        return jsonify({'message': 'Invalid RSVP status. Must be one of: attending, maybe, declined'}), 400
    
    # Check if already at capacity
    if status == 'attending' and event.max_participants and event.participants.count() >= event.max_participants:
        return jsonify({'message': 'Event is at capacity'}), 400
    
    # Check if already RSVPed
    is_participant = user in event.participants.all()
    
    if is_participant:
        # Update RSVP status
        db.session.execute(
            "UPDATE event_participants SET rsvp_status = :status WHERE user_id = :user_id AND event_id = :event_id",
            {"status": status, "user_id": user.id, "event_id": event.id}
        )
    else:
        # Add as new participant
        event.participants.append(user)
        # Set RSVP status
        db.session.execute(
            "UPDATE event_participants SET rsvp_status = :status WHERE user_id = :user_id AND event_id = :event_id",
            {"status": status, "user_id": user.id, "event_id": event.id}
        )
    
    db.session.commit()
    
    return jsonify({'message': f'RSVP status updated to {status}'}), 200

@api.route('/events/<int:id>/cancel-rsvp', methods=['POST'])
@jwt_required()
def cancel_rsvp(id):
    """Cancel RSVP to an event"""
    current_user_id = get_jwt_identity()
    event = Event.query.get_or_404(id)
    user = User.query.get(current_user_id)
    
    # Check if user is a participant
    if user not in event.participants.all():
        return jsonify({'message': 'You are not registered for this event'}), 400
    
    # Remove participant
    event.participants.remove(user)
    db.session.commit()
    
    return jsonify({'message': 'RSVP cancelled successfully'}), 200

@api.route('/events/<int:id>/comments', methods=['POST'])
@jwt_required()
def add_event_comment(id):
    """Add a comment to an event"""
    current_user_id = get_jwt_identity()
    event = Event.query.get_or_404(id)
    
    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({'message': 'Comment content is required'}), 400
    
    comment = Comment(
        content=data['content'],
        user_id=current_user_id,
        event_id=id
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

@api.route('/event-series', methods=['POST'])
@jwt_required()
def create_event_series():
    """Create a new event series"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'frequency']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Create series
    series = EventSeries(
        title=data['title'],
        description=data.get('description', ''),
        frequency=data['frequency']
    )
    
    db.session.add(series)
    db.session.commit()
    
    return jsonify({
        'message': 'Event series created successfully',
        'series_id': series.id
    }), 201 