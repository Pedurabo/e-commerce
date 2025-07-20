import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react'
import toast from 'react-hot-toast'

// Types
interface User {
  id: number
  email: string
  username: string
  first_name: string
  last_name: string
  phone?: string
  role: 'customer' | 'admin'
  is_active: boolean
  is_verified: boolean
  is_premium: boolean
  premium_expires_at?: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  isAdmin: boolean
}

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<boolean>
  register: (userData: RegisterData) => Promise<boolean>
  loginWithGoogle: () => Promise<boolean>
  loginWithFacebook: () => Promise<boolean>
  logout: () => void
  refreshToken: () => Promise<void>
  hasPremiumAccess: () => boolean
}

interface RegisterData {
  email: string
  username: string
  password: string
  first_name: string
  last_name: string
  phone?: string
}

// Action types
type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: { user: User; token: string } }
  | { type: 'LOGIN_FAILURE' }
  | { type: 'LOGOUT' }
  | { type: 'REGISTER_START' }
  | { type: 'REGISTER_SUCCESS'; payload: { user: User; token: string } }
  | { type: 'REGISTER_FAILURE' }
  | { type: 'REFRESH_TOKEN'; payload: { user: User; token: string } }

// Initial state
const initialState: AuthState = {
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: false,
  isLoading: true,
  isAdmin: false,
}

// Reducer
function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'LOGIN_START':
    case 'REGISTER_START':
      return { ...state, isLoading: true }
    
    case 'LOGIN_SUCCESS':
    case 'REGISTER_SUCCESS':
    case 'REFRESH_TOKEN':
      localStorage.setItem('token', action.payload.token)
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        isLoading: false,
        isAdmin: action.payload.user.role === 'admin',
      }
    
    case 'LOGIN_FAILURE':
    case 'REGISTER_FAILURE':
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        isAdmin: false,
      }
    
    case 'LOGOUT':
      localStorage.removeItem('token')
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        isAdmin: false,
      }
    
    default:
      return state
  }
}

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined)

// Provider component
export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, initialState)

  // Check token validity on mount
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token')
      if (token) {
        try {
          const response = await fetch('http://localhost:8000/api/v1/users/me', {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          })
          
          if (response.ok) {
            const user = await response.json()
            dispatch({
              type: 'REFRESH_TOKEN',
              payload: { user, token },
            })
          } else {
            localStorage.removeItem('token')
            dispatch({ type: 'LOGOUT' })
          }
        } catch (error) {
          console.error('Auth check failed:', error)
          localStorage.removeItem('token')
          dispatch({ type: 'LOGOUT' })
        }
      } else {
        dispatch({ type: 'LOGOUT' })
      }
    }

    checkAuth()
  }, [])

  // Login function
  const login = async (email: string, password: string): Promise<boolean> => {
    dispatch({ type: 'LOGIN_START' })
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      if (response.ok) {
        const data = await response.json()
        
        // Get user profile
        const userResponse = await fetch('http://localhost:8000/api/v1/users/me', {
          headers: {
            'Authorization': `Bearer ${data.access_token}`,
            'Content-Type': 'application/json',
          },
        })
        
        if (userResponse.ok) {
          const user = await userResponse.json()
          dispatch({
            type: 'LOGIN_SUCCESS',
            payload: { user, token: data.access_token },
          })
          toast.success(`Welcome back, ${user.first_name}!`)
          return true
        }
      } else {
        const error = await response.json()
        toast.error(error.detail || 'Login failed')
      }
    } catch (error) {
      console.error('Login error:', error)
      toast.error('Network error. Please try again.')
    }
    
    dispatch({ type: 'LOGIN_FAILURE' })
    return false
  }

  // Register function
  const register = async (userData: RegisterData): Promise<boolean> => {
    dispatch({ type: 'REGISTER_START' })
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/users/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      })

      if (response.ok) {
        const user = await response.json()
        
        // Don't auto-login after registration, let the registration page handle the flow
        dispatch({ type: 'REGISTER_SUCCESS', payload: { user, token: '' } })
        return true
      } else {
        const error = await response.json()
        toast.error(error.detail || 'Registration failed')
      }
    } catch (error) {
      console.error('Registration error:', error)
      toast.error('Network error. Please try again.')
    }
    
    dispatch({ type: 'REGISTER_FAILURE' })
    return false
  }

  // Logout function
  const logout = () => {
    dispatch({ type: 'LOGOUT' })
    toast.success('Logged out successfully')
  }

  // Refresh token function
  const refreshToken = async () => {
    const token = localStorage.getItem('token')
    if (!token) return

    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/refresh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: token }),
      })

      if (response.ok) {
        const data = await response.json()
        const userResponse = await fetch('http://localhost:8000/api/v1/users/me', {
          headers: {
            'Authorization': `Bearer ${data.access_token}`,
            'Content-Type': 'application/json',
          },
        })
        
        if (userResponse.ok) {
          const user = await userResponse.json()
          dispatch({
            type: 'REFRESH_TOKEN',
            payload: { user, token: data.access_token },
          })
        }
      }
    } catch (error) {
      console.error('Token refresh failed:', error)
      logout()
    }
  }

  // OAuth login functions
  const loginWithGoogle = async (): Promise<boolean> => {
    dispatch({ type: 'LOGIN_START' })
    
    try {
      // Open Google OAuth popup
      const popup = window.open(
        `https://accounts.google.com/o/oauth2/v2/auth?client_id=your-actual-google-client-id.apps.googleusercontent.com&redirect_uri=${encodeURIComponent('http://localhost:3003/auth/google/callback')}&scope=${encodeURIComponent('email profile')}&response_type=code&access_type=offline&prompt=consent`,
        'google-oauth',
        'width=500,height=600,scrollbars=yes,resizable=yes'
      )

      // Listen for the OAuth callback
      const handleMessage = async (event: MessageEvent) => {
        if (event.origin !== window.location.origin) return
        
        if (event.data.type === 'GOOGLE_OAUTH_SUCCESS' && event.data.code) {
          window.removeEventListener('message', handleMessage)
          popup?.close()
          
          // Send code to backend
          const response = await fetch('http://localhost:8000/api/v1/auth/google', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
              code: event.data.code, 
              redirect_uri: 'http://localhost:3003/auth/google/callback' 
            }),
          })

          if (response.ok) {
            const data = await response.json()
            
            // Get user profile
            const userResponse = await fetch('http://localhost:8000/api/v1/users/me', {
              headers: {
                'Authorization': `Bearer ${data.access_token}`,
                'Content-Type': 'application/json',
              },
            })
            
            if (userResponse.ok) {
              const user = await userResponse.json()
              dispatch({
                type: 'LOGIN_SUCCESS',
                payload: { user, token: data.access_token },
              })
              toast.success(`Welcome back, ${user.first_name}!`)
              return true
            }
          } else {
            const error = await response.json()
            toast.error(error.detail || 'Google login failed')
          }
        } else if (event.data.type === 'GOOGLE_OAUTH_ERROR') {
          window.removeEventListener('message', handleMessage)
          popup?.close()
          toast.error('Google login was cancelled or failed')
        }
      }

      window.addEventListener('message', handleMessage)
      
      // Handle popup closed
      const checkClosed = setInterval(() => {
        if (popup?.closed) {
          clearInterval(checkClosed)
          window.removeEventListener('message', handleMessage)
          dispatch({ type: 'LOGIN_FAILURE' })
        }
      }, 1000)
      
    } catch (error) {
      console.error('Google login error:', error)
      toast.error('Network error during Google login')
    }
    
    dispatch({ type: 'LOGIN_FAILURE' })
    return false
  }

  const loginWithFacebook = async (): Promise<boolean> => {
    dispatch({ type: 'LOGIN_START' })
    
    try {
      // Open Facebook OAuth popup
      const popup = window.open(
        `https://www.facebook.com/v12.0/dialog/oauth?client_id=your-facebook-app-id&redirect_uri=${encodeURIComponent('http://localhost:3003/auth/facebook/callback')}&scope=${encodeURIComponent('email public_profile')}&response_type=code`,
        'facebook-oauth',
        'width=500,height=600,scrollbars=yes,resizable=yes'
      )

      // Listen for the OAuth callback
      const handleMessage = async (event: MessageEvent) => {
        if (event.origin !== window.location.origin) return
        
        if (event.data.type === 'FACEBOOK_OAUTH_SUCCESS' && event.data.code) {
          window.removeEventListener('message', handleMessage)
          popup?.close()
          
          // Send code to backend
          const response = await fetch('http://localhost:8000/api/v1/auth/facebook', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
              code: event.data.code, 
              redirect_uri: 'http://localhost:3003/auth/facebook/callback' 
            }),
          })

          if (response.ok) {
            const data = await response.json()
            
            // Get user profile
            const userResponse = await fetch('http://localhost:8000/api/v1/users/me', {
              headers: {
                'Authorization': `Bearer ${data.access_token}`,
                'Content-Type': 'application/json',
              },
            })
            
            if (userResponse.ok) {
              const user = await userResponse.json()
              dispatch({
                type: 'LOGIN_SUCCESS',
                payload: { user, token: data.access_token },
              })
              toast.success(`Welcome back, ${user.first_name}!`)
              return true
            }
          } else {
            const error = await response.json()
            toast.error(error.detail || 'Facebook login failed')
          }
        } else if (event.data.type === 'FACEBOOK_OAUTH_ERROR') {
          window.removeEventListener('message', handleMessage)
          popup?.close()
          toast.error('Facebook login was cancelled or failed')
        }
      }

      window.addEventListener('message', handleMessage)
      
      // Handle popup closed
      const checkClosed = setInterval(() => {
        if (popup?.closed) {
          clearInterval(checkClosed)
          window.removeEventListener('message', handleMessage)
          dispatch({ type: 'LOGIN_FAILURE' })
        }
      }, 1000)
      
    } catch (error) {
      console.error('Facebook login error:', error)
      toast.error('Network error during Facebook login')
    }
    
    dispatch({ type: 'LOGIN_FAILURE' })
    return false
  }

  const hasPremiumAccess = (): boolean => {
    if (!state.user) return false
    
    // Admin always has premium access
    if (state.user.role === 'admin') return true
    
    // Check if user has premium access
    if (!state.user.is_premium) return false
    
    // Check if premium hasn't expired
    if (state.user.premium_expires_at) {
      const expiryDate = new Date(state.user.premium_expires_at)
      const now = new Date()
      return expiryDate > now
    }
    
    return state.user.is_premium
  }

  const value: AuthContextType = {
    ...state,
    login,
    register,
    loginWithGoogle,
    loginWithFacebook,
    logout,
    refreshToken,
    hasPremiumAccess,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// Hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
} 