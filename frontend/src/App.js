import React, { useState, useEffect } from 'react';
import './App.css';
import CodeEditor from './components/CodeEditor';
import Visualization from './components/Visualization';
import { pythonExamples, rExamples } from './examples';

function App() {
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [examples, setExamples] = useState([]);
  const [selectedExample, setSelectedExample] = useState('');

  // Set the initial example code based on the selected language
  useEffect(() => {
    if (language === 'python') {
      setExamples(pythonExamples);
      // Set default code to first example if no example is selected
      if (!selectedExample && pythonExamples.length > 0) {
        setCode(pythonExamples[0].code);
        setSelectedExample(pythonExamples[0].name);
      }
    } else {
      setExamples(rExamples);
      // Set default code to first example if no example is selected
      if (!selectedExample && rExamples.length > 0) {
        setCode(rExamples[0].code);
        setSelectedExample(rExamples[0].name);
      }
    }
  }, [language, selectedExample]);

  // Update code when example changes
  useEffect(() => {
    if (selectedExample) {
      const example = examples.find(ex => ex.name === selectedExample);
      if (example) {
        setCode(example.code);
      }
    }
  }, [selectedExample, examples]);

  // Handle language change
  const handleLanguageChange = (e) => {
    const newLanguage = e.target.value;
    setLanguage(newLanguage);
    setSelectedExample('');
    setResult(null);
    
    // Examples will be updated in the useEffect above
  };

  // Handle example change
  const handleExampleChange = (e) => {
    setSelectedExample(e.target.value);
  };

  // Handle code generation
  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const response = await fetch('/api/visualize', {  // Use relative URL for proxy to work
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code, language }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate visualization');
      }
      
      if (data.error) {
        setError(data.error);
      } else {
        setResult(data);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Language Agnostic Visualization</h1>
      </header>
      
      <main className="App-main">
        <div className="control-panel">
          <div className="language-selector">
            <label>
              Select Language:
              <select value={language} onChange={handleLanguageChange}>
                <option value="python">Python</option>
                <option value="r">R</option>
              </select>
            </label>
          </div>
          
          <div className="example-selector">
            <label>
              Example Visualizations:
              <select value={selectedExample} onChange={handleExampleChange}>
                <option value="">Select an example</option>
                {examples.map((example) => (
                  <option key={example.name} value={example.name}>
                    {example.name}
                  </option>
                ))}
              </select>
            </label>
          </div>
          
          <CodeEditor 
            code={code} 
            setCode={setCode} 
            language={language}
          />
          
          <button 
            className="generate-button" 
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? 'Generating...' : 'Generate Visualization'}
          </button>
        </div>
        
        <div className="visualization-panel">
          {loading && <div className="loading">Generating visualization...</div>}
          
          {error && <div className="error">
            <h3>Error:</h3>
            <pre>{error}</pre>
          </div>}
          
          {result && !error && <Visualization result={result} />}
          
          {!result && !error && !loading && (
            <div className="placeholder">
              <p>Your visualization will appear here</p>
            </div>
          )}
        </div>
      </main>
      
      <footer className="App-footer">
        <p>Language Agnostic Visualization Web Application</p>
      </footer>
    </div>
  );
}

export default App;