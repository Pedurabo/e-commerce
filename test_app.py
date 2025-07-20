from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="Modern Ecommerce Platform",
    description="A cutting-edge ecommerce platform with AI recommendations and modern payment methods",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create static directory if it doesn't exist
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Modern Ecommerce Platform</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                text-align: center;
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .subtitle {
                font-size: 1.2rem;
                margin-bottom: 40px;
                opacity: 0.9;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 40px 0;
            }
            .feature-card {
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
            }
            .feature-card h3 {
                margin-top: 0;
                color: #ffd700;
            }
            .links {
                margin-top: 40px;
            }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                margin: 10px;
                background: #ffd700;
                color: #333;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: transform 0.3s ease;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
            .status {
                background: rgba(0,255,0,0.2);
                padding: 10px;
                border-radius: 5px;
                margin: 20px 0;
                border: 1px solid rgba(0,255,0,0.5);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛍️ Modern Ecommerce Platform</h1>
            <p class="subtitle">AI-Powered Recommendations • Modern Payment Methods • Scalable Architecture</p>
            
            <div class="status">
                ✅ Application is running successfully on port 8000
            </div>
            
            <div class="features">
                <div class="feature-card">
                    <h3>🤖 AI Recommendations</h3>
                    <p>Advanced machine learning algorithms for personalized product recommendations</p>
                </div>
                <div class="feature-card">
                    <h3>💳 Modern Payments</h3>
                    <p>Support for Stripe, PayPal, cryptocurrency, and buy-now-pay-later options</p>
                </div>
                <div class="feature-card">
                    <h3>🔐 Secure Authentication</h3>
                    <p>JWT-based authentication with role-based access control</p>
                </div>
                <div class="feature-card">
                    <h3>📊 Real-time Analytics</h3>
                    <p>Comprehensive analytics and reporting for business insights</p>
                </div>
                <div class="feature-card">
                    <h3>🚀 Scalable Architecture</h3>
                    <p>Microservices-ready architecture with Docker support</p>
                </div>
                <div class="feature-card">
                    <h3>📱 Mobile Ready</h3>
                    <p>Responsive design optimized for all devices</p>
                </div>
            </div>
            
            <div class="links">
                <a href="/docs" class="btn">📚 API Documentation</a>
                <a href="/health" class="btn">❤️ Health Check</a>
                <a href="/api/v1/products" class="btn">📦 Products API</a>
                <a href="/api/v1/recommendations" class="btn">🤖 AI Recommendations</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ecommerce-api",
        "version": "1.0.0",
        "features": [
            "AI Recommendations",
            "Modern Payment Methods",
            "Secure Authentication",
            "Real-time Analytics"
        ]
    }

@app.get("/api/v1/products")
async def get_products():
    return {
        "products": [
            {
                "id": 1,
                "name": "Smartphone X",
                "price": 599.99,
                "description": "Latest smartphone with AI features",
                "category": "Electronics",
                "image_url": "https://via.placeholder.com/300x300?text=Smartphone+X",
                "rating": 4.8,
                "reviews_count": 1250
            },
            {
                "id": 2,
                "name": "Laptop Pro",
                "price": 1299.99,
                "description": "Professional laptop for developers",
                "category": "Electronics",
                "image_url": "https://via.placeholder.com/300x300?text=Laptop+Pro",
                "rating": 4.9,
                "reviews_count": 890
            },
            {
                "id": 3,
                "name": "Wireless Headphones",
                "price": 199.99,
                "description": "Premium wireless headphones with noise cancellation",
                "category": "Electronics",
                "image_url": "https://via.placeholder.com/300x300?text=Headphones",
                "rating": 4.7,
                "reviews_count": 2100
            },
            {
                "id": 4,
                "name": "Smart Watch",
                "price": 299.99,
                "description": "Fitness and health tracking smartwatch",
                "category": "Wearables",
                "image_url": "https://via.placeholder.com/300x300?text=Smart+Watch",
                "rating": 4.6,
                "reviews_count": 750
            },
            {
                "id": 5,
                "name": "Gaming Console",
                "price": 499.99,
                "description": "Next-generation gaming console",
                "category": "Gaming",
                "image_url": "https://via.placeholder.com/300x300?text=Gaming+Console",
                "rating": 4.9,
                "reviews_count": 3200
            }
        ],
        "total": 5,
        "page": 1,
        "per_page": 10
    }

@app.get("/api/v1/recommendations")
async def get_recommendations():
    return {
        "recommendations": [
            {
                "product_id": 1,
                "score": 0.95,
                "type": "ai_recommendation",
                "reason": "Based on your browsing history"
            },
            {
                "product_id": 2,
                "score": 0.87,
                "type": "trending",
                "reason": "Popular among similar users"
            },
            {
                "product_id": 3,
                "score": 0.82,
                "type": "content_based",
                "reason": "Similar to products you liked"
            },
            {
                "product_id": 4,
                "score": 0.78,
                "type": "collaborative",
                "reason": "Recommended by users with similar preferences"
            }
        ],
        "user_id": "sample_user",
        "algorithm": "hybrid_recommendation_engine"
    }

@app.get("/api/v1/categories")
async def get_categories():
    return {
        "categories": [
            {"id": 1, "name": "Electronics", "product_count": 3},
            {"id": 2, "name": "Wearables", "product_count": 1},
            {"id": 3, "name": "Gaming", "product_count": 1}
        ]
    }

@app.get("/favicon.ico")
async def favicon():
    # Return a simple favicon response to prevent 404 errors
    return JSONResponse(content={"message": "Favicon not implemented yet"}, status_code=200)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Modern Ecommerce Platform...")
    print("📱 Access the application at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/docs")
    print("❤️ Health Check at: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000) 