from flask import Blueprint, request, jsonify
import requests

login_bp = Blueprint('login', __name__)
dashboard_bp = Blueprint('dashboard', __name__)

USERS_SERVICE_URL = 'http://users-service:8000'


@login_bp.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    if not request_data:
        return jsonify({'message': 'Invalid request'}), 400

    username = request_data.get('username')
    password = request_data.get('password')

    if username == 'admin' and password == 'password':
        return jsonify({'message': 'Login successful'}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


@dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        response = requests.get(f'{USERS_SERVICE_URL}/users', timeout=3)
        response.raise_for_status()
        users = response.json()
        return jsonify({'users': users}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({
            'message': 'Users service unavailable',
            'error': str(e)
        }), 503


@dashboard_bp.route('/update_dashboard', methods=['POST'])
def update_dashboard():
    request_data = request.get_json()
    if not request_data:
        return jsonify({'message': 'Invalid request'}), 400

    new_user = {
        "name": request_data.get('name'),
        "email": request_data.get('email')
    }

    if not new_user['name'] or not new_user['email']:
        return jsonify({'message': 'Name and email required'}), 400

    try:
        response = requests.post(
            f'{USERS_SERVICE_URL}/add_user',
            json=new_user,
            timeout=3
        )
        response.raise_for_status()
        return jsonify({'message': 'Dashboard updated with new user'}), 201

    except requests.exceptions.RequestException as e:
        return jsonify({
            'message': 'Failed to update dashboard',
            'error': str(e)
        }), 503
