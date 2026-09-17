import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { fetchBilling, generateBilling } from '../services/billingService';

export default function OwnerBillingPage() {
  const [bills, setBills] = useState([]);
  const [month, setMonth] = useState('2026-09');
  const [selectedBill, setSelectedBill] = useState(null);

  useEffect(() => {
    const loadBills = async () => {
      try {
        const data = await fetchBilling(1);
        setBills(data);
      } catch (error) {
        console.error('Failed to load billing', error);
      }
    };

    loadBills();
  }, []);

  const handleGenerate = async () => {
    try {
      const response = await generateBilling(month, 1);
      setBills(response.bills || []);
    } catch (error) {
      console.error('Failed to generate bill', error);
    }
  };

  return (
    <Layout title="Billing">
      <div className="panel full-width-panel">
        <div className="panel-header">
          <h3>Monthly Billing</h3>
          <div className="inline-actions">
            <input
              type="month"
              value={month}
              onChange={(event) => setMonth(event.target.value)}
              className="search-input"
            />
            <button className="primary-button" onClick={handleGenerate}>Generate Bill</button>
          </div>
        </div>

        <table className="data-table">
          <thead>
            <tr>
              <th>Month</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {bills.length === 0 ? (
              <tr><td colSpan="4">No bills available yet.</td></tr>
            ) : bills.map((bill) => (
              <tr key={bill.id}>
                <td>{bill.billing_month}</td>
                <td>{bill.total_amount}</td>
                <td><span className="badge active">{bill.status}</span></td>
                <td><button className="ghost-button" onClick={() => setSelectedBill(bill)}>Open</button></td>
              </tr>
            ))}
          </tbody>
        </table>

        {selectedBill && (
          <div className="customer-detail">
            <div className="panel-header">
              <h3>Bill details</h3>
              <button className="ghost-button" onClick={() => setSelectedBill(null)}>Close</button>
            </div>
            <p>Customer ID: {selectedBill.customer}</p>
            <p>Served days: {selectedBill.served_days}</p>
            <p>Total: {selectedBill.total_amount}</p>
          </div>
        )}
      </div>
    </Layout>
  );
}
