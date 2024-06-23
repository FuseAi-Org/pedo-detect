import React, { useState, useEffect } from 'react';

const MessageInput = ({ addMessage, sender }) => {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim() === '') return; // Avoid adding empty messages
    addMessage({ user: sender, text });
    setText('');
  };

  return (
    <form className="message-form" onSubmit={handleSubmit}>
      <input 
        type="text" 
        className="input"
        value={text} 
        onChange={(e) => setText(e.target.value)} 
        placeholder="Type a message..." 
      />
      <button type="submit" className="button">Send</button>
    </form>
  );
};

export default MessageInput;

