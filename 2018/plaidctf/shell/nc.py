from pwn import *
l=listen(7777)

conn=l.wait_for_connection()

data=conn.recv()

with open("./bin","w+") as f:
	f.write(data)
