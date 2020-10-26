import socket, time
import bisect
from threading import *
from multiprocessing import *

class SocketServer(Thread):
    def __init__(self, host, port, chat_application):
        Thread.__init__(self)
        self.host = host
        self.port = int(port)
        self.chat_application = chat_application
        self.killed = False
        self.start()
        self.clients = {}

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen()
        while True:
            try:
                conn, addr = self.s.accept()
                ip, port = addr
                port = str(port)
                self.clients[conn] = addr
                self.chat_application.map_ip_to_server[(ip, port)] = conn
                bisect.insort_left(self.chat_application.connected_remote_hosts, (ip, port))
                print("%s made a connection with you."%ip)
                Thread(target=self.handle_client, args=(conn, addr)).start()
            except Exception:
                print("Shutting down server...")
                break

    def handle_client(self, client, addr):
        """Handles a single client connection."""
        ip, port = addr
        port = str(port)
        while True:
            try:
                msg = client.recv(1024).decode()
            except:
                return
            if msg == "connect":
                # initial message for when a client attempts to connect to server
                continue
            if msg == "{quit}":
                self.close_connection(client, (ip, port))
                print("%s:%s terminated the connection"%(ip, port))
                return
            print(f"\nMessage receieved from: {ip}\nSender's Port: {port}\nMessage: {msg}")

    def send_message(self, client, message):
        try:
            client.sendall(message.encode())
        except:
            return False
        return True

    # def broadcast(self, msg):
    #     """Broadcasts a message to all the clients."""
    #     # print(msg.decode())
    #     for sock in self.clients:
    #         sock.send(msg)

    def close_connection(self, client, addr):
        try:
            self.send_message(client, "{quit}")
            client.close()
            del self.clients[client]
            del self.chat_application.map_ip_to_server[addr]
            self.chat_application.connected_remote_hosts.remove(addr)
        except:
            return False
        return True

    def stop(self):
        self.s.close()
        time.sleep(0.3)
