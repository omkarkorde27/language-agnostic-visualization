from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import subprocess
import tempfile
import uuid
import base64
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create a directory to store temporary files
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/api/visualize', methods=['POST'])
def visualize():
    data = request.json
    if not data or 'code' not in data or 'language' not in data:
        return jsonify({'error': 'Missing code or language parameter'}), 400
    
    code = data['code']
    language = data['language'].lower()
    
    if language not in ['python', 'r']:
        return jsonify({'error': 'Unsupported language. Use "python" or "r"'}), 400
    
    try:
        # Generate unique ID for this visualization
        viz_id = str(uuid.uuid4())
        output_path = os.path.join(TEMP_DIR, f'{viz_id}.png')
        
        if language == 'python':
            result = execute_python(code, output_path)
        else:  # language == 'r'
            result = execute_r(code, output_path)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def execute_python(code, output_path):
    # Create a temporary Python file
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
        # Add imports for common visualization libraries
        full_code = f"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.io as pio
import io
import base64
from io import BytesIO

# Function to convert plotly figure to base64
def fig_to_base64(fig):
    img_bytes = pio.to_image(fig, format="png")
    encoded = base64.b64encode(img_bytes).decode('utf-8')
    return encoded

# User code starts here
{code}

# Check if there's a plt figure to save
try:
    plt.savefig('{output_path}')
    plt.close()
except:
    pass

# Check if there's a plotly figure in a variable named 'fig'
try:
    if 'fig' in locals() or 'fig' in globals():
        if str(type(fig)).find('plotly') >= 0:
            img_bytes = pio.to_image(fig, format="png")
            with open('{output_path}', 'wb') as f:
                f.write(img_bytes)
except:
    pass
"""
        f.write(full_code)
        temp_file = f.name
    
    # Execute the Python file
    try:
        result = subprocess.run(['python', temp_file], 
                                capture_output=True, 
                                text=True, 
                                timeout=30)
        
        if result.returncode != 0:
            return {'error': result.stderr}
        
        # Check if output file exists
        if os.path.exists(output_path):
            with open(output_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
            
            return {
                'success': True,
                'image': img_data,
                'format': 'image/png',
                'output': result.stdout
            }
        else:
            return {'error': 'Failed to generate visualization'}
    
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)

def execute_r(code, output_path):
    # Create a temporary R file
    with tempfile.NamedTemporaryFile(suffix='.R', mode='w', delete=False) as f:
        # Add standard library imports and save code
        full_code = f"""
# Load common visualization libraries
library(ggplot2)
library(plotly)
library(rgl)

# User code
{code}

# Try to save the last plot
tryCatch({{
  # For ggplot2
  if(exists("p") && "ggplot" %in% class(p)) {{
    ggsave("{output_path}", plot = p, width = 8, height = 6)
  }}
  # For base R plots
  else {{
    png("{output_path}", width = 800, height = 600)
    if(exists("p")) {{ print(p) }}
    dev.off()
  }}
  # For plotly
  if(exists("p") && "plotly" %in% class(p)) {{
    png("{output_path}", width = 800, height = 600)
    print(p)
    dev.off()
  }}
}}, error = function(e) {{
  # If specific plot object fails, try to capture the current plot
  png("{output_path}", width = 800, height = 600)
  dev.off()
}})
"""
        f.write(full_code)
        temp_file = f.name
    
    # Execute the R file
    try:
        result = subprocess.run(['Rscript', temp_file], 
                                capture_output=True, 
                                text=True, 
                                timeout=30)
        
        if result.returncode != 0:
            return {'error': result.stderr}
        
        # Check if output file exists
        if os.path.exists(output_path):
            with open(output_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
            
            return {
                'success': True,
                'image': img_data,
                'format': 'image/png',
                'output': result.stdout
            }
        else:
            return {'error': 'Failed to generate visualization'}
    
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)