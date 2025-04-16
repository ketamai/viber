import { useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Bars3Icon, XMarkIcon, UserCircleIcon } from '@heroicons/react/24/outline';

const Header = () => {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  
  const handleLogout = () => {
    logout();
    navigate('/');
    setIsProfileMenuOpen(false);
  };
  
  const closeMenus = () => {
    setIsMenuOpen(false);
    setIsProfileMenuOpen(false);
  };
  
  const navLinkClass = ({ isActive }) => 
    isActive 
      ? "text-wow-gold font-semibold px-3 py-2 rounded-md text-sm hover:bg-wow-brown/50 transition-colors" 
      : "text-wow-light px-3 py-2 rounded-md text-sm hover:bg-wow-brown/50 transition-colors";
  
  return (
    <header className="bg-wow-dark border-b border-neutral/30 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link to="/" className="flex items-center" onClick={closeMenus}>
              <h1 className="text-3xl font-wow text-wow-gold">Viber</h1>
            </Link>
          </div>
          
          {/* Desktop Navigation */}
          <nav className="hidden md:block">
            <div className="flex items-center space-x-4">
              <NavLink to="/characters" className={navLinkClass} onClick={closeMenus}>
                Characters
              </NavLink>
              <NavLink to="/events" className={navLinkClass} onClick={closeMenus}>
                Events
              </NavLink>
              {currentUser && (
                <NavLink to="/dashboard" className={navLinkClass} onClick={closeMenus}>
                  Dashboard
                </NavLink>
              )}
            </div>
          </nav>
          
          {/* Authentication Links */}
          <div className="hidden md:flex items-center space-x-2">
            {currentUser ? (
              <div className="relative">
                <button
                  className="flex items-center space-x-2 text-wow-light hover:text-wow-gold"
                  onClick={() => setIsProfileMenuOpen(!isProfileMenuOpen)}
                >
                  <UserCircleIcon className="h-8 w-8" />
                  <span>{currentUser.username}</span>
                </button>
                
                {/* Profile Dropdown */}
                {isProfileMenuOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-wow-brown rounded-md shadow-wow py-1 z-10">
                    <Link
                      to="/my-characters"
                      className="block px-4 py-2 text-sm text-wow-light hover:bg-wow-dark/30"
                      onClick={closeMenus}
                    >
                      My Characters
                    </Link>
                    <Link
                      to="/my-events"
                      className="block px-4 py-2 text-sm text-wow-light hover:bg-wow-dark/30"
                      onClick={closeMenus}
                    >
                      My Events
                    </Link>
                    <Link
                      to="/account-settings"
                      className="block px-4 py-2 text-sm text-wow-light hover:bg-wow-dark/30"
                      onClick={closeMenus}
                    >
                      Account Settings
                    </Link>
                    <button
                      className="block w-full text-left px-4 py-2 text-sm text-wow-light hover:bg-wow-dark/30"
                      onClick={handleLogout}
                    >
                      Logout
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <>
                <Link
                  to="/login"
                  className="px-4 py-1 text-sm rounded-md bg-wow-brown text-wow-light hover:bg-wow-brown/80"
                  onClick={closeMenus}
                >
                  Log In
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-1 text-sm rounded-md bg-wow-gold text-wow-dark hover:bg-yellow-500"
                  onClick={closeMenus}
                >
                  Register
                </Link>
              </>
            )}
          </div>
          
          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              className="text-wow-light hover:text-wow-gold focus:outline-none"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? (
                <XMarkIcon className="h-6 w-6" />
              ) : (
                <Bars3Icon className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>
      </div>
      
      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-wow-brown border-t border-neutral/30">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <NavLink
              to="/characters"
              className={({ isActive }) =>
                isActive
                  ? "block px-3 py-2 text-base font-medium text-wow-gold bg-wow-dark/30 rounded-md"
                  : "block px-3 py-2 text-base font-medium text-wow-light hover:bg-wow-dark/30 rounded-md"
              }
              onClick={closeMenus}
            >
              Characters
            </NavLink>
            <NavLink
              to="/events"
              className={({ isActive }) =>
                isActive
                  ? "block px-3 py-2 text-base font-medium text-wow-gold bg-wow-dark/30 rounded-md"
                  : "block px-3 py-2 text-base font-medium text-wow-light hover:bg-wow-dark/30 rounded-md"
              }
              onClick={closeMenus}
            >
              Events
            </NavLink>
            {currentUser ? (
              <>
                <NavLink
                  to="/dashboard"
                  className={({ isActive }) =>
                    isActive
                      ? "block px-3 py-2 text-base font-medium text-wow-gold bg-wow-dark/30 rounded-md"
                      : "block px-3 py-2 text-base font-medium text-wow-light hover:bg-wow-dark/30 rounded-md"
                  }
                  onClick={closeMenus}
                >
                  Dashboard
                </NavLink>
                <NavLink
                  to="/my-characters"
                  className={({ isActive }) =>
                    isActive
                      ? "block px-3 py-2 text-base font-medium text-wow-gold bg-wow-dark/30 rounded-md"
                      : "block px-3 py-2 text-base font-medium text-wow-light hover:bg-wow-dark/30 rounded-md"
                  }
                  onClick={closeMenus}
                >
                  My Characters
                </NavLink>
                <NavLink
                  to="/my-events"
                  className={({ isActive }) =>
                    isActive
                      ? "block px-3 py-2 text-base font-medium text-wow-gold bg-wow-dark/30 rounded-md"
                      : "block px-3 py-2 text-base font-medium text-wow-light hover:bg-wow-dark/30 rounded-md"
                  }
                  onClick={closeMenus}
                >
                  My Events
                </NavLink>
                <NavLink
                  to="/account-settings"
                  className={({ isActive }) =>
                    isActive
                      ? "block px-3 py-2 text-base font-medium text-wow-gold bg-wow-dark/30 rounded-md"
                      : "block px-3 py-2 text-base font-medium text-wow-light hover:bg-wow-dark/30 rounded-md"
                  }
                  onClick={closeMenus}
                >
                  Account Settings
                </NavLink>
                <button
                  className="block w-full text-left px-3 py-2 text-base font-medium text-wow-light hover:bg-wow-dark/30 rounded-md"
                  onClick={handleLogout}
                >
                  Logout
                </button>
              </>
            ) : (
              <div className="flex flex-col space-y-2 px-3 py-2">
                <Link
                  to="/login"
                  className="w-full text-center px-4 py-2 text-sm rounded-md bg-wow-brown text-wow-light border border-neutral/30"
                  onClick={closeMenus}
                >
                  Log In
                </Link>
                <Link
                  to="/register"
                  className="w-full text-center px-4 py-2 text-sm rounded-md bg-wow-gold text-wow-dark"
                  onClick={closeMenus}
                >
                  Register
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
};

export default Header; 