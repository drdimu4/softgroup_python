import socket
import sys
import select

def send_msg(usr_name):
    # ask for type msg
    msg = input()

    if msg == '<exit>':
        sock.close()
        sys.exit()

    msg = msg.lstrip()
    if 'user:' in msg:
        user_name = msg[5:msg.find(' ')]
        msg = msg[msg.find(' ')+1:]
        json = {"name": usr_name, "msg": msg, "to": user_name}
    else:
        json = {"name": usr_name, "msg": msg}
    stroka = (str(json)+'<end>').encode('utf-8')
    return stroka

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 5051
    address = (HOST, PORT)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect(address)

    except:
        print('Unable to connect')
        sys.exit()

    name = input('name=')

    print('Connected to remote host. Start sending messages')


    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            # incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write(send_msg(name))


            # user entered a message
            else:
                msg = send_msg(name)
                s.send(msg)
