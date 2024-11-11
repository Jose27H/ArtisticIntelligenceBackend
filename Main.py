from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/message', methods=['POST'])
def message():
    # Check if the request contains JSON data
    if request.is_json:
        # Extract JSON data
        data = request.get_json()
        # Log data to the console
        print(f"Received message: {data}")
        # Respond to the client
        return jsonify({"response": "Message received"}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
