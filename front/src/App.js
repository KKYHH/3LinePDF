import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [data, setData] = useState(null);

  const handleSendMessage = () => {
    if (inputMessage.trim() !== '') {
      setMessages([...messages, { content: inputMessage, isUser: true }]);
      setInputMessage('');
      // You can implement logic here to send the message to the backend if needed
    }
  };

  const handleLoadData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/pdf/');
      setData(response.data);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    // 초기 데이터 로딩을 위해 handleLoadData 함수를 호출합니다.
    handleLoadData();
  }, []);


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
          <button onClick={handleSendMessage}><i className="fa-regular fa-paper-plane"></i></button>
        </div>
      </div>


      {/* 데이터를 표시하는 부분 */}
      <div className='data-container'>
        {data && (
          <div className='data'>
            <h2>불러온 데이터</h2>
            <p>{data.someProperty}</p> {/* 데이터에 따라 표시할 내용을 수정 */}
          </div>
        )}
        <button onClick={handleLoadData}>데이터 다시 불러오기</button>
        {data && <textarea rows={15} value={JSON.stringify(data, null, 2)} readOnly={true} />}
      </div>


    </>
  );
}

export default App;