/**
 * ML Products Service - Handles interactions with ML-powered product endpoints
 */

export interface MLProduct {
  id: number;
  name: string;
  description: string;
  short_description: string;
  price: number;
  original_price: number;
  category: string;
  subcategory: string;
  brand: string;
  rating: number;
  reviews: number;
  stock_quantity: number;
  is_featured: boolean;
  is_bestseller: boolean;
  is_new: boolean;
  is_on_sale: boolean;
  discount_percentage: number;
  tags: string[];
  images: string[];
  features: string[];
  specifications: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface ProductRecommendation {
  product: MLProduct;
  score: number;
  reason: string;
}

export interface UserSegment {
  user_count: number;
  avg_purchases: number;
  avg_order_value: number;
  user_ids: number[];
}

export interface DemandTrend {
  trend_direction: 'increasing' | 'decreasing';
  trend_strength: number;
  total_sales: number;
  avg_daily_sales: number;
}

export interface PaginationInfo {
  page: number;
  limit: number;
  total: number;
  pages: number;
}

export interface LimitlessProductsResponse {
  products: MLProduct[];
  pagination: PaginationInfo;
}

export interface UserSegmentsResponse {
  user_segments: Record<string, UserSegment>;
  total_users: number;
}

export interface DemandTrendsResponse {
  demand_trends: Record<string, DemandTrend>;
  analysis_date: string;
}

class MLProductsService {
  private baseUrl = 'http://localhost:8000/api/v1/ml';

  /**
   * Get limitless products with advanced filtering
   */
  async getLimitlessProducts(params: {
    page?: number;
    limit?: number;
    category?: string;
    search?: string;
    sort_by?: string;
    sort_order?: 'asc' | 'desc';
  } = {}): Promise<LimitlessProductsResponse> {
    const searchParams = new URLSearchParams();
    
    if (params.page) searchParams.append('page', params.page.toString());
    if (params.limit) searchParams.append('limit', params.limit.toString());
    if (params.category) searchParams.append('category', params.category);
    if (params.search) searchParams.append('search', params.search);
    if (params.sort_by) searchParams.append('sort_by', params.sort_by);
    if (params.sort_order) searchParams.append('sort_order', params.sort_order);

    const response = await fetch(`${this.baseUrl}/products/limitless?${searchParams}`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch limitless products: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Generate new products using ML
   */
  async generateProducts(count: number = 100, category?: string): Promise<{
    message: string;
    products_count: number;
    category?: string;
  }> {
    const response = await fetch(`${this.baseUrl}/generate-products`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ count, category }),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate products: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Optimize product prices using ML
   */
  async optimizePrices(): Promise<{
    message: string;
    updated_count: number;
  }> {
    const response = await fetch(`${this.baseUrl}/products/optimize-prices`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to optimize prices: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get personalized recommendations for a user
   */
  async getPersonalizedRecommendations(
    userId: number,
    limit: number = 10
  ): Promise<{
    user_id: number;
    recommendations: ProductRecommendation[];
  }> {
    const response = await fetch(
      `${this.baseUrl}/products/recommendations/${userId}?limit=${limit}`
    );

    if (!response.ok) {
      throw new Error(`Failed to get recommendations: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Analyze user behavior and create segments
   */
  async analyzeUserSegments(): Promise<UserSegmentsResponse> {
    const response = await fetch(`${this.baseUrl}/analytics/user-segments`);

    if (!response.ok) {
      throw new Error(`Failed to analyze user segments: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get demand trends and predictions
   */
  async getDemandTrends(): Promise<DemandTrendsResponse> {
    const response = await fetch(`${this.baseUrl}/analytics/demand-trends`);

    if (!response.ok) {
      throw new Error(`Failed to get demand trends: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Save ML models
   */
  async saveModels(): Promise<{ message: string }> {
    const response = await fetch(`${this.baseUrl}/models/save`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error(`Failed to save models: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Load ML models
   */
  async loadModels(): Promise<{ message: string }> {
    const response = await fetch(`${this.baseUrl}/models/load`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error(`Failed to load models: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Search products with ML-powered relevance
   */
  async searchProducts(query: string, filters: {
    category?: string;
    price_min?: number;
    price_max?: number;
    rating_min?: number;
    brand?: string;
  } = {}): Promise<LimitlessProductsResponse> {
    const searchParams = new URLSearchParams();
    searchParams.append('search', query);
    
    if (filters.category) searchParams.append('category', filters.category);
    if (filters.price_min) searchParams.append('price_min', filters.price_min.toString());
    if (filters.price_max) searchParams.append('price_max', filters.price_max.toString());
    if (filters.rating_min) searchParams.append('rating_min', filters.rating_min.toString());
    if (filters.brand) searchParams.append('brand', filters.brand);

    const response = await fetch(`${this.baseUrl}/products/limitless?${searchParams}`);
    
    if (!response.ok) {
      throw new Error(`Failed to search products: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get trending products based on ML analysis
   */
  async getTrendingProducts(limit: number = 20): Promise<MLProduct[]> {
    const response = await fetch(
      `${this.baseUrl}/products/limitless?sort_by=reviews&sort_order=desc&limit=${limit}`
    );

    if (!response.ok) {
      throw new Error(`Failed to get trending products: ${response.statusText}`);
    }

    const data = await response.json();
    return data.products;
  }

  /**
   * Get products by category with ML-powered sorting
   */
  async getProductsByCategory(
    category: string,
    page: number = 1,
    limit: number = 50
  ): Promise<LimitlessProductsResponse> {
    return this.getLimitlessProducts({
      category,
      page,
      limit,
      sort_by: 'rating',
      sort_order: 'desc'
    });
  }

  /**
   * Get featured products with ML optimization
   */
  async getFeaturedProducts(limit: number = 12): Promise<MLProduct[]> {
    const response = await fetch(
      `${this.baseUrl}/products/limitless?limit=${limit}&sort_by=rating&sort_order=desc`
    );

    if (!response.ok) {
      throw new Error(`Failed to get featured products: ${response.statusText}`);
    }

    const data = await response.json();
    return data.products.filter((product: MLProduct) => product.is_featured);
  }
}

// Export singleton instance
export const mlProductsService = new MLProductsService();
export default mlProductsService; 