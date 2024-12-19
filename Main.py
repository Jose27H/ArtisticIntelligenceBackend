import os
from requestHelper import generateRequest, sketchRequest, styleRequest, outpaintRequest
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from google.oauth2 import id_token
from google.auth.transport import requests
from flask import send_file

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Replace this with your Web Client ID from Google Cloud Console
CLIENT_ID = "106905994125-blt7hpufeifo2lt46gafm8frf9fmaed5.apps.googleusercontent.com"
SD_API_KEY = "sk-7pxhh6aU3wEzQW9VCTqbiDASmMMXgQhUmw7PbedAimUyOjVl"#os.environ.get('SD_API_KEY')

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


# Image model for PostgreSQL
class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to users table
    image = db.Column(db.LargeBinary, nullable=False)  # Binary data for the image
    date = db.Column(db.DateTime, default=db.func.now(), nullable=False)  # Auto-generated timestamp

    def __init__(self, user_id, image):
        self.user_id = user_id
        self.image = image



@app.route('/login', methods=['POST'])
def login():
    print("login init")
    # Get the ID token from the request body
    data = request.get_json()
    token = data.get('token')

    if not token:
        
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
    

@app.route('/loadName', methods=['POST'])
def load_name():
    try:
        # Parse the JSON payload from the request
        data = request.get_json()
        user_id = data.get('user_id')

        # Check if the Google ID is provided
        if not user_id:
            return jsonify({"error": "Google ID is missing"}), 400

        # Query the database for the user with the given Google ID
        user = User.query.filter_by(id=user_id).first()

        if user:
            # Return the user's name
            return jsonify({"name": user.name}), 200
        else:
            # User not found
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        # Log unexpected errors and return a 500 error
        print(f"Error in /loadName: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/generate', methods=['POST'])
def generate():
    #Requires: prompt, aspect_ratio, filetype, user_id
    #Optional: negative_prompt, seed
    try:
        # Parse the JSON payload from the request
        data = request.get_json()
        prompt = data.get('prompt')
        negative_prompt = data.get('negative_prompt')
        if negative_prompt == "":
            negative_prompt = None
        aspect_ratio = data.get('aspect_ratio')
        filetype = data.get('filetype')
        seed = int(data.get('seed'))
        if seed == "":
            seed = 42 # If no seed is provided, use 42 because it's the answer to everything
        user_id = data.get('user_id')
        # Check if the Google ID is provided
        if not user_id:
            return jsonify({"error": "Google ID is missing"}), 400

        # Query the database for the user with the given Google ID
        user = User.query.filter_by(id=user_id).first()
        if not os.path.exists("output"):
            os.makedirs("output")
        if user:
            generateRequest(SD_API_KEY, prompt, negative_prompt, f"output/{user_id}", filetype, aspect_ratio, seed)
            return send_file (
                f"output/{user_id}.{filetype}",
                mimetype='image/*',
                as_attachment=True,
                download_name=f"output.{filetype}"
            )
        else:
            # User not found
            return jsonify({"error": "User not found"}), 404
        

        

    except Exception as e:
        # Log unexpected errors and return a 500 error
        print(f"Error in /generate: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/sketch', methods=['POST'])
def sketch():
    #Requires: prompt, control_strength, filetype, user_id, b64String
    #Optional: negative_prompt, seed
    try:
        # Parse the JSON payload from the request
        data = request.get_json()
        prompt = data.get('prompt')
        negative_prompt = data.get('negative_prompt')
        if negative_prompt == "":
            negative_prompt = None
        control_strength = float(data.get('control_strength'))
        filetype = data.get('filetype')
        seed = int(data.get('seed'))
        if seed == "":
            seed = 42 # If no seed is provided, use 42 because it's the answer to everything
        user_id = data.get('user_id')
        b64String = data.get('b64String')
        # Check if the Google ID is provided
        if not user_id:
            return jsonify({"error": "Google ID is missing"}), 400

        # Query the database for the user with the given Google ID
        user = User.query.filter_by(id=user_id).first()
        if not os.path.exists("output"):
            os.makedirs("output")
        if user:
            sketchRequest(SD_API_KEY, prompt, negative_prompt, f"output/{user_id}", filetype, b64String, control_strength, seed)
            return send_file (
                f"output/{user_id}.{filetype}",
                mimetype='image/*',
                as_attachment=True,
                download_name=f"output.{filetype}"
            )
        else:
            # User not found
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        # Log unexpected errors and return a 500 error
        print(f"Error in /sketch: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/style', methods=['POST'])
def style():
    #Requires: prompt, filetype, user_id, b64String, fidelity
    #Optional: negative_prompt, seed
    try:
        # Parse the JSON payload from the request
        data = request.get_json()
        prompt = data.get('prompt')
        negative_prompt = data.get('negative_prompt')
        if negative_prompt == "":
            negative_prompt = None
        fidelity = float(data.get('fidelity'))
        filetype = data.get('filetype')
        seed = int(data.get('seed'))
        if seed == "":
            seed = 42 # If no seed is provided, use 42 because it's the answer to everything
        user_id = data.get('user_id')
        b64String = data.get('b64String')
        # Check if the Google ID is provided
        if not user_id:
            return jsonify({"error": "Google ID is missing"}), 400

        # Query the database for the user with the given Google ID
        user = User.query.filter_by(id=user_id).first()
        if not os.path.exists("output"):
            os.makedirs("output")
        if user:
            styleRequest(SD_API_KEY, prompt, negative_prompt, f"output/{user_id}", filetype, b64String, fidelity, seed)
            return send_file (
                f"output/{user_id}.{filetype}",
                mimetype='image/*',
                as_attachment=True,
                download_name=f"output.{filetype}"
            )
        else:
            # User not found
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        # Log unexpected errors and return a 500 error
        print(f"Error in /style: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
    
def save_image(user_id, base64_image):
    try:
        # Decode Base64 image string into binary data
        image_data = base64.b64decode(base64_image)

        # Verify if the user exists
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {"error": "User not found"}, 404

        # Save the image to the database
        new_image = Image(user_id=user_id, image=image_data)
        db.session.add(new_image)
        db.session.commit()

        return {"message": "Image saved successfully", "image_id": new_image.id}, 200

    except Exception as e:
        print(f"Error in save_image: {e}")
        return {"error": "Internal server error"}, 500

@app.route('/outpaint', methods=['POST'])
def outpaint():
    #Required: filetype, creativity, user_id, b64String, (left&&right&&up&&down != ""||0)
    #Optional: seed, prompt, every other direction
    try:
        # Parse the JSON payload from the request
        data = request.get_json()
        prompt = data.get('prompt')
        filetype = data.get('filetype')
        seed = int(data.get('seed'))
        if seed == "":
            seed = 42 # If no seed is provided, use 42 because it's the answer to everything
        user_id = data.get('user_id')
        b64String = data.get('b64String')
        try:
            left = int(data.get('left'))
        except:
            left = 0
        try:
            right = int(data.get('right'))
        except:
            right = 0
        try:
            up = int(data.get('up'))
        except:
            up = 0
        try:
            down = int(data.get('down'))
        except:
            down = 0
        creativity = float(data.get('creativity'))
        # Check if the Google ID is provided
        if not user_id:
            return jsonify({"error": "Google ID is missing"}), 400

        # Query the database for the user with the given Google ID
        user = User.query.filter_by(id=user_id).first()
        if not os.path.exists("output"):
            os.makedirs("output")
        if user:
            outpaintRequest(SD_API_KEY, prompt, left, right, up, down, b64String, f"output/{user_id}", filetype, creativity, seed)
            return send_file (
                f"output/{user_id}.{filetype}",
                mimetype='image/*',
                as_attachment=True,
                download_name=f"output.{filetype}"
            )
        else:
            # User not found
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        # Log unexpected errors and return a 500 error
        print(f"Error in /outpaint: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Initialize the database
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the 'users' table if it doesn't already exist
    app.run(debug=True, host='0.0.0.0', port=5000)
