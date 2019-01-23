import os
import cv2
import time
import datetime


dir_img = 'img'
dir_video = 'video'
for d in [dir_img, dir_video]:
    if not os.path.exists(d):
        os.mkdir(d)


def demo():
    cap = cv2.VideoCapture(0)
    i = 0
    while(1):
        ret, frame = cap.read()
        k = cv2.waitKey(1)
        if k == 27:
            break
        elif k == ord('s'):
            cv2.imwrite('img/' + str(i) + '.jpg', frame)
            i += 1
        frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_CUBIC)
        cv2.imshow("capture", frame)
    cap.release()


def takePhoto():
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_CUBIC)
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    img = '%s/%s.jpg' % (dir_img, ts)
    cv2.imwrite(img, frame)
    cap.release()
    return img


def shooting():
    cap = cv2.VideoCapture(0)
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    video = '%s/%s.mp4' % (dir_video, ts)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(video, fourcc, fps, size)
    i = 0
    while i < (fps * 8):
        i += 1
        ret, frame = cap.read()
        cv2.putText(frame, str(i), (10, 20), cv2.FONT_HERSHEY_PLAIN,
                    1, (0, 255, 0), 1, cv2.LINE_AA)
        out.write(frame)
    out.release()
    cap.release()
    return video


if __name__ == '__main__':
    # demo()
    takePhoto()
    # shooting()
