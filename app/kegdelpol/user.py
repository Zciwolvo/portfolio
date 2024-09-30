from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/edit_profile', methods=['PUT'])
@jwt_required()
def edit_user_profile():
    current_user = get_jwt_identity()
    # Implement your edit profile logic here
    return jsonify({'message': 'Profile edited successfully'}), 200

@user_blueprint.route('/change_username', methods=['PUT'])
@jwt_required()
def change_username():
    current_user = get_jwt_identity()
    # Implement your change username logic here
    return jsonify({'message': 'Username changed successfully'}), 200

@user_blueprint.route('/change_password', methods=['PUT'])
@jwt_required()
def change_password():
    current_user = get_jwt_identity()
    # Implement your change password logic here
    return jsonify({'message': 'Password changed successfully'}), 200

@user_blueprint.route('/delete_account', methods=['DELETE'])
@jwt_required()
def delete_account():
    current_user = get_jwt_identity()
    # Implement your delete account logic here
    return jsonify({'message': 'Account deleted successfully'}), 200