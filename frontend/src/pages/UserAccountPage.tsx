import React, { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate, useSearchParams } from 'react-router-dom'
import PremiumCart from '../components/ui/PremiumCart'

interface Order {
  id: number
  order_number: string
  total_amount: number
  status: string
  created_at: string
  items: OrderItem[]
}

interface OrderItem {
  id: number
  product_name: string
  quantity: number
  price: number
}

export default function UserAccountPage() {
  const { user, isAuthenticated, isLoading, logout, hasPremiumAccess } = useAuth()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [activeTab, setActiveTab] = useState<'profile' | 'orders' | 'settings' | 'cart' | 'premium'>('profile')
  const [orders, setOrders] = useState<Order[]>([])
  const [isEditing, setIsEditing] = useState(false)
  const [editForm, setEditForm] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    phone: user?.phone || '',
  })

  // Handle URL parameters for tab switching
  useEffect(() => {
    const tabParam = searchParams.get('tab')
    if (tabParam && ['profile', 'orders', 'settings', 'cart', 'premium'].includes(tabParam)) {
      setActiveTab(tabParam as any)
    }
  }, [searchParams])

  // Redirect if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      navigate('/login')
    }
  }, [isAuthenticated, isLoading, navigate])

  // Load user orders
  useEffect(() => {
    if (isAuthenticated && user) {
      loadOrders()
    }
  }, [isAuthenticated, user])

  const loadOrders = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/api/v1/orders/my-orders', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
      
      if (response.ok) {
        const data = await response.json()
        setOrders(data)
      }
    } catch (error) {
      console.error('Error loading orders:', error)
    }
  }

  const handleEditSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/api/v1/users/me', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editForm),
      })
      
      if (response.ok) {
        setIsEditing(false)
        // Refresh user data
        window.location.reload()
      }
    } catch (error) {
      console.error('Error updating profile:', error)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">My Account</h1>
          <p className="text-gray-400 mt-2">Manage your profile, orders, and preferences</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-gray-800 rounded-lg p-6">
              <div className="text-center mb-6">
                <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-white">
                    {user?.first_name?.[0]}{user?.last_name?.[0]}
                  </span>
                </div>
                <h3 className="text-lg font-semibold text-white">{user?.first_name} {user?.last_name}</h3>
                <p className="text-gray-400 text-sm">{user?.email}</p>
                <span className={`inline-block px-2 py-1 text-xs rounded-full mt-2 ${
                  user?.role === 'admin' 
                    ? 'bg-purple-600 text-white' 
                    : 'bg-green-600 text-white'
                }`}>
                  {user?.role === 'admin' ? 'Admin' : 'Customer'}
                </span>
              </div>

              {/* Navigation */}
              <nav className="space-y-2">
                <button
                  onClick={() => setActiveTab('profile')}
                  className={`w-full text-left px-3 py-2 rounded-md transition-colors ${
                    activeTab === 'profile'
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  Profile
                </button>
                <button
                  onClick={() => setActiveTab('orders')}
                  className={`w-full text-left px-3 py-2 rounded-md transition-colors ${
                    activeTab === 'orders'
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  Orders
                </button>
                <button
                  onClick={() => setActiveTab('cart')}
                  className={`w-full text-left px-3 py-2 rounded-md transition-colors ${
                    activeTab === 'cart'
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span>Cart</span>
                    {hasPremiumAccess() && (
                      <span className="text-xs bg-green-600 text-white px-2 py-1 rounded-full">Premium</span>
                    )}
                  </div>
                </button>
                <button
                  onClick={() => setActiveTab('premium')}
                  className={`w-full text-left px-3 py-2 rounded-md transition-colors ${
                    activeTab === 'premium'
                      ? 'bg-purple-600 text-white'
                      : 'text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span>Premium</span>
                    {hasPremiumAccess() && (
                      <span className="text-xs bg-green-600 text-white px-2 py-1 rounded-full">Active</span>
                    )}
                  </div>
                </button>
                <button
                  onClick={() => setActiveTab('settings')}
                  className={`w-full text-left px-3 py-2 rounded-md transition-colors ${
                    activeTab === 'settings'
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  Settings
                </button>
              </nav>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <div className="bg-gray-800 rounded-lg p-6">
              {/* Profile Tab */}
              {activeTab === 'profile' && (
                <div>
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-xl font-semibold text-white">Profile Information</h2>
                    <button
                      onClick={() => setIsEditing(!isEditing)}
                      className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors"
                    >
                      {isEditing ? 'Cancel' : 'Edit Profile'}
                    </button>
                  </div>

                  {isEditing ? (
                    <form onSubmit={handleEditSubmit} className="space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-300 mb-2">
                            First Name
                          </label>
                          <input
                            type="text"
                            value={editForm.first_name}
                            onChange={(e) => setEditForm(prev => ({ ...prev, first_name: e.target.value }))}
                            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-300 mb-2">
                            Last Name
                          </label>
                          <input
                            type="text"
                            value={editForm.last_name}
                            onChange={(e) => setEditForm(prev => ({ ...prev, last_name: e.target.value }))}
                            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                          />
                        </div>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Phone
                        </label>
                        <input
                          type="tel"
                          value={editForm.phone}
                          onChange={(e) => setEditForm(prev => ({ ...prev, phone: e.target.value }))}
                          className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                      <div className="flex space-x-4">
                        <button
                          type="submit"
                          className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md transition-colors"
                        >
                          Save Changes
                        </button>
                        <button
                          type="button"
                          onClick={() => setIsEditing(false)}
                          className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md transition-colors"
                        >
                          Cancel
                        </button>
                      </div>
                    </form>
                  ) : (
                    <div className="space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-400 mb-1">
                            First Name
                          </label>
                          <p className="text-white">{user?.first_name}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-400 mb-1">
                            Last Name
                          </label>
                          <p className="text-white">{user?.last_name}</p>
                        </div>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-400 mb-1">
                          Email
                        </label>
                        <p className="text-white">{user?.email}</p>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-400 mb-1">
                          Phone
                        </label>
                        <p className="text-white">{user?.phone || 'Not provided'}</p>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-400 mb-1">
                          Account Status
                        </label>
                        <div className="flex items-center space-x-2">
                          <span className={`inline-block px-2 py-1 text-xs rounded-full ${
                            user?.is_active ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
                          }`}>
                            {user?.is_active ? 'Active' : 'Inactive'}
                          </span>
                          <span className={`inline-block px-2 py-1 text-xs rounded-full ${
                            user?.is_verified ? 'bg-blue-600 text-white' : 'bg-yellow-600 text-white'
                          }`}>
                            {user?.is_verified ? 'Verified' : 'Unverified'}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Orders Tab */}
              {activeTab === 'orders' && (
                <div>
                  <h2 className="text-xl font-semibold text-white mb-6">Order History</h2>
                  {orders.length === 0 ? (
                    <div className="text-center py-8">
                      <p className="text-gray-400">No orders found</p>
                      <button
                        onClick={() => navigate('/products')}
                        className="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors"
                      >
                        Start Shopping
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {orders.map((order) => (
                        <div key={order.id} className="border border-gray-700 rounded-lg p-4">
                          <div className="flex justify-between items-start mb-4">
                            <div>
                              <h3 className="text-lg font-semibold text-white">
                                Order #{order.order_number}
                              </h3>
                              <p className="text-gray-400 text-sm">
                                {new Date(order.created_at).toLocaleDateString()}
                              </p>
                            </div>
                            <div className="text-right">
                              <p className="text-lg font-semibold text-white">
                                ${order.total_amount.toFixed(2)}
                              </p>
                              <span className={`inline-block px-2 py-1 text-xs rounded-full ${
                                order.status === 'completed' ? 'bg-green-600 text-white' :
                                order.status === 'pending' ? 'bg-yellow-600 text-white' :
                                'bg-gray-600 text-white'
                              }`}>
                                {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                              </span>
                            </div>
                          </div>
                          <div className="space-y-2">
                            {order.items.map((item) => (
                              <div key={item.id} className="flex justify-between text-sm">
                                <span className="text-gray-300">
                                  {item.product_name} x {item.quantity}
                                </span>
                                <span className="text-white">${item.price.toFixed(2)}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Cart Tab */}
              {activeTab === 'cart' && (
                <div>
                  <PremiumCart />
                </div>
              )}

              {/* Premium Tab */}
              {activeTab === 'premium' && (
                <div>
                  <h2 className="text-xl font-semibold text-white mb-6">Premium Membership</h2>
                  {hasPremiumAccess() ? (
                    <div className="bg-gradient-to-r from-purple-900/20 to-blue-900/20 border border-purple-500/30 rounded-lg p-6">
                      <div className="text-center mb-6">
                        <div className="text-6xl mb-4">👑</div>
                        <h3 className="text-2xl font-bold text-white mb-2">Premium Active</h3>
                        <p className="text-gray-400">
                          {user?.premium_expires_at 
                            ? `Expires: ${new Date(user.premium_expires_at).toLocaleDateString()}`
                            : 'Lifetime membership'
                          }
                        </p>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div className="bg-gray-700 rounded-lg p-4">
                          <h4 className="text-lg font-semibold text-white mb-3">Premium Benefits</h4>
                          <ul className="space-y-2 text-gray-300">
                            <li className="flex items-center">
                              <span className="text-green-400 mr-2">✓</span>
                              10% discount on all purchases
                            </li>
                            <li className="flex items-center">
                              <span className="text-green-400 mr-2">✓</span>
                              Priority customer support
                            </li>
                            <li className="flex items-center">
                              <span className="text-green-400 mr-2">✓</span>
                              Exclusive product access
                            </li>
                            <li className="flex items-center">
                              <span className="text-green-400 mr-2">✓</span>
                              Free shipping on orders over $50
                            </li>
                            <li className="flex items-center">
                              <span className="text-green-400 mr-2">✓</span>
                              Advanced shopping cart features
                            </li>
                          </ul>
                        </div>
                        
                        <div className="bg-gray-700 rounded-lg p-4">
                          <h4 className="text-lg font-semibold text-white mb-3">Account Status</h4>
                          <div className="space-y-3">
                            <div className="flex justify-between">
                              <span className="text-gray-300">Membership:</span>
                              <span className="text-green-400 font-medium">Premium</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-300">Status:</span>
                              <span className="text-green-400 font-medium">Active</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-300">Since:</span>
                              <span className="text-white">Account creation</span>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <div className="text-center">
                        <button
                          onClick={() => setActiveTab('cart')}
                          className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-lg font-semibold transition-all duration-200 transform hover:scale-105"
                        >
                          Use Premium Cart
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="bg-gradient-to-r from-purple-900/20 to-blue-900/20 border border-purple-500/30 rounded-lg p-8 text-center">
                      <div className="text-6xl mb-6">👑</div>
                      <h3 className="text-2xl font-bold text-white mb-4">Upgrade to Premium</h3>
                      <p className="text-gray-400 mb-8 max-w-md mx-auto">
                        Unlock exclusive features including the premium shopping cart, discounts, and priority support.
                      </p>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                        <div className="bg-gray-700 rounded-lg p-4">
                          <h4 className="text-lg font-semibold text-white mb-3">Premium Features</h4>
                          <ul className="space-y-2 text-gray-300 text-left">
                            <li className="flex items-center">
                              <span className="text-blue-400 mr-2">→</span>
                              Advanced shopping cart
                            </li>
                            <li className="flex items-center">
                              <span className="text-blue-400 mr-2">→</span>
                              10% discount on purchases
                            </li>
                            <li className="flex items-center">
                              <span className="text-blue-400 mr-2">→</span>
                              Priority customer support
                            </li>
                            <li className="flex items-center">
                              <span className="text-blue-400 mr-2">→</span>
                              Exclusive product access
                            </li>
                            <li className="flex items-center">
                              <span className="text-blue-400 mr-2">→</span>
                              Free shipping over $50
                            </li>
                          </ul>
                        </div>
                        
                        <div className="bg-gray-700 rounded-lg p-4">
                          <h4 className="text-lg font-semibold text-white mb-3">Pricing</h4>
                          <div className="text-center">
                            <div className="text-3xl font-bold text-white mb-2">$9.99</div>
                            <div className="text-gray-400 mb-4">per month</div>
                            <div className="text-sm text-gray-300">
                              Cancel anytime • No setup fees
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <button className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-lg font-semibold text-lg transition-all duration-200 transform hover:scale-105">
                        Upgrade Now
                      </button>
                    </div>
                  )}
                </div>
              )}

              {/* Settings Tab */}
              {activeTab === 'settings' && (
                <div>
                  <h2 className="text-xl font-semibold text-white mb-6">Account Settings</h2>
                  <div className="space-y-6">
                    <div>
                      <h3 className="text-lg font-medium text-white mb-4">Danger Zone</h3>
                      <div className="border border-red-600 rounded-lg p-4">
                        <p className="text-gray-300 mb-4">
                          Once you delete your account, there is no going back. Please be certain.
                        </p>
                        <button className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md transition-colors">
                          Delete Account
                        </button>
                      </div>
                    </div>
                    
                    <div>
                      <h3 className="text-lg font-medium text-white mb-4">Actions</h3>
                      <div className="space-y-3">
                        <button
                          onClick={logout}
                          className="w-full px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md transition-colors"
                        >
                          Sign Out
                        </button>
                        {user?.role === 'admin' && (
                          <button
                            onClick={() => navigate('/dashboard')}
                            className="w-full px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-md transition-colors"
                          >
                            Go to Admin Dashboard
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 