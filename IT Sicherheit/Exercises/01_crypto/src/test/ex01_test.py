#!/usr/bin/env python3

'''
@author: Christian Wressnegger
'''

import ex01_testdata as testdata


import filecmp
import os
import subprocess
import sys
import tempfile
import unittest
import string
from random import shuffle
from itertools import islice

unittest.TestLoader.sortTestMethodsUsing = None
PYTHON = "python3"
PYERROR = "For running your solutions we call '{}'.\nThe name might be different for your installation (e.g. on Windows)\n"


class Ex01(unittest.TestCase):
    @staticmethod
    def _gen_mono_key():
        key = list(string.ascii_lowercase)
        shuffle(key)
        return ''.join(key)

    @staticmethod
    def _gen_random_chars():
        letters = list(string.ascii_lowercase)
        while True:
            shuffle(letters)
            yield letters[0]

    @staticmethod
    def _gen_viginere_key(n):
        return ''.join(islice(Ex01._gen_random_chars(), n))

    TASKS = 0
    MY_DIR = os.path.dirname(os.path.abspath(__file__))
    MY_DIR = os.path.join(MY_DIR, '../')

    @staticmethod
    def call(tool, params):
        script = os.path.join(Ex01.MY_DIR, tool)
        cmd = '{} "{}" {}'.format(PYTHON, script, params)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, _ = p.communicate()

        if p.returncode != 0:
            sys.stderr.write(PYERROR.format(PYTHON))

        return out, p.returncode

    @staticmethod
    def tmpfile():
        fd, fname = tempfile.mkstemp(dir=Ex01.MY_DIR)
        os.close(fd)
        return fname

    def _check_encrypttool(self, tool, x, s=slice(0, None)):
        for alphabet, a, b in testdata.TOOL_MAP[tool][x][s]:
            fname = Ex01.tmpfile()

            with open(fname, 'wb') as f:
                f.write(a)
                f.seek(0)

            out, _ = Ex01.call(
                tool, '--{} {} "{}"'.format(x, alphabet, fname))

            os.remove(fname)
            self.assertEqual(out.strip(), b, "wrong {}ion".format(x))

    def _check_analysistool(self, k, tools, params=""):
        for plaintext, ciphertext in testdata.TOOL_MAP[tools[0]]:
            enc = Ex01.tmpfile()
            dec = Ex01.tmpfile()
            dec_ = Ex01.tmpfile()

            Ex01.call(tools[1], f'--encrypt {k} --out {enc} "{plaintext}"')
            Ex01.call(tools[1], f'--decrypt {k} --out "{dec}" {enc}')

            k_, _ = Ex01.call(tools[0], f'{enc} {params}')
            k_ = k_.decode()
            Ex01.call(tools[1], f'--decrypt {k_} --out {dec_} {enc}')

            ok = os.path.getsize(dec) > 0 and filecmp.cmp(dec, dec_)

            os.remove(enc)
            os.remove(dec)
            os.remove(dec_)

            self.assertTrue(len(k_) > 0, "No key extracted")
            self.assertTrue(ok, "Incorrect key/ decryption :(")

    def test_04_mono(self):
        TOOL = "mono/mono.py"
        self._check_encrypttool(TOOL, "encrypt", slice(0, 1))
        self._check_encrypttool(TOOL, "encrypt", slice(1, None))
        self._check_encrypttool(TOOL, "decrypt")
        Ex01.TASKS += 1

    def test_05_breakmono(self):
        TOOLS = ("mono/break_mono.py", "mono/mono.py")
        k = self._gen_mono_key()
        self._check_analysistool(k, TOOLS)
        Ex01.TASKS += 1

    def test_06_vig(self):
        TOOL = "vigenere/vig.py"
        self._check_encrypttool(TOOL, "encrypt")
        self._check_encrypttool(TOOL, "decrypt")
        Ex01.TASKS += 1

    def test_07_breakvig(self):
        TOOLS = ("vigenere/break_vig.py", "vigenere/vig.py")
        k = self._gen_viginere_key(testdata.BREAK_VIG_KEYLEN)
        self._check_analysistool(
            k, TOOLS, "--keylen {}".format(testdata.BREAK_VIG_KEYLEN))


if __name__ == "__main__":
    unittest.main()
