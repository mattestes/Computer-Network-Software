import cmd, sys
import socket
import bisect

from server import SocketServer
from client import SocketClient

class ChatApplicationShell(cmd.Cmd):
	def __init__(self, port):
		cmd.Cmd.__init__(self)
		self.prompt = ">> "
		self.intro = "Welcome to Chat Application!"
		self.port = port
		self.client_ip = socket.gethostbyname(socket.gethostname())
		if self.client_ip == "127.0.0.1":
			try:
				self.client_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
			except Exception:
				print("Was not able to find a valid client ip...")

		self.connected_remote_hosts = []
		self.map_ip_to_server = {}

		self.create_new_room()
		# self.do_connect(self.client_ip + " " + self.port) <- uncomment if you are using more than 1 machine
		# commenting this line allows u to have multiple ip connections to only one machine

	def create_new_room(self):
		self.client_server = SocketServer(self.client_ip, self.port, self)

	def do_connect(self, line):
		"""
		Connect to a remote machine.
		connect <remote host, remote port>
		args
		remote host - remote hosts IP
		remote port - remote hosts chat port
		"""
		split_line = line.split(" ")
		if len(split_line) != 2:
			print("Please enter two args only! run 'help connect' for more info.")
			return
		remote_host, remote_port = split_line
		if remote_host == self.client_ip and remote_port == self.port:
			print("Cannot connect to self")
			return
		if (remote_host, remote_port) in self.connected_remote_hosts:
			print("Already connected to %s!"%remote_host)
			return
		socket_client = SocketClient(remote_host, remote_port, self)
		if socket_client.connect():
			print("Successfully connected to %s:%s"%(remote_host, remote_port))
			self.map_ip_to_server[(remote_host, remote_port)] = socket_client
			#print("ip type:",type(remote_host)," port type:",type(remote_port))
			bisect.insort_left(self.connected_remote_hosts, (remote_host, remote_port))
		else:
			print("Connection to %s:%s failed!"%(remote_host, remote_port))

	def default(self, line):
		if line.isdigit():
			print("Connecting to port %s"%line)
		else:
			print("Unrecognized command %s, please enter 'help' for help!"%line)

	def preloop(self):
		"""
		Initialize history and other stateful variables.
		"""
		cmd.Cmd.preloop(self)
		self._hist = []

	def postloop(self):
		"""
		Sends a shutdown message to the user.
		Clears up any stateful variable if needed.
		"""
		self.client_server.stop()
		print("Bye!")

	def precmd(self, line):
		"""
		Add commands to self._hist variable.
		"""
		if line != '':
			self._hist.append(line.strip())
		return line

	def do_hist(self, args):
		"""Print a list of commands that have been entered"""
		print(self._hist)

	def do_exit(self, line):
		"""Exit the application"""
		for i in range(len(self.connected_remote_hosts)):
			self.do_terminate("1")
		return -1

	def do_myip(self, line):
		"""Get my ip"""
		print(self.client_ip)

	def do_myport(self, line):
		"""Get the port"""
		print(self.port)

	def do_list(self, line):
		"""List all the TCP connections you are connected to."""
		print('id: IP address         Port No.')
		f = '{:<2}: {:<15}        {:<5}' #format
		i = 1
		for (remote_host, remote_port) in self.connected_remote_hosts:
			print(f.format(*[i, remote_host, remote_port]))
			i += 1

	def do_send(self, line):
		"""
		Send a message to a listed connection id.
		For example enter 'list' and see this:
		id: IP address      Port No.
		1   192.xyz.abc.tuv 5432
		2   192.qwe.bvc.ijk 3233
		to send a message to the connection to 192.qwe.bvc.ijk 3233
		enter 'send 2 Hello'
		"""
		split_message = line.split(" ")
		if len(split_message) < 2:
			print("For the send command, please enter two paramters <connection id> <message>, please see 'help send' for more info.")
			return

		connection_id = split_message[0]
		if not connection_id.isdigit() or int(connection_id) <= 0:
			print("For the send command, please enter a valid connection id! (positive integer only!)")
			return
		connection_id = int(connection_id)
		if connection_id > len(self.connected_remote_hosts):
			print("Cannot connect to that!")
			return
		message = ' '.join(split_message[1:])
		if len(message) > 100:
			print("message is too big to send! please enter a shorter message!")
			return
		ip = self.connected_remote_hosts[connection_id - 1]
		remote_server = self.map_ip_to_server[ip]
		# this type checking doesn't feel very elegant to me, but I decided it worked fine and was more 
		# trouble that it's worth to think of a prettier way
		if isinstance(remote_server, SocketClient):
			success = remote_server.send_message(message)
		# in this case, remote_server is directly a socket, instead of a SocketClient wrapper
		else:
			success = self.client_server.send_message(remote_server, message)
		if success:
			print(f"Successfully sent message to connection {connection_id}")
		else:
			print(f"Failed sending message to conneciton {connection_id}")


	def do_terminate(self, line):
		"""
		Terminate the connection to a listed connection id.
		For example enter 'list' and see this:
		id: IP address      Port No.
		1   192.xyz.abc.tuv 5432
		2   192.qwe.bvc.ijk 3233
		to delete the connection to 192.qwe.bvc.ijk 3233
		enter'terminate 2'
		"""
		if not line.isdigit() or int(line) <= 0:
			print("Please enter a positive number to terminate!")
		_id = int(line)
		if _id > len(self.connected_remote_hosts):
			print("Connection id %s does not exist"%line)
			return
		i = 1
		ip_to_delete = ip = self.connected_remote_hosts[_id - 1]
		socket_connection = self.map_ip_to_server[ip_to_delete]
		ip, port = ip_to_delete
		if isinstance(socket_connection, SocketClient):
			success = socket_connection.close(ip, port)	
		else:
			success = self.client_server.close_connection(socket_connection, ip_to_delete)
		# the connection is removed from connected_remote_hosts and map_ip_to_server in the SocketClient or SocketServer
		# there were less complications/code redundancy to put it there instead of here
		if success:
			print(f"Successfully closed connection to {ip}:{port}")
		else:
			print(f"Failed to close connection to {ip}:{port}")

if __name__ == '__main__':
	port = sys.argv[1]
	ChatApplicationShell(port).cmdloop()
