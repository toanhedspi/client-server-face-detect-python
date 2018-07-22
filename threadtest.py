import _thread
import time

def func_1(delay):
    while True:
        time.sleep(delay)
        print("1")

def func_2(delay):
    while True:
        time.sleep(delay)
        print("2")

try:
    _thread.start_new_thread(func_1, (1,))
    _thread.start_new_thread(func_2, (2,))
except:
    print("Error")

while 1:
    pass
