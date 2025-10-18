import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Plus, MessageSquare, User, Settings, LogOut } from 'lucide-react';
import { apiService } from '../services/api';
import { authService } from '../services/auth';
import LoadingSpinner from '../components/LoadingSpinner';
import CreateChatModal from '../components/CreateChatModal';
import GlobalAIConfigModal from '../components/GlobalAIConfigModal';

const DashboardPage = ({ user }) => {
  const navigate = useNavigate();
  const [chats, setChats] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateChat, setShowCreateChat] = useState(false);
  const [showAIConfig, setShowAIConfig] = useState(false);

  const loadChats = async () => {
    try {
      setError('');
      const response = await apiService.getChats();
      setChats(response.chats);
    } catch (error) {
      setError('Failed to load chats');
      console.error('Error loading chats:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadChats();
  }, []);

  const handleCreateChat = async (name, clientDescription, specialInstructions) => {
    try {
      await apiService.createChat(name, clientDescription, specialInstructions);
      setShowCreateChat(false);
      loadChats(); // Reload chats
    } catch (error) {
      console.error('Error creating chat:', error);
      throw error;
    }
  };

  const handleDeleteChat = async (chatId) => {
    if (!confirm('Are you sure you want to delete this chat?')) {
      return;
    }

    try {
      await apiService.deleteChat(chatId);
      loadChats(); // Reload chats
    } catch (error) {
      console.error('Error deleting chat:', error);
      setError('Failed to delete chat');
    }
  };

  const handleLogout = async () => {
    await authService.logout();
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-gray-600">Welcome, {user?.name}</p>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowAIConfig(true)}
                className="btn-secondary flex items-center space-x-2"
              >
                <Settings className="w-4 h-4" />
                <span>AI Settings</span>
              </button>
              <button
                onClick={handleLogout}
                className="btn-secondary flex items-center space-x-2"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {/* Create Chat Button */}
        <div className="mb-8">
          <button
            onClick={() => setShowCreateChat(true)}
            className="btn-primary flex items-center space-x-2"
          >
            <Plus className="w-5 h-5" />
            <span>New Chat</span>
          </button>
        </div>

        {/* Chats List */}
        <div className="space-y-6">
          <h2 className="text-lg font-semibold text-gray-900">Your Chats</h2>
          
          {isLoading ? (
            <div className="flex justify-center py-12">
              <LoadingSpinner />
            </div>
          ) : chats.length === 0 ? (
            <div className="text-center py-12">
              <MessageSquare className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No chats yet</h3>
              <p className="text-gray-600 mb-6">Create your first chat to start simulating customer conversations.</p>
              <button
                onClick={() => setShowCreateChat(true)}
                className="btn-primary flex items-center space-x-2 mx-auto"
              >
                <Plus className="w-4 h-4" />
                <span>Create Chat</span>
              </button>
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {chats.map((chat) => (
                <div key={chat.id} className="card hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="text-lg font-medium text-gray-900 truncate flex-1">
                      {chat.name}
                    </h3>
                    <button
                      onClick={() => handleDeleteChat(chat.id)}
                      className="text-gray-400 hover:text-red-600 ml-2"
                      title="Delete chat"
                    >
                      ×
                    </button>
                  </div>
                  
                  {chat.client_description && (
                    <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                      {chat.client_description}
                    </p>
                  )}
                  
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span>Created {formatDate(chat.created_at)}</span>
                    <Link
                      to={`/chat/${chat.id}`}
                      className="text-primary-600 hover:text-primary-700 font-medium"
                    >
                      Open →
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Modals */}
      {showCreateChat && (
        <CreateChatModal
          onClose={() => setShowCreateChat(false)}
          onSubmit={handleCreateChat}
        />
      )}

      {showAIConfig && (
        <GlobalAIConfigModal
          onClose={() => setShowAIConfig(false)}
        />
      )}
    </div>
  );
};

export default DashboardPage;