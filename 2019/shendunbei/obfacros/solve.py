highestBit = 0x8000000000000000
mask = highestBit*2-1
def reverse_box1(a, b):
	not_a = a
	if a&1:
		not_a_xor_b = b
		b = not_a_xor_b ^ not_a
		a = mask ^ not_a
	else:
		a_xor_b = b
		a = mask ^ not_a
		b = a_xor_b ^ a
	return (a, b)
	
def reverse_equation(b, apb):
	a = (apb-b)&mask
	return (a, b)
def reverse_shl_ab(a, b):
	b_high = a&1
	a_high = b&1
	b = ((b >> 1) & mask) | (highestBit if b_high else 0)
	a = ((a >> 1) & mask) | (highestBit if a_high else 0)
	return (a, b)
	
a, b = (0x209E9FA397B934D2, 0xFDADF00EFE1F6806)
for i in xrange(1024):
	a, b = reverse_shl_ab(a, b)
	a, b = reverse_equation(a, b)
	a, b = reverse_shl_ab(a, b)
	a, b = reverse_box1(a, b)
	
print hex(a)[2:-1][::-1] + hex(b)[2:-1][::-1]
