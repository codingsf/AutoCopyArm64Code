import struct

class GlobalVariable(object):
    def __init__(self):
        self._tag = "GlobalVariable"

    def getTag(self):
        return self._tag


    def modify(self, uc_, addr_, size_, value_):
        if addr_ == 0x5C140:
            uc_.mem_write(addr_, struct.pack("<q", addr_))
            value_ = addr_
