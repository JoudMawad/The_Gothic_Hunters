import argparse
import os
import string
import sys

ALPHABET = string.ascii_lowercase

def load_plaintext():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    plaintext_path = os.path.join(base_dir, "..", "mono", "plaintext.txt")
    plaintext_path = os.path.normpath(plaintext_path)

    with open(plaintext_path, "r", encoding="utf-8") as f:
        plaintext_data = f.read()

    return "".join(ch.lower() for ch in plaintext_data if ch.isalpha())

def load_ciphertext(ciphertext_file):
    with open(ciphertext_file, "r", encoding="utf-8") as f:
        ciphertext_data = f.read()
    return "".join(ch.lower() for ch in ciphertext_data if ch.isalpha())

def derive_key_from_plain_and_cipher(plaintext, ciphertext):
    if len(plaintext) != len(ciphertext):
        return ALPHABET

    letter_mapping = {}
    used_cipher_letters = set()

    for plain_char, cipher_char in zip(plaintext, ciphertext):
        if plain_char not in letter_mapping:
            letter_mapping[plain_char] = cipher_char
            used_cipher_letters.add(cipher_char)

    remaining_plain_letters = [ch for ch in ALPHABET if ch not in letter_mapping]
    remaining_cipher_letters = [ch for ch in ALPHABET if ch not in used_cipher_letters]

    for plain_char, cipher_char in zip(remaining_plain_letters, remaining_cipher_letters):
        letter_mapping[plain_char] = cipher_char

    key = "".join(letter_mapping[ch] for ch in ALPHABET)
    return key

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE")
    args = parser.parse_args()

    plaintext = load_plaintext()
    ciphertext = load_ciphertext(args.FILE)

    key = derive_key_from_plain_and_cipher(plaintext, ciphertext)

    sys.stdout.write(key)

if __name__ == "__main__":
    main()
