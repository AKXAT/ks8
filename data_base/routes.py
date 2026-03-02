from flask import Blueprint, jsonify, request
import json
import os
from json import JSONDecodeError

user_bp = Blueprint('user', __name__)

USERS_FILE = 'users.json'


def load_users():
    if not os.path.exists(USERS_FILE):
        return []

    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except JSONDecodeError:
        return []


def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)


@user_bp.route('/users', methods=['GET'])
def get_users():
    users = load_users()
    return jsonify(users), 200


@user_bp.route('/add_user', methods=['POST'])
def add_user():
    users = load_users()

    request_data = request.get_json()
    new_user = {
        "id": len(users) + 1,
        "name": request_data['name'],
        "email": request_data['email']
    }

    users.append(new_user)
    save_users(users)

    return jsonify(new_user), 201
