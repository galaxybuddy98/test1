import { create } from 'zustand';
import { apiService, User, Order, Product, ServiceInfo, HealthResponse } from '../services/api';

interface AppState {
  // Loading states
  isLoading: boolean;
  isHealthLoading: boolean;
  isServicesLoading: boolean;
  
  // Data states
  health: HealthResponse | null;
  services: ServiceInfo[];
  users: User[];
  orders: Order[];
  products: Product[];
  
  // Error states
  error: string | null;
  
  // Actions
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  
  // Health check
  fetchHealth: () => Promise<void>;
  
  // Service discovery
  fetchServices: () => Promise<void>;
  
  // User management
  fetchUsers: () => Promise<void>;
  createUser: (userData: Omit<User, 'id' | 'created_at'>) => Promise<void>;
  updateUser: (id: string, userData: Partial<User>) => Promise<void>;
  deleteUser: (id: string) => Promise<void>;
  
  // Order management
  fetchOrders: () => Promise<void>;
  createOrder: (orderData: Omit<Order, 'id' | 'created_at'>) => Promise<void>;
  updateOrder: (id: string, orderData: Partial<Order>) => Promise<void>;
  deleteOrder: (id: string) => Promise<void>;
  
  // Product management
  fetchProducts: () => Promise<void>;
  createProduct: (productData: Omit<Product, 'id' | 'created_at'>) => Promise<void>;
  updateProduct: (id: string, productData: Partial<Product>) => Promise<void>;
  deleteProduct: (id: string) => Promise<void>;
}

export const useStore = create<AppState>((set, get) => ({
  // Initial states
  isLoading: false,
  isHealthLoading: false,
  isServicesLoading: false,
  health: null,
  services: [],
  users: [],
  orders: [],
  products: [],
  error: null,
  
  // Basic actions
  setLoading: (loading: boolean) => set({ isLoading: loading }),
  setError: (error: string | null) => set({ error }),
  
  // Health check
  fetchHealth: async () => {
    set({ isHealthLoading: true, error: null });
    try {
      const health = await apiService.getHealth();
      set({ health, isHealthLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Health check failed', 
        isHealthLoading: false 
      });
    }
  },
  
  // Service discovery
  fetchServices: async () => {
    set({ isServicesLoading: true, error: null });
    try {
      const services = await apiService.getServices();
      set({ services, isServicesLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to fetch services', 
        isServicesLoading: false 
      });
    }
  },
  
  // User management
  fetchUsers: async () => {
    set({ isLoading: true, error: null });
    try {
      const users = await apiService.getUsers();
      set({ users, isLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to fetch users', 
        isLoading: false 
      });
    }
  },
  
  createUser: async (userData) => {
    set({ isLoading: true, error: null });
    try {
      await apiService.createUser(userData);
      await get().fetchUsers(); // Refresh users list
      set({ isLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to create user', 
        isLoading: false 
      });
    }
  },
  
  updateUser: async (id, userData) => {
    set({ isLoading: true, error: null });
    try {
      await apiService.updateUser(id, userData);
      await get().fetchUsers(); // Refresh users list
      set({ isLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to update user', 
        isLoading: false 
      });
    }
  },
  
  deleteUser: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await apiService.deleteUser(id);
      await get().fetchUsers(); // Refresh users list
      set({ isLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to delete user', 
        isLoading: false 
      });
    }
  },
  
  // Order management
  fetchOrders: async () => {
    set({ isLoading: true, error: null });
    try {
      const orders = await apiService.getOrders();
      set({ orders, isLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to fetch orders', 
        isLoading: false 
      });
    }
  },
  
  createOrder: async (orderData) => {
    set({ isLoading: true, error: null });
    try {
      await apiService.createOrder(orderData);
      await get().fetchOrders(); // Refresh orders list
      set({ isLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to create order', 
        isLoading: false 
      });
    }
  },
  
  updateOrder: async (id, orderData) => {
    set({ isLoading: true, error: null });
    try {
      await apiService.updateOrder(id, orderData);
      await get().fetchOrders(); // Refresh orders list
      set({ isLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to update order', 
        isLoading: false 
      });
    }
  },
  
  deleteOrder: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await apiService.deleteOrder(id);
      await get().fetchOrders(); // Refresh orders list
      set({ isLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to delete order', 
        isLoading: false 
      });
    }
  },
  
  // Product management
  fetchProducts: async () => {
    set({ isLoading: true, error: null });
    try {
      const products = await apiService.getProducts();
      set({ products, isLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to fetch products', 
        isLoading: false 
      });
    }
  },
  
  createProduct: async (productData) => {
    set({ isLoading: true, error: null });
    try {
      await apiService.createProduct(productData);
      await get().fetchProducts(); // Refresh products list
      set({ isLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to create product', 
        isLoading: false 
      });
    }
  },
  
  updateProduct: async (id, productData) => {
    set({ isLoading: true, error: null });
    try {
      await apiService.updateProduct(id, productData);
      await get().fetchProducts(); // Refresh products list
      set({ isLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to update product', 
        isLoading: false 
      });
    }
  },
  
  deleteProduct: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await apiService.deleteProduct(id);
      await get().fetchProducts(); // Refresh products list
      set({ isLoading: false });
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to delete product', 
        isLoading: false 
      });
    }
  },
})); 