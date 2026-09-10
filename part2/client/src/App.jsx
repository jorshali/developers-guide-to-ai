import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown';
import './App.css'

function LoadingIndicator() {
  return (
    <div className="loading-indicator">
      <div className="dot"></div>
      <div className="dot"></div>
      <div className="dot"></div>
    </div>
  );
}

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [isSummarizing, setIsSummarizing] = useState(false);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleInputChange = (event) => {
    setInputMessage(event.target.value);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const handleSummarize = async () => {
    if (messages.length === 0) return;
    
    setIsLoading(true);
    setIsSummarizing(true);

    try {
      const response = await fetch('http://localhost:8000/summarize', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          history: messages
        })
      });

      const summaryMessage = await response.json();

      setMessages([summaryMessage]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
      setIsSummarizing(false);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    // Add user message to chat
    const userMessage = { role: 'user', content: inputMessage };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setIsSending(true);

    const url = 'http://localhost:8000';

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question: inputMessage,
          history: messages
        })
      });

      let assistantMessage = '';
      const reader = response.body
        .pipeThrough(new TextDecoderStream())
        .getReader();

      while (true) {
        const { done, value } = await reader.read();
        
        if (value) {
          assistantMessage += value;
          setMessages(prev => {
            const newMessages = [...prev];
            const lastMessage = newMessages[newMessages.length - 1];
            if (lastMessage && lastMessage.role === 'assistant') {
              lastMessage.content = assistantMessage;
            } else {
              newMessages.push({ role: 'assistant', content: assistantMessage });
            }
            return newMessages;
          });
        }
 
        if (done) {
          break;
        }
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, there was an error processing your request.' }]);
    } finally {
      setIsLoading(false);
      setIsSending(false);
    }
  };

  return (
    <div className="chat-container">
      <h1>The Developer's Guide to AI</h1>
      <h5>Basic Llama 3.2 Chatbot</h5>
      <div className="chat-box">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <LoadingIndicator />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-area">
        <textarea
          value={inputMessage}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="You can ask me anything..."
          disabled={isLoading}
        />
        <button 
          onClick={handleSendMessage}
          disabled={isLoading || !inputMessage.trim()}
          title='Send a question to the LLM.'
        >
          {isSending ? 'Sending...' : 'Send'}
        </button>
        <button 
          onClick={handleSummarize}
          disabled={isLoading || messages.length === 0}
          title='Summarize the conversation so far.'
        >
          {isSummarizing ? 'Summarizing...' : 'Summarize'}
        </button>
      </div>
    </div>
  )
}

export default App