import os, random, time
from flask import Flask, request, jsonify


app = Flask(__name__)
user_stack = []


@app.route('/', methods = ['POST'])
def index():
    if len(user_stack) > 9:
        return jsonify({'message': 'server is full'})

    global user_stack
    headers = request.headers
    req = request.get_json()

    while True:
        api_key = random.randint(1,10)
        if api_key not in user_stack:
            user_stack.append(api_key)
            break

    response ={'key': str(api_key)}

    print('request to server:', req)
    print("server's response:", response)
    return jsonify(response)


@app.route('/search_enemy', methods = ['POST'])
def search_for_enemy():
    req = request.get_json()
    if 0 < int(req['key']) < 11:
        if len(user_stack) > 1:
            while True:
                enemy = random.choice(user_stack)
                if req['key'] != enemy:
                    response = {'enemy_key': enemy}
                    return jsonify(response)
        else: return None

# для пробной игры
buffer = None

@app.route('/req', methods = ['POST'])
def get_req():
    global buffer
    buffer = request.get_json()
    print(buffer)
    return jsonify({'message': 'success'})
    
@app.route('/res', methods=['POST'])
def send_res():
    global buffer
    return jsonify(buffer)


if __name__ == '__main__':
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
