from flask import request, Blueprint

token_blueprint = Blueprint('token', __name__)

@token_blueprint.route('/get_data', methods=['GET'])
def get_data():
    # Retrieve the value of the 'code' parameter from the URL
    code = request.args.get('code')

    if code:
        return f'The value of the "code" parameter is: {code}'
    else:
        return 'No code parameter provided in the URL'

