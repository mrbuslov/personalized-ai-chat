import React, { useState, useEffect } from 'react';
import { X, Settings } from 'lucide-react';
import { apiService } from '../services/api';
import LoadingSpinner from './LoadingSpinner';

const ChatSettingsModal = ({ chatId, onClose }) => {
  const [specialInstructions, setSpecialInstructions] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const loadConfig = async () => {
    try {
      const config = await apiService.getChatAIConfig(chatId);
      if (config && config.global_prompt) {
        setSpecialInstructions(config.global_prompt);
      }
    } catch (error) {
      console.error('Error loading chat AI config:', error);
    } finally {
      setIsInitialLoading(false);
    }
  };

  useEffect(() => {
    loadConfig();
  }, [chatId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess(false);
    setIsLoading(true);

    try {
      await apiService.updateChatAIConfig(chatId, specialInstructions);
      setSuccess(true);
      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to update chat settings');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-2">
            <Settings className="w-5 h-5 text-gray-600" />
            <h3 className="text-lg font-semibold text-gray-900">Chat AI Settings</h3>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 max-h-[70vh] overflow-y-auto">
          {isInitialLoading ? (
            <div className="flex justify-center py-8">
              <LoadingSpinner />
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                  {error}
                </div>
              )}

              {success && (
                <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
                  Chat AI settings updated successfully!
                </div>
              )}

              <div>
                <label htmlFor="specialInstructions" className="block text-sm font-medium text-gray-700 mb-2">
                  Special Instructions for this Chat
                </label>
                <textarea
                  id="specialInstructions"
                  rows={12}
                  className="textarea"
                  placeholder="Enter special instructions for AI behavior in this specific chat. These instructions will override the global AI configuration for this chat only.&#10;&#10;Example:&#10;For this client, be extra patient and detailed in explanations. They are new to our service and need step-by-step guidance. Always offer to schedule a call if they seem confused."
                  value={specialInstructions}
                  onChange={(e) => setSpecialInstructions(e.target.value)}
                />
                <p className="text-xs text-gray-500 mt-2">
                  These instructions will override your global AI configuration for this specific chat.
                  Leave empty to use global settings.
                </p>
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={onClose}
                  className="btn-secondary"
                  disabled={isLoading}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn-primary flex items-center space-x-2"
                  disabled={isLoading}
                >
                  {isLoading ? <LoadingSpinner size="small" /> : 'Save Settings'}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatSettingsModal;