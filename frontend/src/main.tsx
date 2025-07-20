import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'

import App from './App.tsx'
import HomePage from './pages/HomePage.tsx'
import LoginPage from './pages/LoginPage.tsx'
import RegisterPage from './pages/RegisterPage.tsx'
import ProductsPage from './pages/ProductsPage.tsx'
import ProductDetailPage from './pages/ProductDetailPage.tsx'
import CartPage from './pages/CartPage.tsx'
import DashboardPage from './pages/DashboardPage.tsx'
import UserAccountPage from './pages/UserAccountPage.tsx'
import NotFoundPage from './pages/NotFoundPage.tsx'
import OAuthCallbackPage from './pages/OAuthCallbackPage.tsx'
import { AuthProvider } from './contexts/AuthContext.tsx'
import ErrorBoundary from './components/ui/ErrorBoundary.tsx'
import './index.css'

// Development environment detection
const isDevelopment = process.env.NODE_ENV === 'development'

// Log development info
if (isDevelopment) {
  console.log('🔧 Development mode enabled')
  console.log('💡 Install React DevTools browser extension for better debugging:')
  console.log('   Chrome: https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi')
  console.log('   Firefox: https://addons.mozilla.org/en-US/firefox/addon/react-devtools/')
}

// Define routes
const routes = [
  {
    path: '/',
    element: <App />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: 'login',
        element: <LoginPage />,
      },
      {
        path: 'register',
        element: <RegisterPage />,
      },
      {
        path: 'products',
        children: [
          {
            index: true,
            element: <ProductsPage />,
          },
          {
            path: ':id',
            element: <ProductDetailPage />,
          },
        ],
      },
      {
        path: 'cart',
        element: <UserAccountPage />,
      },
      {
        path: 'dashboard',
        element: <DashboardPage />,
      },
      {
        path: 'account',
        element: <UserAccountPage />,
      },
      {
        path: 'auth/google/callback',
        element: <OAuthCallbackPage />,
      },
      {
        path: 'auth/facebook/callback',
        element: <OAuthCallbackPage />,
      },
      {
        path: '*',
        element: <NotFoundPage />,
      },
    ],
  },
]

// Create router
const router = createBrowserRouter(routes)

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <AuthProvider>
        <RouterProvider router={router} />
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#22c55e',
                secondary: '#fff',
              },
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </AuthProvider>
    </ErrorBoundary>
  </React.StrictMode>,
) 