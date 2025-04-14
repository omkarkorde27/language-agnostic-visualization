import React from 'react';
import './Visualization.css';

const Visualization = ({ result }) => {
  // If there's an error
  if (result.error) {
    return (
      <div className="visualization-container">
        <h3>Error</h3>
        <div className="error-message">
          <pre>{result.error}</pre>
          {result.details && <pre>{result.details}</pre>}
        </div>
      </div>
    );
  }
  
  // If the result contains an HTML (for interactive visualizations)
  if (result.html) {
    return (
      <div className="visualization-container">
        <h3>Interactive Visualization</h3>
        <iframe
          srcDoc={result.html}
          title="Interactive Visualization"
          className="visualization-iframe"
          sandbox="allow-scripts allow-same-origin"
          frameBorder="0"
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
  
  // If the result contains an image
  if (result.image) {
    return (
      <div className="visualization-container">
        <h3>Visualization Result</h3>
        <img 
          src={`data:${result.format};base64,${result.image}`} 
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
  
  // Fallback for other result types or no result
  return (
    <div className="visualization-container">
      <h3>Visualization Result</h3>
      <div className="visualization-placeholder">
        <p>No visualization data available</p>
      </div>
    </div>
  );
};

export default Visualization;