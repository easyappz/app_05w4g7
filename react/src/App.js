import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import { registerUser, sendHeartbeat, getOnlineCount, getMessages, sendMessage } from './api/chatApi';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [username, setUsername] = useState('');
  const [messages, setMessages] = useState([]);
  const [onlineCount, setOnlineCount] = useState(0);
  const [messageText, setMessageText] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);
  const messagesPollInterval = useRef(null);
  const onlinePollInterval = useRef(null);
  const heartbeatInterval = useRef(null);

  const MAX_MESSAGE_LENGTH = 1000;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const initializeChat = async () => {
      try {
        const newSessionId = crypto.randomUUID();
        setSessionId(newSessionId);

        const userData = await registerUser(newSessionId);
        setUsername(userData.username);

        const messagesData = await getMessages();
        setMessages(messagesData);

        const onlineData = await getOnlineCount();
        setOnlineCount(onlineData.count);

        setLoading(false);

        messagesPollInterval.current = setInterval(async () => {
          try {
            const messagesData = await getMessages();
            setMessages(messagesData);
          } catch (err) {
            console.error('Error fetching messages:', err);
          }
        }, 2000);

        onlinePollInterval.current = setInterval(async () => {
          try {
            const onlineData = await getOnlineCount();
            setOnlineCount(onlineData.count);
          } catch (err) {
            console.error('Error fetching online count:', err);
          }
        }, 5000);

        heartbeatInterval.current = setInterval(async () => {
          try {
            await sendHeartbeat(newSessionId);
          } catch (err) {
            console.error('Error sending heartbeat:', err);
          }
        }, 30000);
      } catch (err) {
        setError('Ошибка при инициализации чата: ' + (err.response?.data?.message || err.message));
        setLoading(false);
      }
    };

    initializeChat();

    return () => {
      if (messagesPollInterval.current) clearInterval(messagesPollInterval.current);
      if (onlinePollInterval.current) clearInterval(onlinePollInterval.current);
      if (heartbeatInterval.current) clearInterval(heartbeatInterval.current);
    };
  }, []);

  useEffect(() => {
    window.handleRoutes(['/']);
  }, []);

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!messageText.trim() || messageText.length > MAX_MESSAGE_LENGTH) {
      return;
    }

    setSending(true);
    setError(null);

    try {
      const newMessage = await sendMessage(username, messageText.trim());
      setMessages(prev => [...prev, newMessage]);
      setMessageText('');
    } catch (err) {
      setError('Ошибка при отправке сообщения: ' + (err.response?.data?.message || err.message));
    } finally {
      setSending(false);
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${day}.${month}.${year} ${hours}:${minutes}`;
  };

  if (loading) {
    return (
      <div className="app" data-easytag="id1-react/src/App.js">
        <div className="loading" data-easytag="id2-react/src/App.js">Загрузка...</div>
      </div>
    );
  }

  return (
    <div className="app" data-easytag="id3-react/src/App.js">
      <div className="chat-container" data-easytag="id4-react/src/App.js">
        <div className="chat-header" data-easytag="id5-react/src/App.js">
          <h1 className="chat-title" data-easytag="id6-react/src/App.js">Групповой чат</h1>
          <div className="online-counter" data-easytag="id7-react/src/App.js">
            <span className="online-indicator" data-easytag="id8-react/src/App.js"></span>
            Онлайн: {onlineCount} {onlineCount === 1 ? 'пользователь' : 'пользователей'}
          </div>
          <div className="current-user" data-easytag="id9-react/src/App.js">
            Вы: <strong data-easytag="id10-react/src/App.js">{username}</strong>
          </div>
        </div>

        <div className="messages-area" data-easytag="id11-react/src/App.js">
          {messages.length === 0 ? (
            <div className="no-messages" data-easytag="id12-react/src/App.js">
              Пока нет сообщений. Будьте первым!
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={message.id || index}
                className={`message ${message.username === username ? 'own-message' : 'other-message'}`}
                data-easytag="id13-react/src/App.js"
              >
                <div className="message-header" data-easytag="id14-react/src/App.js">
                  <span className="message-username" data-easytag="id15-react/src/App.js">
                    {message.username}
                  </span>
                  <span className="message-timestamp" data-easytag="id16-react/src/App.js">
                    {formatTimestamp(message.timestamp)}
                  </span>
                </div>
                <div className="message-text" data-easytag="id17-react/src/App.js">
                  {message.message_text}
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        <form className="message-input-form" onSubmit={handleSendMessage} data-easytag="id18-react/src/App.js">
          {error && (
            <div className="error-message" data-easytag="id19-react/src/App.js">
              {error}
            </div>
          )}
          <div className="input-wrapper" data-easytag="id20-react/src/App.js">
            <textarea
              className="message-input"
              placeholder="Введите сообщение..."
              value={messageText}
              onChange={(e) => setMessageText(e.target.value)}
              disabled={sending}
              rows={3}
              data-easytag="id21-react/src/App.js"
            />
            <div className="input-footer" data-easytag="id22-react/src/App.js">
              <span
                className={`character-counter ${messageText.length > MAX_MESSAGE_LENGTH ? 'exceeded' : ''}`}
                data-easytag="id23-react/src/App.js"
              >
                {messageText.length} / {MAX_MESSAGE_LENGTH}
              </span>
              <button
                type="submit"
                className="send-button"
                disabled={!messageText.trim() || messageText.length > MAX_MESSAGE_LENGTH || sending}
                data-easytag="id24-react/src/App.js"
              >
                {sending ? 'Отправка...' : 'Отправить'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
