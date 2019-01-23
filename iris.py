import os
import datetime
import platform
import util
import itchat
from itchat.content import *

# -----------------------

absdir = os.path.abspath('.')

# set user's nick name
myNick = 'nick1'
user1Nick = 'nick2'
user_list = [myNick, user1Nick]

# set your commands
take_photo_cmds = ['tp', 'tpx']
shooting_video_cmds = ['shoot']

# -----------------------


@itchat.msg_register(TEXT)
def cmd_handler(msg):
    fromNick = msg.user.nickName
    if fromNick in user_list:
        if msg.text in take_photo_cmds:
            ret = util.takePhoto()
            ret = '@img@%s/%s' % (absdir, ret)
        elif msg.text in shooting_video_cmds:
            ret = util.shooting()
            ret = '@vid@%s/%s' % (absdir, ret)
        else:
            return

        myself.send(ret)
        user1.send(ret)

        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        name = fromNick if fromNick == myself else 'self'
        log = '[%s] %-5s %s' % (dt, name, ret)
        print(log)


cmd_qr = True if platform.system() == "Windows" else 2
itchat.auto_login(hotReload=True,
                  enableCmdQR=cmd_qr,
                  statusStorageDir='mychat.pkl')

myself = itchat.search_friends(nickName=myNick)[0]
user1 = itchat.search_friends(nickName=user1Nick)[0]

sayhi = 'iris online !'
# myself.send(sayhi)
# user1.send(sayhi)
itchat.send(sayhi)

itchat.run()
