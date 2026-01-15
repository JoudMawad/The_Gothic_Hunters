#!/usr/bin/env python3

'''
@author: Christian Wressnegger and Stefan Czybik
'''
try:
    # For evaluating the exercises we'll provide a similar but
    # different configuration that contains alternative input
    # values than those provided in the script that was handed
    # out (nothing mean though). Develop your solution robust
    # enough to work with various kinds and variations of input.
    import ex05_testdata_lecturer as testdata  # @UnresolvedImport @UnusedImport

except:
    import ex05_testdata as testdata  # @UnusedImport


import os
import subprocess
import unittest
import concurrent.futures
import random
import socket
import time
from scapy.all import IP

unittest.TestLoader.sortTestMethodsUsing = None
PYTHON = "python3"
PYERROR = "For running your solutions we call '{}'.\nThe name might be different for your installation (e.g. on Windows)\n"


class Ex05(unittest.TestCase):

    TASKS = 0
    MY_DIR = os.path.dirname(os.path.abspath(__file__))
    MY_DIR = os.path.join(MY_DIR, '../')

    @staticmethod
    def call(tool, params):
        script = os.path.join(Ex05.MY_DIR, tool)
        cmd = '{} "{}" {}'.format(PYTHON, script, params)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()

        # if p.returncode != 0:
        #    sys.stderr.write(PYERROR.format(PYTHON))

        return out, err, p.returncode

    def read_line(self, fname):
        my_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            line = None
            with open(os.path.join(my_dir, fname), 'r') as f:
                for line in f:
                    break

            self.assertTrue(line, "No data provided")
        except IOError:
            self.assertTrue(False, "Unable to read file")

        return line

    @staticmethod
    def receive_packet(host, port, timeout):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.bind((host, port))
        except socket.error as msg:
            print('Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            raise
        timeout = time.time() + timeout
        while True:
            packet = IP(s.recvfrom(65565)[0])
            flags = None
            if packet.payload.name == "TCP" and packet.payload.dport == port:
                flags = packet.payload.flags
                break
            if time.time() > timeout:
                break
        s.close()
        return flags

    def test_03_test_packet(self, test_flag, result_flags, port):
        timeout = 1
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(Ex05.receive_packet, '127.0.0.1', port, timeout)
            Ex05.call("send_packet.py", str(test_flag) + " 127.0.0.1 " + str(port))
            flags = future.result(timeout=timeout)
            self.assertIsNotNone(flags, f"Could not receive or parse packet for '{test_flag}'")
            self.assertEqual(flags.value, result_flags, f"Flags are not correct for '{test_flag}'")

    def test_03_send_packet(self):
        _, out, _ = Ex05.call("send_packet.py", "")
        self.assertTrue(testdata.verify_synopsis("send_packet", out))

        self.test_03_test_packet("--syn", 2,  random.randint(20000, 30000))
        self.test_03_test_packet("--xmas", 41,  random.randint(20000, 30000))
        self.test_03_test_packet("--fin", 1,  random.randint(20000, 30000))
        self.test_03_test_packet("--null", 0,  random.randint(20000, 30000))

        Ex05.TASKS += 1


if __name__ == "__main__":
    unittest.main()
