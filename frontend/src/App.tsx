import React, { Suspense } from 'react'
import { Outlet } from 'react-router-dom'
import { CartProvider } from './components/ui/CartProvider'
import CartSidebar from './components/ui/CartSidebar'
import Layout from './components/layout/Layout'
import LoadingSpinner from './components/ui/LoadingSpinner'

const App = () => {
  return (
    <CartProvider>
      <div className="min-h-screen bg-gray-900">
        <Layout>
          <Suspense fallback={
            <div className="flex items-center justify-center min-h-screen">
              <LoadingSpinner size="lg" />
            </div>
          }>
            <Outlet />
          </Suspense>
        </Layout>
        <CartSidebar />
      </div>
    </CartProvider>
  )
}

export default App 