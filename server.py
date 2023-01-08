import socketserver
import socket
import controls

class Handler_TCPServer(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request - TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #print("{} sent:".format(self.client_address[0]))
        print(self.data)
        if self.data == b'f':
            controls.drive(1)
            self.request.sendall("DRIVING FORWARD".encode())

        if self.data == b'b':
            controls.drive(0)
            self.request.sendall("DRIVING BACKWARD".encode())

        if self.data == b's':
            controls.stop()
            self.request.sendall("STOPING".encode())

        if self.data == b'l':
            controls.steer("l")
            self.request.sendall("STEERING LEFT".encode())

        if self.data == b'r':
            controls.steer("r")
            self.request.sendall("STEERING RIGHT".encode())

        if self.data == b'n':
            controls.steer(None)
            self.request.sendall("STEERING STRAIGT".encode())

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    HOST, PORT = socket.gethostbyname("autole"), 9999

    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)
    tcp_server.serve_forever()