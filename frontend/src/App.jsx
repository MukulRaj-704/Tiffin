import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import OwnerDashboardPage from './pages/OwnerDashboardPage';
import OwnerCustomersPage from './pages/OwnerCustomersPage';
import OwnerBillingPage from './pages/OwnerBillingPage';
import CustomerDashboardPage from './pages/CustomerDashboardPage';
import ProtectedRoute from './pages/ProtectedRoute';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginPage />} />

        <Route path="/owner/dashboard" element={<ProtectedRoute><OwnerDashboardPage /></ProtectedRoute>} />
        <Route path="/owner/customers" element={<ProtectedRoute><OwnerCustomersPage /></ProtectedRoute>} />
        <Route path="/owner/billing" element={<ProtectedRoute><OwnerBillingPage /></ProtectedRoute>} />

        <Route path="/customer/dashboard" element={<ProtectedRoute><CustomerDashboardPage /></ProtectedRoute>} />
        <Route path="/customer/calendar" element={<ProtectedRoute><CustomerDashboardPage /></ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  );
}
