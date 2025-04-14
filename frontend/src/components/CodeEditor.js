import React from 'react';
import './CodeEditor.css';

const CodeEditor = ({ code, setCode, language }) => {
  const handleCodeChange = (e) => {
    setCode(e.target.value);
  };

  return (
    <div className="code-editor">
      <h3>Code Editor ({language})</h3>
      <textarea
        className="code-textarea"
        value={code}
        onChange={handleCodeChange}
        placeholder={`Enter your ${language} code here...`}
        rows={12}
        spellCheck="false"
      />
    </div>
  );
};

export default CodeEditor;