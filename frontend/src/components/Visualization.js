import React, { useState, useEffect } from 'react';
import './Visualization.css';

const Visualization = ({ result }) => {
  const [isErrored, setIsErrored] = useState(false);
  
  // Log result for debugging
  useEffect(() => {
    console.log("Visualization result:", result);
  }, [result]);

  // Check if the result has an error property
  if (result.error) {
    return (
      <div className="visualization-container">
        <div className="error">
          <h3>Error:</h3>
          <pre>{result.error}</pre>
          
          {result.traceback && (
            <div>
              <h4>Traceback:</h4>
              <pre>{Array.isArray(result.traceback) 
                ? result.traceback.join('\n') 
                : result.traceback}</pre>
            </div>
          )}
        </div>
      </div>
    );
  }

  // If the result contains an image (static visualization)
  if (result.image) {
    return (
      <div className="visualization-container">
        <img 
          src={`data:${result.format || 'image/png'};base64,${result.image}`} 
          alt="Visualization" 
          className="visualization-image" 
        />
        
        {result.output && (
          <div className="output-log">
            <h4>Output Log:</h4>
            <pre>{result.output}</pre>
          </div>
        )}
      </div>
    );
  }
  
  // If the result contains HTML (interactive visualization)
  if (result.html) {
    return (
      <div className="visualization-container">
        {isErrored ? (
          <div className="error">
            <h3>Error Loading Interactive Visualization</h3>
            <p>The interactive visualization couldn't be displayed. This might be due to:</p>
            <ul>
              <li>Complex interactive elements</li>
              <li>Browser security restrictions</li>
              <li>Incompatible HTML content</li>
            </ul>
            <p>You can try regenerating the visualization or selecting a different example.</p>
          </div>
        ) : (
          <div className="iframe-container">
            <iframe
              title="Interactive Visualization"
              srcDoc={result.html}
              className="visualization-iframe"
              sandbox="allow-scripts allow-same-origin"
              onError={() => setIsErrored(true)}
              onLoad={() => console.log("iframe loaded successfully")}
            />
          </div>
        )}
        
        {result.output && (
          <div className="output-log">
            <h4>Output Log:</h4>
            <pre>{result.output}</pre>
          </div>
        )}
      </div>
    );
  }
  
  // If no visualization data is available
  return (
    <div className="visualization-container">
      <div className="error">
        <h3>Unexpected Result Format</h3>
        <p>The visualization couldn't be displayed. The server response didn't contain 
        expected visualization data.</p>
        <p>Response received:</p>
        <pre>{JSON.stringify(result, null, 2)}</pre>
      </div>
    </div>
  );
};

export default Visualization;