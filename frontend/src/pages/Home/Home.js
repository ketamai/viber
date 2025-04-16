import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const Home = () => {
  const [featuredCharacters, setFeaturedCharacters] = useState([]);
  const [upcomingEvents, setUpcomingEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch featured characters
        const charactersResponse = await axios.get('/api/characters?sort_by=created_at&sort_order=desc&per_page=3');
        setFeaturedCharacters(charactersResponse.data.characters || []);
        
        // Fetch upcoming events
        const eventsResponse = await axios.get('/api/events?sort_by=start_time&sort_order=asc&per_page=3');
        setUpcomingEvents(eventsResponse.data.events || []);
      } catch (error) {
        console.error('Error fetching homepage data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);
  
  return (
    <div className="flex flex-col space-y-12">
      {/* Hero Section */}
      <section className="relative rounded-xl overflow-hidden shadow-wow bg-wow-brown">
        <div className="relative py-20 px-6 md:px-12 flex flex-col items-center text-center z-10">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-wow text-wow-gold mb-4">
            Tell Your Story in Azeroth
          </h1>
          <p className="text-wow-light text-lg md:text-xl max-w-3xl mb-8">
            Share your character's backstory, join role-playing events, and connect with the Turtle WoW community.
          </p>
          <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
            <Link to="/register" className="btn-primary text-center py-3 px-8">
              Create an Account
            </Link>
            <Link to="/characters" className="btn-secondary text-center py-3 px-8">
              Browse Characters
            </Link>
          </div>
        </div>
      </section>
      
      {/* Featured Characters */}
      <section>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl md:text-3xl font-wow text-wow-gold">Featured Characters</h2>
          <Link to="/characters" className="text-wow-light hover:text-wow-gold text-sm">
            View All Characters
          </Link>
        </div>
        
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-wow-gold"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {featuredCharacters.length > 0 ? (
              featuredCharacters.map(character => (
                <div key={character.id} className="card hover:shadow-lg transition-all">
                  <h3 className="text-wow-gold font-semibold text-lg">{character.name}</h3>
                  <p className="text-wow-light text-sm">
                    {character.race} {character.class}
                  </p>
                  <div className="mt-4">
                    <Link 
                      to={`/characters/${character.id}`}
                      className="text-wow-gold hover:text-yellow-500 text-sm font-semibold"
                    >
                      View Backstory
                    </Link>
                  </div>
                </div>
              ))
            ) : (
              <div className="col-span-3 text-center py-8">
                <p className="text-wow-light">No characters have been created yet. Be the first!</p>
              </div>
            )}
          </div>
        )}
      </section>
      
      {/* Upcoming Events */}
      <section>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl md:text-3xl font-wow text-wow-gold">Upcoming Events</h2>
          <Link to="/events" className="text-wow-light hover:text-wow-gold text-sm">
            View All Events
          </Link>
        </div>
        
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-wow-gold"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {upcomingEvents.length > 0 ? (
              upcomingEvents.map(event => (
                <div key={event.id} className="card hover:shadow-lg transition-all">
                  <div className="mb-3">
                    <span className="inline-block px-2 py-1 text-xs rounded-md bg-wow-dark text-wow-light">
                      {event.event_type}
                    </span>
                  </div>
                  <h3 className="text-wow-gold font-semibold text-lg mb-2">{event.title}</h3>
                  <p className="text-wow-light text-sm mb-3 line-clamp-2">{event.description}</p>
                  <Link 
                    to={`/events/${event.id}`}
                    className="text-wow-gold hover:text-yellow-500 text-sm font-semibold"
                  >
                    View Event
                  </Link>
                </div>
              ))
            ) : (
              <div className="col-span-3 text-center py-8">
                <p className="text-wow-light">No upcoming events yet. Why not create one?</p>
              </div>
            )}
          </div>
        )}
      </section>
      
      {/* Call to Action */}
      <section className="bg-wow-brown/50 rounded-xl p-8 text-center">
        <h2 className="text-2xl md:text-3xl font-wow text-wow-gold mb-4">Ready to Join the Adventure?</h2>
        <p className="text-wow-light text-lg max-w-2xl mx-auto mb-6">
          Create your account today and start sharing your characters' stories with the Turtle WoW community.
        </p>
        <Link to="/register" className="btn-primary inline-block py-3 px-8">
          Get Started
        </Link>
      </section>
    </div>
  );
};

export default Home; 