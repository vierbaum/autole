import socketserver
import socket
import controls

class Handler_TCPServer(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request - TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #print("{} sent:".format(self.client_address[0]))
        print(list(self.data))
        if list(self.data)[0] == 102:
            print("HERE")
            controls.drive(1)
            self.request.sendall("DRIVING FORWARD".encode())

        if self.data[0] == 98:
            controls.drive(0)
            self.request.sendall("DRIVING BACKWARD".encode())

        if list(self.data)[0] == 115:
            controls.stop()
            self.request.sendall("STOPING".encode())
        
        controls.steer(int(self.data[2:]))


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    HOST, PORT = socket.gethostbyname("autole"), 9999

    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)
    tcp_server.serve_forever()