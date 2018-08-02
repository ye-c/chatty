import threading
import os
import signal
import time
import platform
import readline
import itchat
from itchat.content import *
from PIL import Image

MsgType_Dict = {3: 'img', -1: 'file'}
download_dir = 'download'
is_open_group = True
imgshow = ''
itchat_status = False


def format_print(nickName='', remarkName='', content='', msgtype='', isGroupChat=False):
    tnow = time.strftime('%H:%M:%S', time.localtime(time.time()))
    msgtype = '[%s] ' % msgtype if msgtype else ''
    if isGroupChat:
        print('\r%s | [%s] %s: %s%s\n' %
              (tnow, nickName, remarkName, msgtype, content))
    else:
        print('\r%s | %s%s: %s%s\n' %
              (tnow, nickName, ' (%s)' % remarkName if remarkName.strip() else '',
               msgtype, content))


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isFriendChat=True)
def print_friend_msg(msg):
    if msg.ToUserName == 'filehelper':
        print('\r>> filehelper: %s\n' % msg.content)
    elif 'userName' in msg.User:
        format_print(nickName=msg.User['userName'], content=msg.content)
    else:
        format_print(msg.User.NickName, msg.User.RemarkName, msg.content)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def download_friend_files(msg):
    tnow = time.strftime('%y%m%d%H%M%S', time.localtime(time.time()))
    filename = '%s.%s' % (tnow, msg.fileName.split('.')[1])
    typename = MsgType_Dict[
        msg.MsgType] if msg.MsgType in MsgType_Dict else MsgType_Dict[-1]
    if msg.ToUserName == 'filehelper':
        path = '%s/filehelper-%s' % (download_dir, filename)
        print('\r>> filehelper: [%s] %s\n' % (typename, filename))
    else:
        path = '%s/%s-%s' % (download_dir, msg.User.NickName, filename)
        format_print(msg.User.NickName, msg.User.RemarkName,
                     filename, typename)
    if typename == 'img':
        global imgshow
        imgshow = path
    msg.download(path)


@itchat.msg_register([TEXT, NOTE, SHARING], isGroupChat=True)
def print_group_msg(msg):
    if is_open_group:
        format_print(msg.User.NickName, msg.actualNickName, msg.text, '', True)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def download_group_files(msg):
    tnow = time.strftime('%y%m%d%H%M%S', time.localtime(time.time()))
    filename = '%s.%s' % (tnow, msg.fileName.split('.')[1])
    typename = MsgType_Dict[
        msg.MsgType] if msg.MsgType in MsgType_Dict else MsgType_Dict[-1]
    path = '%s/%s-%s-%s' % (download_dir, msg.User.NickName,
                            msg.actualNickName, filename)
    if typename == 'img':
        global imgshow
        imgshow = path
    if is_open_group:
        format_print(msg.User.NickName, msg.actualNickName,
                     filename, typename, True)
    msg.download(path)


@itchat.msg_register('Note')
def get_note(msg):
    if any(s in msg['Text'] for s in (u'红包', u'转账')):
        format_print(msg.User.NickName, msg.User.RemarkName, msg.Text, '红包')
        format_print(msg.User.NickName, msg.User.RemarkName, msg.Text, '红包')
        format_print(msg.User.NickName, msg.User.RemarkName, msg.Text, '红包')
    else:
        format_print(msg.User.NickName, msg.User.RemarkName,
                     msg.Text, 'Note')


def clear():
    msg = 'cls' if platform.system() == "Windows" else 'clear'
    os.system(msg)


def showFriends(switch):
    fls = itchat.get_friends()
    for p in fls:
        print('NickName: %-25s RemarkName: %s' %
              (p.NickName, p.RemarkName))
    return switch - 1


def showGroups(switch):
    gls = itchat.get_chatrooms()
    for g in gls:
        print('--', g.NickName)
    return switch - 1


def searchFriend(user_code, switch):
    f = itchat.search_friends(userName=user_code)
    if f:
        for k, v in f.items():
            print('%-20s: %s' % (k, v))
    return switch - 1


def call(toWho, UserCode, cmd, switch):
    content = cmd.split(' ')
    if len(content) == 2:
        name = content[1] if content[1] != 'me' else me
        ser_who = itchat.search_friends(name=name)
        if ser_who:
            toWho = content[1]
            UserCode = ser_who[0]['UserName']
            print('->', toWho)
        else:
            print('->', 'Non-existent Friend')
    elif len(content) == 3:
        ser_group = itchat.get_chatrooms()
        if ser_group:
            for g in ser_group:
                if g.NickName == content[2]:
                    toWho = g.NickName
                    UserCode = g.UserName
                    print('->', toWho)
                    break
        else:
            print('-> Non-existent Group')
    return switch - 1, toWho, UserCode


def show(imgshow, switch):
    try:
        img = Image.open(imgshow)
        img.show()
    except:
        pass
    return switch - 1


def count(n):
    n += 1
    if n == 3:
        n = 0
        clear()
    return n


def itchat_run():
    global itchat_status
    n = 0
    while True:
        if n > 10:
            tnow = time.strftime('%H:%M:%S', time.localtime(time.time()))
            print('\r%s | Login times exceeded limit, log out!' % tnow)
            itchat_status = False
            break
        if itchat_status is False:
            cmd_qr = True if platform.system() == "Windows" else 2
            itchat.auto_login(hotReload=True, enableCmdQR=cmd_qr,
                              statusStorageDir='mychat.pkl')
            itchat_status = True

        try:
            itchat.run()
        except Exception as e:
            print(e)
            break
        finally:
            itchat_status = False
            
        n += 1
        tnow = time.strftime('%H:%M:%S', time.localtime(time.time()))
        print('\r%s | Wait for 10 seconds to reload. ' % tnow)
        time.sleep(10)


if __name__ == '__main__':
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    cmd_qr = True if platform.system() == "Windows" else 2
    itchat.auto_login(hotReload=True, enableCmdQR=cmd_qr,
                      statusStorageDir='mychat.pkl')
    itchat_status = True
    wechat = threading.Thread(target=itchat_run, args=())
    wechat.setDaemon(True)
    wechat.start()

    switch = 0
    me = itchat.search_friends()
    me = me.NickName
    toWho, UserCode = 'me', None
    while True:
        switch = count(switch)
        msg = input('\n@@ %s: ' % toWho)
        if msg == 'quit' or itchat_status is False:
            break
        elif msg == 'help':
            print()
            print('- @img@path')
            print('- @fil@path')
            print('- @vid@path')
            print()
            print('- cls')
            print('- who')
            print('- open g')
            print('- close g')
            print('- show')
            print('- show f')
            print('- show g')
            print('- call who/me')
            print('- call g group')
            print('- quit')
            switch -= 1
        elif msg == 'cls':
            clear()
        elif msg == 'open g':
            is_open_group = True
            print('-> is_open_group is %s' % is_open_group)
        elif msg == 'close g':
            is_open_group = False
            print('-> is_open_group is %s' % is_open_group)
        elif msg == 'who':
            switch = searchFriend(UserCode, switch)
        elif msg == 'show':
            switch = show(imgshow, switch)
        elif msg == 'show f':
            switch = showFriends(switch)
        elif msg == 'show g':
            switch = showGroups(switch)
        elif msg.split(' ')[0] == 'call':
            switch, toWho, UserCode = call(toWho, UserCode, msg, switch)
        else:
            itchat.send(msg, toUserName=UserCode)
