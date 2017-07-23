from GlobalVariable import *

class UcReadModify(object):
    def __init__(self):
        self._tag = "UcReadModify"

    def getTag(self):
        return self._tag

    def modify(self, uc_, addr_, size_, value_):
        GlobalVariable().modify(uc_, addr_, size_, value_)
        return