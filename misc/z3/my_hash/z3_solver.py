"""
unsigned int my_hash(char *x)
{
	int i = 1;
	int result = 0;
	for(;*x>='A' && *x<='Z'; ++x) {
		result += (*x-('A'-1)) * i;
		i *= 23;
	}
	return result;
}
"""
#https://ericpony.github.io/z3py-tutorial/guide-examples.htm
from z3 import *

MAX_IDX = 7
inp = [BitVec('inp_%d'%i, 32) for i in range(MAX_IDX)]
res = [BitVec('res_%d'%i, 32) for i in range(MAX_IDX)]
coeff = [BitVecVal(23**i, 32) for i in range(MAX_IDX)]

A = BitVecVal(65, 32)  # value for character 'A'
Z = BitVecVal(90, 32)  # value for character 'Z'

s = Solver()

s.add(res[MAX_IDX-1] == 770283071)

s.add(inp[0] >= A)
s.add(inp[0] <= Z)

res[0] = (inp[0] - A + 1)
	
for i in range(1, MAX_IDX):
	# c code is: res[i] += (input[i] - 'A' + 1) * 23**i-1
	# for z3: res[i] = res[i-1] + (input[i-1] - A + 1) * 23**i
	s.add(inp[i] >= A)
	
	s.add(inp[i] <= Z)
	s.add( (res[i-1] + (inp[i] - A + 1) * coeff[i]) == res[i])

if s.check() == sat:
	model = s.model()
	#print(f"Solution: {model}")
	print("".join(chr(model[inp[i]].as_long()) for i in range(MAX_IDX)))
else:
	print("Not solvable.")