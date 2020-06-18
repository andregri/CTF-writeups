# Analyse me

![challenge](zh3r0_2020/analyse_me/challenge.png)

The challenge is made of 2 separated parts.

## Part1

[server.py](zh3r0_2020/analyse_me/server.py)
```Python
from Crypto.Util.number import *
from Crypto.Util.strxor import strxor
from binascii import *
from base64 import *
import random
from flags import *
import string


assert len(msg)==80

msg1=msg
def from_the_bases(msg,count):
    count=(count%4)+1
    msg=''.join(msg)
    if count == 1:
        return b64encode(msg.encode())
    elif count == 2:
        return b32encode(msg.encode())
    elif count == 3 :
        return b85encode(msg.encode())
    else:
        return hexlify(msg.encode())



print('''Hello!
Welcome to Xor analysis..
There are two parts.
All the best ;)

Here is the first part:

''')
count=0
for i in range(0,len(msg1),4):
    
    print(bytes_to_long(from_the_bases(msg1[i:i+4],count)),end='|')
    count+=1

print()

user_input=input('Enter the decoded message:')

assert len(user_input)==80

if user_input==msg:
    print('You have done well.')
    print('Here is the key: ',bytes_to_long(key.encode()))

else:
    print('Try harder ;)')
    quit()

print('\nYou completed the first part \n Here is the second and final part ;) ')

print('GOOD LUCK DECODING!!! \n')
```

Running the command `nc crypto.zh3r0.ml 3871`

```
Hello!
Welcome to Xor analysis..
There are two parts.
All the best ;)

Here is the first part:

5943134639005711677|5491378081737038141|366970695973|3833466206172886320|5640277313745009981|5351739078059639101|302416945480|3762814891798442803|6354696933901548861|5139258452082510141|305635213400|3688506584576963897|5568232986773634365|5139251786226882877|357308525154|3847819437120304993|7008813202989464893|5786655223480211773|306693940071|3689633605503693413|

Enter the decoded message:
```

Reversing the algorithm I get the decoded message:

```Python
def to_bases(msg,count):
    count=(count%4)+1
    #msg=''.join(msg)
    if count == 1:
        return b64decode(msg.decode())
    elif count == 2:
        return b32decode(msg.decode())
    elif count == 3 :
        return b85decode(msg.decode())
    else:
        return unhexlify(msg.decode())

words = "5943134639005711677|5491378081737038141|366970695973|3833466206172886320|5640277313745009981|5351739078059639101|302416945480|3762814891798442803|6354696933901548861|5139258452082510141|305635213400|3688506584576963897|5568232986773634365|5139251786226882877|357308525154|3847819437120304993|7008813202989464893|5786655223480211773|306693940071|3689633605503693413|".split('|')

count = 0
final_msg = ""
for w in words:
    if w == '':
        break;
    num = long_to_bytes(int(w))
    msg = to_bases(num, count)
    count +=1
    final_msg += msg.decode()

print(final_msg)  #G00D_TH3_FIRST_P4RT_I5_D0N3_HER3_I5_4_F14G_F0R_Y0U_H4RD_W0RK_=_zh3r0{f4k3_f14g}.
```

and that's the result:

```Python
Enter the decoded message:G00D_TH3_FIRST_P4RT_I5_D0N3_HER3_I5_4_F14G_F0R_Y0U_H4RD_W0RK_=_zh3r0{f4k3_f14g}.
You have done well.
Here is the key:  140262390255733908276964893730429404145946321017929888946337794323005965712203877415028

You completed the first part
 Here is the second and final part ;)
GOOD LUCK DECODING!!!
```
[b'\x01Z\nU\x05R\x06R', b'\x0b\t\x00RV\x04\x0e\x01', b'\x06\x0b\x00W\n\x06\x05W', b'\x07\x07\x01\\\x0e\x07\x04P', b'T\x01\x06W\x03\x04\x05R', b'\x04QS\x06\x0b\n\r_', b'W\x0b\x04P\x0cST\r', b'\nUS\x01\x01U\r\x00', b'\x05T\x03\x02\x05\x08\x03\x03']
Enter the flag: