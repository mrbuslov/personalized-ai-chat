import React, { useState } from 'react';
import { X, Wand2 } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';
import AIRevisionModal from './AIRevisionModal';

const EditMessageModal = ({ message, onClose, onSave, onReviseWithAI }) => {
  const [content, setContent] = useState(message.content);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [showAIRevision, setShowAIRevision] = useState(false);

  const handleSave = async (e) => {
    e.preventDefault();
    if (!content.trim()) {
      setError('Message content cannot be empty');
      return;
    }

    setError('');
    setIsLoading(true);

    try {
      await onSave(message.id, content.trim());
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to update message');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReviseWithAI = async (instructions) => {
    try {
      await onReviseWithAI(message.id, instructions);
      setShowAIRevision(false);
      onClose();
    } catch (error) {
      console.error('Error revising message:', error);
      throw error;
    }
  };

  return (
    <>
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-hidden">
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Edit Message</h3>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          <div className="p-6">
            <form onSubmit={handleSave} className="space-y-4">
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                  {error}
                </div>
              )}

              <div>
                <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
                  Message Content
                </label>
                <textarea
                  id="content"
                  rows={8}
                  className="textarea"
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  placeholder="Enter message content..."
                />
              </div>

              <div className="flex justify-between">
                <div>
                  {message.role === 'manager' && (
                    <button
                      type="button"
                      onClick={() => setShowAIRevision(true)}
                      className="btn-secondary flex items-center space-x-2"
                    >
                      <Wand2 className="w-4 h-4" />
                      <span>Edit with AI</span>
                    </button>
                  )}
                </div>
                
                <div className="flex space-x-3">
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
                    disabled={isLoading || !content.trim()}
                  >
                    {isLoading ? <LoadingSpinner size="small" /> : 'Save Changes'}
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* AI Revision Modal */}
      {showAIRevision && (
        <AIRevisionModal
          message={message}
          onClose={() => setShowAIRevision(false)}
          onRevise={handleReviseWithAI}
        />
      )}
    </>
  );
};

export default EditMessageModal;