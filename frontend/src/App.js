import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';

// Layout
import Layout from './components/Layout/Layout';

// Authentication pages
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import VerifyEmail from './pages/Auth/VerifyEmail';
import ResetPassword from './pages/Auth/ResetPassword';

// Public pages
import Home from './pages/Home/Home';
import CharacterDirectory from './pages/Characters/CharacterDirectory';
import CharacterDetails from './pages/Characters/CharacterDetails';
import EventCalendar from './pages/Events/EventCalendar';
import EventDetails from './pages/Events/EventDetails';
import UserProfile from './pages/Users/UserProfile';

// Protected pages
import Dashboard from './pages/Dashboard/Dashboard';
import MyCharacters from './pages/Dashboard/MyCharacters';
import EditCharacter from './pages/Characters/EditCharacter';
import CreateCharacter from './pages/Characters/CreateCharacter';
import MyEvents from './pages/Dashboard/MyEvents';
import CreateEvent from './pages/Events/CreateEvent';
import EditEvent from './pages/Events/EditEvent';
import AccountSettings from './pages/Dashboard/AccountSettings';

// Other
import NotFound from './pages/NotFound';

// Protected route wrapper
const ProtectedRoute = ({ children }) => {
  const { currentUser, loading } = useAuth();
  
  // If auth is still loading, show nothing or a spinner
  if (loading) {
    return <div className="flex items-center justify-center h-screen">
      <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-wow-gold"></div>
    </div>;
  }
  
  // If not authenticated, redirect to login
  if (!currentUser) {
    return <Navigate to="/login" />;
  }
  
  // Otherwise, show the protected component
  return children;
};

function App() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        
        {/* Auth Routes */}
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
        <Route path="verify-email" element={<VerifyEmail />} />
        <Route path="reset-password" element={<ResetPassword />} />
        
        {/* Character Routes */}
        <Route path="characters" element={<CharacterDirectory />} />
        <Route path="characters/:id" element={<CharacterDetails />} />
        
        {/* Event Routes */}
        <Route path="events" element={<EventCalendar />} />
        <Route path="events/:id" element={<EventDetails />} />
        
        {/* User Routes */}
        <Route path="users/:id" element={<UserProfile />} />
        
        {/* Protected Routes */}
        <Route path="dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
        
        <Route path="my-characters" element={
          <ProtectedRoute>
            <MyCharacters />
          </ProtectedRoute>
        } />
        
        <Route path="create-character" element={
          <ProtectedRoute>
            <CreateCharacter />
          </ProtectedRoute>
        } />
        
        <Route path="edit-character/:id" element={
          <ProtectedRoute>
            <EditCharacter />
          </ProtectedRoute>
        } />
        
        <Route path="my-events" element={
          <ProtectedRoute>
            <MyEvents />
          </ProtectedRoute>
        } />
        
        <Route path="create-event" element={
          <ProtectedRoute>
            <CreateEvent />
          </ProtectedRoute>
        } />
        
        <Route path="edit-event/:id" element={
          <ProtectedRoute>
            <EditEvent />
          </ProtectedRoute>
        } />
        
        <Route path="account-settings" element={
          <ProtectedRoute>
            <AccountSettings />
          </ProtectedRoute>
        } />
        
        {/* 404 Not Found */}
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App; 