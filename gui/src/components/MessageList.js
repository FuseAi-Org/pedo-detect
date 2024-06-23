import React from 'react';

const MessageList = ({ messages, sender }) => {
  return (
    <div className="messages">
      {messages.map((msg, index) => (
        <div key={index} className={`message-container ${msg.user === sender ? 'sender' : ''}`}>
          <div className={`username ${msg.user === sender ? 'sender' : ''}`}>
              {msg.user}
          </div>
          <div className={`message-bubble-container ${msg.user === sender ? 'sender' : ''}`}>
            <div className={`profile-circle ${msg.user === sender ? 'sender' : ''}`}>
              {msg.user.charAt(0)}
            </div>
            <div className={`message-bubble ${msg.user === sender ? 'sender' : ''}`}>
              {msg.text}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MessageList;


