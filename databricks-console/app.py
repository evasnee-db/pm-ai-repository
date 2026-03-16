from flask import Flask, send_from_directory, send_file
import os

app = Flask(__name__)

# Path to the public directory
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), 'public')

@app.route('/')
def index():
    """Serve the main index.html file"""
    return send_file(os.path.join(PUBLIC_DIR, 'index.html'))

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, images, etc.)"""
    return send_from_directory(PUBLIC_DIR, path)

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors by redirecting to index for client-side routing"""
    return send_file(os.path.join(PUBLIC_DIR, 'index.html'))

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Databricks Console Starting...")
    print("=" * 60)
    print(f"📂 Serving files from: {PUBLIC_DIR}")
    print("🌐 Open your browser and navigate to:")
    print("   http://localhost:5000")
    print("=" * 60)
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

