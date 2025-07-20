import React from 'react'
import { Link, Routes, Route } from 'react-router-dom'

// Dashboard sub-components
const DashboardHome = () => (
  <div className="p-6">
    <h3 className="text-2xl font-bold text-white mb-4">Dashboard Overview</h3>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="card p-6">
        <h4 className="text-lg font-semibold text-white mb-2">Total Orders</h4>
        <p className="text-3xl font-bold text-blue-400">24</p>
      </div>
      <div className="card p-6">
        <h4 className="text-lg font-semibold text-white mb-2">Revenue</h4>
        <p className="text-3xl font-bold text-green-400">$1,234</p>
      </div>
      <div className="card p-6">
        <h4 className="text-lg font-semibold text-white mb-2">Products</h4>
        <p className="text-3xl font-bold text-purple-400">156</p>
      </div>
    </div>
  </div>
)

const DashboardOrders = () => (
  <div className="p-6">
    <h3 className="text-2xl font-bold text-white mb-4">Order Management</h3>
    <div className="card p-6">
      <p className="text-gray-300">Manage your orders, track shipments, and handle returns.</p>
    </div>
  </div>
)

const DashboardProducts = () => (
  <div className="p-6">
    <h3 className="text-2xl font-bold text-white mb-4">Product Management</h3>
    <div className="card p-6">
      <p className="text-gray-300">Add, edit, and manage your product catalog.</p>
    </div>
  </div>
)

const DashboardAnalytics = () => (
  <div className="p-6">
    <h3 className="text-2xl font-bold text-white mb-4">Analytics</h3>
    <div className="card p-6">
      <p className="text-gray-300">View sales reports, customer insights, and performance metrics.</p>
    </div>
  </div>
)

const DashboardPage = () => {
  return (
    <div className="min-h-screen bg-gray-900">
      <div className="flex">
        {/* Sidebar Navigation */}
        <div className="w-64 bg-gray-800 min-h-screen p-6">
          <h2 className="text-2xl font-bold text-white mb-6">Admin Dashboard</h2>
          <nav className="space-y-2">
            <Link 
              to="../" 
              className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-700 rounded transition-colors"
            >
              ← Back to Store
            </Link>
            <Link 
              to="." 
              className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-700 rounded transition-colors"
            >
              Dashboard Home
            </Link>
            <Link 
              to="orders" 
              className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-700 rounded transition-colors"
            >
              Orders
            </Link>
            <Link 
              to="products" 
              className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-700 rounded transition-colors"
            >
              Products
            </Link>
            <Link 
              to="analytics" 
              className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-700 rounded transition-colors"
            >
              Analytics
            </Link>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          <Routes>
            <Route path="/" element={<DashboardHome />} />
            <Route path="orders" element={<DashboardOrders />} />
            <Route path="products" element={<DashboardProducts />} />
            <Route path="analytics" element={<DashboardAnalytics />} />
          </Routes>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage 