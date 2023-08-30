import React, { useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');

  const handleSendMessage = () => {
    if (inputMessage.trim() !== '') {
      setMessages([...messages, { content: inputMessage, isUser: true }]);
      setInputMessage('');
      // You can implement logic here to send the message to the backend if needed
    }
  };

  return (
    <>

      <div className='title'>3LinePDF</div>
      <div className='chat-container'>
        <div className='chat-messages'>
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.isUser ? 'user-message' : 'bot-message'}`}>
              {message.content}
            </div>
          ))}
        </div>
        <div className='user-input'>
          <input
            type='text'
            placeholder='내용을 입력하세요.'
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
          />
          <button onClick={handleSendMessage}><i class="fa-regular fa-paper-plane"></i></button>
        </div>
      </div>

    </>
  );
}

export default App;
