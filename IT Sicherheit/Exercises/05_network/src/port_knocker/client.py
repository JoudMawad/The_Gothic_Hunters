#!/usr/bin/env python3
import argparse
import hashlib
import socket

from scapy.all import IP, UDP, TCP, Raw, sr1, send, conf


def knock_port(shared_key: int, challenge: int, i: int) -> int:
    x = shared_key * challenge + i
    h = hashlib.sha256(str(x).encode()).digest()
    v = int.from_bytes(h, "big") % 28657
    return 1024 + v


def resolve_host(host: str) -> str:
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return host


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shared-key", type=int, required=True)
    parser.add_argument("--num-knocks", type=int, required=True)
    parser.add_argument("host", metavar="IP/DOMAIN")
    parser.add_argument("port", metavar="PORT", type=int)  # UDP port for challenge
    args = parser.parse_args()

    conf.verb = 0

    dst_ip = resolve_host(args.host)
    udp_port = args.port

    req = IP(dst=dst_ip) / UDP(dport=udp_port) / Raw(b"hi")
    resp = sr1(req, timeout=2, verbose=False)

    if resp is None or Raw not in resp:
        return

    try:
        c = int(bytes(resp[Raw].load).decode(errors="ignore").strip())
    except ValueError:
        return

    for i in range(1, args.num_knocks + 1):
        p = knock_port(args.shared_key, c, i)
        send(IP(dst=dst_ip) / TCP(dport=p, flags="S"), verbose=False)


if __name__ == "__main__":
    main()
