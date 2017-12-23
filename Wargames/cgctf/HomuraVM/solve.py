from z3 import *
import copy
inputt=[BitVec("input_%d"%i,8) for i in range(35)]
z=copy.copy(inputt)
s=Solver()
offset=[0,-3,2,0,3,-2,1,5,1,-1,4,-1,0,2,2,5,2,-2,2,1,1,2,0,2,2,2,6,-3,-1,-1,2,-2,-1,0]
answer=[27,114,17,118,8,74,126,5,55,124,31,88,104,7,112,7,49,108,4,47,4,105,54,77,127,8,80,12,109,28,127,80,29,96]

for i in range(34):
	
	s.add((inputt[i]+inputt[i+1]+offset[i]-2*(inputt[i]&(inputt[i+1]+offset[i])))==answer[i])
	inputt[i+1]=(inputt[i]+inputt[i+1]+offset[i]-2*(inputt[i]&(inputt[i+1]+offset[i])))

if s.check() !=sat:
	print "unsat"
else:
	m=s.model()
	print m
	print repr("".join([chr(m[z[i]].as_long()) for i in range(35)]))
	#print m[z[0]]
