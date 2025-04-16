#!/usr/bin/env python
import os
import click
from flask.cli import FlaskGroup
from app import create_app, db
from app.models import User, Character, Event, Comment, Guild, EventSeries

app = create_app(os.getenv('FLASK_ENV', 'development'))

cli = FlaskGroup(create_app=lambda: app)

@cli.command('create_db')
def create_db():
    """Create the database tables."""
    db.create_all()
    click.echo('Database tables created!')

@cli.command('drop_db')
def drop_db():
    """Drop all database tables."""
    if click.confirm('Are you sure you want to drop all tables?', abort=True):
        db.drop_all()
        click.echo('Database tables dropped!')

@cli.command('seed_db')
def seed_db():
    """Seed the database with initial data."""
    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        password='admin123',
        is_verified=True
    )
    db.session.add(admin)
    
    # Create some sample users
    users = [
        User(
            username='thrall',
            email='thrall@example.com',
            password='password',
            is_verified=True
        ),
        User(
            username='jaina',
            email='jaina@example.com',
            password='password',
            is_verified=True
        ),
        User(
            username='sylvanas',
            email='sylvanas@example.com',
            password='password',
            is_verified=True
        )
    ]
    db.session.add_all(users)
    db.session.commit()
    
    # Create some characters
    characters = [
        Character(
            name='Thrall',
            race='Orc',
            character_class='Shaman',
            level=60,
            faction='Horde',
            backstory="Former Warchief of the Horde. Son of Durotan and Draka.",
            user_id=users[0].id
        ),
        Character(
            name='Jaina Proudmoore',
            race='Human',
            character_class='Mage',
            level=60,
            faction='Alliance',
            backstory="Leader of the Kul Tiras and powerful mage. Former leader of Dalaran.",
            user_id=users[1].id
        ),
        Character(
            name='Sylvanas Windrunner',
            race='Undead',
            character_class='Hunter',
            level=60,
            faction='Horde',
            backstory="Former Ranger-General of Silvermoon, killed and raised by the Lich King.",
            user_id=users[2].id
        )
    ]
    db.session.add_all(characters)
    db.session.commit()
    
    # Create some events
    events = [
        Event(
            title='The Crossroads Tavern Night',
            description='A night of storytelling and drinking at the Crossroads tavern.',
            event_type='Tavern',
            location='The Crossroads, Barrens',
            map_coordinates='45,36',
            start_time='2023-10-15T20:00:00',
            creator_id=users[0].id
        ),
        Event(
            title='Stormwind Ball',
            description='Annual ball in Stormwind Castle. Formal attire required.',
            event_type='Ceremony',
            location='Stormwind Castle',
            map_coordinates='50,50',
            start_time='2023-10-20T19:00:00',
            creator_id=users[1].id
        ),
        Event(
            title='Warsong Gulch Battle',
            description='Join the battle for resources in Warsong Gulch!',
            event_type='Adventure',
            location='Warsong Gulch',
            map_coordinates='60,30',
            start_time='2023-10-25T18:00:00',
            creator_id=users[2].id
        )
    ]
    db.session.add_all(events)
    db.session.commit()
    
    # Add some RSVPs
    events[0].participants.append(users[0])
    events[0].participants.append(users[2])
    events[1].participants.append(users[1])
    events[2].participants.append(users[0])
    events[2].participants.append(users[1])
    events[2].participants.append(users[2])
    
    # Add some comments
    comments = [
        Comment(
            content="Great backstory! I love the character development.",
            user_id=users[0].id,
            character_id=characters[1].id
        ),
        Comment(
            content="Looking forward to this event!",
            user_id=users[1].id,
            event_id=events[0].id
        )
    ]
    db.session.add_all(comments)
    
    # Create a guild
    guild = Guild(
        name='Knights of the Silver Hand',
        description='Paladins united under the Light',
        faction='Alliance'
    )
    db.session.add(guild)
    db.session.commit()
    
    click.echo('Database seeded with sample data!')

@cli.command('run')
@click.option('--host', default='0.0.0.0', help='The host to bind to.')
@click.option('--port', default=5000, help='The port to bind to.')
def run(host, port):
    """Run the Flask development server."""
    app.run(host=host, port=port)

if __name__ == '__main__':
    cli() 