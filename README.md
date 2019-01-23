# chatty 

A wechat app on terminal or cmd base on itchat.


## Login

Scan the qrcode to login. "@@ me: " means talk to yourself by default.

```
Please press confirm on your phone.
Log in time out, reloading QR code.
Getting uuid of QR code.
Downloading QR code.
███████████████████████████████████████
█              ██      █    ███  ██  ██
█  █████  ██  ███    ████  █  ███  ████
█  █      █  █          ██    █  ██    
█  █      █  █  █      ██  █  █  █    █
█  █      █  ██  █  ████  █  ██      █ 
█  █████  ███  ████  █  █      █  ██  █
█              █  █  █  █  █  █  █  █  
...

Please scan the QR code to log in.
Login successfully as ...

@@ me:
```

## Usage

```
@@ me: help

- @img@path				# send img
- @fil@path				# send file
- @vid@path				# send video

- cls                   # windows cls, linux clear
- who                   # show the detail information you are talking to
- open g                # show group message
- close g               # don't show group message
- show                  # show recently picture
- show f                # show friends list
- show g                # show group list
- call who/me           # talk to someone
- call g group          # talk to a group
- quit                  # quit

```

# Iris

You can control your laptop by WeChat. 

Example:

1. Send 'take a photo' to yourself, the laptop will make it done, and send the photo back. 
2. Send 'shooting a video' to yourself, the laptop will make it done, and send the video back.