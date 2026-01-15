#!/usr/bin/env python3

"""
@author: Christian Wressnegger and Stefan Czybik
"""

import os
import subprocess
import unittest

import requests
import yaml

unittest.TestLoader.sortTestMethodsUsing = None
PYTHON = "python3"
PYERROR = "For running your solutions we call '{}'.\nThe name might be different for your installation (e.g. on Windows)\n"


class Ex06(unittest.TestCase):
    TASKS = 0
    MY_DIR = os.path.dirname(os.path.abspath(__file__))
    MY_DIR = os.path.join(MY_DIR, "../")

    SQLI_URL = "http://localhost:80/sqli"

    @staticmethod
    def check_xss(file):
        cmd = "{} {} {}".format("node", "/browser.js", file)

        p = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        out, err = p.communicate()

        return out, err, p.returncode

    def xss_read_url(self, var):
        try:
            url = None
            file = os.path.join(self.MY_DIR, "xss-var{}.url".format(var))
            with open(file, "r") as f:
                for line in f:
                    url = line
                    break
            self.assertTrue(
                url and url.startswith("https://web.exercise.itsec.ias.tu-bs.de/xss/"),
                "No URL!?",
            )
            self.assertEqual(
                1, url.count("var"), "Only var{} should be used.".format(var)
            )
            self.assertTrue(
                "var{}".format(var) in url, "Use var{} for this attack.".format(var)
            )
            out, err, returncode = self.check_xss(file)
            out = out.split(b"\n")
            version = out[0].decode("utf-8")
            success = False
            if len(out) > 1:
                success = out[1].decode("utf-8")
            print("Using {} for testing the XSS attack".format(version))
            if returncode != 0:
                self.assertTrue(False, "Error: {}".format(str(err)))
            self.assertEqual(success, "XSS-Success", "XSS not successful")
        except IOError:
            self.assertTrue(False, "Unable to read file")

    def test_01_xss_var0(self):
        self.xss_read_url(0)
        Ex06.TASKS += 1

    def test_01_xss_var1(self):
        self.xss_read_url(1)
        Ex06.TASKS += 1

    def test_01_xss_var2(self):
        self.xss_read_url(2)
        Ex06.TASKS += 1

    def test_01_xss_var3(self):
        self.xss_read_url(3)
        Ex06.TASKS += 1

    def test_01_xss_var4(self):
        self.xss_read_url(4)
        Ex06.TASKS += 1

    def test_01_xss_var5(self):
        self.xss_read_url(5)
        Ex06.TASKS += 1

    def check_sqli_bachelor(self):
        filepath = os.path.join(self.MY_DIR, "sqli-bachelor.yml")
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)

            self.assertIsNotNone(data, "Invalid YAML file")
            self.assertTrue("username" in data, "Missing 'username' key in YAML file")
            self.assertTrue("password" in data, "Missing 'password' key in YAML file")

            req = requests.post(self.SQLI_URL + "/bachelor.php", data=data)
            self.assertEqual(req.status_code, 200, "Request failed")

            with open("/tmp/bachelor.txt", "r") as server_secret_file:
                server_secret = server_secret_file.read().strip()
                self.assertTrue(
                    server_secret.startswith("ITSEC"), "Invalid server secret"
                )

                self.assertTrue(server_secret in req.text, "SQL injection unsuccessful")

    def check_sqli_master(self):
        filepath = os.path.join(self.MY_DIR, "sqli-master.yml")
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)

            self.assertIsNotNone(data, "Invalid YAML file")
            self.assertTrue("search" in data, "Missing 'search' key in YAML file")

            req = requests.get(self.SQLI_URL + "/master.php", params=data)
            self.assertEqual(req.status_code, 200, "Request failed")

            with open("/tmp/master.txt", "r") as server_secret_file:
                server_secret = server_secret_file.read().strip()
                self.assertTrue(
                    server_secret.startswith("ITSEC"), "Invalid server secret"
                )

                self.assertTrue(server_secret in req.text, "SQL injection unsuccessful")

    def test_02_sqli_bachelor(self):
        self.check_sqli_bachelor()
        Ex06.TASKS += 1

    def test_02_sqli_master(self):
        self.check_sqli_master()
        Ex06.TASKS += 1


if __name__ == "__main__":
    unittest.main()
