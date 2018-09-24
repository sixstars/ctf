1. The memory not cleared after garbage collection. So we can leak one byte per time to bypass PIE.
2. The pointer to work line are not updated after deletion. So we can insert an egg into the pointer of storage and forge the function pointer.

Since server still available, here is the flag. `flag{7h!s_S1mpl3_G4rbageC0ll3ct!0n_!s_F**k3d_up}`
