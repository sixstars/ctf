# -*-coding:utf-8-*-
'''
Created on 2016-4-6

@author: 014731
'''

''' 
填充规则 
''' 
SM4_PAD_PBOC = 0x04 
PAD_PBOC = '80000000000000000000000000000000' 

SM4_PAD_UNION = 0x08 
PAD_UNION = '00000000000000000000000000000000' 

try:
    integer_types = (int, long)
except NameError:
    integer_types = (int,)

def is_integer(obj):
    return isinstance(obj, integer_types)

def is_byte(int_num):
    '''
          定义8位为一个byte
    byte 范围为 0x00 - 0xFF
    '''
    if is_integer(int_num) == False:
        return False
    if int_num < 0x00 or int_num > 0xFF:
        return False
    return True
    
def is_word(int_num):
    '''
           定义32位为一个word
           即一个字的大小范围为 0x00000000 - 0xFFFFFFFF
    '''
    if is_integer(int_num) == False:
        return False
    if int_num < 0x00000000 or int_num > 0xFFFFFFFF:
        return False
    return True

def IsHexCharacter(hexstring):
    '''
           判断字符串中字符是否都是16进制字符 0-9 a-f A-F
    '''
    base = [str(x) for x in range(0,10)] + [chr(y) for y in range(ord('A'), ord('A') + 6)]
    for character in hexstring:
        if character.upper() not in base:
            return False
    return True

def lrotate(src, bits):
    '''
           循环左移计算
    '''
    if is_integer(src) == False:
        raise Exception('源数据不是整数类型，不能进行移位操作')
    
    return ((src << bits) | (src >> abs(32 - bits))) & 0xFFFFFFFF

def Xor(data1, data2):
    '''
           异或运算
    '''
    if is_integer(data1) == False or is_integer(data2) == False:
        raise Exception('源数据不是整数类型，不能进行异或运算')
    return data1 ^ data2

def message_padding(message, rule = 4): 
    if len(message) % 2 != 0: 
        raise Exception('待加密数据长度不正确,必须为2的整倍数')
    padmsg = '' 
    if rule == SM4_PAD_PBOC: 
        ''' 
        PBOC规范要求填充80 
        ''' 
        if len(message) % 32 == 0: 
            padmsg = message + PAD_PBOC 
        else: 
            padmsg = message + PAD_PBOC[0:(len(message) / 32 + 1) * 32 - len(message)] 
    elif rule == SM4_PAD_UNION: 
        ''' 
        UNION规范要求填充00 
        ''' 
        if len(message) % 32 == 0: 
            padmsg = message 
        else: 
            padmsg = message + PAD_UNION[0:(len(message) / 32 + 1) * 32 - len(message)] 
    else: 
        raise Exception('未知填充规则') 
     
    return padmsg 

def gcd(a, b):
    '''
    求a,b最大公约数
    '''
    while b != 0:
        c = a%b
        a = b
        b = c
    return a
#-------------------------------------------------------------
if __name__ == '__main__':
    print lrotate(0x00000001, 2)
    print Xor(0xF0, 0x0F)
    print gcd(0xFF00AB,0xAABB00)