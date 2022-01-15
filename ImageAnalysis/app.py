import socketio
import eventlet
import json

sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):  ## session ID (), dictionary with details of client request
    print(sid, " connected")
    print(environ)

@sio.event
def my_message(sid, data):
    print('message :', data)
    print("sid: ", sid)
    dic = { "we": "did", "it": "!"}
    data = data.split()
    jdata = json.dumps(data)
    jdata2 = json.dumps(dic)
    sio.emit("greetings", jdata2)

@sio.event
def Hello(sid, data):
    print('message :', data)

@sio.event
def disconnect(sid):
    print(sid, " disconnected")


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 3050)), app)
