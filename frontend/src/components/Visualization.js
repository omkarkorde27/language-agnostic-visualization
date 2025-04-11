import React from 'react';
import './Visualization.css';

const Visualization = ({ result }) => {
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
  
  // If there's something else (like HTML for interactive viz)
  if (result.html) {
    return (
      <div className="visualization-container">
        <h3>Visualization Result</h3>
        <iframe
          srcDoc={result.html}
          title="Interactive Visualization"
          className="visualization-iframe"
          sandbox="allow-scripts"
        />
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