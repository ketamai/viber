# Viber - WoW Character Backstory & RP Event Platform

A modern communication platform designed for Turtle WoW private server players to enhance their role-playing experience.

## Overview
Viber allows players to create and share detailed character backstories, organize role-playing events, RSVP to community events, and connect with other role-players.

## Features

- **User Authentication & Profiles**
  - Account creation with email verification
  - Character profiles linked to Turtle WoW characters
  - User dashboard showing owned characters and upcoming events

- **Character Backstory Creation**
  - Rich text editor for writing detailed backstories
  - Templates for different character archetypes
  - Tags for race, class, allegiance, etc.

- **Event Organization**
  - Event creation with date/time, location, description
  - Map integration showing event location in Azeroth
  - RSVP functionality and attendance tracking

- **Social Features**
  - Following favorite character stories
  - Commenting on backstories
  - Guild pages for collective roleplay
  - Real-time messaging between players
  - Group chats for guilds and events

## Tech Stack

- **Frontend**: React with Tailwind CSS
- **Backend**: Python with Flask
- **Database**: MySQL
- **Authentication**: JWT
- **Real-time communication**: Socket.IO

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- MySQL 8.0+

### Installation

1. Clone the repository
```bash
git clone https://github.com/jessearbon/Viber.git
cd Viber
```

2. Set up the backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure the environment
```bash
cp .env.example .env
# Edit .env with your database credentials and other configuration
```

4. Set up the database
```bash
python manage.py create_db
python manage.py seed_db  # Optional: seed with sample data
```

5. Set up the frontend
```bash
cd ../frontend
npm install
```

6. Start the development servers
```bash
# In the backend directory
python manage.py run

# In the frontend directory
npm run dev
```

7. Access the application at http://localhost:3000

## Development

### Project Structure
```
Viber/
├── backend/               # Python Flask backend
│   ├── app/               # Application code
│   ├── migrations/        # Database migrations
│   ├── tests/             # Backend tests
│   └── config.py          # Configuration
├── frontend/              # React frontend
│   ├── public/            # Static files
│   ├── src/               # React source code
│   └── package.json       # Node.js dependencies
└── docker/                # Docker configuration
```

## Deployment

This project uses GitHub Actions for automated deployment. The deployment workflow is triggered automatically when changes are pushed to the `main` branch.

### Deployment Process
1. Builds the frontend application
2. Sets up Python environment
3. Installs dependencies
4. Deploys to production server
5. Restarts necessary services

### Infrastructure
- Frontend: React/Vue.js with Node.js
- Backend: Python
- Database: MySQL
- Server: Nginx

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.