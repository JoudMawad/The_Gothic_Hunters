#!/usr/bin/env python3
import argparse
import os
import random
import socket
import struct


def checksum(data: bytes) -> int:
    if len(data) % 2 == 1:
        data += b"\x00"
    s = 0
    for i in range(0, len(data), 2):
        w = (data[i] << 8) + data[i + 1]
        s += w
        s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF


def resolve_host(host: str) -> str:
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return host


def guess_src_ip(dst_ip: str) -> str:
    if dst_ip.startswith("127."):
        return "127.0.0.1"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((dst_ip, 1))
        return s.getsockname()[0]
    finally:
        s.close()


def build_ip_header(src_ip: str, dst_ip: str, payload_len: int, ident: int) -> bytes:
    ver_ihl = (4 << 4) + 5
    tos = 0
    total_len = 20 + payload_len
    flags_frag = 0
    ttl = 64
    proto = socket.IPPROTO_TCP
    hdr_checksum = 0

    src = socket.inet_aton(src_ip)
    dst = socket.inet_aton(dst_ip)

    ip_hdr_wo_csum = struct.pack(
        "!BBHHHBBH4s4s",
        ver_ihl,
        tos,
        total_len,
        ident,
        flags_frag,
        ttl,
        proto,
        hdr_checksum,
        src,
        dst,
    )

    csum = checksum(ip_hdr_wo_csum)
    ip_hdr = struct.pack(
        "!BBHHHBBH4s4s",
        ver_ihl,
        tos,
        total_len,
        ident,
        flags_frag,
        ttl,
        proto,
        csum,
        src,
        dst,
    )
    return ip_hdr


def build_tcp_header(src_ip: str, dst_ip: str, sport: int, dport: int, flags: int) -> bytes:
    seq = 0
    ack = 0
    data_offset = 5  # 5 * 4 = 20 bytes
    offset_res = (data_offset << 4) + 0
    window = 5840
    urg_ptr = 0
    tcp_checksum = 0

    tcp_hdr_wo_csum = struct.pack(
        "!HHLLBBHHH",
        sport,
        dport,
        seq,
        ack,
        offset_res,
        flags,
        window,
        tcp_checksum,
        urg_ptr,
    )

    src_addr = socket.inet_aton(src_ip)
    dst_addr = socket.inet_aton(dst_ip)
    placeholder = 0
    proto = socket.IPPROTO_TCP
    tcp_len = len(tcp_hdr_wo_csum)

    pseudo_hdr = struct.pack("!4s4sBBH", src_addr, dst_addr, placeholder, proto, tcp_len)
    tcp_checksum = checksum(pseudo_hdr + tcp_hdr_wo_csum)

    tcp_hdr = struct.pack(
        "!HHLLBBHHH",
        sport,
        dport,
        seq,
        ack,
        offset_res,
        flags,
        window,
        tcp_checksum,
        urg_ptr,
    )
    return tcp_hdr


def main():
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--syn", action="store_true")
    g.add_argument("--xmas", action="store_true")
    g.add_argument("--fin", action="store_true")
    g.add_argument("--null", action="store_true")
    parser.add_argument("host", metavar="IP/DOMAIN")
    parser.add_argument("port", metavar="PORT", type=int)
    args = parser.parse_args()

    dst_ip = resolve_host(args.host)
    dst_port = int(args.port)

    if args.syn:
        flags = 0x02
    elif args.xmas:
        flags = 0x01 | 0x08 | 0x20
    elif args.fin:
        flags = 0x01
    else:
        flags = 0x00

    src_ip = guess_src_ip(dst_ip)
    src_port = 12345

    ident = random.randint(0, 65535)

    tcp_hdr = build_tcp_header(src_ip, dst_ip, src_port, dst_port, flags)
    ip_hdr = build_ip_header(src_ip, dst_ip, payload_len=len(tcp_hdr), ident=ident)
    packet = ip_hdr + tcp_hdr

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    try:
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        s.sendto(packet, (dst_ip, 0))
    finally:
        s.close()


if __name__ == "__main__":
    main()
