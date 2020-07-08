"""
In this code I want to generate an ASCII character in [A-Za-z] as the xor of two
ASCII characters not in [A-Za-z]
"""

from z3 import *

def find_letter_as_xor(c):
#Find 2 ascii symbols such that their XOR is equal to the char c.
    a = BitVec('a', 8)
    b = BitVec('b', 8)

    s = Solver()
    cond1_a = And(a >= ord('!'), a < ord('A'))
    cond2_a = And(a > ord('Z'), a < ord('a'))
    cond3_a = And(a > ord('z'), a <= ord('~'))
    s.add(Or(cond1_a, cond2_a, cond3_a))
    s.add(a != ord('"'))
    s.add(a != ord('\\'))
    s.add(a != ord('`'))

    cond1_b = And(b >= ord('!'), b < ord('A'))
    cond2_b = And(b > ord('Z'),  b < ord('a'))
    cond3_b = And(b > ord('z'),  b <= ord('~'))
    s.add(Or(cond1_b, cond2_b, cond3_b))
    s.add(b != ord('"'))
    s.add(b != ord('\\'))
    s.add(b != ord('`'))

    s.add(a^b == ord(c))

    if s.check() == sat:
        #print(s.model())
        char1 = chr(s.model()[a].as_long())
        char2 = chr(s.model()[b].as_long())
        assert(ord(char1)^ord(char2) == ord(c))
        #print(f"{char1} ^ {char2} = {result}")
        return char1, char2


# echo(file_get_contents('flag.txt'));
php_string = "_GET"
php_1 = ""
php_2 = ""
for c in php_string:
    char1, char2 = find_letter_as_xor(c)
    php_1 += char1
    php_2 += char2

print(f'"{php_1}"^"{php_2}"')