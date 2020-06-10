import socket
import _thread as thread
import sys
from src.player import Player
from src.bullet import Bullet
import pickle
import random

HOST = "192.168.100.62"  # 192.168.100.62
PORT = 5569

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))
except socket.error as e:
    print("[ERROR] ", str(e))
    sys.exit(1)

s.listen()
print("[LOG] Server Started! Waiting for connection...")

players = []
bullets = []


# print(players)
def threaded_client(conn, currentPlayer):
    global connections
    player = Player(currentPlayer, random.randint(50, 1000), random.randint(50, 800))
    players.append(player)
    conn.send(pickle.dumps(player))
    reply = ''
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            # players[currentPlayer] = data

            if not data:
                print("Disconnected")
                break
            else:
                if data[0] == '0':
                    print("[LOG] collided")
                    for player in players:
                        if player.idx == data[1].idx:
                            players[players.index(player)] = data[1]
                    reply = players
                elif data[0] == '1':
                    for player in players:
                        # print(f"shu wle {len(player.bullets)}")
                        if player.idx == currentPlayer:
                            players[players.index(player)] = data[1]
                    reply = players
                elif data[0] == '2':
                    pass

                # print("Received: ", data)
                # print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print(e)
            break

    for player in players:
        if player.idx == currentPlayer:
            players.remove(player)
    print("Lost Connection")
    connections -= 1
    conn.close()


currentPlayer = 0
connections = 0
while True:
    conn, addr = s.accept()
    printf("[CONN] Connected to: {addr}")

    thread.start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    connections += 1
