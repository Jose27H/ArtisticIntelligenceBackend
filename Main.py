from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from google.oauth2 import id_token
from google.auth.transport import requests

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Replace this with your Web Client ID from Google Cloud Console
CLIENT_ID = "106905994125-blt7hpufeifo2lt46gafm8frf9fmaed5.apps.googleusercontent.com"

# Replace this with your PostgreSQL connection URL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:dEuOkPJxLBZbVAmThWQzjcordfOVBNdw@postgres.railway.internal:5432/railway"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# User model for PostgreSQL
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing user ID
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique user email
    name = db.Column(db.String(120), nullable=True)  # User's name

    def __init__(self, email, name):
        self.email = email
        self.name = name


@app.route('/login', methods=['POST'])
def login():
    # Get the ID token from the request body
    data = request.get_json()
    token = data.get('token')

    if not token:
        print("token not")
        return jsonify({"error": "ID Token is missing"}), 400

    try:
        # Verify the token with Google's public keys
        id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # Extract user information from the token
        email = id_info['email']
        name = id_info.get('name', 'Unknown')

        # Check if the user already exists in the database
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            print(f"User already exists: {existing_user.email}")
            user_id = existing_user.id
        else:
            # Add a new user to the database
            print(f"Creating new user: {email}")
            new_user = User(email=email, name=name)
            db.session.add(new_user)
            db.session.commit()  # Ensure the transaction is committed
            user_id = new_user.id
            print(f"New user created with ID: {user_id}")

        # Return a success response with user details
        return jsonify({
            "message": "Login successful",
            "user_id": user_id,
            "email": email,
            "name": name
        }), 200

    except ValueError as e:
        # Invalid token
        print(f"Token verification failed: {e}")
        return jsonify({"error": "Invalid ID Token"}), 401

    except Exception as e:
        # Log unexpected errors
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500



# Endpoint: Message
@app.route('/message', methods=['POST'])
def message():
    # Check if the request contains JSON data
    if request.is_json:
        # Extract JSON data
        data = request.get_json()

        # Extract the message from the request
        message = data.get("message", "No message provided")

        # Log the received data to the console
        print(f"Received message: {message}")

        # Respond back with the received message
        return jsonify({"response": f"You sent: {message}"}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400


# Initialize the database
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the 'users' table if it doesn't already exist
    app.run(debug=True, host='0.0.0.0', port=5000)
