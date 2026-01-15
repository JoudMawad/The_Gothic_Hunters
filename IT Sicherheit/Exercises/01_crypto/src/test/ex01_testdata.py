'''
@author: Christian Wressnegger
'''

import os
MY_DIR = os.path.dirname(os.path.abspath(__file__))
MY_DIR = os.path.join(MY_DIR, '../')

MONO = {
    "encrypt": [
        ("abcdefghijklmnopqrstuvwxyz", b"Exercise 01", b"exercise"),
        ("vyjlnfubidxaqmshprwkgeoztc",
         b"Security exercises are fun", b"wnjgriktnznrjiwnwvrnfgm")
    ],
    "decrypt": [
        ("vyjlnfubidxaqmshprwkgeoztc",
         b"wnjgriktnznrjiwnwvrnfgm", b"securityexercisesarefun")
    ]
}

BREAK_MONO = {
    (os.path.join(MY_DIR, 'mono/plaintext.txt'),
     os.path.join(MY_DIR, 'mono/ciphertext.txt'))
}

VIG = {
    "encrypt": [
        ("abcdefghijklmnopqrstuvwxyz", b"Exercise 01", b"eygugnyl"),
        ("sectubs",
         b"Security exercises are fun", b"kienljlqizxldakiutlfxmr")
    ],
    "decrypt": [
        ("sectubs",
         b"kienljlqizxldakiutlfxmr", b"securityexercisesarefun")
    ]
}

BREAK_VIG = {
    (os.path.join(MY_DIR, 'vigenere/plaintext.txt'),
     os.path.join(MY_DIR, 'vigenere/ciphertext.txt'))
}

BREAK_VIG_KEYLEN = 5

TOOL_MAP = {"mono/mono.py": MONO, "mono/break_mono.py": BREAK_MONO,
            "vigenere/vig.py": VIG, "vigenere/break_vig.py": BREAK_VIG}
