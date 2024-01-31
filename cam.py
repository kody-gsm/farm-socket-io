import socket
import cv2

server = ''
port = ''

soc =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cv2.waitKey(33) < 0:

    ret,frame  =cam.read()
    cv2.imshow('cam',frame)

    d =frame.flatten()
    s=d.tostring()
