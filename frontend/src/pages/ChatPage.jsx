import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  Settings, 
  Send, 
  Edit3, 
  Trash2, 
  Bot,
  User,
  Upload,
  Save
} from 'lucide-react';
import { apiService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import MessageComponent from '../components/MessageComponent';
import EditMessageModal from '../components/EditMessageModal';
import ImportMessagesModal from '../components/ImportMessagesModal';
import ChatSettingsModal from '../components/ChatSettingsModal';

const ChatPage = ({ user }) => {
  const { chatId } = useParams();
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);
  
  const [chat, setChat] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isGeneratingAI, setIsGeneratingAI] = useState(false);
  const [error, setError] = useState('');
  
  const [editingMessage, setEditingMessage] = useState(null);
  const [showImportMessages, setShowImportMessages] = useState(false);
  const [showChatSettings, setShowChatSettings] = useState(false);
  const [isEditingChat, setIsEditingChat] = useState(false);
  const [editChatData, setEditChatData] = useState({
    name: '',
    client_description: '',
    special_instructions: ''
  });

  const loadChat = async () => {
    try {
      const chatData = await apiService.getChat(chatId);
      setChat(chatData);
      setEditChatData({
        name: chatData.name,
        client_description: chatData.client_description || '',
        special_instructions: chatData.special_instructions || ''
      });
    } catch (error) {
      setError('Failed to load chat');
      console.error('Error loading chat:', error);
    }
  };

  const loadMessages = async () => {
    try {
      const response = await apiService.getChatMessages(chatId);
      setMessages(response.messages);
    } catch (error) {
      setError('Failed to load messages');
      console.error('Error loading messages:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (chatId) {
      loadChat();
      loadMessages();
    }
  }, [chatId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    try {
      const message = await apiService.createMessage(chatId, newMessage.trim(), 'client');
      setMessages([...messages, message]);
      setNewMessage('');
    } catch (error) {
      setError('Failed to send message');
      console.error('Error sending message:', error);
    }
  };

  const handleGenerateAI = async () => {
    setIsGeneratingAI(true);
    try {
      const aiMessage = await apiService.generateAIResponse(chatId);
      setMessages([...messages, aiMessage]);
    } catch (error) {
      setError('Failed to generate AI response');
      console.error('Error generating AI response:', error);
    } finally {
      setIsGeneratingAI(false);
    }
  };

  const handleEditMessage = async (messageId, newContent) => {
    try {
      await apiService.updateMessage(messageId, newContent);
      setMessages(messages.map(msg => 
        msg.id === messageId ? { ...msg, content: newContent } : msg
      ));
      setEditingMessage(null);
    } catch (error) {
      console.error('Error editing message:', error);
      throw error;
    }
  };

  const handleDeleteMessage = async (messageId) => {
    if (!confirm('Are you sure you want to delete this message?')) return;

    try {
      await apiService.deleteMessage(messageId);
      setMessages(messages.filter(msg => msg.id !== messageId));
    } catch (error) {
      setError('Failed to delete message');
      console.error('Error deleting message:', error);
    }
  };

  const handleReviseWithAI = async (messageId, instructions) => {
    try {
      const revisedMessage = await apiService.reviseMessageWithAI(messageId, instructions);
      setMessages(messages.map(msg => 
        msg.id === messageId ? revisedMessage : msg
      ));
    } catch (error) {
      setError('Failed to revise message with AI');
      console.error('Error revising message:', error);
    }
  };

  const handleImportMessages = async (importedMessages) => {
    try {
      await apiService.importMessages(chatId, importedMessages);
      loadMessages(); // Reload all messages
      setShowImportMessages(false);
    } catch (error) {
      console.error('Error importing messages:', error);
      throw error;
    }
  };

  const handleSaveChatChanges = async () => {
    try {
      const updatedChat = await apiService.updateChat(chatId, editChatData);
      setChat(updatedChat);
      setIsEditingChat(false);
    } catch (error) {
      setError('Failed to update chat');
      console.error('Error updating chat:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  if (!chat) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Chat not found</h2>
          <Link to="/dashboard" className="text-primary-600 hover:text-primary-700">
            ← Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-4">
            <div className="flex items-center space-x-4">
              <Link to="/dashboard" className="text-gray-600 hover:text-gray-900">
                <ArrowLeft className="w-5 h-5" />
              </Link>
              <div>
                {isEditingChat ? (
                  <div className="flex items-center space-x-2">
                    <input
                      type="text"
                      value={editChatData.name}
                      onChange={(e) => setEditChatData({...editChatData, name: e.target.value})}
                      className="text-xl font-bold border-none p-0 focus:ring-0"
                    />
                    <button
                      onClick={handleSaveChatChanges}
                      className="text-green-600 hover:text-green-700"
                    >
                      <Save className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => setIsEditingChat(false)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      ×
                    </button>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <h1 className="text-xl font-bold text-gray-900">{chat.name}</h1>
                    <button
                      onClick={() => setIsEditingChat(true)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      <Edit3 className="w-4 h-4" />
                    </button>
                  </div>
                )}
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setShowImportMessages(true)}
                className="btn-secondary flex items-center space-x-2"
              >
                <Upload className="w-4 h-4" />
                <span>Import Messages</span>
              </button>
              <button
                onClick={() => setShowChatSettings(true)}
                className="btn-secondary flex items-center space-x-2"
              >
                <Settings className="w-4 h-4" />
                <span>Chat Settings</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Chat Info */}
      {(chat.client_description || isEditingChat) && (
        <div className="bg-blue-50 border-b border-blue-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
            {isEditingChat ? (
              <div className="space-y-2">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Client Description
                  </label>
                  <textarea
                    value={editChatData.client_description}
                    onChange={(e) => setEditChatData({...editChatData, client_description: e.target.value})}
                    className="textarea w-full"
                    rows={2}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Special Instructions
                  </label>
                  <textarea
                    value={editChatData.special_instructions}
                    onChange={(e) => setEditChatData({...editChatData, special_instructions: e.target.value})}
                    className="textarea w-full"
                    rows={2}
                  />
                </div>
              </div>
            ) : (
              <div>
                {chat.client_description && (
                  <p className="text-sm text-blue-800">
                    <strong>Client:</strong> {chat.client_description}
                  </p>
                )}
                {chat.special_instructions && (
                  <p className="text-sm text-blue-800 mt-1">
                    <strong>Instructions:</strong> {chat.special_instructions}
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border-b border-red-200 text-red-700 px-4 py-3">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {error}
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <div className="max-w-4xl mx-auto h-full flex flex-col">
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-gray-400 mb-4">
                  <User className="w-16 h-16 mx-auto mb-2" />
                  <p>No messages yet. Start the conversation by writing as the client.</p>
                </div>
              </div>
            ) : (
              messages.map((message) => (
                <MessageComponent
                  key={message.id}
                  message={message}
                  onEdit={() => setEditingMessage(message)}
                  onDelete={() => handleDeleteMessage(message.id)}
                  onReviseWithAI={handleReviseWithAI}
                />
              ))
            )}
            {isGeneratingAI && (
              <div className="flex items-center space-x-2 text-gray-600">
                <Bot className="w-5 h-5" />
                <span>AI is generating response...</span>
                <LoadingSpinner size="small" />
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Message Input */}
          <div className="border-t border-gray-200 bg-white p-4">
            <div className="flex items-center space-x-2 mb-2">
              <User className="w-5 h-5 text-blue-600" />
              <span className="text-sm font-medium text-blue-600">Writing as Client</span>
            </div>
            <form onSubmit={handleSendMessage} className="flex space-x-3">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder="Type client message..."
                className="input flex-1"
                disabled={isGeneratingAI}
              />
              <button
                type="submit"
                disabled={!newMessage.trim() || isGeneratingAI}
                className="btn-primary flex items-center space-x-2 disabled:opacity-50"
              >
                <Send className="w-4 h-4" />
                <span>Send</span>
              </button>
              <button
                type="button"
                onClick={handleGenerateAI}
                disabled={isGeneratingAI}
                className="btn-secondary flex items-center space-x-2 disabled:opacity-50"
              >
                <Bot className="w-4 h-4" />
                <span>Generate AI</span>
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Modals */}
      {editingMessage && (
        <EditMessageModal
          message={editingMessage}
          onClose={() => setEditingMessage(null)}
          onSave={handleEditMessage}
          onReviseWithAI={handleReviseWithAI}
        />
      )}

      {showImportMessages && (
        <ImportMessagesModal
          onClose={() => setShowImportMessages(false)}
          onImport={handleImportMessages}
        />
      )}

      {showChatSettings && (
        <ChatSettingsModal
          chatId={chatId}
          onClose={() => setShowChatSettings(false)}
        />
      )}
    </div>
  );
};

export default ChatPage;