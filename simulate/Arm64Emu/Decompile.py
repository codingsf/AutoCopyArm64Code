from capstone import *

class Decompile(object):
    def __init__(self):
        self._tag = "Decompile"

    def getTag(self):
        return self._tag

    def disasm(self, code_):
        md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
        for i in md.disasm(code_, 0):
            #print("Asm : 0x%x:\t%s\t%s" % (i.address, i.mnemonic, i.op_str))
            return "%s\t%s" % (i.mnemonic, i.op_str)