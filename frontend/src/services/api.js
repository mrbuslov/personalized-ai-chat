import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_FRONTEND_API_BASE_URL;

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': 'true',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Response interceptor to handle token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const original = error.config;
        
        // Don't retry if it's the refresh endpoint itself or already retried
        if (error.response?.status === 401 && !original._retry && !original.url?.includes('/auth/refresh')) {
          original._retry = true;
          
          try {
            const refreshToken = localStorage.getItem('refresh_token');
            
            if (!refreshToken) {
              // No refresh token available, redirect to login
              localStorage.removeItem('access_token');
              localStorage.removeItem('refresh_token');
              window.location.href = '/login';
              return Promise.reject(error);
            }
            
            // Use axios directly to avoid interceptor loop
            const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
              refresh_token: refreshToken,
            });
            
            const { access_token, refresh_token } = response.data;
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('refresh_token', refresh_token);
            
            // Update the failed request with new token
            original.headers.Authorization = `Bearer ${access_token}`;
            
            return this.client(original);
          } catch (refreshError) {
            // Refresh failed, clear tokens and redirect
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }
        
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(email, password) {
    const response = await this.client.post('/auth/login', { email, password });
    return response.data;
  }

  async register(email, password, name, companyName) {
    const response = await this.client.post('/auth/register', {
      email,
      password,
      name,
      company_name: companyName,
    });
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  async logout() {
    await this.client.post('/auth/logout');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // Chat endpoints
  async getChats(page = 1, pageSize = 20) {
    const response = await this.client.get(`/chats/?page=${page}&page_size=${pageSize}`);
    return response.data;
  }

  async getChat(chatId) {
    const response = await this.client.get(`/chats/${chatId}`);
    return response.data;
  }

  async getChatWithMessages(chatId) {
    const response = await this.client.get(`/chats/${chatId}/with-messages`);
    return response.data;
  }

  async createChat(name, clientDescription = '', specialInstructions = '') {
    const response = await this.client.post('/chats/', {
      name,
    });
    
    // If we have client description or special instructions, create AI config
    if (clientDescription || specialInstructions) {
      await this.updateChatAIConfig(response.data.id, clientDescription, specialInstructions);
    }
    
    return response.data;
  }

  async updateChat(chatId, data) {
    const response = await this.client.put(`/chats/${chatId}`, data);
    return response.data;
  }

  async deleteChat(chatId) {
    await this.client.delete(`/chats/${chatId}`);
  }

  async getChatMessages(chatId, page = 1, pageSize = 50) {
    const response = await this.client.get(`/chats/${chatId}/messages?page=${page}&page_size=${pageSize}`);
    return response.data;
  }

  // Message endpoints
  async createMessage(chatId, content, role) {
    const response = await this.client.post('/messages/', {
      chat_id: chatId,
      content,
      role,
    });
    return response.data;
  }

  async updateMessage(messageId, content) {
    const response = await this.client.put(`/messages/${messageId}`, { content });
    return response.data;
  }

  async deleteMessage(messageId) {
    await this.client.delete(`/messages/${messageId}`);
  }

  async generateAIResponse(chatId, contextCount = 10) {
    const response = await this.client.post('/messages/generate-ai-response', {
      chat_id: chatId,
      context_messages_count: contextCount,
    });
    return response.data;
  }

  async reviseMessageWithAI(messageId, revisionInstructions) {
    const response = await this.client.post('/messages/revise-with-ai', {
      message_id: messageId,
      revision_instructions: revisionInstructions,
    });
    return response.data;
  }

  async importMessages(chatId, messages) {
    const response = await this.client.post('/messages/import', {
      chat_id: chatId,
      messages,
    });
    return response.data;
  }

  // AI Configuration endpoints
  async getGlobalAIConfig() {
    const response = await this.client.get('/ai-config/global');
    return response.data;
  }

  async getChatAIConfig(chatId) {
    const response = await this.client.get(`/ai-config/chat/${chatId}`);
    return response.data;
  }

  async updateGlobalAIConfig(clientDescription = '', specialInstructions = '') {
    const response = await this.client.put('/ai-config/global', {
      client_description: clientDescription,
      special_instructions: specialInstructions,
    });
    return response.data;
  }

  async updateChatAIConfig(chatId, clientDescription = '', specialInstructions = '') {
    const response = await this.client.put(`/ai-config/chat/${chatId}`, {
      client_description: clientDescription,
      special_instructions: specialInstructions,
    });
    return response.data;
  }
}

export const apiService = new ApiService();
