from socketIO_client import SocketIO, LoggingNamespace
import json
def on_connect():
    print('connect')


def on_message(data):
    jdata = json.loads(json.dumps(data) )
    print(data["sid"]+" said :"+jdata["message"])
    x = input()
    socketIO.emit("message", {"message": x})




socketIO = SocketIO('192.168.1.100', 80, LoggingNamespace)
socketIO.on('tomessage', on_message)

socketIO.emit("message",{"message":"hi"})
socketIO.wait()