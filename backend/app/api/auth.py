from flask import request, jsonify, current_app, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db, mail
from ..models import User
from . import api
from flask_mail import Message
import datetime
import uuid

@api.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 409
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],  # Will be hashed by the setter
        is_verified=False
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Generate verification token
    verification_token = str(uuid.uuid4())
    
    # Store token in cache or database
    # For simplicity, we'll just use the token as is, but in production you'd want to store it securely
    
    # Send verification email
    send_verification_email(user, verification_token)
    
    return jsonify({
        'message': 'User registered successfully. Please check your email to verify your account.',
        'user_id': user.id
    }), 201

@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate input
    if not all(k in data for k in ('username', 'password')):
        return jsonify({'message': 'Missing username or password'}), 400
    
    # Find user
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.verify_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    if not user.is_verified:
        return jsonify({'message': 'Please verify your email before logging in'}), 403
    
    # Create tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200

@api.route('/auth/verify/<token>', methods=['GET'])
def verify_email(token):
    # In a real app, you'd validate the token against what you stored
    # For demonstration, we'll just simulate a successful verification
    
    # Find user by token (in a real app)
    # user = User.query.filter_by(verification_token=token).first()
    
    # For demo purposes:
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'message': 'Invalid verification link'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user.is_verified = True
    db.session.commit()
    
    return jsonify({'message': 'Email verified successfully. You can now log in.'}), 200

@api.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        'access_token': access_token
    }), 200

@api.route('/auth/reset-password', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    if not data or not data.get('email'):
        return jsonify({'message': 'Email is required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        # Security best practice: Don't reveal if email exists
        return jsonify({'message': 'If your email is registered, you will receive a password reset link'}), 200
    
    # Generate reset token (in a real app, store this securely)
    reset_token = str(uuid.uuid4())
    
    # Send password reset email
    send_password_reset_email(user, reset_token)
    
    return jsonify({'message': 'If your email is registered, you will receive a password reset link'}), 200

@api.route('/auth/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    if not data or not data.get('password'):
        return jsonify({'message': 'New password is required'}), 400
    
    # In a real app, validate the token and find the associated user
    # For demo purposes:
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'message': 'Invalid reset link'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Invalid reset link'}), 400
    
    user.password = data['password']
    db.session.commit()
    
    return jsonify({'message': 'Password reset successfully'}), 200

# Helper functions

def send_verification_email(user, token):
    """Send an email verification link to the user"""
    verify_url = url_for('api.verify_email', token=token, user_id=user.id, _external=True)
    
    msg = Message(
        'Verify Your Viber Account',
        recipients=[user.email],
        body=f'''Hello {user.username},

Thank you for registering with Viber, the WoW Character Backstory & RP Event Platform!

Please click the following link to verify your email address:
{verify_url}

If you did not register for Viber, please ignore this email.

The Viber Team
'''
    )
    mail.send(msg)

def send_password_reset_email(user, token):
    """Send a password reset link to the user"""
    reset_url = url_for('api.reset_password', token=token, user_id=user.id, _external=True)
    
    msg = Message(
        'Reset Your Viber Password',
        recipients=[user.email],
        body=f'''Hello {user.username},

You've requested to reset your password for your Viber account.

Please click the following link to reset your password:
{reset_url}

If you did not request a password reset, please ignore this email.

The Viber Team
'''
    )
    mail.send(msg) 