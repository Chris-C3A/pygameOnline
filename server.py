import socket
import _thread as thread
import sys
from src.player import Player
from src.bullet import Bullet
import pickle
import random

HOST = "192.168.100.149"  # 192.168.100.62
PORT = 5569

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))
except socket.error as e:
    print("[ERROR] ", str(e))
    sys.exit(1)

s.listen()
print("[LOG] Server Started! Waiting for connection...")


players = {}

def threaded_client(conn, idx):
    global players
    global connections
    WIDTH, HEIGHT = 800, 800
    player = Player(idx, random.randint(50, WIDTH-150), random.randint(50, HEIGHT-150))
    players[idx] = player
    conn.send(pickle.dumps({"idx": idx}))

    # set username of the player
    try:
        username = pickle.loads(conn.recv(2048))
        players[idx].name = username["username"]
        conn.send(pickle.dumps({"OK": players[idx].name}))
    except Exception as e:
        print(e)
    reply = ''
    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("Disconnected")
                break
            else:
                if "get" in data:
                    if data["get"] == "players":
                        reply = players
                elif "key" in data:
                    if data["key"] == "w":
                        players[idx].move(direction=-1)
                    elif data["key"] == "s":
                        players[idx].move(direction=0.7)
                    elif data["key"] == "a":
                        players[idx].rotate(direction=-1)
                    elif data["key"] == "d":
                        players[idx].rotate(direction=1)
                    elif data["key"] == "space":
                        if players[idx].turret.primary_ammo > 0:
                            players[idx].fire()
                            players[idx].turret.primary_ammo -= 1
                elif "mouse" in data:
                    players[idx].update_pivot()
                    players[idx].turret.rotate(data["mouse"]["x"], data["mouse"]["y"])
                elif "server" in data:
                    if data["server"] == "update":
                        for bullet in players[idx].bullets:
                            bullet.move()

                            # collision
                            for player in players.values():
                                if player.idx == idx:
                                    continue

                                if bullet.collide(player):
                                    print("[LOG] collision")
                                    player.health -= 25
                                    players[idx].bullets.pop(players[idx].bullets.index(bullet))


                            if bullet.x > WIDTH or bullet.x < 0 or bullet.y > HEIGHT or bullet.y < 0:
                                players[idx].bullets.pop(players[idx].bullets.index(bullet))

                # print("Received: ", data)
                # print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print(e)
            break

    del players[idx]
    print("Lost Connection")
    connections -= 1
    conn.close()


currentPlayer = 0
connections = 0
while True:
    conn, addr = s.accept()
    print(f"[CONN] Connected to: {addr}")

    thread.start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    connections += 1
