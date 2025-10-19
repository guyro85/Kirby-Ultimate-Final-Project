import socket
import pickle

BROADCAST_PORT = 4001
DISCOVERY_TIMEOUT = 10  # seconds


def discover_server(broadcast_port=4001, timeout=10):
    """
    Discover the game server on the local network by listening for broadcasts
    """
    print("Searching for game server on the network...")

    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    discovery_socket.bind(('', broadcast_port))
    discovery_socket.settimeout(timeout)

    try:
        data, addr = discovery_socket.recvfrom(1024)
        message = data.decode()
        server_ip, server_port = message.split(':')
        print(f"Found server at {server_ip}:{server_port}")
        discovery_socket.close()
        return server_ip, int(server_port)
    except socket.timeout:
        discovery_socket.close()
        print(f"Server not found after {timeout} seconds.")
        print("Make sure the server is running on the same network.")
        return None, None
    except Exception as e:
        discovery_socket.close()
        print(f"Error during server discovery: {e}")
        return None, None


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Discover server on the network
        self.server, self.port = discover_server(BROADCAST_PORT, DISCOVERY_TIMEOUT)

        if self.server is None or self.port is None:
            raise Exception("Failed to discover game server. Please ensure the server is running.")

        self.address = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        """
        connects to the server
        """
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print(e)

    def send(self, data):
        """
        send info to the server and get in return
        :param data: the info to send
        :return: the info that the server sent back
        """
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

