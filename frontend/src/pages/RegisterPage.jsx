import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { register } from '../services/authService';

const initialForm = {
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
};

export default function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  };

  const handleRegister = async (event) => {
    event.preventDefault();
    setError('');
    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      await register({
        username: form.username,
        email: form.email,
        phone: form.phone,
        password: form.password,
      });
      navigate('/login', { replace: true, state: { username: form.username, registered: true } });
    } catch (registrationError) {
      const responseData = registrationError.response?.data;
      const detail = responseData?.detail || Object.values(responseData || {})[0]?.[0];
      setError(detail || 'Registration failed. Check your details and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Create your account</h2>
        <p>Start managing your tiffin subscription</p>

        <form onSubmit={handleRegister} className="auth-form">
          <label>
            Username
            <input name="username" value={form.username} onChange={handleChange} required autoComplete="username" />
          </label>

          <label>
            Email
            <input type="email" name="email" value={form.email} onChange={handleChange} required autoComplete="email" />
          </label>

          <label>
            Phone
            <input name="phone" value={form.phone} onChange={handleChange} required autoComplete="tel" />
          </label>

          <label>
            Password
            <input type="password" name="password" value={form.password} onChange={handleChange} required minLength="8" autoComplete="new-password" />
          </label>

          <label>
            Confirm password
            <input type="password" name="confirmPassword" value={form.confirmPassword} onChange={handleChange} required minLength="8" autoComplete="new-password" />
          </label>

          {error && <div className="error-box">{error}</div>}

          <div className="auth-actions">
            <button type="submit" className="primary-button" disabled={loading}>
              {loading ? 'Creating account...' : 'Create account'}
            </button>
            <button type="button" className="ghost-button" onClick={() => navigate('/login')}>Back to login</button>
          </div>
        </form>
      </div>
    </div>
  );
}