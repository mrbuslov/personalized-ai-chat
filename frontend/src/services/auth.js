import { apiService } from './api';

class AuthService {
  constructor() {
    this.currentUser = null;
    this.isAuthenticated = false;
    this.listeners = [];
  }

  subscribe(listener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  notify() {
    this.listeners.forEach(listener => listener(this.isAuthenticated, this.currentUser));
  }

  async login(email, password) {
    try {
      const tokens = await apiService.login(email, password);
      
      localStorage.setItem('access_token', tokens.access_token);
      localStorage.setItem('refresh_token', tokens.refresh_token);
      
      await this.loadCurrentUser();
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      };
    }
  }

  async register(email, password, name, companyName) {
    try {
      const user = await apiService.register(email, password, name, companyName);
      
      // Auto-login after registration
      const loginResult = await this.login(email, password);
      if (loginResult.success) {
        return { success: true, user };
      } else {
        return { success: false, error: 'Registration successful but login failed' };
      }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed' 
      };
    }
  }

  async loadCurrentUser() {
    try {
      const user = await apiService.getCurrentUser();
      this.currentUser = user;
      this.isAuthenticated = true;
      this.notify();
      return user;
    } catch (error) {
      this.currentUser = null;
      this.isAuthenticated = false;
      this.notify();
      throw error;
    }
  }

  async logout() {
    try {
      await apiService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.currentUser = null;
      this.isAuthenticated = false;
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      this.notify();
    }
  }

  async checkAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) {
      this.isAuthenticated = false;
      this.currentUser = null;
      this.notify();
      return false;
    }

    try {
      await this.loadCurrentUser();
      return true;
    } catch (error) {
      this.isAuthenticated = false;
      this.currentUser = null;
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      this.notify();
      return false;
    }
  }

  getCurrentUser() {
    return this.currentUser;
  }

  getIsAuthenticated() {
    return this.isAuthenticated;
  }
}

export const authService = new AuthService();