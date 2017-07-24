from Emulator import *
from Hook import *
from Profile import *
from Util import *
import sys
import os
from capstone import *
import binascii

def testDisasm():
    #CODE = b'\xfc\x6f\xba\xa9' #\xfa\x67\x01\xa9\xf8\x5f\x02\xa9\xf6\x57\x03\xa9\xf4\x4f\x04\xa9\xfd\x7b\x05\xa9\xfd\x43\x01\x91\xff\x43\x04\xd1\xa5\x83\x15\xf8\xa3\x13\x38\xa9\xa1\x8b\x36\xa9\xa0\x03\x16\xf8\x1f\x20\x03\xd5\xa8\x07\x0c\x58\x08\x01\x40\xf9\xa8\x83\x1a\xf8\x7f\x00\x00\xf1\xe8\x17\x9f\x1a\x9f\x00\x00\xf1\xe9\x17\x9f\x1a\x08\x01\x09\x2a\xbf\x00\x00\xf1\xe9\x17\x9f\x1a\x08\x01\x09\x2a\x73\x46\xa3\x52\x53\x21\x88\x72\x69\x26\x00\x51\x09\x7d\x09\x1b\x0a\x25\x00\x11\xb8\x6d\x0b\x10\x1f\x20\x03\xd5\x0a\xdb\xaa\xb8\x4b\xff\xff\x10\x1f\x20\x03\xd5\x4a\x01\x0b\x8b\x1b\xf9\x95\x12\x40\x01\x1f\xd6'

    CODE = binascii.unhexlify("fc6fbaa9")

    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    for i in md.disasm(CODE, 0x1000):
        print("0x%x:\t%s\t%s" % (i.address, i.mnemonic, i.op_str))

def test():
    # Base vars

    rawdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
    path = os.path.join(rawdir, "keyfunc")

    with open(path, "rb") as fr:
        data = fr.read()
        datalen = len(data)

    nsProf = Profile(path, 0x5000, 0x500000, 0x1000, 0x700000, 0x50000)

    # Emulate code
    res = Emulator().emulateKeyFunc(nsProf, 0x44018, datalen / 4 - 1)

    # Display resulting data


    Util().dumpData(res, nsProf._heapstart, nsProf._tls)

if __name__ == "__main__":
    test()
    #testDisasm()