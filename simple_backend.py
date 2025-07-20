from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Ecommerce API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Ecommerce API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ecommerce-api"}

@app.get("/api/products")
async def get_products():
    return {
        "products": [
            {"id": 1, "name": "Sample Product 1", "price": 29.99},
            {"id": 2, "name": "Sample Product 2", "price": 49.99},
            {"id": 3, "name": "Sample Product 3", "price": 79.99},
        ]
    }

@app.get("/api/users/me")
async def get_current_user():
    # Mock premium user for testing
    return {
        "id": 1,
        "email": "premium@example.com",
        "username": "premiumuser",
        "first_name": "Premium",
        "last_name": "User",
        "phone": "+1234567890",
        "role": "customer",
        "is_active": True,
        "is_verified": True,
        "is_premium": True,
        "premium_expires_at": "2025-12-31T23:59:59Z"
    }

@app.post("/api/orders")
async def create_order():
    return {
        "id": 1,
        "order_number": "ORD-2025-001",
        "total_amount": 89.97,
        "status": "pending",
        "created_at": "2025-01-01T12:00:00Z"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001) 