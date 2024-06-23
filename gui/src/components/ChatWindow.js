import React, { useState, useEffect } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import generateUniqueName from '../utils/nameGenerator'; // Import the utility function

import data from '../example_chat_data/example2.json';


const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const initializeStateVars = (data) => {
      let messages = [];
      let usersSet = new Set(); // Use a Set to ensure uniqueness
      data.forEach((message) => {
        const userName = generateUniqueName(message.user); // Generate unique name
        messages.push({ user: userName, text: message.text });
        usersSet.add(userName); // Add user to the Set
      });
      setUsers(Array.from(usersSet)); // Convert Set to Array
      setMessages(messages);
    };

    initializeStateVars(data);
  }, []);

  const addMessage = (message) => {
    setMessages([...messages, message]);
  };

  // Designate a single user as the sender
  const sender = users[0]; // or you can specify any user from the list

  return (
    <div className="chat-container">
      <div className="header">Chat App</div>
      <MessageList messages={messages} sender={sender} />
      <MessageInput addMessage={addMessage} sender={sender} />
    </div>
  );
};

export default ChatWindow;


