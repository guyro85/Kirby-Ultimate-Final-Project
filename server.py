import socket
from _thread import *
import pickle
import ai
import time

# Auto-detect server IP address
def get_local_ip():
    """
    Automatically detect the local IP address of this computer
    """
    try:
        # Create a socket to determine the local IP
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to an external address (doesn't actually send data)
        temp_socket.connect(("8.8.8.8", 80))
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_ip
    except Exception:
        # Fallback method
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return "127.0.0.1"

def broadcast_server(server_ip, server_port, broadcast_port=4001):
    """
    Broadcast server information on the local network
    """
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    message = f"{server_ip}:{server_port}".encode()

    while True:
        try:
            broadcast_socket.sendto(message, ('<broadcast>', broadcast_port))
            time.sleep(1)  # Broadcast every second
        except Exception as e:
            print(f"Broadcast error: {e}")
            time.sleep(1)

SERVER = get_local_ip()
PORT = 4000
BROADCAST_PORT = 4001

print(f"Server IP auto-detected: {SERVER}")
print(f"Broadcasting server information on port {BROADCAST_PORT}...")

enemies = [ai.AI(700, 500, 40, 1)]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CURRENT_PLAYER = 0


try:
    s.bind((SERVER, PORT))

except socket.error as e:
    print(e)

s.listen(2)
print("server started, waiting for connection...")


def threaded_client(conn, p):
    """
    the main loop for the server. gets information from the players and return as well
    :param conn: the socket
    :param p: the player number (0 for p1 and 1 for p2)
    :return:
    """
    global CURRENT_PLAYER
    global enemies
    reply = ""
    conn.send(pickle.dumps(ai.players[p]))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if data == '1':
                reply = enemies[0]

            else:
                if ai.players[p].hit == 1:  # save if the other player was damaged
                    ai.players[p] = data
                    ai.players[p].hit = 1
                else:
                    ai.players[p] = data
                if not data:
                    print("disconnected")
                    break
                else:
                    if p == 0:
                        if enemies[0].p1Hit == 1:  # lets the player know if he was hit
                            ai.players[1].hit = 1
                            enemies[0].p1Hit = 0
                        reply = ai.players[1]
                    else:
                        if enemies[0].p2Hit == 1:
                            ai.players[0].hit = 1
                            enemies[0].p2Hit = 0
                        reply = ai.players[0]

            print("received: ", data)
            print("sending: ", reply)
            conn.sendall(pickle.dumps(reply))

            if p == 0 and ai.players[1].hit == 1:  # reset the hit indicator
                ai.players[1].hit = 0
            elif p == 1 and ai.players[0].hit == 1:
                ai.players[0].hit = 0

            if p == 0 and data == '1':  # lets the AI know that the players have printed him
                enemies[0].printed1 = 1
            elif p == 1 and data == '1':
                enemies[0].printed2 = 1

        except Exception as err:
            print(err)
            break

    print("connection lost")
    conn.close()
    CURRENT_PLAYER -= 1


start_new_thread(ai.move, (enemies[0],))  # runs the AI
start_new_thread(broadcast_server, (SERVER, PORT, BROADCAST_PORT))  # broadcast server info

while True:  # start receiving new players
    con, adrr = s.accept()
    print("connected to: ", adrr)

    start_new_thread(threaded_client, (con, CURRENT_PLAYER))
    CURRENT_PLAYER += 1
