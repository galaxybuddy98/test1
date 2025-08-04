const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ServiceInfo {
  id: string;
  name: string;
  url: string;
  port: number;
  status: string;
  last_heartbeat: string;
  metadata?: Record<string, any>;
}

export interface HealthResponse {
  status: string;
  gateway: string;
  active_services: number;
  total_services: number;
  timestamp: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

export interface Order {
  id: string;
  user_id: string;
  product_id: string;
  quantity: number;
  total_price: number;
  status: string;
  created_at: string;
}

export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  stock: number;
  created_at: string;
}

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Gateway Health Check
  async getHealth(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/health');
  }

  // Service Discovery
  async getServices(): Promise<ServiceInfo[]> {
    return this.request<ServiceInfo[]>('/discovery/services');
  }

  async registerService(serviceInfo: Omit<ServiceInfo, 'id' | 'last_heartbeat'>): Promise<ServiceInfo> {
    return this.request<ServiceInfo>('/discovery/register', {
      method: 'POST',
      body: JSON.stringify(serviceInfo),
    });
  }

  // User Service
  async getUsers(): Promise<User[]> {
    return this.request<User[]>('/api/users/users');
  }

  async getUser(id: string): Promise<User> {
    return this.request<User>(`/api/users/users/${id}`);
  }

  async createUser(userData: Omit<User, 'id' | 'created_at'>): Promise<User> {
    return this.request<User>('/api/users/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async updateUser(id: string, userData: Partial<User>): Promise<User> {
    return this.request<User>(`/api/users/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  async deleteUser(id: string): Promise<void> {
    return this.request<void>(`/api/users/users/${id}`, {
      method: 'DELETE',
    });
  }

  // Order Service
  async getOrders(): Promise<Order[]> {
    return this.request<Order[]>('/api/orders/orders');
  }

  async getOrder(id: string): Promise<Order> {
    return this.request<Order>(`/api/orders/orders/${id}`);
  }

  async createOrder(orderData: Omit<Order, 'id' | 'created_at'>): Promise<Order> {
    return this.request<Order>('/api/orders/orders', {
      method: 'POST',
      body: JSON.stringify(orderData),
    });
  }

  async updateOrder(id: string, orderData: Partial<Order>): Promise<Order> {
    return this.request<Order>(`/api/orders/orders/${id}`, {
      method: 'PUT',
      body: JSON.stringify(orderData),
    });
  }

  async deleteOrder(id: string): Promise<void> {
    return this.request<void>(`/api/orders/orders/${id}`, {
      method: 'DELETE',
    });
  }

  // Product Service
  async getProducts(): Promise<Product[]> {
    return this.request<Product[]>('/api/products/products');
  }

  async getProduct(id: string): Promise<Product> {
    return this.request<Product>(`/api/products/products/${id}`);
  }

  async createProduct(productData: Omit<Product, 'id' | 'created_at'>): Promise<Product> {
    return this.request<Product>('/api/products/products', {
      method: 'POST',
      body: JSON.stringify(productData),
    });
  }

  async updateProduct(id: string, productData: Partial<Product>): Promise<Product> {
    return this.request<Product>(`/api/products/products/${id}`, {
      method: 'PUT',
      body: JSON.stringify(productData),
    });
  }

  async deleteProduct(id: string): Promise<void> {
    return this.request<void>(`/api/products/products/${id}`, {
      method: 'DELETE',
    });
  }
}

export const apiService = new ApiService(); 