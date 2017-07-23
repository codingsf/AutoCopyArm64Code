
from __future__ import print_function
from unicorn import *
from unicorn.arm64_const import *
import struct

class Util(object):
    def __init__(self):
        self._tag = "Util"

    def getTag(self):
        return self._tag

    def readMem(self, emu_, addr_, size_):
        try:
            tmp = emu_.mem_read(addr_, size_)
            print("[0x%X bytes @ 0x%x]:\n" % (size_, addr_), end="")
            str = ''
            for i in tmp:
                str += ''.join('{:02X}'.format(i))
                str += ' '
                size_ -= 1
                if size_ % 8 == 0:
                    str += ' '
                if size_ % 16 == 0:
                    print(str + ' ')
                    str = ''
        except UcError as e:
            print("ERROR: %s" % e)

    def dumpData(self, uc_, heap_, tls_):
        if uc_ is not None:
            print("Registers:\n-----------------")
            cnt = 0
            for x in range(UC_ARM64_REG_X0, UC_ARM64_REG_X0 + 32):
                r = uc_.reg_read(x)
                print("  X%d = 0x%x" % (cnt, r))
                cnt += 1
            print("  SP = 0x%x" % uc_.reg_read(UC_ARM64_REG_SP))
            print("  PC = 0x%x\n" % uc_.reg_read(UC_ARM64_REG_PC))

            print("Memory:\n-----------------")
            print("Stack Pointer:")
            self.readMem(uc_, uc_.reg_read(UC_ARM64_REG_SP), 0x80)
            print("Frame Pointer:")
            self.readMem(uc_, uc_.reg_read(UC_ARM64_REG_FP), 0x80)

            print("IPC Command Buffer:")

            self.readMem(uc_, tls_, 0x100)