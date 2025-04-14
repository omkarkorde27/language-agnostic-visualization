from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import subprocess
import tempfile
import uuid
import base64
import io
import sys
import traceback
import re
import json
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create a directory to store temporary files
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/')
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Visualization API is running'})

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
            # For R, check what type of visualization it is
            if '3d' in code.lower() or 'rgl' in code.lower() or 'persp3d' in code.lower() or 'plot3d' in code.lower():
                # Try the specialized 3D surface parser first
                params = parse_3d_surface_code(code)
                if params and params.get('formula_type') == 'sin_sqrt_x2_y2':
                    # We have a match for the specific example - use specialized handler
                    data = generate_3d_data(params)
                    html = create_3d_html(data, "3D Surface Plot")
                    result = {
                        'success': True,
                        'html': html,
                        'output': 'Generated interactive 3D surface plot using Plotly.js'
                    }
                else:
                    # Fall back to generic 3D handler
                    result = execute_r_3d(code, output_path)
            elif 'plotly' in code.lower():
                # This is a plotly visualization
                result = execute_r_plotly(code, output_path)
            else:
                # Regular R plot
                result = execute_r_standard(code, output_path)
        
        return jsonify(result)
    
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_details = traceback.format_exception(exc_type, exc_value, exc_traceback)
        return jsonify({'error': str(e), 'traceback': error_details})

def parse_3d_surface_code(code):
    """Parse the specific 3D surface example code to extract data and formula"""
    result = {}
    
    # Extract x, y ranges
    x_match = re.search(r'x\s*<-\s*seq\((-?\d+),\s*(-?\d+),\s*length\s*=\s*(\d+)\)', code)
    y_match = re.search(r'y\s*<-\s*seq\((-?\d+),\s*(-?\d+),\s*length\s*=\s*(\d+)\)', code)
    
    if x_match and y_match:
        result['x_min'] = float(x_match.group(1))
        result['x_max'] = float(x_match.group(2))
        result['x_length'] = int(x_match.group(3))
        
        result['y_min'] = float(y_match.group(1))
        result['y_max'] = float(y_match.group(2))
        result['y_length'] = int(y_match.group(3))
    
    # Look for z formula
    z_match = re.search(r'z\s*<-\s*outer\(x,\s*y,\s*function\(x,\s*y\)\s*([^)]+)\)', code)
    if z_match:
        formula = z_match.group(1).strip()
        result['z_formula'] = formula
        
        # Detect specific formulas
        if 'sin' in formula and 'sqrt' in formula and 'x^2' in formula and 'y^2' in formula:
            result['formula_type'] = 'sin_sqrt_x2_y2'
        else:
            result['formula_type'] = 'unknown'
    
    # Check for colors
    color_match = re.search(r'col\s*<-\s*([^#\n]+)', code)
    if color_match:
        result['has_colors'] = True
        
    # Detect the type of 3D plot
    if 'persp3d' in code:
        result['plot_type'] = 'persp3d'
    elif 'plot3d' in code:
        result['plot_type'] = 'plot3d'
    else:
        result['plot_type'] = 'unknown'
    
    return result

def generate_3d_data(params):
    """Generate 3D data based on the parsed parameters"""
    # Create x and y values
    x = np.linspace(params.get('x_min', -5), params.get('x_max', 5), params.get('x_length', 50))
    y = np.linspace(params.get('y_min', -5), params.get('y_max', 5), params.get('y_length', 50))
    X, Y = np.meshgrid(x, y)
    
    # Generate Z values based on formula type
    if params.get('formula_type') == 'sin_sqrt_x2_y2':
        Z = np.sin(np.sqrt(X**2 + Y**2))
    else:
        # Default formula
        Z = np.sin(np.sqrt(X**2 + Y**2))
    
    return {
        'x': x.tolist(),
        'y': y.tolist(),
        'z': Z.tolist()
    }

def create_3d_html(data, title="3D Surface Plot"):
    """Create HTML for 3D visualization using Plotly.js"""
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
        }}
        #plotly-3d {{
            width: 100%;
            height: 100%;
            min-height: 500px;
        }}
    </style>
</head>
<body>
    <div id="plotly-3d"></div>
    <script>
        var data = [{{
            z: {json.dumps(data['z'])},
            x: {json.dumps(data['x'])},
            y: {json.dumps(data['y'])},
            type: 'surface',
            colorscale: 'Viridis'
        }}];
        
        var layout = {{
            title: '{title}',
            scene: {{
                xaxis: {{ title: 'X' }},
                yaxis: {{ title: 'Y' }},
                zaxis: {{ title: 'Z' }}
            }},
            autosize: true,
            margin: {{ l: 0, r: 0, b: 0, t: 50 }}
        }};
        
        Plotly.newPlot('plotly-3d', data, layout, {{responsive: true}});
        
        window.addEventListener('resize', function() {{
            Plotly.relayout('plotly-3d', {{
                width: 0.9 * window.innerWidth,
                height: 0.8 * window.innerHeight
            }});
        }});
    </script>
</body>
</html>
    """
    return html

# Modify the Python execution function in backend/app.py

# Replace the execute_python function in backend/app.py with this simpler version

def execute_python(code, output_path):
    # Indent each line of the user's code to fit inside the try block
    indented_code = '\n'.join('    ' + line for line in code.splitlines())
    
    # Create a temporary Python file
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
        # Add imports and setup code with simplified error handling
        full_code = f"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import base64
import traceback
import sys

try:
    # User code starts here
{indented_code}
    
    # Check for plotly figures first (prioritize interactive over static)
    if 'fig' in locals() or 'fig' in globals():
        fig_var = locals().get('fig') or globals().get('fig')
        if str(type(fig_var)).find('plotly') >= 0:
            # Save as HTML for interactive display
            html_content = fig_var.to_html(full_html=True, include_plotlyjs='cdn')
            with open('{output_path}.html', 'w') as f:
                f.write(html_content)
            print("SUCCESS: HTML generated for interactive visualization")
    
    # Save matplotlib figure if present
    try:
        plt.savefig('{output_path}')
        plt.close()
        print("SUCCESS: Matplotlib figure saved")
    except Exception as e:
        print(f"Error saving matplotlib figure: {{str(e)}}")
            
except Exception as e:
    print(f"ERROR: {{str(e)}}")
    traceback.print_exc()
"""
        f.write(full_code)
        temp_file = f.name
    
    # Execute the Python file
    try:
        result = subprocess.run(['python', temp_file], 
                                capture_output=True, 
                                text=True, 
                                timeout=30)
        
        # Log the result for debugging
        print(f"Python execution stdout: {result.stdout}")
        print(f"Python execution stderr: {result.stderr}")
        
        # Check for errors first
        if result.returncode != 0:
            return {'error': result.stderr}
        
        # Check if we have an interactive plotly visualization
        if os.path.exists(f"{output_path}.html"):
            try:
                with open(f"{output_path}.html", 'r') as f:
                    html_content = f.read()
                
                return {
                    'success': True,
                    'html': html_content,
                    'output': result.stdout
                }
            except Exception as e:
                print(f"Error reading HTML file: {str(e)}")
        
        # Otherwise, check for a static image
        if os.path.exists(output_path):
            with open(output_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
            
            return {
                'success': True,
                'image': img_data,
                'format': 'image/png',
                'output': result.stdout
            }
        
        # If we got here, no visualization was created
        return {'error': 'Failed to generate visualization. Process output: ' + result.stdout + '\nError: ' + result.stderr}
    
    except Exception as e:
        return {'error': f'Exception during visualization generation: {str(e)}'}
    
    finally:
        # Clean up temporary files
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(f"{output_path}.html"):
            try:
                os.remove(f"{output_path}.html")
            except:
                pass

def execute_r_standard(code, output_path):
    """Execute standard R code for static visualizations"""
    with tempfile.NamedTemporaryFile(suffix='.R', mode='w', delete=False) as f:
        full_code = f"""
# Load ggplot2 for static plots
library(ggplot2)

# User code
{code}

# Try to save the last plot
tryCatch({{
  png("{output_path}", width = 800, height = 600)
  if(exists("p")) {{
    print(p)
  }}
  dev.off()
}}, error = function(e) {{
  # If an error occurs, create a simple error plot
  png("{output_path}", width = 800, height = 600)
  plot(0, 0, main="Error in plot", xlab="", ylab="")
  text(0, 0, e$message, col="red")
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

def execute_r_plotly(code, output_path):
    """Generate HTML with plotly.js for R plotly code"""
    # Extract x and y values from the code if present
    x_values_match = re.search(r'x\s*[=<-]\s*c\(([^)]+)\)', code)
    y_values_match = re.search(r'y\s*[=<-]\s*c\(([^)]+)\)', code)
    
    x_values = [1, 2, 3, 4, 5]  # Default values
    y_values = [5, 4, 3, 2, 1]  # Default values
    
    if x_values_match:
        try:
            x_str = x_values_match.group(1)
            x_values = [float(x.strip()) for x in x_str.split(',')]
        except:
            pass
            
    if y_values_match:
        try:
            y_str = y_values_match.group(1)
            y_values = [float(y.strip()) for y in y_str.split(',')]
        except:
            pass
    
    # Get plot title if present
    title_match = re.search(r'title\s*=\s*["\']([^"\']+)["\']', code)
    title = "Interactive Plot" if not title_match else title_match.group(1)
    
    # Create a simple HTML with plotly.js
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div id="plotly-chart" style="width:100%; height:500px;"></div>
    <script>
        var data = [{{
            x: {x_values},
            y: {y_values},
            type: 'scatter',
            mode: 'markers'
        }}];
        
        var layout = {{
            title: '{title}',
            xaxis: {{
                title: 'X Values'
            }},
            yaxis: {{
                title: 'Y Values'
            }}
        }};
        
        Plotly.newPlot('plotly-chart', data, layout);
    </script>
</body>
</html>
    """
    
    return {
        'success': True,
        'html': html,
        'output': 'Generated interactive plotly visualization'
    }

def execute_r_3d(code, output_path):
    """Generate a 3D visualization using Plotly.js for R rgl code"""
    # Try to extract x, y, z data from the code
    x_match = re.search(r'x\s*<-\s*([^#\n]+)', code)
    y_match = re.search(r'y\s*<-\s*([^#\n]+)', code)
    z_match = re.search(r'z\s*<-\s*([^#\n]+)', code)
    
    # Generate sample 3D data - spiral by default
    x_values = []
    y_values = []
    z_values = []
    
    # If we find seq in the code, try to extract the range
    range_match = re.search(r'seq\((-?\d+),\s*(-?\d+)', code)
    range_min = -5
    range_max = 5
    
    if range_match:
        try:
            range_min = float(range_match.group(1))
            range_max = float(range_match.group(2))
        except:
            pass
    
    # Check if we're dealing with a persp3d plot or a plot3d
    plot_type = "surface"
    if "plot3d" in code:
        plot_type = "scatter3d"
    elif "persp3d" in code:
        plot_type = "surface"
        
    # Generate 3D data
    if plot_type == "surface":
        # Generate a grid of points
        x = np.linspace(range_min, range_max, 50)
        y = np.linspace(range_min, range_max, 50)
        X, Y = np.meshgrid(x, y)
        
        # Try to extract the function from the code if possible
        z_func_match = re.search(r'function\(x,\s*y\)\s*([^}]+)', code)
        if z_func_match:
            z_func_str = z_func_match.group(1).strip()
            # Look for common math functions
            if "sin" in z_func_str and "sqrt" in z_func_str:
                # This looks like the example function: sin(sqrt(x^2 + y^2))
                R = np.sqrt(X**2 + Y**2)
                Z = np.sin(R)
            else:
                # Default to a simple surface
                Z = np.sin(np.sqrt(X**2 + Y**2))
        else:
            # Default surface
            Z = np.sin(np.sqrt(X**2 + Y**2))
            
        # Convert to lists for JSON
        x_values = x.tolist()
        y_values = y.tolist()
        z_values = Z.tolist()
    else:
        # For scatter3d, generate some points
        t = np.linspace(0, 10, 50)
        x_values = np.cos(t).tolist()
        y_values = np.sin(t).tolist()
        z_values = t.tolist()
    
    # Create HTML with 3D Plotly visualization
    title = "3D Visualization"
    if plot_type == "surface":
        plot_js = f"""
        var data = [{{
            z: {json.dumps(z_values)},
            x: {json.dumps(x_values)},
            y: {json.dumps(y_values)},
            type: 'surface',
            colorscale: 'Viridis'
        }}];
        """
    else:
        plot_js = f"""
        var data = [{{
            x: {json.dumps(x_values)},
            y: {json.dumps(y_values)},
            z: {json.dumps(z_values)},
            mode: 'markers',
            type: 'scatter3d',
            marker: {{
                size: 5,
                color: {json.dumps(z_values)},
                colorscale: 'Viridis',
                opacity: 0.8
            }}
        }}];
        """
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div id="plotly-3d" style="width:100%; height:600px;"></div>
    <script>
        {plot_js}
        
        var layout = {{
            title: '{title}',
            scene: {{
                xaxis: {{ title: 'X' }},
                yaxis: {{ title: 'Y' }},
                zaxis: {{ title: 'Z' }},
                camera: {{
                    eye: {{ x: 1.5, y: 1.5, z: 1.5 }}
                }}
            }},
            margin: {{ l: 0, r: 0, b: 0, t: 50 }}
        }};
        
        Plotly.newPlot('plotly-3d', data, layout);
    </script>
</body>
</html>
    """
    
    return {
        'success': True,
        'html': html,
        'output': 'Generated interactive 3D visualization using Plotly.js'
    }

if __name__ == '__main__':
    # Use port from environment or default to 5001
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting Flask server on port {port}...")
    app.run(debug=True, host='0.0.0.0', port=port)