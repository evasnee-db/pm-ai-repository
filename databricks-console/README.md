# Databricks Console

A modern, responsive web console inspired by Databricks' interface. This application features a clean, professional UI with dark mode support, interactive components, and a sophisticated design.

## Features

### 🎨 Modern UI Design
- **Clean Interface**: Inspired by Databricks with a modern, professional look
- **Dark/Light Mode**: Toggle between themes with preferences saved locally
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Smooth Animations**: Professional transitions and hover effects

### 📊 Dashboard Components
- **Quick Actions**: Cards for creating notebooks, importing data, running queries, and managing clusters
- **Recent Notebooks**: Table view of recent work with type badges and actions
- **Compute Clusters**: Status cards showing cluster information and controls
- **Navigation**: Intuitive sidebar with key sections (Home, Workspace, Data, SQL, Notebooks, etc.)

### ⚡ Interactive Features
- **Theme Toggle**: Switch between light and dark modes
- **Search Bar**: Global search functionality (Ctrl/Cmd + K)
- **Sidebar Navigation**: Active state tracking and smooth transitions
- **Notifications**: Toast-style notifications for user actions
- **Responsive Sidebar**: Mobile-friendly collapsible navigation
- **Keyboard Shortcuts**: Quick access via keyboard commands

### 🛠️ Technical Features
- Pure HTML, CSS, and JavaScript (no build tools required)
- Font Awesome icons for consistent iconography
- CSS variables for easy theming
- LocalStorage for theme persistence
- Mobile-first responsive design

## Getting Started

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Navigate to the project directory**:
   ```bash
   cd databricks-console
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser**:
   Navigate to `http://localhost:5000`

## Usage

### Navigation
- Use the **sidebar** to navigate between different sections
- Click on the **logo** to return to home
- Use the **workspace selector** to switch workspaces

### Search
- Click the search bar or press **Ctrl/Cmd + K** to focus
- Type to search for notebooks, files, tables, etc.

### Theme Toggle
- Click the **moon/sun icon** in the top-right corner
- Your preference is saved automatically

### Quick Actions
- Click any action card to start a new task:
  - **Create Notebook**: Start coding in Python, SQL, Scala, or R
  - **Import Data**: Upload files or connect to data sources
  - **Run Query**: Execute SQL queries
  - **Create Cluster**: Set up compute resources

### Notebooks
- View recent notebooks in the table
- Click **Open** to view a notebook
- Click **Share** to share with team members

### Clusters
- Monitor cluster status (Running/Stopped)
- **Start/Stop** clusters as needed
- View cluster details (workers, driver type, uptime)
- **Configure** cluster settings
- **Terminate** clusters when done

### Keyboard Shortcuts
- **Ctrl/Cmd + K**: Focus search bar
- **Ctrl/Cmd + B**: Toggle sidebar (mobile)

## Project Structure

```
databricks-console/
├── app.py                 # Flask server
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
└── public/               # Static files
    ├── index.html        # Main HTML file
    ├── styles.css        # CSS styles with theming
    └── script.js         # JavaScript for interactivity
```

## Customization

### Colors and Theming
Edit the CSS variables in `public/styles.css`:

```css
:root {
    --accent-primary: #ff3621;    /* Primary accent color */
    --accent-hover: #e62e1a;      /* Hover state */
    /* ... more variables ... */
}
```

### Adding New Pages
1. Create a new section in the sidebar
2. Add corresponding content in the main area
3. Update the navigation logic in `script.js`

### Styling
The application uses CSS variables for easy theming. Modify `styles.css` to customize:
- Colors and gradients
- Spacing and layout
- Typography
- Component styles

## Browser Support

- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Flask (Python)
- **Icons**: Font Awesome 6
- **Fonts**: System fonts (-apple-system, Segoe UI, etc.)

## Development

### Local Development
The Flask server runs in debug mode by default, providing:
- Auto-reload on file changes
- Detailed error messages
- Interactive debugger

### Production Deployment
For production, consider:
- Setting `debug=False` in `app.py`
- Using a production WSGI server (Gunicorn, uWSGI)
- Adding environment variable configuration
- Implementing proper authentication
- Adding backend API endpoints

## Features to Extend

This is a UI mockup that can be extended with:
- **Backend API**: Connect to actual data sources
- **Authentication**: User login and access control
- **Real Data**: Connect to databases and file systems
- **Notebook Editor**: Interactive code editor (CodeMirror, Monaco)
- **Job Scheduling**: Workflow automation
- **Real-time Updates**: WebSocket connections for live data
- **Data Visualization**: Charts and graphs (D3.js, Chart.js)

## License

This is a demo/educational project. Feel free to use and modify as needed.

## Acknowledgments

Inspired by the Databricks platform interface and modern data workspace design patterns.

