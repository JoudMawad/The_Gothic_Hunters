import socket
import ssl
import sys
import argparse

parser = argparse.ArgumentParser(description="Weird Service Client")
parser.add_argument("host", metavar="IP/DOMAIN", help="Server Hostname or IP")
parser.add_argument("port", metavar="PORT", type=int, help="Server Port")
parser.add_argument("--out", metavar="FILE", help="Output file to save the dialog", default=None)

args = parser.parse_args()

HOST = args.host
PORT = args.port
OUT_FILE = args.out

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

def connect():
    try:
        s = socket.create_connection((HOST, PORT))
        return context.wrap_socket(s, server_hostname=HOST)
    except Exception as e:
        print(f"Error connecting to {HOST}:{PORT} - {e}")
        sys.exit(1)

def log_message(msg, file_handle=None):
    print(msg)

    if file_handle:
        file_handle.write(msg + "\n")

def main():
    c1 = connect()
    c2 = connect()

    f1 = c1.makefile("rwb")
    f2 = c2.makefile("rwb")

    file_handle = open(OUT_FILE, "w", encoding="utf-8") if OUT_FILE else None

    try:
        while True:
            l1 = f1.readline()
            l2 = f2.readline()
            if not l1 or not l2:
                break

            t1 = l1.decode().strip()
            t2 = l2.decode().strip()

            log_message(f" {t1}", file_handle)
            log_message(f" {t2}", file_handle)

            if t1.isdigit():
                f2.write((t1 + "\n").encode())
                f2.flush()
            if t2.isdigit():
                f1.write((t2 + "\n").encode())
                f1.flush()

    finally:
        if file_handle:
            file_handle.close()
        c1.close()
        c2.close()

if __name__ == "__main__":
    main()