from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    message = "Welcome to Daily Digest Backend!"
    status = "success"
    version = "1.0.0"
    return jsonify({
        "message": message,
        "status": status,
        "version": version
    })

if __name__ == '__main__':
    app.run(debug=True)