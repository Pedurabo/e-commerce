import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

interface CartItem {
  id: number;
  product_id: number;
  quantity: number;
  product: {
    id: number;
    name: string;
    price: number;
    image_url: string;
  };
}

interface CartContextType {
  items: CartItem[];
  addToCart: (productId: number, quantity: number) => Promise<void>;
  removeFromCart: (itemId: number) => Promise<void>;
  updateQuantity: (itemId: number, quantity: number) => Promise<void>;
  clearCart: () => Promise<void>;
  getCartTotal: () => number;
  getItemCount: () => number;
  isLoading: boolean;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const useCart = () => {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};

interface CartProviderProps {
  children: ReactNode;
}

export const CartProvider: React.FC<CartProviderProps> = ({ children }) => {
  const [items, setItems] = useState<CartItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchCart = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get('/api/v1/cart/');
      setItems(response.data.items || []);
      console.log('🛒 Cart loaded successfully:', response.data.items?.length || 0, 'items');
    } catch (error) {
      console.error('❌ Failed to fetch cart:', error);
      // Don't show alert for fetch errors as they might be expected when not logged in
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const addToCart = async (productId: number, quantity: number) => {
    try {
      const response = await axios.post('/api/v1/cart/add', {
        product_id: productId,
        quantity: quantity
      });
      
      // Refresh cart after adding item
      await fetchCart();
      
      // Show success message
      console.log('✅ Item added to cart successfully!');
    } catch (error) {
      console.error('❌ Failed to add to cart:', error);
      // Show user-friendly error message
      alert('Failed to add item to cart. Please try again.');
      throw error;
    }
  };

  const removeFromCart = async (itemId: number) => {
    try {
      await axios.delete(`/api/v1/cart/items/${itemId}`);
      setItems(items.filter(item => item.id !== itemId));
    } catch (error) {
      console.error('Failed to remove from cart:', error);
      throw error;
    }
  };

  const updateQuantity = async (itemId: number, quantity: number) => {
    try {
      await axios.put(`/api/v1/cart/items/${itemId}`, { quantity });
      setItems(items.map(item => 
        item.id === itemId ? { ...item, quantity } : item
      ));
    } catch (error) {
      console.error('Failed to update quantity:', error);
      throw error;
    }
  };

  const clearCart = async () => {
    try {
      await axios.delete('/api/v1/cart/');
      setItems([]);
    } catch (error) {
      console.error('Failed to clear cart:', error);
      throw error;
    }
  };

  const getCartTotal = () => {
    return items.reduce((total, item) => total + (item.product.price * item.quantity), 0);
  };

  const getItemCount = () => {
    return items.reduce((count, item) => count + item.quantity, 0);
  };

  return (
    <CartContext.Provider value={{
      items,
      addToCart,
      removeFromCart,
      updateQuantity,
      clearCart,
      getCartTotal,
      getItemCount,
      isLoading
    }}>
      {children}
    </CartContext.Provider>
  );
}; 