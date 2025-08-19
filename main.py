import os
import sys
# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, render_template, request
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.wildfire import wildfire_bp

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), 'static'),
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(wildfire_bp, url_prefix='/api/wildfire')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# --- Routes for HTML pages ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ai', methods=['GET', 'POST'])
def ai():
    result = None
    if request.method == 'POST':
        user_input = request.form.get('user_input')

        result = f"Processed: {user_input}" 
    return render_template('ai.html', result=result)

# --- Serve static files ---
@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

# --- Catch-all fallback for unknown paths ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=True)
