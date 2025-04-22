import { useState } from 'react'
import ReactMarkdown from 'react-markdown';
import './App.css'

function App() {
  const [question, setQuestion] = useState('');
  const [llmResponse, setLlmResponse] = useState('');

  let llmResponseProgress = '';

  const renderResponseChunk = (chunk) => {
    llmResponseProgress += chunk || '';
    
    if (llmResponseProgress) {
      setLlmResponse(llmResponseProgress);
    }
  };

  const handleInputChange = (event) => {
    setQuestion(event.target.value);
  };

  const fetchData = async () => {
    setLlmResponse('Please be patient, calling a local LLM can take some time.  While you wait check the server logs...');

    const url = 'http://localhost:8000';

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question })
    });

    llmResponseProgress = ''

    const reader = response.body
      .pipeThrough(new TextDecoderStream())
      .getReader();

    while (true) {
      const { done, value } = await reader.read();
      
      renderResponseChunk(value);
 
      if (done) {
        return;
      }
    }
  };

  return (
    <>
      <h1>The Developer's Guide to AI</h1>
      <div className="card">
        <label>
          <input name="question" type="textarea" value={question} onChange={handleInputChange} placeholder="Ask me a question!" />
        </label>

        <button onClick={fetchData}>
          Call your API
        </button>

        <ReactMarkdown className="llm-response">
          {llmResponse}
        </ReactMarkdown>
      </div>
    </>
  )
}

export default App