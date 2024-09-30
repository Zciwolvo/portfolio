from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, render_template, make_response
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta

from user_data import User

bcrypt = Bcrypt()
auth_blueprint = Blueprint('auth', __name__)


# Route to display the login page
@auth_blueprint.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# Register a new user
@auth_blueprint.route('/register', methods=['POST'])
def register_user():
    user_data = request.form  # Use request.form for form data

    # Check if the user already exists
    user = User.load_from_json(user_data['username'])
    if user:
        return jsonify({'message': 'User already exists'}), 400

    # Hash and salt the password before storing it
    hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')

    # Create a new user with the hashed password
    user = User(
        username=user_data['username'],
        password=hashed_password,
        role='user'
    )
    user.save_to_json()
    return jsonify({'message': 'User registered successfully'}), 201

# Route to display the login page
@auth_blueprint.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Login
@auth_blueprint.route('/login', methods=['POST'])
def login():
    user_data = request.form  # Assuming form data with username and password

    # Check if the user exists
    user = User.load_from_json(user_data['username'])
    if not user or not bcrypt.check_password_hash(user.password, user_data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Calculate the expiration delta (one year from the current date)
    expires_delta = timedelta(days=365)

    # Generate an access token using JWT with the specified expiration delta
    access_token = create_access_token(identity=user.to_dict(), expires_delta=expires_delta)

    # Create a JSON response with the access token
    response_data = {'access_token': access_token}

    # Create a response object
    response = make_response(jsonify(response_data), 200)

    # Set the access token as an HTTP-only cookie
    response.set_cookie('access_token', value=access_token, httponly=True)

    return response

# Homepage accessible after login
@auth_blueprint.route('/home', methods=['GET'])
@jwt_required()
def home():
    current_user = get_jwt_identity()
    return jsonify({'message': 'Welcome to the home page', 'user': current_user}), 200
