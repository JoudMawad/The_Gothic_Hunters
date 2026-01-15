#!/usr/bin/env python3

'''
@author: Christian Wressnegger
'''

import os
import subprocess
import sys
import types
import unittest
from base64 import b64encode
sys.path.append('.')
USAGE = b'''usage: exercises.py [-h] [-b] [-f FLOAT] [-i INT] FILE

positional arguments:
  FILE        The input positional parameter.

options:
  -h, --help  show this help message and exit
  -b          An optional boolean flag (Default: False).
  -f FLOAT    An optional parameter of type float (Default: 0.0).
  -i INT      An optional parameter of type int (Default: 0).'''

import ex00_testdata as testdata

try:
    from sectubs.exercises import Exercise00
except ImportError:
    pass

unittest.TestLoader.sortTestMethodsUsing = None
PYTHON = "python3"
PYERROR = "For running your solution we call '{}'.\nThe name might be different for your installation (e.g. on Windows)\n"


class Ex00(unittest.TestCase):

    def test_00_packages(self):
        self.assertTrue("Exercise00" in globals())

    def test_01_static_field(self):
        try:
            print("[I] Name: " + Exercise00.STUDENT_NAME)

        except AttributeError:
            self.assertFalse(True, "No name specified")

    def test_02_static_method(self):
        self.assertEqual(
            Exercise00.deadline(testdata.DATE_FORMAT[0]),
            testdata.DATE_FORMAT[1])

    def test_03_property(self):
        ex = Exercise00(testdata.STR1[0])
        try:
            ex.txt = "test"
            self.assertFalse(True, "not a property")

        except AttributeError as e:
            self.assertIn(
                "object has no setter", str(e), "no setter allowed")

        s = ex.txt
        self.assertEqual(s, testdata.STR1[1], "wrong output")

    def test_04_format_strings(self):
        def get_format(ex, mode):
            fmt = ex.format(mode)
            if '%' in fmt:
                self.assertFalse(True, "Python-2 format string")

            return fmt

        ex = Exercise00()

        fmt = get_format(ex, "order")
        s = fmt.format('third', 'second', 'first')
        self.assertEqual(s, "first - second - third")

        fmt = get_format(ex, "dict")

        d = {'x': 41.123, 'y': 71.091}
        s = fmt.format(**d)

        self.assertEqual(s, "x, y = (41.1, 71.0910)")

    def test_05_generators(self):
        ex = Exercise00()
        g = ex.listfiles(testdata.FILE_LIST[0])
        self.assertTrue(isinstance(g, types.GeneratorType), "not a generator")

        g = ex.listfiles(testdata.FILE_LIST[0], testdata.FILE_LIST[2])
        s = '\n'.join(sorted(g))

        self.assertEqual(
            s, testdata.FILE_LIST[1], "wrong list of files")

    def test_06_functionparams(self):
        ex = Exercise00()
        s = testdata.CALL(ex)

        self.assertEqual(s, testdata.OUTPUT, "wrong output")

    def test_07_collatz(self):
        ex = Exercise00()
        for test in testdata.COLLATZ:
            seq, stopping_time = ex.collatz(test[0])
            self.assertEqual((seq, stopping_time), test[1])

    def test_08_base64(self):
        for test_str in testdata.BASE64_STRs:
            ex = Exercise00(test_str)
            s = str(ex)
            b64 = b64encode(test_str.encode()).decode()
            self.assertEqual(
                s, b64, "wrong output")

    def test_09_argparse(self):
        def call(params):
            my_dir = os.path.dirname(os.path.abspath(__file__))
            script = os.path.join(my_dir, "../", "sectubs", "exercises.py")
            cmd = '{} "{}" {}'.format(PYTHON, script, params)

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            out, _ = p.communicate()

            if p.returncode not in [0, 42]:
                sys.stderr.write(PYERROR.format(PYTHON))

            return out, p.returncode

        out, ret = call("-h")
        out_s = str(out.strip().replace(b'\r', b''))

        self.assertEqual(
            out.strip().replace(b'\r', b''), USAGE.replace(b'\r', b''),
            "wrong usage information")


if __name__ == "__main__":
    unittest.main()
