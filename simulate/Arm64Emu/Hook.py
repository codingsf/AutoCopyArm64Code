
from __future__ import print_function
from unicorn import *
from unicorn.arm64_const import *
from Decompile import *

from Emulator import *
from UcReadModify import *
from UcWriteModify import *

import binascii

class Hook(object):
    def __init__(self):
        self._tag = "Hook"

    def getTag(self):
        return self._tag

    def hookMemInvalid(self, uc_, access_, addr_, size_, value_, userdata_):
        if access_ == UC_MEM_WRITE:
            print("Memory fault on WRITE @ 0x%08X, size = %u, value = 0x%08X" % (addr_, size_, value_))
        else:
            print("Memory fault on READ @ 0x%08X, size = %u" % (addr_, size_))


    def hookMemRw(self, uc_, access_, addr_, size_, value_, userdata_):
        if access_ == UC_MEM_WRITE:
            access_ = "WRITE"
            UcWriteModify().modify(uc_, addr_, size_, value_)
        else:
            access_ = "READ"
            UcReadModify().modify(uc_, addr_, size_, value_)
        print("Memory %s @ 0x%X,\t[0x%08X]" % (access_, addr_, value_))


    def hookInst(self, uc_, intno_, userdata_):
        if intno_ == 2:
            print("Int No. is 2")
        else:
            Emulator().stopEmu(uc_, "Unknown exception![%u]" % (intno_))

    def hookCode(self, uc_, addr_, size_, userdata_):
        pc = uc_.reg_read(UC_ARM64_REG_PC)
        inst = uc_.mem_read(pc, 4)
        inst = binascii.unhexlify(binascii.b2a_hex(inst))
        asm = Decompile().disasm(inst)
        addr = userdata_
        print("PC = 0x%X [0x%X], asm : %s, inst : %s" % (pc, pc - addr, asm, binascii.b2a_hex(inst)))