import socket

server_port = 9999

try:
    host_ip = socket.gethostbyname("autole")
    print("Found server on", host_ip)
except Exception:
    host_ip = input("Unable to locate server!\nPlease input ip manually:\n")

# Initialize a TCP client socket using SOCK_STREAM

while True:
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = input("input string to send:\n")

    try:
        tcp_client.connect((host_ip, server_port))
        # Establish connection to TCP server and exchange data
        tcp_client.sendall(data.encode())

        # Read data from the TCP server and close the connection
        received = tcp_client.recv(1024)
    finally:
        tcp_client.close()

    print ("Bytes Received: {}".format(received.decode()))
