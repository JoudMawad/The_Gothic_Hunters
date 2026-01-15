import argparse
import string
import sys

ALPHABET = string.ascii_lowercase
ALPHABET_SIZE = len(ALPHABET)

ENGLISH_FREQUENCY = { "a": 0.08167, "b": 0.01492, "c": 0.02782, "d": 0.04253, "e": 0.12702, "f": 0.02228, "g": 0.02015, "h": 0.06094, "i": 0.06966, "j": 0.00153, "k": 0.00772, "l": 0.04025, "m": 0.02406,
                      "n": 0.06749, "o": 0.07507, "p": 0.01929, "q": 0.00095, "r": 0.05987, "s": 0.06327, "t": 0.09056, "u": 0.02758, "v": 0.00978, "w": 0.02360, "x": 0.00150, "y": 0.01974, "z": 0.00074, }

def chi_squared_for_shift(text_segment, shift_amount):
    if not text_segment:
        return 0.0

    letter_counts = [0] * ALPHABET_SIZE

    for letter in text_segment:
        c_index = ord(letter) - ord("a")
        plain_index = (c_index - shift_amount) % ALPHABET_SIZE
        letter_counts[plain_index] += 1

    total_letters = len(text_segment)
    chi_value = 0.0

    for i, letter in enumerate(ALPHABET):
        observed = letter_counts[i]
        expected = ENGLISH_FREQUENCY[letter] * total_letters
        if expected > 0:
            difference = observed - expected
            chi_value += (difference * difference) / expected

    return chi_value

def derive_vigenere_key(ciphertext, key_length):
    key_letters = []

    for key_pos in range(key_length):
        segment = ciphertext[key_pos::key_length]

        best_shift = 0
        best_chi = None

        for shift_amount in range(ALPHABET_SIZE):
            chi = chi_squared_for_shift(segment, shift_amount)
            if best_chi is None or chi < best_chi:
                best_chi = chi
                best_shift = shift_amount

        key_letter = chr(ord("a") + best_shift)
        key_letters.append(key_letter)

    return "".join(key_letters)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keylen", type=int, required=True)
    parser.add_argument("FILE")
    args = parser.parse_args()

    with open(args.FILE, "r", encoding="utf-8") as f:
        file_data = f.read()

    ciphertext = "".join(ch.lower() for ch in file_data if ch.isalpha())

    key = derive_vigenere_key(ciphertext, args.keylen)

    sys.stdout.write(key)

if __name__ == "__main__":
    main()
