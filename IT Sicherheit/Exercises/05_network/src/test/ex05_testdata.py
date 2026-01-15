'''
@author: Christian Wressnegger and Stefan Czybik
'''


SEND_PACKET = b'''
usage: send_packet.py [-h] (--syn | --xmas | --fin | --null) IP/DOMAIN PORT
send_packet.py: error: the following arguments are required: IP/DOMAIN, PORT
'''

SYNOPSIS = {
    "send_packet": SEND_PACKET,
}


def verify_synopsis(x, s):
    try:
        return (SYNOPSIS[x].strip() in s)
    except KeyError:
        return False
