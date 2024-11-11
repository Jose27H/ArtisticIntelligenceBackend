from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message():
    # You can process the message here if you want to
    return jsonify({"response": "You are gay"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
