#!/usr/bin/env python3

'''
@author: Christian Wressnegger, Stefan Czybik
'''

try:
    # For evaluating the exercises we'll provide a similar but
    # different configuration that contains alternative input
    # values than those provided in the script that was handed
    # out (nothing mean though). Develop your solution robust
    # enough to work with various kinds and variations of input.
    import ex02_testdata_lecturer as testdata  # @UnresolvedImport @UnusedImport

except:
    import ex02_testdata as testdata  # @UnusedImport


import os
import subprocess
import sys
import unittest

unittest.TestLoader.sortTestMethodsUsing = None
PYTHON = "python3"
PYERROR = "For running your solutions we call '{}'.\nThe name might be different for your installation (e.g. on Windows)\n"


class Ex02(unittest.TestCase):

    MY_DIR = os.path.dirname(os.path.abspath(__file__))
    MY_DIR = os.path.join(MY_DIR, '../')

    @staticmethod
    def call(tool, params):
        script = os.path.join(Ex02.MY_DIR, tool)
        cmd = '{} "{}" {}'.format(PYTHON, script, params)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, _ = p.communicate()

        if p.returncode != 0:
            sys.stderr.write(PYERROR.format(PYTHON))

        return out, p.returncode

    def test_02_dh(self):
        for d in testdata.DH:
            key, _ = Ex02.call(os.path.join(
                "dh", "crack_dh.py"), "-g {g} -n {n} --alice {alice} --bob {bob}".format(**d))

            key = key.strip().decode('ascii')
            self.assertEqual(key, str(d['key']))

    def test_04_rsa(self):
        for d in testdata.RSA:
            msg, _ = Ex02.call(os.path.join(
                "rsa", "crack_rsa.py"), "-e {e} -n {n} --ciphertext {ciphertext}".format(**d))

            msg = msg.strip().decode('ascii')
            self.assertEqual(msg, str(d['msg']))


if __name__ == "__main__":
    unittest.main()
