import argparse
import string
import sys

ALPHABET = string.ascii_lowercase

def check_key(key):
    if len(key) != 26 or set(key) != set(ALPHABET):
        raise ValueError("Key must contain all 26 letters exactly once.")

def clean_text(text):
    return "".join(ch.lower() for ch in text if ch.isalpha())

def encrypt(text, key):
    check_key(key)
    mapping = {}
    for p, c in zip(ALPHABET, key):
        mapping[p] = c
    return "".join(mapping[ch] for ch in text)

def decrypt(text, key):
    check_key(key)
    mapping = {}
    for p, c in zip(ALPHABET, key):
        mapping[c] = p
    return "".join(mapping[ch] for ch in text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE")
    parser.add_argument("--encrypt", help="encrypt with key")
    parser.add_argument("--decrypt", help="decrypt with key")
    parser.add_argument("--out", help="output file")
    args = parser.parse_args()

    with open(args.FILE, "r", encoding="utf-8") as f:
        data = f.read()

    if args.encrypt:
        key = args.encrypt.lower()
        text = clean_text(data)
        result = encrypt(text, key)
    elif args.decrypt:
        key = args.decrypt.lower()
        text = clean_text(data)
        result = decrypt(text, key)
    else:
        print("Need --encrypt or --decrypt.")
        sys.exit(1)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f_out:
            f_out.write(result)
    else:
        sys.stdout.write(result)

if __name__ == "__main__":
    main()
