'''
@author: Christian Wressnegger
'''

DATE_FORMAT = (
    "Deadline: %dth of %B, %I:%M %p", "Deadline: 15th of November, 09:00 AM")
STR1 = ("Too short",
        "Too short...")
BASE64_STRs = ["It's easier to ask forgiveness than it is to get permission",
                "Passwords are like underwear: don't let people see it, change it very often, and you shouldn't share it with strangers."]





class Test():

    def __init__(self):
        pass

    def __str__(self):
        return "TEST"


CALL = (lambda ex: ex(c=[1, 2, 3], a=Test(), d='4', b=2.0))
OUTPUT = """a = TEST\nb = 2.0\nc = [1, 2, 3]\nd = 4"""

import os
FILE_LIST = (
    os.path.join(os.getcwd(), 'src/test/'), "__init__.py\nex00_test.py\nex00_testdata.py", ".py")
ARGPARSE = "'filename with spaces' -i -1 -f 1e-10"

COLLATZ = [(-3.14, ([], 0)),
           (12, ([12, 6, 3, 10, 5, 16, 8, 4, 2, 1], 10)),
           (19, ([19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1], 21))]
