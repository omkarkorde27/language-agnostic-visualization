import React from 'react';
import './CodeEditor.css';

const CodeEditor = ({ code, setCode, language }) => {
  return (
    <div className="code-editor-container">
      <h3>Enter your {language === 'python' ? 'Python' : 'R'} code:</h3>
      <textarea
        className="code-editor"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        spellCheck="false"
        placeholder={`Enter your ${language} code here...`}
      />
    </div>
  );
};

export default CodeEditor;