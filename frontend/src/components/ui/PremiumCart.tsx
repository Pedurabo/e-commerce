import React, { useState, useEffect } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

interface CartItem {
  id: number
  name: string
  price: number
  quantity: number
  image: string
}

export default function PremiumCart() {
  const { user, hasPremiumAccess } = useAuth()
  const navigate = useNavigate()
  const [cartItems, setCartItems] = useState<CartItem[]>([])
  const [isLoading, setIsLoading] = useState(false)

  // Check premium access
  if (!hasPremiumAccess()) {
    return (
      <div className="text-center py-12">
        <div className="bg-gray-800 rounded-lg p-8 max-w-md mx-auto">
          <div className="text-6xl mb-4">👑</div>
          <h3 className="text-xl font-semibold text-white mb-4">Premium Feature</h3>
          <p className="text-gray-400 mb-6">
            The shopping cart is a premium feature. Upgrade your account to access this functionality.
          </p>
          <button
            onClick={() => navigate('/account?tab=premium')}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-lg font-semibold transition-all duration-200 transform hover:scale-105"
          >
            Upgrade to Premium
          </button>
        </div>
      </div>
    )
  }

  // Load cart items from localStorage
  useEffect(() => {
    const savedCart = localStorage.getItem('cart')
    if (savedCart) {
      try {
        setCartItems(JSON.parse(savedCart))
      } catch (error) {
        console.error('Error parsing cart:', error)
        setCartItems([])
      }
    }
  }, [])

  const updateQuantity = (itemId: number, newQuantity: number) => {
    if (newQuantity <= 0) {
      removeItem(itemId)
      return
    }

    const updatedCart = cartItems.map(item =>
      item.id === itemId ? { ...item, quantity: newQuantity } : item
    )
    setCartItems(updatedCart)
    localStorage.setItem('cart', JSON.stringify(updatedCart))
  }

  const removeItem = (itemId: number) => {
    const updatedCart = cartItems.filter(item => item.id !== itemId)
    setCartItems(updatedCart)
    localStorage.setItem('cart', JSON.stringify(updatedCart))
    toast.success('Item removed from cart')
  }

  const clearCart = () => {
    setCartItems([])
    localStorage.removeItem('cart')
    toast.success('Cart cleared')
  }

  const getTotalPrice = () => {
    return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0)
  }

  const handleCheckout = async () => {
    if (cartItems.length === 0) {
      toast.error('Your cart is empty')
      return
    }

    setIsLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8001/api/orders', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          items: cartItems.map(item => ({
            product_id: item.id,
            quantity: item.quantity,
            price: item.price
          })),
          total_amount: getTotalPrice()
        }),
      })

      if (response.ok) {
        const order = await response.json()
        clearCart()
        toast.success('Order placed successfully!')
        navigate(`/account?tab=orders`)
      } else {
        const error = await response.json()
        toast.error(error.detail || 'Failed to place order')
      }
    } catch (error) {
      console.error('Checkout error:', error)
      toast.error('Network error. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  if (cartItems.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="bg-gray-800 rounded-lg p-8">
          <div className="text-6xl mb-4">🛒</div>
          <h3 className="text-xl font-semibold text-white mb-4">Your Cart is Empty</h3>
          <p className="text-gray-400 mb-6">
            Start shopping to add items to your premium cart.
          </p>
          <button
            onClick={() => navigate('/products')}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors"
          >
            Browse Products
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-white">Premium Shopping Cart</h2>
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-400">
            {cartItems.length} item{cartItems.length !== 1 ? 's' : ''}
          </span>
          <button
            onClick={clearCart}
            className="text-red-400 hover:text-red-300 text-sm transition-colors"
          >
            Clear Cart
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {cartItems.map((item) => (
          <div key={item.id} className="bg-gray-700 rounded-lg p-4 flex items-center space-x-4">
            <img
              src={item.image}
              alt={item.name}
              className="w-16 h-16 object-cover rounded-md"
            />
            <div className="flex-1">
              <h3 className="text-white font-medium">{item.name}</h3>
              <p className="text-gray-400">${item.price.toFixed(2)}</p>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => updateQuantity(item.id, item.quantity - 1)}
                className="w-8 h-8 bg-gray-600 hover:bg-gray-500 text-white rounded-md flex items-center justify-center transition-colors"
              >
                -
              </button>
              <span className="text-white w-12 text-center">{item.quantity}</span>
              <button
                onClick={() => updateQuantity(item.id, item.quantity + 1)}
                className="w-8 h-8 bg-gray-600 hover:bg-gray-500 text-white rounded-md flex items-center justify-center transition-colors"
              >
                +
              </button>
            </div>
            <div className="text-right">
              <p className="text-white font-medium">${(item.price * item.quantity).toFixed(2)}</p>
              <button
                onClick={() => removeItem(item.id)}
                className="text-red-400 hover:text-red-300 text-sm transition-colors"
              >
                Remove
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-gray-700 rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <span className="text-gray-300">Subtotal:</span>
          <span className="text-white font-medium">${getTotalPrice().toFixed(2)}</span>
        </div>
        <div className="flex justify-between items-center mb-4">
          <span className="text-gray-300">Premium Discount (10%):</span>
          <span className="text-green-400">-${(getTotalPrice() * 0.1).toFixed(2)}</span>
        </div>
        <div className="border-t border-gray-600 pt-4">
          <div className="flex justify-between items-center mb-6">
            <span className="text-white font-semibold text-lg">Total:</span>
            <span className="text-white font-bold text-xl">
              ${(getTotalPrice() * 0.9).toFixed(2)}
            </span>
          </div>
          <button
            onClick={handleCheckout}
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white py-3 px-6 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Processing...' : 'Proceed to Checkout'}
          </button>
        </div>
      </div>

      <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-4">
        <div className="flex items-center space-x-2 mb-2">
          <span className="text-blue-400">👑</span>
          <span className="text-blue-400 font-medium">Premium Benefits</span>
        </div>
        <ul className="text-sm text-gray-300 space-y-1">
          <li>• 10% discount on all purchases</li>
          <li>• Priority customer support</li>
          <li>• Exclusive product access</li>
          <li>• Free shipping on orders over $50</li>
        </ul>
      </div>
    </div>
  )
} 