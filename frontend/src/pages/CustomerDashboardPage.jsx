import { useState } from 'react';
import Layout from '../components/Layout';
import { customerSummary, billingHistory, calendarDays } from '../data/mockData';

export default function CustomerDashboardPage() {
  const [pauseNotice, setPauseNotice] = useState('');

  return (
    <Layout title="Customer Dashboard">
      <section className="customer-hero panel">
        <div>
          <p className="eyebrow">Hello Rahul 👋</p>
          <h3>{customerSummary.name}</h3>
        </div>

        <div className="customer-meta">
          <div>
            <span>Subscription</span>
            <strong>{customerSummary.subscription}</strong>
          </div>
          <div>
            <span>Status</span>
            <strong className="status-active">{customerSummary.status}</strong>
          </div>
        </div>
      </section>

      <section className="stats-grid compact">
        <div className="stat-card">
          <div className="stat-label">Served</div>
          <div className="stat-value">{customerSummary.servedDays} days</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Paused</div>
          <div className="stat-value">{customerSummary.pausedDays} days</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Current Bill</div>
          <div className="stat-value">{customerSummary.currentBill}</div>
        </div>
      </section>

      <section className="section-grid two-col">
        <div className="panel">
          <div className="panel-header">
            <h3>Monthly Calendar</h3>
            <button
              className="primary-button"
              onClick={() => setPauseNotice('Pause requests will be available once your active subscription is connected.')}
            >
              Pause Tiffin
            </button>
          </div>

          {pauseNotice && <p className="form-feedback">{pauseNotice}</p>}

          <div className="calendar-grid">
            {calendarDays.map((day) => (
              <div key={day.date} className="calendar-day">
                <div className="calendar-date">{day.date.slice(-2)}</div>
                <span className={`badge ${day.status.toLowerCase()}`}>{day.status}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h3>Billing History</h3>
          </div>

          <ul className="list-stack">
            {billingHistory.map((bill) => (
              <li key={bill.month} className="bill-row">
                <span>{bill.month}</span>
                <strong>{bill.amount}</strong>
                <span className={`badge ${bill.status.toLowerCase().replace(/_/g, '-')}`}>{bill.status}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>
    </Layout>
  );
}
