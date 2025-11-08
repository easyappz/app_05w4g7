import instance from './axios';

export const registerUser = async (sessionId) => {
  const response = await instance.post('/api/users/register/', {
    session_id: sessionId
  });
  return response.data;
};

export const sendHeartbeat = async (sessionId) => {
  const response = await instance.post('/api/users/heartbeat/', {
    session_id: sessionId
  });
  return response.data;
};

export const getOnlineCount = async () => {
  const response = await instance.get('/api/users/online/');
  return response.data;
};

export const getMessages = async () => {
  const response = await instance.get('/api/messages/');
  return response.data;
};

export const sendMessage = async (username, messageText) => {
  const response = await instance.post('/api/messages/', {
    username: username,
    message_text: messageText
  });
  return response.data;
};
