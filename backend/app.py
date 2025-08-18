from flask import Flask, jsonify
from flask_cors import CORS
from routes import routes


app = Flask(__name__)
CORS(app)  # Enables CORS for all routes
app.register_blueprint(routes) # what does register mean? it means that the routes defined in the routes module will be available in the app 

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
    print(app.url_map)
    app.run(debug=True)