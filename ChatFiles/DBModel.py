from mongoengine import *
import time
import datetime

# connect("aihelp",host="localhost",port=8085,username="mohamad171",password="09382138446",authentication_source="admin")
connect("aihelp",host="localhost")


class Users(Document):
    DeviceId = StringField(required=True)
    LastLogin = StringField(required=True)

class Helpers(Document):
    Name = StringField(required=True)
    Email = StringField(required=True)
    Password = StringField(required=True)
    isActive = BooleanField(required=True)

    CreateDate = StringField(default= str(int(time.time())) )

class WebsiteUsers(Document):
    Fname = StringField(required=True)
    Lname = StringField(required=True)
    PhoneNumber = StringField()
    Email = EmailField(required=True)
    Password = StringField(required=True)
    isActive = BooleanField(default=False,required=True)
    Credit = IntField(required=True)
    CreateDate = StringField(default=str(int(time.time())))
    LastLogin = StringField()

class Applications(Document):
    Owner = ReferenceField(WebsiteUsers,required=True)
    AppName = StringField(required=True)
    PackageName = StringField(required=True)
    AllowUsers = ListField(ReferenceField(Helpers))
    Credit = IntField(required=True)

class Chats(Document):
    App = ReferenceField(Applications,required=True)
    Helper = ReferenceField(Helpers)
    User = ReferenceField(Users,required=True)
    TrackingId = StringField(required=True)
    isAccept = BooleanField(default=False)
    isClosed = BooleanField(default=False)
    AdditionalFields = StringField(required=True)
    BackUpEmail = StringField()
    CreateDate = StringField(default=str(int(time.time())))

class Messages(Document):
    ChatId = ReferenceField(Chats,required=True)
    isHelper = BooleanField(required=True)
    MessageType = StringField(required=True)
    isAI = BooleanField()
    Text = StringField()
    FileId = StringField()
    AddDate = DateTimeField(default=datetime.datetime.now())

class MessageHelper(Document):
    App = ReferenceField(Applications, required=True)
    Question = StringField(required=True)
    Answer = StringField(required=True)
    CreateDate = StringField(default=str(int(time.time())))
    meta = {'indexes': [
        {'fields': ['$Question'],

         'weights': {'Question': 5}
         }
    ]}

class Files(Document):
    FileType = StringField(required=True)
    UploadDate = StringField(default=str(int(time.time())))
    filePath = StringField(required=True)
    FileName = StringField(required=True)






