# Language Agnostic Visualization Web Application

A web application that allows users to generate and view simple visualizations by submitting custom scripts written in Python or R. The app executes these scripts on the backend and renders the resulting visualizations in the frontend.

## Overview

This project consists of two main components:

1. **Frontend (React)**
   - Provides an interface to select scripting language (Python or R)
   - Includes a text area to input code that generates charts
   - Offers a set of example visualizations in both Python and R
   - Displays the resulting visualization

2. **Backend (Flask)**
   - Accepts code and language selection via an API endpoint
   - Dynamically executes scripts in secure isolated environments
   - Generates visualizations
   - Returns visualization data to be embedded in the frontend

## Supported Visualization Libraries

### Python
- **Matplotlib** - Static visualizations
- **Plotly** - Interactive and 3D visualizations

### R
- **ggplot2** - Static visualizations
- **plotly** - Interactive visualizations
- **rgl** - 3D visualizations

## Project Structure

```
.
├── backend/
│   ├── app.py                # Flask application
│   ├── Dockerfile            # Docker configuration for backend
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Styles for App component
│   │   ├── components/       # React components
│   │   │   ├── CodeEditor.js     # Code input component
│   │   │   ├── CodeEditor.css    # Styles for code editor
│   │   │   ├── Visualization.js  # Visualization display component
│   │   │   └── Visualization.css # Styles for visualization
│   │   ├── examples.js       # Example code for Python and R
│   │   ├── index.js          # React entry point
│   │   └── index.css         # Global styles
│   ├── package.json          # Node.js dependencies
│   └── Dockerfile            # Docker configuration for frontend
└── docker-compose.yml        # Docker Compose configuration
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js and npm (if running the frontend outside Docker)
- Python 3.9+ (if running the backend outside Docker)
- R (if running the backend outside Docker)

### Running with Docker Compose

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/language-agnostic-visualization.git
   cd language-agnostic-visualization
   ```

2. Start the application with Docker Compose:
   ```
   docker-compose up
   ```

3. Access the application at http://localhost:3000

### Running without Docker

#### Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Start the Flask server:
   ```
   python app.py
   ```

#### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install Node.js dependencies:
   ```
   npm install
   ```

3. Start the React development server:
   ```
   npm start
   ```

4. Access the application at http://localhost:3000

## Implementation Details and Challenges

### Security Considerations

The application executes user-provided code, which presents security challenges. The following measures have been implemented:

- Code execution in isolated environments
- Timeout limits to prevent infinite loops
- Resource limitations to prevent excessive resource usage

### Cross-Language Support

Supporting both Python and R required:

- Designing a unified API for both languages
- Managing different environment dependencies
- Standardizing visualization output formats

### Visualization Rendering

Different visualization libraries produce different output formats. The application handles:

- Static images (PNG) for simple visualizations
- Interactive HTML/JavaScript for Plotly visualizations
- Conversion of 3D visualizations to static images (for libraries like rgl)

## Future Improvements

- Add more supported visualization libraries
- Implement user authentication and saved visualizations
- Add dataset upload functionality
- Improve error handling and debugging tools
- Add option to export visualizations in different formats