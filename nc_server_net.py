import os
import random
from time import sleep
from flask import Flask, request, jsonify



app = Flask(__name__)
app.clients = list()
app.rooms = list()


@app.route('/connect', methods=['POST'])
def connection():
    print(app.clients)
    id = len(app.clients) + 1
    app.clients.append(id)
    
    print(request.get_json())
    
    return jsonify( {'id': id} )
    

@app.route('/enemy', methods=['POST'])
def enemy():
    if len(app.clients) == 0:
       return False
    else:
        client_id = request.get_json()['id']
        qty_clients = range(len(app.rooms))
        
        if len(app.rooms) > 0:
            for i in qty_clients:        
                if client_id in app.rooms[i][0]:
                    return jsonify( {'room_id': i, 'turn': 0} )
                elif client_id in app.rooms[i][1]:
                    return jsonify( {'room_id': i, 'turn': 1} )
        else:
            for i in qty_clients:
                if client_id != app.clients[i]:
                    app.rooms.append(client_id, app.clients[i], None)
                    return jsonify( {'room_id': i, 'turn': 0} )
                    


@app.route('/req/<room>', methods=['POST'])
def req():
   data = request.get_json()['data']
   room = request.args['room']
   
   app.rooms[room][2] = data
   
   return True
   

@app.route('/res/<room>', methods=['POST'])
def resp():
    room = request.args['room']
    result = app.rooms[room][2]
    
    return result
    

if __name__ == '__main__':
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
