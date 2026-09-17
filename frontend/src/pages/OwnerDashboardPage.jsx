import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { fetchCustomers } from '../services/customerService';

const defaultStats = [
  { label: 'Total Customers', value: '0' },
  { label: 'Active Customers', value: '0' },
  { label: 'Paused Customers', value: '0' },
  { label: 'Today\'s Deliveries', value: '0' },
  { label: 'This Month\'s Revenue', value: '₹ 0' },
];

export default function OwnerDashboardPage() {
  const [customers, setCustomers] = useState([]);
  const [stats, setStats] = useState(defaultStats);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchCustomers();
        setCustomers(data);
        setStats([
          { label: 'Total Customers', value: String(data.length) },
          { label: 'Active Customers', value: String(data.filter((customer) => customer.status === 'ACTIVE').length || 0) },
          { label: 'Paused Customers', value: String(data.filter((customer) => customer.status === 'PAUSED').length || 0) },
          { label: 'Today\'s Deliveries', value: '0' },
          { label: 'This Month\'s Revenue', value: '₹ 0' },
        ]);
      } catch (error) {
        console.error('Failed to load customers', error);
      }
    };

    loadData();
  }, []);

  return (
    <Layout title="Owner Dashboard">
      <section className="stats-grid">
        {stats.map((stat) => (
          <div key={stat.label} className="stat-card">
            <div className="stat-label">{stat.label}</div>
            <div className="stat-value">{stat.value}</div>
          </div>
        ))}
      </section>

      <section className="section-grid two-col">
        <div className="panel">
          <div className="panel-header">
            <h3>Today's Delivery List</h3>
            <button className="ghost-button">View all</button>
          </div>

          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Phone</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {customers.length === 0 ? (
                <tr><td colSpan="3">No customers available yet.</td></tr>
              ) : customers.map((row) => (
                <tr key={row.id}>
                  <td>{row.name}</td>
                  <td>{row.phone}</td>
                  <td>
                    <span className="badge active">ACTIVE</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h3>Customer Overview</h3>
            <button className="ghost-button">Filter</button>
          </div>

          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Status</th>
                <th>Phone</th>
              </tr>
            </thead>
            <tbody>
              {customers.length === 0 ? (
                <tr><td colSpan="3">No customers to display.</td></tr>
              ) : customers.map((row) => (
                <tr key={row.id}>
                  <td>{row.name}</td>
                  <td><span className="badge active">ACTIVE</span></td>
                  <td>{row.phone}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </Layout>
  );
}
