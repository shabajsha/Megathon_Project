import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { authService } from '../services';

function Login() {
  const [userType, setUserType] = useState('participant');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let response;
      if (userType === 'participant') {
        response = await authService.loginParticipant({ email, password });
      } else if (userType === 'organizer') {
        response = await authService.loginOrganizer({ email, password });
      } else {
        response = await authService.loginAdmin({ email, password });
      }

      login(response.data.token, response.data.user);
      
      // Redirect based on role
      if (userType === 'participant') {
        navigate('/participant/dashboard');
      } else if (userType === 'organizer') {
        navigate('/organizer/dashboard');
      } else {
        navigate('/admin/dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Event Management System</h2>
        <h3>Login</h3>
        
        <div className="user-type-selector">
          <button
            className={userType === 'participant' ? 'active' : ''}
            onClick={() => setUserType('participant')}
          >
            Participant
          </button>
          <button
            className={userType === 'organizer' ? 'active' : ''}
            onClick={() => setUserType('organizer')}
          >
            Organizer
          </button>
          <button
            className={userType === 'admin' ? 'active' : ''}
            onClick={() => setUserType('admin')}
          >
            Admin
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        {userType === 'participant' && (
          <p className="signup-link">
            Don't have an account? <Link to="/register">Register here</Link>
          </p>
        )}
      </div>
    </div>
  );
}

export default Login;
