import { Link } from 'react-router-dom'

const NotFoundPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full text-center">
        <div className="text-8xl mb-4">😕</div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Page not found</h1>
        <p className="text-lg text-gray-600 mb-8">
          Sorry, we couldn't find the page you're looking for. It might have been moved, deleted, or you entered the wrong URL.
        </p>
        
        <div className="space-y-4">
          <Link to="/" className="btn-primary w-full py-3 text-lg">
            Go back home
          </Link>
          <Link to="/products" className="btn-outline w-full py-3">
            Browse products
          </Link>
        </div>

        <div className="mt-8 text-sm text-gray-500">
          <p>Need help? <a href="/contact" className="text-primary-600 hover:text-primary-500">Contact our support team</a></p>
        </div>
      </div>
    </div>
  )
}

export default NotFoundPage 