import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"  # Replace with your server IP
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player_id = None  # Track player ID
        self.players = self.connect()

    def get_players(self):
        return self.players

    def connect(self):
        try:
            self.client.connect(self.addr)
            data = pickle.loads(self.client.recv(2048))  # Receive initial data
            self.player_id = data["player_id"]  # Extract player ID
            return data["players"]  # Extract the player list
        except Exception as e:
            print(f"Connection error: {e}")
            return None

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(f"Send error: {e}")
            return None
