# MicroPython compatible version of an md5 calculator
# Use in the same way as haslib's md5 class, with .update() and .digest() methods
# Also with :bytes input and :bytes output
# Useful because some hashlibs no longer include md5 functionality
# Derived from https://github.com/Utkarsh87/md5-hashing

class md5():
    #
    def __init__(self, msg:bytes=b'') -> None:
        self.rLUT = [7,12,17,22]*4 + [5,9,14,20]*4 + [4,11,16,23]*4 + [6,10,15,21]*4
        self.cLUT = [3614090360, 3905402710,  606105819, 3250441966, 4118548399, 1200080426, 2821735955, 4249261313,
                     1770035416, 2336552879, 4294925233, 2304563134, 1804603682, 4254626195, 2792965006, 1236535329,
                     4129170786, 3225465664,  643717713, 3921069994, 3593408605,   38016083, 3634488961, 3889429448,
                      568446438, 3275163606, 4107603335, 1163531501, 2850285829, 4243563512, 1735328473, 2368359562,
                     4294588738, 2272392833, 1839030562, 4259657740, 2763975236, 1272893353, 4139469664, 3200236656,
                      681279174, 3936430074, 3572445317,   76029189, 3654602809, 3873151461,  530742520, 3299628645,
                     4096336452, 1126891415, 2878612391, 4237533241, 1700485571, 2399980690, 4293915773, 2240044497,
                     1873313359, 4264355552, 2734768916, 1309151649, 4149444226, 3174756917,  718787259, 3951481745]
        self.buff = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]
        self.blkCnt = 0 ; self.msgTail = msg
    #
    def __proc64(self, blk64:bytes):
        def rl(x, cnt): return (x << cnt | (x & 0xFFFFFFFF) >> (32-cnt)) & 0xFFFFFFFF
        assert(len(blk64) == 64)
        A,B,C,D = self.buff
        f1 = [lambda b,c,d: (b & c) | (~b & d), lambda b,c,d: (d & b) | (~d & c), lambda b,c,d: b ^ c ^ d, lambda b,c,d: c ^ (b | ~d)]
        f2 = [lambda i: i, lambda i: (5*i + 1)%16, lambda i: (3*i + 5)%16, lambda i: (7*i)%16]
        for i in range(64):
            F,G = f1[i//16](B, C, D), f2[i//16](i)
            rot = A + F + self.cLUT[i] + int.from_bytes(blk64[4*G : 4*G + 4], 'little')
            A,B,C,D = D, (B + rl(rot, self.rLUT[i])) & 0xFFFFFFFF, B, C
        for i, val in enumerate([A, B, C, D]): self.buff[i] = (self.buff[i] + val) & 0xFFFFFFFF
        return
    #
    def update(self, msg:bytes) -> None:
        self.msgTail += msg
        while len(self.msgTail) >= 64:
            self.__proc64(self.msgTail[:64])
            self.msgTail = self.msgTail[64:]
            self.blkCnt += 1
    #
    def digest(self) -> bytes:
        bitLen = (8*(len(self.msgTail) + 64*self.blkCnt)) & 0xFFFFFFFFFFFFFFFF
        msg = self.msgTail + b'\x80'
        while len(msg)%64 != 56: msg += b'\x00'
        while len(msg) >= 64: self.__proc64(msg[:64]) ; msg = msg[64:]
        msg += bitLen.to_bytes(8, 'little')
        self.__proc64(msg)
        hash = sum(val<<(32*i) for i, val in enumerate(self.buff))
        msg = b''
        self.blkCnt = 0
        self.msgTail = b''
        return hash.to_bytes(16,'little')
