from twisted.internet import reactor, protocol
from secret import FLAG
import time
import os
import random
import struct
import seccure
import gmpy

PORT = 2345

def gen_d(order):
    d = os.urandom(32)
    d = int(d.encode('hex'),16)
    return d % order

def generate_backdoor(curve,d):
    #Create a known relationship between P and Q
    Q = curve.base
    Q = Q * d

    e = gmpy.mpz(0)
    e = gmpy.invert(gmpy.mpz(d),curve.order)
    return Q

class dual_ec_dbrg(object):
    def __init__(self,seed,curve,qx,qy):
        self.i0 = seed
        self.curve = curve
        self.P = curve.base
        self.Q = seccure.AffinePoint(qx,qy,self.curve)
        if (not self.Q.on_curve):
            print "Chosen Q Not on Curve!"
            return

    def getrand(self):
        first = self.P * gmpy.mpz(self.i0) 
        x = first.x
        out = self.Q * x
        self.i0 = int(first.x)
        return int(out.x)

class MyServer(protocol.Protocol):
    def dataReceived(self,data):
        if(data.startswith("predict:")):
            if(self.gen.getrand() == int(data[8:])):
                self.transport.write("Congratz!")
                self.transport.write(FLAG)
                self.transport.loseConnection()
        else:
            self.transport.write("Syntax Error")
            self.transport.loseConnection()

    def connectionMade(self):
        self.p256curve = seccure.Curve.by_name_substring("nistp256")
        self.d = gen_d(self.p256curve.order)
        Q = generate_backdoor(self.p256curve,self.d)
		
        self.gen = dual_ec_dbrg(random.randint(0,2 ** 32),self.p256curve,int(Q.x),int(Q.y))
        self.transport.write(str(int(Q.x)) + "," + str(int(Q.y))+ "\n")
        self.transport.write(str(int(self.d))+"\n")
        self.transport.write(str(int(self.gen.getrand()))+ "\n")

class MyServerFactory(protocol.Factory):
    protocol = MyServer


factory = MyServerFactory()
reactor.listenTCP(PORT, factory)
reactor.run()
