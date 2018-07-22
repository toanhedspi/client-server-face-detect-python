import cv2
import numpy as np
import socket
import sys
import pickle
import _thread
import struct ### new code
import face_analyze
import time
import o_facerec_from_video_file as facerec

# face_cascade = cv2.CascadeClassifier("/home/toan/Downloads/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_default.xml")

cap=cv2.VideoCapture(0)

clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8089))
process_this_frame = True
face_encodings = []
name = "Unknown"

def show():

    while True:
        ret, img = cap.read()
        global name
        global face_encodings
        # print(name)
        frame, face_encodings = face_analyze.face_detect(img, name)

        cv2.imshow('img',frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

def send():
    while True:
        global face_encodings

        if face_encodings:

            data = pickle.dumps(face_encodings)
            size = struct.pack("i", len(data))
            clientsocket.sendall(bytes([struct.calcsize('i')])+size+data)


def recv():
    global name
    names = []
    data = b''
    payload_size = int.from_bytes(clientsocket.recv(1),byteorder='little')
    while len(data) < payload_size:
        data += clientsocket.recv(4)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("i", packed_msg_size)[0]

    while len(data) < msg_size:
        if ((len(data)+4) > msg_size):
            data += clientsocket.recv(msg_size - len(data))
        else:
            data += clientsocket.recv(4)

    names_data = data[:msg_size]
    names = pickle.loads(names_data)
    name = names[0]

try:
    _thread.start_new_thread(send,())
    _thread.start_new_thread(recv,())
except:
    print("error")

while 1:
    show()

cv2.destroyAllWindows()
