"""
FLASK(pip install Flask)
"""
import os
from flask import Flask, request,jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return 'Hey, you are connected'


@app.route('/move', methods=['POST'])
def move():
    json = request.json
    print(json)
    return jsonify(json)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True
        )