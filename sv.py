import socket
import _thread as thread
import sys
from src.game import Game
import pickle
import random

HOST = "192.168.100.62"
PORT = 5569

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))
except socket.error as e:
    print("[ERROR] ", str(e))
    sys.exit(1)

s.listen()
print("[LOG] Server Started! Waiting for connection...")


def threaded_client(conn, playerID):
    global connections
    global game
    # add new player to game
    game.add_player(playerID)
    conn.send(pickle.dumps([playerID, game]))
    reply = ''
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if not data:
                print("Disconnected")
                break
            else:
                # process data
                pass
            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print(e)
            break

    print("Lost Connection")
    connections -= 1
    conn.close()


playerID = 0
connections = 0
# create game instance
game = Game(1)
while True:
    conn, addr = s.accept()
    print(f"[CONN] Connected to: {addr}")
    # start new thread
    thread.start_new_thread(threaded_client, (conn, playerID))
    playerID += 1
    connections += 1


