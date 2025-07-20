#!/usr/bin/env python3
"""
Script to generate limitless products using ML service.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ai.ml_service import MLService
from app.database import SessionLocal
from app.models.product import Product
from app.schemas.product import ProductCreate
import json

async def generate_and_store_products(count: int = 1000, category: str = None):
    """Generate and store products in the database."""
    ml_service = MLService()
    db = SessionLocal()
    
    try:
        print(f"Generating {count} products...")
        
        # Generate products in batches
        batch_size = 100
        total_generated = 0
        
        for i in range(0, count, batch_size):
            batch_count = min(batch_size, count - i)
            print(f"Generating batch {i//batch_size + 1} ({batch_count} products)...")
            
            # Generate products
            products = await ml_service.generate_limitless_products(batch_count)
            
            # Store in database
            for product_data in products:
                try:
                    # Check if product already exists
                    existing = db.query(Product).filter(Product.name == product_data["name"]).first()
                    if existing:
                        continue
                    
                    # Create product with proper field mapping
                    product_create = ProductCreate(
                        name=product_data["name"],
                        description=product_data["description"],
                        short_description=product_data["short_description"],
                        sku=f"SKU-{product_data['name'].replace(' ', '-').upper()}-{product_data['brand'].replace(' ', '-').upper()}",
                        price=product_data["price"],
                        sale_price=product_data["original_price"] if product_data["is_on_sale"] else None,
                        cost_price=product_data["price"] * 0.6,  # Assume 40% margin
                        stock_quantity=product_data["stock_quantity"],
                        weight=1.0,  # Default weight
                        dimensions="10x10x5 cm",  # Default dimensions
                        category_id=hash(product_data["category"]) % 1000 + 1,  # Generate category_id from category name
                        is_featured=product_data["is_featured"],
                        is_bestseller=product_data["is_bestseller"],
                        tags=", ".join(product_data["tags"]) if product_data["tags"] else "",
                        meta_title=product_data["name"],
                        meta_description=product_data["short_description"]
                    )
                    
                    db_product = Product(**product_create.model_dump())
                    db.add(db_product)
                    total_generated += 1
                    
                except Exception as e:
                    print(f"Error creating product {product_data['name']}: {e}")
                    continue
            
            # Commit batch
            db.commit()
            print(f"Batch {i//batch_size + 1} completed. Total generated: {total_generated}")
        
        print(f"Successfully generated {total_generated} products!")
        
        # Get statistics
        total_products = db.query(Product).count()
        categories = db.query(Product.category).distinct().all()
        
        print(f"\nDatabase Statistics:")
        print(f"Total products: {total_products}")
        print(f"Categories: {[cat[0] for cat in categories]}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

def export_products_to_json(filename: str = "generated_products.json"):
    """Export products to JSON file for frontend use."""
    db = SessionLocal()
    
    try:
        products = db.query(Product).all()
        
        products_data = []
        for product in products:
            products_data.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "short_description": product.short_description,
                "price": float(product.price),
                "original_price": float(product.original_price),
                "category": product.category,
                "subcategory": product.subcategory,
                "brand": product.brand,
                "rating": float(product.rating),
                "reviews": product.reviews,
                "stock_quantity": product.stock_quantity,
                "is_featured": product.is_featured,
                "is_bestseller": product.is_bestseller,
                "is_new": product.is_new,
                "is_on_sale": product.is_on_sale,
                "discount_percentage": product.discount_percentage,
                "tags": product.tags,
                "images": product.images,
                "features": product.features,
                "specifications": product.specifications,
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "updated_at": product.updated_at.isoformat() if product.updated_at else None
            })
        
        with open(filename, 'w') as f:
            json.dump(products_data, f, indent=2)
        
        print(f"Exported {len(products_data)} products to {filename}")
        
    except Exception as e:
        print(f"Error exporting products: {e}")
    finally:
        db.close()

async def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate limitless products using ML")
    parser.add_argument("--count", type=int, default=1000, help="Number of products to generate")
    parser.add_argument("--category", type=str, help="Specific category to generate")
    parser.add_argument("--export", action="store_true", help="Export products to JSON")
    parser.add_argument("--export-file", type=str, default="generated_products.json", help="Export filename")
    
    args = parser.parse_args()
    
    if args.export:
        export_products_to_json(args.export_file)
    else:
        await generate_and_store_products(args.count, args.category)

if __name__ == "__main__":
    asyncio.run(main()) 