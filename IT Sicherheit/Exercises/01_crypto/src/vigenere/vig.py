import argparse
import string
import sys

ALPHABET = string.ascii_lowercase
ALPHABET_SIZE = len(ALPHABET)

def clean_text(text):
    return "".join(ch.lower() for ch in text if ch.isalpha())

def check_key(key):
    if not key:
        raise ValueError("Key cannot be empty.")
    if not all(ch.isalpha() for ch in key):
        raise ValueError("Key must only contain letters.")

def vigenere_encrypt(plain, key):
    check_key(key)
    key = key.lower()

    key_shifts = [ord(k) - ord("a") for k in key]

    result = []
    for i, letter in enumerate(plain):
        plain_value = ord(letter) - ord("a")
        shift = key_shifts[i % len(key_shifts)]
        encrypted_value = (plain_value + shift) % ALPHABET_SIZE
        result.append(chr(ord("a") + encrypted_value))
    return "".join(result)

def vigenere_decrypt(cipher, key):
    check_key(key)
    key = key.lower()

    key_shifts = [ord(k) - ord("a") for k in key]

    result = []
    for i, letter in enumerate(cipher):
        cipher_value = ord(letter) - ord("a")
        shift = key_shifts[i % len(key_shifts)]
        plain_value = (cipher_value - shift) % ALPHABET_SIZE
        result.append(chr(ord("a") + plain_value))
    return "".join(result)

def main():
    parser = argparse.ArgumentParser(description="Vigenère encrypt/decrypt")
    parser.add_argument("FILE")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--encrypt")
    group.add_argument("--decrypt")
    parser.add_argument("--out")
    args = parser.parse_args()

    with open(args.FILE, "r", encoding="utf-8") as f:
        file_data = f.read()

    if args.encrypt is not None:
        cleaned = clean_text(file_data)
        result = vigenere_encrypt(cleaned, args.encrypt)
    else:
        cleaned = clean_text(file_data)
        result = vigenere_decrypt(cleaned, args.decrypt)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f_out:
            f_out.write(result)
    else:
        sys.stdout.write(result)

if __name__ == "__main__":
    main()
