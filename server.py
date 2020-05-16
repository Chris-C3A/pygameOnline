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
    player = Player(currentPlayer, random.randint(50, 800), random.randint(50, 1000))
    print(player)
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
                if data == "0":
                    print("0 nega")
                    # p = pickle.loads(conn.recv(2048))
                    for player in players:
                        if player.idx == currentPlayer:
                            p = players[players.index(player)]
                            bullets.append(Bullet(p.pivot, p.turret.angle))
                    reply = bullets
                else:
                    for player in players:
                        if player.idx == currentPlayer:
                            players[players.index(player)] = data
                    reply = players

                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print(e)
            break

    for player in players:
        if player.idx == currentPlayer:
            players.remove(player)
    print("Lost Connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print(f"[CONN] Connected to: {addr}")

    thread.start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1