import { NavLink } from 'react-router-dom';

const navItems = [
  { name: 'Dashboard', path: '/owner/dashboard' },
  { name: 'Customers', path: '/owner/customers' },
  { name: 'Billing', path: '/owner/billing' },
  { name: 'Calendar', path: '/customer/calendar' },
];

export default function Layout({ title, children }) {
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
            <button className="ghost-button">Profile</button>
            <button className="primary-button">Logout</button>
          </div>
        </header>

        <div className="content">{children}</div>
      </main>
    </div>
  );
}
