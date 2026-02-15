import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

function ParticipantDashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <h1>Event Management System</h1>
        <div className="nav-links">
          <button onClick={() => navigate('/participant/dashboard')}>Dashboard</button>
          <button onClick={() => navigate('/participant/events')}>Browse Events</button>
          <button onClick={() => navigate('/participant/clubs')}>Clubs</button>
          <button onClick={() => navigate('/participant/profile')}>Profile</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </nav>

      <div className="dashboard-content">
        <h2>Welcome, {user?.firstName} {user?.lastName}!</h2>
        
        <div className="dashboard-cards">
          <div className="card">
            <h3>Upcoming Events</h3>
            <p>You have no upcoming events yet.</p>
            <button onClick={() => navigate('/participant/events')}>Browse Events</button>
          </div>

          <div className="card">
            <h3>Participation History</h3>
            <p>No participation history yet.</p>
          </div>

          <div className="card">
            <h3>Followed Clubs</h3>
            <p>You are not following any clubs yet.</p>
            <button onClick={() => navigate('/participant/clubs')}>Explore Clubs</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ParticipantDashboard;
