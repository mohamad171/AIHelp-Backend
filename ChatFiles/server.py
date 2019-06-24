import socketio
import eventlet
import base64
import json
import DBModel
import time

from datetime import datetime
from difflib import SequenceMatcher


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
    arr = []
    for chat in chats:
        r_data = {
            "Text":chat.Text,
            "isHelper":chat.isHelper,
            "AddDate": str(chat.AddDate.strftime("%H:%M"))
        }
        arr.append(r_data)
    return arr


@sio.on('message')
def my_custom_event(sid, data):
    encrypted = str_xor(data["message"],"Mohamad_171_FA_09382138446")

    decrypted = str_xor(encrypted,"Mohamad_171_FA_09382138446")
    mesages = DBModel.Messages.objects()

    chat = DBModel.Chats.objects.get(id=data["ChatId"])
    message = DBModel.Messages()
    message.ChatId = chat
    message.isHelper = data["isHelper"]
    message.MessageType = data["type"]
    message.isAI = False
    message.Text = data["message"]
    message.AddDate = datetime.now()
    message.save()
    data["sid"] = sid
    data["addDate"] = datetime.now().strftime("%H:%M")
    sio.emit("client_message", data)

    if data["isHelper"] != True:
        best = ""
        helpers = DBModel.MessageHelper.objects()
        for message in helpers:
            if similar(message.Question,data["message"]) >= 0.7:
                best = message.Answer
        if best != "":
            chat = DBModel.Chats.objects.get(id=data["ChatId"])
            message = DBModel.Messages()
            message.ChatId = chat
            message.isHelper = True
            message.MessageType = data["type"]
            message.isAI = True
            message.Text = best
            message.AddDate = datetime.now()
            message.save()

            data["message"] = best
            data["isHelper"] = True
            data["sid"] = sid
            data["addDate"] = datetime.now().strftime("%H:%M")
            sio.emit("client_message", data)


def str_xor(s1, s2):
 return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(s1,s2)])

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

if __name__ == "__main__":

    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 4000)), app)