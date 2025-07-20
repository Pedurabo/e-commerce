import React, { useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import LoadingSpinner from '../components/ui/LoadingSpinner'

const OAuthCallbackPage = () => {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()

  useEffect(() => {
    const code = searchParams.get('code')
    const error = searchParams.get('error')
    const state = searchParams.get('state')
    
    // Determine which OAuth provider this is for
    const pathname = window.location.pathname
    const provider = pathname.includes('google') ? 'google' : 'facebook'
    
    if (error) {
      // OAuth error occurred
      window.opener?.postMessage(
        { type: `${provider.toUpperCase()}_OAUTH_ERROR`, error },
        window.location.origin
      )
      window.close()
      return
    }
    
    if (code) {
      // OAuth success - send code back to parent window
      window.opener?.postMessage(
        { type: `${provider.toUpperCase()}_OAUTH_SUCCESS`, code, state },
        window.location.origin
      )
      window.close()
    } else {
      // No code or error - something went wrong
      window.opener?.postMessage(
        { type: `${provider.toUpperCase()}_OAUTH_ERROR`, error: 'No authorization code received' },
        window.location.origin
      )
      window.close()
    }
  }, [searchParams, navigate])

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center">
      <div className="text-center">
        <LoadingSpinner size="lg" />
        <p className="mt-4 text-gray-400">Completing authentication...</p>
      </div>
    </div>
  )
}

export default OAuthCallbackPage 