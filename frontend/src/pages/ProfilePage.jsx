import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { useAuth } from '../hooks/useAuth';

export default function ProfilePage() {
  const navigate = useNavigate();
  const { user, loading } = useAuth();

  return (
    <Layout title="Profile">
      <section className="panel profile-panel">
        <h3>Account details</h3>
        {loading ? <p>Loading profile...</p> : (
          <dl className="profile-details">
            <dt>Username</dt><dd>{user?.username}</dd>
            <dt>Email</dt><dd>{user?.email || 'Not provided'}</dd>
            <dt>Phone</dt><dd>{user?.phone || 'Not provided'}</dd>
            <dt>Role</dt><dd>{user?.role}</dd>
          </dl>
        )}
        <button className="ghost-button" onClick={() => navigate(-1)}>Back</button>
      </section>
    </Layout>
  );
}