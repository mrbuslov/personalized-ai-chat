import React, { useState } from 'react';
import { X, Upload, FileText } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';

const ImportMessagesModal = ({ onClose, onImport }) => {
  const [importText, setImportText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleImport = async (e) => {
    e.preventDefault();
    if (!importText.trim()) {
      setError('Please provide messages to import');
      return;
    }

    setError('');
    setIsLoading(true);

    try {
      // Parse the input text into messages
      const messages = parseMessages(importText.trim());
      if (messages.length === 0) {
        throw new Error('No valid messages found in the input');
      }

      await onImport(messages);
    } catch (error) {
      setError(error.message || 'Failed to import messages');
    } finally {
      setIsLoading(false);
    }
  };

  const parseMessages = (text) => {
    const messages = [];
    const lines = text.split('\n');
    let currentMessage = null;
    
    for (const line of lines) {
      const trimmedLine = line.trim();
      if (!trimmedLine) continue;
      
      // Check if line starts with CLIENT: or MANAGER:
      if (trimmedLine.startsWith('CLIENT:')) {
        // Save previous message if exists
        if (currentMessage) {
          messages.push(currentMessage);
        }
        
        currentMessage = {
          role: 'client',
          content: trimmedLine.substring(7).trim(),
          is_ai_generated: false
        };
      } else if (trimmedLine.startsWith('MANAGER:')) {
        // Save previous message if exists
        if (currentMessage) {
          messages.push(currentMessage);
        }
        
        currentMessage = {
          role: 'manager',
          content: trimmedLine.substring(8).trim(),
          is_ai_generated: false
        };
      } else if (currentMessage) {
        // Continue the current message content
        currentMessage.content += '\n' + trimmedLine;
      } else {
        // If no role specified, treat as client message
        currentMessage = {
          role: 'client',
          content: trimmedLine,
          is_ai_generated: false
        };
      }
    }
    
    // Add the last message
    if (currentMessage) {
      messages.push(currentMessage);
    }
    
    return messages;
  };

  const exampleText = `CLIENT: Hi, I'm having trouble with my order. It hasn't arrived yet and it's been 2 weeks.

MANAGER: I'm sorry to hear about the delay with your order. I understand how frustrating that must be. Let me look into this for you right away.

CLIENT: Thank you. My order number is #12345.

MANAGER: I've found your order and I can see there was an issue with the shipping. I'm going to expedite a replacement order for you at no extra charge, and you should receive it within 2-3 business days.`;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-2">
            <Upload className="w-5 h-5 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-900">Import Messages</h3>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 max-h-[70vh] overflow-y-auto">
          <div className="grid md:grid-cols-2 gap-6">
            {/* Instructions */}
            <div>
              <h4 className="text-md font-medium text-gray-900 mb-3 flex items-center">
                <FileText className="w-4 h-4 mr-2" />
                Format Instructions
              </h4>
              
              <div className="text-sm text-gray-600 space-y-2 mb-4">
                <p>Enter messages in the following format:</p>
                <ul className="list-disc list-inside space-y-1 pl-4">
                  <li><code>CLIENT:</code> followed by client message</li>
                  <li><code>MANAGER:</code> followed by manager response</li>
                  <li>Each message can span multiple lines</li>
                  <li>Leave empty lines between messages for clarity</li>
                </ul>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Example Format
                </label>
                <pre className="text-xs bg-gray-50 p-3 rounded border overflow-x-auto whitespace-pre-wrap">
                  {exampleText}
                </pre>
              </div>
            </div>

            {/* Input Form */}
            <div>
              <form onSubmit={handleImport} className="space-y-4">
                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                    {error}
                  </div>
                )}

                <div>
                  <label htmlFor="importText" className="block text-sm font-medium text-gray-700 mb-2">
                    Messages to Import
                  </label>
                  <textarea
                    id="importText"
                    rows={15}
                    className="textarea font-mono text-sm"
                    value={importText}
                    onChange={(e) => setImportText(e.target.value)}
                    placeholder="CLIENT: Hello, I need help with...

MANAGER: I'd be happy to help you with that..."
                  />
                </div>

                <div className="flex justify-end space-x-3">
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
                    disabled={isLoading || !importText.trim()}
                  >
                    {isLoading ? <LoadingSpinner size="small" /> : (
                      <>
                        <Upload className="w-4 h-4" />
                        <span>Import Messages</span>
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImportMessagesModal;