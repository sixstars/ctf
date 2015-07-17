#!/usr/bin/env python
#encoding:utf-8

import SocketServer
import requests
import time

# This function should be replaced.
def submit_flag(flag):
    """
    True => Success
    False => Duplicate
    others => error info
    """
    import random
    return random.choice([True, False, 'error info'])

def submit_with_retry(flag):
    retry = 0
    result = ''
    while retry < 3:
        try:
            result = submit_flag(flag)
            if type(result) is bool:
                return result
        except Exception, e:
            raise e
        retry += 1
        time.sleep(1)
    return result

def log(filename, msg):
    fp = open(filename, 'a')
    fp.write('[%s] %s\n' % (time.asctime(), str(msg).replace('\n', '; ')))
    fp.close()

class FlagHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        flag = self.rfile.read().strip()
        ip = self.client_address[0]
        result = submit_with_retry(flag)
        if result is True:
            log('out.log', '(%s) %s' % (ip, flag))
            self.wfile.write('Success')
        elif result is not False:
            log('error.log', '(%s) %s => %s' % (ip, flag, result))
            self.wfile.write('Error: %r, Flag: %r' % (result, flag))
        else:
            self.wfile.write('Duplicate')

if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(('', 8888), FlagHandler)
    server.serve_forever()
