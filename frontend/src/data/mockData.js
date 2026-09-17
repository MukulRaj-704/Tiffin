export const ownerStats = [
  { label: 'Total Customers', value: '248' },
  { label: 'Active Customers', value: '186' },
  { label: 'Paused Customers', value: '31' },
  { label: 'Today\'s Deliveries', value: '72' },
  { label: 'This Month\'s Revenue', value: '₹ 1,48,500' },
];

export const customerSummary = {
  name: 'Rahul Sharma',
  subscription: '₹3000 / month',
  status: 'ACTIVE',
  servedDays: 17,
  pausedDays: 5,
  currentBill: '₹2318.12',
};

export const deliveryRows = [
  { id: 1, name: 'Rahul Sharma', phone: '9876543210', status: 'SERVED' },
  { id: 2, name: 'Amit Verma', phone: '9876543211', status: 'PENDING' },
  { id: 3, name: 'Priya Nair', phone: '9876543212', status: 'SERVED' },
  { id: 4, name: 'Sneha Iyer', phone: '9876543213', status: 'PAUSED' },
];

export const customerRows = [
  { id: 1, name: 'Rahul Sharma', phone: '9876543210', status: 'ACTIVE', plan: '₹3000', bill: '₹2318.12' },
  { id: 2, name: 'Amit Verma', phone: '9876543211', status: 'PAUSED', plan: '₹3000', bill: '₹1900.00' },
  { id: 3, name: 'Priya Nair', phone: '9876543212', status: 'ACTIVE', plan: '₹2800', bill: '₹2650.00' },
  { id: 4, name: 'Sneha Iyer', phone: '9876543213', status: 'PAUSED', plan: '₹3200', bill: '₹1450.50' },
];

export const billingHistory = [
  { month: 'August 2026', amount: '₹2,985.00', status: 'PAID' },
  { month: 'September 2026', amount: '₹2,318.12', status: 'UNPAID' },
  { month: 'October 2026', amount: '₹3,000.00', status: 'PARTIALLY_PAID' },
];

export const calendarDays = [
  { date: '2026-09-01', status: 'SERVED' },
  { date: '2026-09-02', status: 'SERVED' },
  { date: '2026-09-03', status: 'PAUSED' },
  { date: '2026-09-04', status: 'SERVED' },
  { date: '2026-09-05', status: 'SERVED' },
  { date: '2026-09-08', status: 'SERVED' },
  { date: '2026-09-09', status: 'PAUSED' },
  { date: '2026-09-10', status: 'PAUSED' },
  { date: '2026-09-11', status: 'SERVED' },
  { date: '2026-09-12', status: 'SERVED' },
];
