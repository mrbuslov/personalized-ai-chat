import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { apiService } from '../services/api';
import LoadingSpinner from './LoadingSpinner';

const GlobalAIConfigModal = ({ onClose }) => {
  const [specialInstructions, setSpecialInstructions] = useState('');
  const [clientDescription, setClientDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const loadConfig = async () => {
    try {
      const config = await apiService.getGlobalAIConfig();
      if (config) {
        setSpecialInstructions(config.special_instructions || '');
        setClientDescription(config.client_description || '');
      }
    } catch (error) {
      console.error('Error loading AI config:', error);
    } finally {
      setIsInitialLoading(false);
    }
  };

  useEffect(() => {
    loadConfig();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess(false);
    setIsLoading(true);

    try {
      await apiService.updateGlobalAIConfig(clientDescription, specialInstructions);
      setSuccess(true);
      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to update AI configuration');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Global AI Configuration</h3>
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
                  Global AI configuration updated successfully!
                </div>
              )}

              <div>
                <label htmlFor="clientDescription" className="block text-sm font-medium text-gray-700 mb-2">
                  Global Client Description
                </label>
                <textarea
                  id="clientDescription"
                  rows={3}
                  className="textarea"
                  placeholder="Default description of your clients/customers that applies globally..."
                  value={clientDescription}
                  onChange={(e) => setClientDescription(e.target.value)}
                />
              </div>

              <div>
                <label htmlFor="specialInstructions" className="block text-sm font-medium text-gray-700 mb-2">
                  Global Manager Personality & Behavior
                </label>
                <textarea
                  id="specialInstructions"
                  rows={12}
                  className="textarea"
                  placeholder="Define how the AI should behave as a customer service manager. This will be used as the base prompt for all chats unless overridden by chat-specific instructions.&#10;&#10;Example:&#10;You are a professional customer service manager with 10+ years of experience. You are empathetic, solution-oriented, and always maintain a positive attitude. Your goal is to resolve customer issues quickly and efficiently while ensuring customer satisfaction..."
                  value={specialInstructions}
                  onChange={(e) => setSpecialInstructions(e.target.value)}
                />
                <p className="text-xs text-gray-500 mt-2">
                  This prompt will be used for all chats unless overridden by chat-specific special instructions.
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
                  {isLoading ? <LoadingSpinner size="small" /> : 'Save Configuration'}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default GlobalAIConfigModal;