import socket
import threading
import time
import pickle

server_name = socket.gethostbyname(socket.gethostname())
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_name, 8686))

global client_number
client_number = 0
global vector_clock
vector_clock = [1, 0, 0]


def send():
    while True:
        print("Before sending data : ", vector_clock[0:3])
        vector_clock.append(client_number)
        data = pickle.dumps(vector_clock)
        time.sleep(1)
        client.send(data)
        time.sleep(5)


def receive():
    global vector_clock
    while True:
        data = client.recv(2048)
        data = pickle.loads(data)
        print("After sending data", data)
        vector_clock = data


def sendAndReceieveData():
    # Thread1
    send_message = threading.Thread(target=send)
    send_message.start()
    # Thread2
    receive_message = threading.Thread(target=receive)
    receive_message.start()


if __name__ == '__main__':
    sendAndReceieveData()
