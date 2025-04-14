# Language Agnostic Visualization Web Application

A web application that allows users to create data visualizations using Python or R code, directly in the browser.

## Overview

This application consists of a React frontend and a Flask backend. It enables users to:

* Write code in Python or R
* Generate static and interactive visualizations
* Choose from pre-defined examples or write custom code
* View visualizations directly in the browser

## Features

* **Multi-language Support**: Generate visualizations using either Python or R code
* **Interactive Visualizations**: Create both static and interactive plots
* **Pre-built Examples**: Choose from various visualization examples for quick starts
* **Real-time Rendering**: View visualization outputs directly in the browser
* **Error Handling**: Detailed error reporting for debugging code

## Project Structure

```
/
├── backend/
│   ├── app.py                   # Flask application with visualization API
│   ├── requirements.txt         # Python dependencies
│   └── temp/                    # Directory for temporary visualization files
│
└── frontend/
    ├── public/                  # Public assets
    └── src/
        ├── components/          # React components
        │   ├── CodeEditor.js    # Code editor component
        │   └── Visualization.js # Visualization display component
        ├── App.js               # Main application component
        ├── examples.js          # Pre-defined code examples
        └── api/                 # API client
```

## Technologies Used

### Backend
- **Flask**: Python web framework
- **NumPy**: Numerical computing library
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Static visualization library
- **Plotly**: Interactive visualization library

### Frontend
- **React**: Frontend framework
- **Axios**: HTTP client (defined in API but using fetch in App.js)
- **CSS**: Styling

## Setup and Installation

### Prerequisites
- Node.js and npm
- Python 3.6+
- R (optional, for R visualizations)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the Flask server:
```bash
python app.py
```

The backend will run on http://localhost:5001 by default.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on http://localhost:3000 and proxy API requests to the backend.

## Usage

1. Select the language (Python or R) from the dropdown
2. Choose a pre-built example or write your own code
3. Click "Generate Visualization" to create the visualization
4. View the output in the visualization panel

## Supported Visualization Types

### Python
- Matplotlib static visualizations
- Plotly interactive visualizations
- 3D surface plots
- Line charts, scatter plots, bar charts, etc.

### R
- ggplot2 static visualizations
- plotly interactive visualizations
- 3D visualizations using rgl
- Boxplots, bar charts, scatter plots, etc.

## Error Handling

The application provides detailed error messages when:
- The code contains syntax errors
- The visualization fails to generate
- The backend server is unreachable

## License

[MIT License]

## Credits

Developed as a cross-language data visualization platform.