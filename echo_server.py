import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import time
import face_analyze
import o_facerec_from_video_file as facerec

HOST=''
PORT=8089

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('Socket created')

s.bind((HOST,PORT))
print ('Socket bind complete')
s.listen(10)
print ('Socket now listening')

conn,addr=s.accept()

### init video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter('sent_video.avi', fourcc, 29.97, (640, 480))
count = 1
temp_face_name = "Unknown"

print ('Client\'s connected', count)

while True:
    face_names = []
    
    data = b''
    payload_size = int.from_bytes(conn.recv(1),byteorder='little')

    while len(data) < payload_size:
        data += conn.recv(512)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("i", packed_msg_size)[0]

    while len(data) < msg_size:
        if ((len(data)+512) > msg_size):
            data += conn.recv(msg_size - len(data))
        else:
            data += conn.recv(512)

    face_encodings_data = data[:msg_size]
    # data = data[msg_size:]
    ###

    face_encodings = pickle.loads(face_encodings_data)
    # print(face_analyze.face_match(face_encodings))
    face_names = face_analyze.face_match(face_encodings)
    if (face_names != temp_face_name):
        print("Face detected")
        temp_face_name = face_names

    return_data = pickle.dumps(face_names)
    size = struct.pack("i", len(return_data))
    conn.send(bytes([struct.calcsize('i')])+size+return_data)


    # output_movie.write(frame)
    count+=1

# input_movie.release()
# cv2.destroyAllWindows()
