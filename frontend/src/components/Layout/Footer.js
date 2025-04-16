import { Link } from 'react-router-dom';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="bg-wow-dark border-t border-neutral/30 py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          {/* Logo and tagline */}
          <div className="mb-6 md:mb-0">
            <Link to="/" className="flex items-center justify-center md:justify-start">
              <h2 className="text-2xl font-wow text-wow-gold">Viber</h2>
            </Link>
            <p className="text-wow-light text-sm mt-2">
              WoW Character Backstory & RP Event Platform
            </p>
          </div>
          
          {/* Navigation */}
          <div className="grid grid-cols-2 gap-8 sm:gap-6 sm:grid-cols-3 text-center md:text-left">
            <div>
              <h3 className="text-sm font-semibold text-wow-gold uppercase mb-4">Platform</h3>
              <ul className="space-y-2">
                <li>
                  <Link to="/characters" className="text-wow-light hover:text-wow-gold text-sm">
                    Characters
                  </Link>
                </li>
                <li>
                  <Link to="/events" className="text-wow-light hover:text-wow-gold text-sm">
                    Events
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-wow-gold uppercase mb-4">Resources</h3>
              <ul className="space-y-2">
                <li>
                  <a
                    href="https://turtle-wow.org"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-wow-light hover:text-wow-gold text-sm"
                  >
                    Turtle WoW
                  </a>
                </li>
                <li>
                  <a
                    href="https://discord.gg/turtlewow"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-wow-light hover:text-wow-gold text-sm"
                  >
                    Discord
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-wow-gold uppercase mb-4">Legal</h3>
              <ul className="space-y-2">
                <li>
                  <Link to="/privacy-policy" className="text-wow-light hover:text-wow-gold text-sm">
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link to="/terms-of-service" className="text-wow-light hover:text-wow-gold text-sm">
                    Terms of Service
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        {/* Copyright */}
        <div className="mt-8 pt-6 border-t border-neutral/20 text-center">
          <p className="text-wow-light text-sm">
            &copy; {currentYear} Viber. All rights reserved.
          </p>
          <p className="text-wow-light/60 text-xs mt-2">
            World of Warcraft and Blizzard Entertainment are trademarks or registered trademarks of Blizzard Entertainment, Inc. Viber is not affiliated with Blizzard Entertainment.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 