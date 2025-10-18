import React, { useState } from 'react';
import { User, Bot, Edit3, Trash2, Wand2 } from 'lucide-react';
import AIRevisionModal from './AIRevisionModal';

const MessageComponent = ({ message, onEdit, onDelete, onReviseWithAI }) => {
  const [showAIRevision, setShowAIRevision] = useState(false);
  
  const isClient = message.role === 'client';
  const isAIGenerated = message.is_ai_generated;

  const formatTime = (dateString) => {
    return new Date(dateString).toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
    });
  };

  const handleReviseWithAI = async (instructions) => {
    try {
      await onReviseWithAI(message.id, instructions);
      setShowAIRevision(false);
    } catch (error) {
      console.error('Error revising message:', error);
      throw error;
    }
  };

  return (
    <>
      <div className={`flex ${isClient ? 'justify-start' : 'justify-end'}`}>
        <div className={`max-w-3xl w-full ${isClient ? 'pr-16' : 'pl-16'}`}>
          <div className={`
            p-4 rounded-lg shadow-sm border
            ${isClient 
              ? 'bg-blue-50 border-blue-200' 
              : 'bg-green-50 border-green-200'
            }
          `}>
            {/* Header */}
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                {isClient ? (
                  <User className="w-4 h-4 text-blue-600" />
                ) : (
                  <Bot className="w-4 h-4 text-green-600" />
                )}
                <span className={`text-sm font-medium ${
                  isClient ? 'text-blue-600' : 'text-green-600'
                }`}>
                  {isClient ? 'Client' : 'Manager'}
                  {isAIGenerated && <span className="text-xs ml-1">(AI)</span>}
                </span>
                <span className="text-xs text-gray-500">
                  {formatTime(message.created_at)}
                </span>
              </div>
              
              {/* Action Buttons */}
              <div className="flex items-center space-x-1">
                {!isClient && (
                  <>
                    <button
                      onClick={() => setShowAIRevision(true)}
                      className="text-purple-600 hover:text-purple-700 p-1"
                      title="Edit with AI"
                    >
                      <Wand2 className="w-4 h-4" />
                    </button>
                    <button
                      onClick={onEdit}
                      className="text-blue-600 hover:text-blue-700 p-1"
                      title="Edit"
                    >
                      <Edit3 className="w-4 h-4" />
                    </button>
                  </>
                )}
                {isClient && (
                  <button
                    onClick={onEdit}
                    className="text-blue-600 hover:text-blue-700 p-1"
                    title="Edit"
                  >
                    <Edit3 className="w-4 h-4" />
                  </button>
                )}
                <button
                  onClick={onDelete}
                  className="text-red-600 hover:text-red-700 p-1"
                  title="Delete"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Content */}
            <div className="text-gray-900 whitespace-pre-wrap">
              {message.content}
            </div>
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

export default MessageComponent;