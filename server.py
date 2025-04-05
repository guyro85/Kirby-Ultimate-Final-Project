import socket
from _thread import *
import pickle
import ai

SERVER = "10.0.0.3"
PORT = 4000
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

while True:  # start receiving new players
    con, adrr = s.accept()
    print("connected to: ", adrr)

    start_new_thread(threaded_client, (con, CURRENT_PLAYER))
    CURRENT_PLAYER += 1
