import socketio
import eventlet
import base64
import json
import DBModel
import time

sio = socketio.Server(async_mode='eventlet')
app = socketio.Middleware(sio)
eventlet.monkey_patch()

connected = []

privatekey = None
publickey = None

@sio.on('config')
def my_custom_event(sid,message):
    print("Config")

    DBModel.Users.objects(DeviceId=message["deviceid"]).update_one(set__DeviceId=message["deviceid"],set__LastLogin=str(int(time.time())) , upsert=True)

    jdata = {
        "sid":sid,
        "deviceid":message["deviceid"]
    }
    connected.append(jdata)

    return json.dumps({"status":"ok","trackingCode":123})

@sio.on('getChats')
def my_custom_event(sid, data):

    chats = DBModel.Messages.objects(ChatId=data["chatId"])
    print(chats)
    arr = []
    for chat in chats:
        r_data = {
            "Text":chat.Text,
            "isHelper":chat.isHelper,
        }
        arr.append(r_data)
    print(arr)
    return arr


@sio.on('message')
def my_custom_event(sid, data):
    print("Config")
    encrypted = str_xor(data["message"],"Mohamad_171_FA_09382138446")

    decrypted = str_xor(encrypted,"Mohamad_171_FA_09382138446")

    data["sid"] = sid
    sio.emit("client_message",data)

def str_xor(s1, s2):
 return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(s1,s2)])

if __name__ == "__main__":

    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 4000)), app)