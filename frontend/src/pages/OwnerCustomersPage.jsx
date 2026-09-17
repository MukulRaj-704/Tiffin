import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { createCustomer, fetchCustomers, searchCustomers } from '../services/customerService';

const initialForm = {
  username: '',
  password: '',
  name: '',
  phone: '',
  email: '',
  address: '',
};

export default function OwnerCustomersPage() {
  const [customers, setCustomers] = useState([]);
  const [query, setQuery] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(initialForm);
  const [feedback, setFeedback] = useState('');
  const [selectedCustomer, setSelectedCustomer] = useState(null);

  useEffect(() => {
    const loadCustomers = async () => {
      try {
        const data = await fetchCustomers();
        setCustomers(data);
      } catch (error) {
        console.error('Failed to fetch customers', error);
      }
    };

    loadCustomers();
  }, []);

  const handleSearch = async () => {
    try {
      const data = query ? await searchCustomers(query) : await fetchCustomers();
      setCustomers(data);
    } catch (error) {
      console.error('Search failed', error);
    }
  };

  const handleCreate = async (event) => {
    event.preventDefault();
    setFeedback('');
    try {
      const customer = await createCustomer(form);
      setCustomers((current) => [...current, customer].sort((first, second) => first.name.localeCompare(second.name)));
      setForm(initialForm);
      setShowForm(false);
      setFeedback(`${customer.name} was added successfully.`);
    } catch (error) {
      const detail = error.response?.data?.detail || Object.values(error.response?.data || {})[0]?.[0];
      setFeedback(detail || 'Unable to add customer. Check the form and try again.');
    }
  };

  return (
    <Layout title="Customers">
      <div className="panel full-width-panel">
        <div className="panel-header">
          <h3>Customer Management</h3>
          <div className="inline-actions">
            <input
              type="text"
              placeholder="Search by phone"
              className="search-input"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
            <button className="primary-button" onClick={handleSearch}>Search</button>
            <button className="ghost-button" onClick={() => setShowForm((visible) => !visible)}>
              {showForm ? 'Close' : 'Add customer'}
            </button>
          </div>
        </div>

        {feedback && <p className="form-feedback">{feedback}</p>}

        {showForm && (
          <form className="customer-form" onSubmit={handleCreate}>
            <input required placeholder="Full name" value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} />
            <input required placeholder="Username" value={form.username} onChange={(event) => setForm({ ...form, username: event.target.value })} />
            <input required type="password" minLength="8" placeholder="Temporary password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} />
            <input required placeholder="Phone" value={form.phone} onChange={(event) => setForm({ ...form, phone: event.target.value })} />
            <input type="email" placeholder="Email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} />
            <input placeholder="Address" value={form.address} onChange={(event) => setForm({ ...form, address: event.target.value })} />
            <button className="primary-button" type="submit">Create customer</button>
          </form>
        )}

        <table className="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Phone</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {customers.length === 0 ? (
              <tr><td colSpan="4">No customers found.</td></tr>
            ) : customers.map((row) => (
              <tr key={row.id}>
                <td>{row.name}</td>
                <td>{row.phone}</td>
                <td><span className="badge active">ACTIVE</span></td>
                <td><button className="ghost-button" onClick={() => setSelectedCustomer(row)}>View</button></td>
              </tr>
            ))}
          </tbody>
        </table>

        {selectedCustomer && (
          <div className="customer-detail">
            <div className="panel-header">
              <h3>{selectedCustomer.name}</h3>
              <button className="ghost-button" onClick={() => setSelectedCustomer(null)}>Close</button>
            </div>
            <p>Phone: {selectedCustomer.phone}</p>
            <p>Email: {selectedCustomer.email || 'Not provided'}</p>
            <p>Address: {selectedCustomer.address || 'Not provided'}</p>
          </div>
        )}
      </div>
    </Layout>
  );
}
