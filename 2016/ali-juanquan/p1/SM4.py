# -*-coding:utf-8-*- 
''' 
Created on 2016-4-6 
 
@author: 014731 
''' 
 
import common 
 
''' 
FK=(FK0, FK1, FK2, FK3)为系统参数，CK=(CK0, CK1,…, CK31)为固定参数， 
用于密钥扩展算法，其中FKi(i=0,…,3)、CKi(i=0,…,31)为字。 
FK与CK值由国家密码算法规范指定 
''' 
SM4_FK = (0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC) 
SM4_CK = (0X00070E15, 0X1C232A31, 0X383F464D, 0X545B6269,
          0X70777E85, 0X8C939AA1, 0XA8AFB6BD, 0XC4CBD2D9,
          0XE0E7EEF5, 0XFC030A11, 0X181F262D, 0X343B4249,
          0X50575E65, 0X6C737A81, 0X888F969D, 0XA4ABB2B9,
          0XC0C7CED5, 0XDCE3EAF1, 0XF8FF060D, 0X141B2229,
          0X30373E45, 0X4C535A61, 0X686F767D, 0X848B9299,
          0XA0A7AEB5, 0XBCC3CAD1, 0XD8DFE6ED, 0XF4FB0209,
          0X10171E25, 0X2C333A41, 0X484F565D, 0X646B7279) 
''' 
S 盒为固定的 8 比特输入 8 比特输出的置换，记为 Sbox(.) 
S盒阵列值由国家密码算法规范指定 
''' 
SM4_SBOX = [0XD6, 0X90, 0XE9, 0XFE, 0XCC, 0XE1, 0X3D, 0XB7, 0X16, 0XB6, 0X14, 0XC2, 0X28, 0XFB, 0X2C, 0X05,
            0X2B, 0X67, 0X9A, 0X76, 0X2A, 0XBE, 0X04, 0XC3, 0XAA, 0X44, 0X13, 0X26, 0X49, 0X86, 0X06, 0X99,
            0X9C, 0X42, 0X50, 0XF4, 0X91, 0XEF, 0X98, 0X7A, 0X33, 0X54, 0X0B, 0X43, 0XED, 0XCF, 0XAC, 0X62,
            0XE4, 0XB3, 0X1C, 0XA9, 0XC9, 0X08, 0XE8, 0X95, 0X80, 0XDF, 0X94, 0XFA, 0X75, 0X8F, 0X3F, 0XA6,
            0X47, 0X07, 0XA7, 0XFC, 0XF3, 0X73, 0X17, 0XBA, 0X83, 0X59, 0X3C, 0X19, 0XE6, 0X85, 0X4F, 0XA8,
            0X68, 0X6B, 0X81, 0XB2, 0X71, 0X64, 0XDA, 0X8B, 0XF8, 0XEB, 0X0F, 0X4B, 0X70, 0X56, 0X9D, 0X35,
            0X1E, 0X24, 0X0E, 0X5E, 0X63, 0X58, 0XD1, 0XA2, 0X25, 0X22, 0X7C, 0X3B, 0X01, 0X21, 0X78, 0X87,
            0XD4, 0X00, 0X46, 0X57, 0X9F, 0XD3, 0X27, 0X52, 0X4C, 0X36, 0X02, 0XE7, 0XA0, 0XC4, 0XC8, 0X9E,
            0XEA, 0XBF, 0X8A, 0XD2, 0X40, 0XC7, 0X38, 0XB5, 0XA3, 0XF7, 0XF2, 0XCE, 0XF9, 0X61, 0X15, 0XA1,
            0XE0, 0XAE, 0X5D, 0XA4, 0X9B, 0X34, 0X1A, 0X55, 0XAD, 0X93, 0X32, 0X30, 0XF5, 0X8C, 0XB1, 0XE3,
            0X1D, 0XF6, 0XE2, 0X2E, 0X82, 0X66, 0XCA, 0X60, 0XC0, 0X29, 0X23, 0XAB, 0X0D, 0X53, 0X4E, 0X6F,
            0XD5, 0XDB, 0X37, 0X45, 0XDE, 0XFD, 0X8E, 0X2F, 0X03, 0XFF, 0X6A, 0X72, 0X6D, 0X6C, 0X5B, 0X51,
            0X8D, 0X1B, 0XAF, 0X92, 0XBB, 0XDD, 0XBC, 0X7F, 0X11, 0XD9, 0X5C, 0X41, 0X1F, 0X10, 0X5A, 0XD8,
            0X0A, 0XC1, 0X31, 0X88, 0XA5, 0XCD, 0X7B, 0XBD, 0X2D, 0X74, 0XD0, 0X12, 0XB8, 0XE5, 0XB4, 0XB0,
            0X89, 0X69, 0X97, 0X4A, 0X0C, 0X96, 0X77, 0X7E, 0X65, 0XB9, 0XF1, 0X09, 0XC5, 0X6E, 0XC6, 0X84,
            0X18, 0XF0, 0X7D, 0XEC, 0X3A, 0XDC, 0X4D, 0X20, 0X79, 0XEE, 0X5F, 0X3E, 0XD7, 0XCB, 0X39, 0X48] 
 
''' 
算法模式 
''' 
SM4_ECB = 0x01 
SM4_CBC = 0x02 

'''
CBC模式加解密初始向量
'''
CBC_IV = '00000000000000000000000000000000'

def _line_conv_L(srcdata): 
    ''' 
           线性变换 L C=L(B)=B^(B<<<2)^(B<<<10)^(B<<<18)^(B<<<24) 
    B : 一个word 
    ''' 
    if common.is_word(srcdata) == False: 
        raise Exception('源数据不在word定义范围[0x00000000 - 0xFFFFFFFF]，不能进行变换计算') 
     
    return srcdata ^ common.lrotate(srcdata, 2) ^ common.lrotate(srcdata, 10) ^ common.lrotate(srcdata, 18) ^ common.lrotate(srcdata, 24) 
 
def _line_conv_LN(srcdata): 
    ''' 
           线性变换 L' C=L'(B)=B^(B<<<13)^(B<<<23) 
    B : 一个word 
    ''' 
    if common.is_word(srcdata) == False: 
        raise Exception('源数据不在word定义范围[0x00000000 - 0xFFFFFFFF]，不能进行变换计算') 
     
    return srcdata ^ common.lrotate(srcdata, 13) ^ common.lrotate(srcdata, 23) 
 
def _sbox_conv(srcdata): 
    ''' 
    S 盒变换，输入'ef'，则经 S 盒后的值为表中第 e 行和第 f列的值，Sbox('ef')= '84' 
    ''' 
    if common.is_byte(srcdata) == False: 
        raise Exception('源数据不在byte定义范围[0x00 - 0xFF]，不能进行S 盒变换计算') 
     
    return SM4_SBOX[srcdata] 
 
def _no_line_conv(srcdata): 
    ''' 
           非线性变换  将一个word通过S 盒转换为另外一个word 
    ''' 
    if common.is_word(srcdata) == False: 
        raise Exception('源数据不在word定义范围[0x00000000 - 0xFFFFFFFF]，不能进行变换计算') 
     
    four = srcdata & 0x000000FF 
    three = (srcdata & 0x0000FF00) >> 8 
    secod = (srcdata & 0x00FF0000) >> 16 
    first = (srcdata & 0xFF000000) >> 24 
     
    return (SM4_SBOX[first] << 24) | (SM4_SBOX[secod] << 16) | (SM4_SBOX[three] << 8) | (SM4_SBOX[four]) 
      
def _t_conv(srcdata): 
    ''' 
    T 是一个可逆变换，由非线性变换 τ 和线性变换 L 复合而成,即 T(.)=L(τ(.)) 
    ''' 
    if common.is_word(srcdata) == False: 
        raise Exception('源数据不在word定义范围[0x00000000 - 0xFFFFFFFF]，不能进行变换计算') 
     
    return _line_conv_L(_no_line_conv(srcdata)) 
 
def _tn_conv(srcdata): 
    ''' 
    TN 是一个可逆变换，由非线性变换 τ 和线性变换 L' 复合而成,即 T(.)=L'(τ(.)) 
    ''' 
    if common.is_word(srcdata) == False: 
        raise Exception('源数据不在word定义范围[0x00000000 - 0xFFFFFFFF]，不能进行变换计算') 
     
    return _line_conv_LN(_no_line_conv(srcdata)) 
     
def _generate_ext_keys(initkey): 
    ''' 
          通过密钥扩展算法生成加密算法的轮密钥 
    ''' 
    if len(initkey) % 2 != 0: 
        raise Exception('加密密钥长度[%s]错误' % len(initkey)) 
    if common.IsHexCharacter(initkey) == False: 
        raise Exception('加密密钥含有非法字符(非16进制字符)') 
    MK = (initkey[:8], initkey[8:16], initkey[16:24], initkey[24:]) 
    K = [] 
    for i in xrange(0, len(MK)): 
        K.append(common.Xor(int(MK[i], 16), SM4_FK[i])) 
     
    for i in xrange(0, 32): 
        xorrsp = common.Xor(common.Xor(common.Xor(K[i + 1], K[i + 2]), K[i + 3]), SM4_CK[i]) 
        K.append(common.Xor(K[i], _tn_conv(xorrsp))) 
     
    return K[4:] 
     
class SM4(object): 
    ''' 
           国家密码对称算法类 
           该算法的分组长度为 128 比特，密钥长度为 128 比特。加密算法与密钥扩展算法都采用 32 轮非线性迭代结构。 
           解密算法与加密算法的结构相同，只是轮密钥的使用顺序相反，解密轮密钥是加密轮密钥的逆序。 
    ''' 
     
    def __init__(self, key='00000000000000000000000000000000'): 
        ''' 
        key : 用来加密数据的密钥，长度为128bits  hexstring 
        '''     
        self.key = key 
        self.fk = SM4_FK 
        self.ck = SM4_CK 
        self.sbox = SM4_SBOX 
        self.extkeys = _generate_ext_keys(key) 
        print self.extkeys
     
    def __str__(self): 
        return 'sm4 object, key : %s' % self.key 
     
    def _sm4_encrypt_128bits(self, message): 
        ''' 
                     单组128bits加密 
        ''' 
        if len(message) != 32: 
            raise Exception('原始分组数据长度错误,单个分组长度为128bits') 
        if common.IsHexCharacter(message) == False: 
            raise Exception('原始数据包含非法字符(非16进制字符)') 
         
        X = [int(message[:8], 16), int(message[8:16], 16), int(message[16:24], 16), int(message[24:], 16)] 
        for i in xrange(0, 32): 
            xorrsp = common.Xor(common.Xor(common.Xor(X[i + 1], X[i + 2]), X[i + 3]), self.extkeys[i]) 
            X.append(common.Xor(X[i], _t_conv(xorrsp))) 
        return '%08X%08X%08X%08X' % (X[35], X[34], X[33], X[32]) 
 
    def _sm4_decrypt_128bits(self, message): 
        ''' 
                     单组128bits解密 
        ''' 
        if len(message) != 32: 
            raise Exception('原始分组数据长度错误,单个分组长度为128bits') 
        if common.IsHexCharacter(message) == False: 
            raise Exception('原始数据包含非法字符(非16进制字符)') 
         
        X = [int(message[:8], 16), int(message[8:16], 16), int(message[16:24], 16), int(message[24:], 16)] 
        for i in xrange(0, 32): 
            xorrsp = common.Xor(common.Xor(common.Xor(X[i + 1], X[i + 2]), X[i + 3]), self.extkeys[31 - i]) 
            X.append(common.Xor(X[i], _t_conv(xorrsp))) 
        return '%08X%08X%08X%08X' % (X[35], X[34], X[33], X[32]) 
    
    def sm4_encrypt(self, message, enc_mode): 
        ''' 
        message  待加密数据 
        enc_mode 加密模式   ECB/CBC 
        ''' 

        if len(message) % 32 != 0: 
            raise Exception('待加密数据长度[%s]错误,需要为32的整倍数(含填充数据)' % len(message))
         
        if common.IsHexCharacter(message) == False: 
            raise Exception('待加密数据含有非法字符(非16进制字符)') 
        
        C = '' 
        if enc_mode == SM4_ECB: 
            position = 0 
            while True: 
                ''' 
                                            循环加密所有分组 
                ''' 
                group = message[position:position + 32]
                C += self._sm4_encrypt_128bits(group) 
                position += 32                 
                if len(message) == position: 
                    break 
        elif enc_mode == SM4_CBC: 
            position = 0
            iv = CBC_IV
            while True: 
                ''' 
                                            循环加密所有分组 
                ''' 
                group = message[position:position + 32]
                xorrsp = common.Xor(int(iv,16), int(group, 16))
                iv = self._sm4_encrypt_128bits('%032X' % xorrsp)
                C += iv
                position += 32                 
                if len(message) == position: 
                    break
        else: 
            pass 
        return C 
     
    def sm4_decrypt(self, message, dec_mode): 
        ''' 
        message 待解密密文数据 
        dec_mode 解密模式   ECB/CBC 
        ''' 
        if len(message) % 32 != 0: 
            raise Exception('待解密数据长度[%s]错误,需要为32的整倍数' % len(message))
         
        if common.IsHexCharacter(message) == False: 
            raise Exception('待解密数据含有非法字符(非16进制字符)')
        
        M = '' 
        if dec_mode == SM4_ECB: 
            position = 0 
            while True: 
                ''' 
                                            循环解密所有分组 
                ''' 
                group = message[position:position + 32] 
                M += self._sm4_decrypt_128bits(group) 
                position += 32                 
                if len(message) == position: 
                    break 
        elif dec_mode == SM4_CBC: 
            position = 0
            iv = CBC_IV
            while True: 
                ''' 
                                            循环解密所有分组 
                ''' 
                group = message[position:position + 32]
                decrsp = self._sm4_decrypt_128bits(group)
                M += '%032X' % common.Xor(int(iv,16), int(decrsp, 16))
                position += 32
                iv = group
                if len(message) == position: 
                    break
        else: 
            pass 
        return M 
     
#----------------------------------------------------------------------------------------------------- 
if __name__ == '__main__': 
    from common import *

    ''' 
    print _sbox_conv(0x01) 
    print _no_line_conv(0xe1e10101) 
     
    i = 0 
    for num in _generate_ext_keys('0123456789abcdeffedcba9876543210'): 
        print 'rk[%02d] = [%08X]' % (i, num) 
        i += 1 
    ''' 
    ''' 
    print _message_padding('0123456789abcdeffedcba987654', SM4_PAD_PBOC) 
    print _message_padding('0123456789abcdeffedcba9876543210', SM4_PAD_PBOC) 
    print _message_padding('0123456789abcdeffedcba98765432103210', SM4_PAD_PBOC) 
    print _message_padding('0123456789abcdeffedcba987654', SM4_PAD_UNION) 
    print _message_padding('0123456789abcdeffedcba9876543210', SM4_PAD_UNION) 
    print _message_padding('0123456789abcdeffedcba98765432103210', SM4_PAD_UNION) 
    ''' 
    print 'ECB : '
    # sm4 = SM4(key='0123456789abcdeffedcba9876543210') 
    sm4 = SM4(key='6B8C45BEE7CEA2EB05322199A0BB0BA2') 
    message = '0123456789abcdeffedcba9876543210' 
    print '待加密数据: ', message 
    print '密钥: ', sm4.__str__() 
    C = sm4.sm4_encrypt(message_padding(message, SM4_PAD_PBOC), SM4_ECB) 
    print '密文: ', C 
    M = sm4.sm4_decrypt(C, SM4_ECB) 
    print '明文: ', M 
    print '-'*120
    print 'ECB : '
    message = u'qqwq' 
    extmessage = reduce(lambda x, y: x + '%02X' % y, map(ord, list(message)), '') 
    print 'message:    ', message 
    print 'extmessage: ', extmessage 
    print '待加密数据: ', extmessage 
    print '密钥: ', sm4.__str__() 
    C = sm4.sm4_encrypt(message_padding(extmessage, SM4_PAD_UNION), SM4_ECB) 
    print '密文: ', C 
    M = sm4.sm4_decrypt(C, SM4_ECB) 
    print '明文: ', M 
    print '-'*120
    print 'CBC : '
    # message = '0123456789abcdeffedcba9876543210' 
    message = 'A344228955254FDC354211AE5DE4E7681C4B18B85034051A83E331596B5854DA10101010101010101010101010101010'
    print '待加密数据: ', message 
    print '密钥: ', sm4.__str__() 
    C = sm4.sm4_encrypt(message_padding(message, SM4_PAD_UNION), SM4_CBC)
    print '密文: ', C 
    M = sm4.sm4_decrypt(C, SM4_CBC) 
    print '明文: ', M 
    print '-'*120


    # message = '1DA49363BE14B8E316F323F26828AA166129A5B388DEC30F7EB1B4822A04C958FEEF7F7E6C9000E5F820EC8C497A1CCF'
    # print '待加密数据: ', message 
    print '密钥: ', sm4.__str__() 
    # C = sm4.sm4_encrypt(message_padding(message, SM4_PAD_UNION), SM4_CBC)
    C = '1DA49363BE14B8E316F323F26828AA166129A5B388DEC30F7EB1B4822A04C958FEEF7F7E6C9000E5F820EC8C497A1CCF'
    print '密文: ', C 
    M = sm4.sm4_decrypt(C, SM4_CBC) 
    print '明文: ', M 
    print '-'*120


    # message = '1DA49363BE14B8E316F323F26828AA166129A5B388DEC30F7EB1B4822A04C958FEEF7F7E6C9000E5F820EC8C497A1CCF'
    # print '待加密数据: ', message 
    print '密钥: ', sm4.__str__() 
    # C = sm4.sm4_encrypt(message_padding(message, SM4_PAD_UNION), SM4_CBC)
    C = 'c92208882bedc0249701e009c04d4f0e1e1121abe08c8efb72573f215174e860dfe7f97610dd9ce15c78321342a18e5a'
    print '密文: ', C 
    M = sm4.sm4_decrypt(C, SM4_CBC) 
    print '明文: ', M 
    print '-'*120

