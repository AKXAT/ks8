from flask import Flask, render_template
from flask_cors import CORS
from routes import login_bp, dashboard_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard_page')
def dashboard_page():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)