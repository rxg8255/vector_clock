import threading
import socket
import pickle

server_name = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_name, 8686))

vector_clock = [0, 0, 0]
client_data = []


def clockTime(connector, address):
    while True:
        global client_data, vector_clock
        client_clock_time = connector.recv(2048)
        client_data = pickle.loads(client_clock_time)
        print("Client Data")
        print(client_data)
        client_number = client_data[3]
        vector_clock[client_number] = max(client_data[client_number], vector_clock[client_number])
        vector_clock[client_number] = vector_clock[client_number] + 1
        print(vector_clock)
        send_data = pickle.dumps(vector_clock)
        connector.send(send_data)


def makeClientConnection():
    while True:
        client_server_connector, addr = server.accept()
        client_address = "{}:{}".format(str(addr[0]),str(addr[1]))
        print("{} connected".format(client_address))
        current_thread = threading.Thread(target=clockTime, args=(client_server_connector, client_address,))
        current_thread.start()


if __name__ == '__main__':
    server.listen(5)
    print("Vector Clock server started\n")
    master_thread = threading.Thread(target=makeClientConnection, args=())
    master_thread.start()
