import { NavLink, useNavigate } from 'react-router-dom';
import { logout } from '../services/authService';

const navItems = [
  { name: 'Dashboard', path: '/owner/dashboard' },
  { name: 'Customers', path: '/owner/customers' },
  { name: 'Billing', path: '/owner/billing' },
  { name: 'Calendar', path: '/customer/calendar' },
];

export default function Layout({ title, children }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login', { replace: true });
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">Tiffin</div>
        <nav className="nav">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
            >
              {item.name}
            </NavLink>
          ))}
        </nav>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <h1>{title}</h1>
          <div className="topbar-actions">
            <button className="ghost-button" onClick={() => navigate('/profile')}>Profile</button>
            <button className="primary-button" onClick={handleLogout}>Logout</button>
          </div>
        </header>

        <div className="content">{children}</div>
      </main>
    </div>
  );
}
