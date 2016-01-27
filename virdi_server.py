# -*- coding: utf-8 -*-
import sys
import socket
import binascii
from thread import start_new_thread
from functions import vd_comms
from functions import vd_dbconn


# Function for handling connections. This will be used to create threads
def clientthread(conn, addr, port):
    # infinite loop so that function do not terminate and thread do not end.
    while True:

        try:
            # Receiving from client
            data = conn.recv(4096)

            if not data:
                break

            hex_data = binascii.hexlify(data).decode()
            opt = hex_data[2:4]

            if opt == '01':
                x = hex_data[8:16]
                tid = str(x[6:8] + x[4:6] + x[2:4] + x[0:2])
                vd_dbconn.setTerminal(tid, addr, port)
                replay = vd_comms.options[opt](hex_data)
                if replay is not None:
                    conn.sendall(replay)
            else:
                if opt == '1b':
                    tag_code = binascii.unhexlify(hex_data[64:68]).decode()
                    print tag_code
                    if tag_code == 'EE':
                        replay = vd_comms.options[opt](hex_data)
                        if replay is not None:
                            conn.sendall(replay)
                    else:
                        replay = vd_comms.respBringUserAuthInfoBlock(hex_data)
                        if replay is not None:
                            conn.sendall(replay)
                else:
                    replay = vd_comms.options[opt](hex_data)
                    if replay is not None:
                        conn.sendall(replay)

            if vd_dbconn.getTerminalStatus(addr) == 'open':
                tid = vd_dbconn.getTerminalID(addr)
                vd_dbconn.setTerminalStatus(tid)
                conn.sendall(vd_comms.setGateOpen(tid))

        except KeyboardInterrupt:
            break
    # came out of loop
    conn.close()


if __name__ == "__main__":
    HOST = '172.16.0.1'
    PORT = 9870
    # now keep talking with the client
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print 'Socket created'

    # Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    print 'Socket bind complete'

    # Start listening on socket
    s.listen(3)
    print 'Socket now listening'
    while 1:
        # wait to accept a connection - blocking call
        conn, addr = s.accept()
        ip = addr[0]
        port = str(addr[1])
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        # start new thread takes 1st argument as a function name to be run,
        # second is the tuple of arguments to the function.
        start_new_thread(clientthread, (conn, ip, port))
    s.close()
