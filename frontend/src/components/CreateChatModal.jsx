import React, { useState } from 'react';
import { X } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';

const CreateChatModal = ({ onClose, onSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    clientDescription: '',
    specialInstructions: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await onSubmit(formData.name, formData.clientDescription, formData.specialInstructions);
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to create chat');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Create New Chat</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              Chat Name *
            </label>
            <input
              id="name"
              name="name"
              type="text"
              required
              className="input"
              placeholder="e.g. Support Chat - John Doe"
              value={formData.name}
              onChange={handleChange}
            />
          </div>

          <div>
            <label htmlFor="clientDescription" className="block text-sm font-medium text-gray-700 mb-2">
              Client Description
            </label>
            <textarea
              id="clientDescription"
              name="clientDescription"
              rows={3}
              className="textarea"
              placeholder="Describe your client (personality, background, needs, etc.)"
              value={formData.clientDescription}
              onChange={handleChange}
            />
            <p className="text-xs text-gray-500 mt-1">
              This helps AI understand the client context
            </p>
          </div>

          <div>
            <label htmlFor="specialInstructions" className="block text-sm font-medium text-gray-700 mb-2">
              Special Instructions
            </label>
            <textarea
              id="specialInstructions"
              name="specialInstructions"
              rows={3}
              className="textarea"
              placeholder="Special AI behavior for this chat (tone, approach, etc.)"
              value={formData.specialInstructions}
              onChange={handleChange}
            />
            <p className="text-xs text-gray-500 mt-1">
              Override global AI settings for this specific chat
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
              {isLoading ? <LoadingSpinner size="small" /> : 'Create Chat'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateChatModal;