#!/usr/bin/env python3
import argparse
import os
import random
import hashlib

from scapy.all import IP, UDP, TCP, Raw, sniff, send, conf


def knock_port(shared_key: int, challenge: int, i: int) -> int:
    # pi = 1024 + (sha256(k*c + i) mod 28657)
    x = shared_key * challenge + i
    h = hashlib.sha256(str(x).encode()).digest()
    v = int.from_bytes(h, "big") % 28657
    return 1024 + v


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--shared-key", type=int, required=True)
    parser.add_argument("--num-knocks", type=int, required=True)
    args = parser.parse_args()

    conf.verb = 0

    state = {
        "active": False,
        "client_ip": None,
        "challenge": None,
        "seen_ports": [],
    }

    def handle(pkt):
        if UDP in pkt and pkt[UDP].dport == args.port:
            state["client_ip"] = pkt[IP].src
            state["challenge"] = random.randint(1, 2**31 - 1)
            state["seen_ports"] = []
            state["active"] = True

            reply = IP(dst=state["client_ip"]) / UDP(dport=pkt[UDP].sport, sport=args.port) / Raw(
                str(state["challenge"]).encode()
            )
            send(reply, verbose=False)
            return

        if state["active"] and TCP in pkt and pkt[IP].src == state["client_ip"]:
            tcp = pkt[TCP]
            if tcp.flags == 0x02:
                state["seen_ports"].append(int(tcp.dport))

                if len(state["seen_ports"]) >= args.num_knocks:
                    expected = [knock_port(args.shared_key, state["challenge"], i)
                                for i in range(1, args.num_knocks + 1)]
                    if state["seen_ports"][:args.num_knocks] == expected:
                        print("unlocked", flush=True)
                    state["active"] = False

    sniff(filter="udp or tcp", prn=handle, store=False)


if __name__ == "__main__":
    main()
