import React, { useState } from 'react';
import { X, Wand2 } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';

const AIRevisionModal = ({ message, onClose, onRevise }) => {
  const [instructions, setInstructions] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRevise = async (e) => {
    e.preventDefault();
    if (!instructions.trim()) {
      setError('Please provide revision instructions');
      return;
    }

    setError('');
    setIsLoading(true);

    try {
      await onRevise(instructions.trim());
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to revise message with AI');
    } finally {
      setIsLoading(false);
    }
  };

  const suggestionPrompts = [
    "Make this more professional and formal",
    "Make this more friendly and casual", 
    "Make this more empathetic and understanding",
    "Make this shorter and more concise",
    "Add more detail and explanation",
    "Make this more apologetic",
    "Make this more solution-focused"
  ];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[60]">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-2">
            <Wand2 className="w-5 h-5 text-purple-600" />
            <h3 className="text-lg font-semibold text-gray-900">Edit with AI</h3>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 space-y-4">
          {/* Current Message */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Current Message
            </label>
            <div className="p-3 bg-gray-50 border border-gray-200 rounded-md text-sm">
              {message.content}
            </div>
          </div>

          {/* Revision Form */}
          <form onSubmit={handleRevise} className="space-y-4">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="instructions" className="block text-sm font-medium text-gray-700 mb-2">
                Revision Instructions
              </label>
              <textarea
                id="instructions"
                rows={4}
                className="textarea"
                value={instructions}
                onChange={(e) => setInstructions(e.target.value)}
                placeholder="Tell AI how you want to modify this message..."
              />
            </div>

            {/* Quick Suggestions */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Quick Suggestions
              </label>
              <div className="flex flex-wrap gap-2">
                {suggestionPrompts.map((prompt, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => setInstructions(prompt)}
                    className="text-xs px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-gray-700 transition-colors"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
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
                disabled={isLoading || !instructions.trim()}
              >
                {isLoading ? <LoadingSpinner size="small" /> : (
                  <>
                    <Wand2 className="w-4 h-4" />
                    <span>Revise with AI</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AIRevisionModal;