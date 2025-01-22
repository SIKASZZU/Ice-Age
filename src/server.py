import socket
from _thread import *
from player import Player
import pickle

server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for a connection, Server Started")

# Track connected players dynamically
players = {}
player_id_counter = 0
lock = allocate_lock()  # To prevent race conditions when updating players


def threaded_client(conn, player_id):
    global players, player_id_counter
    try:
        # Send player ID and initial players list
        conn.send(pickle.dumps({"player_id": player_id, "players": list(players.values())}))

        while True:
            data = pickle.loads(conn.recv(2048))
            if not data:
                break

            # Update the current player's data
            with lock:
                players[player_id] = data

            # Send all active players back
            with lock:
                conn.sendall(pickle.dumps(list(players.values())))
    except:
        pass
    finally:
        # Remove player when they disconnect
        with lock:
            print(f"Player {player_id} disconnected")
            del players[player_id]
            player_id_counter -= 1

        conn.close()


while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}")

    with lock:
        player_id = player_id_counter
        players[player_id] = Player(50 * player_id, 50 * player_id, 50, 50, (255, 0, 0))  # Example starting position
        player_id_counter += 1

    start_new_thread(threaded_client, (conn, player_id))
