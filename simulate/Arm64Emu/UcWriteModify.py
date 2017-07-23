

class UcWriteModify(object):
    def __init__(self):
        self._tag = "UcWriteModify"

    def getTag(self):
        return self._tag

    def modify(self, uc_, addr_, size_, value_):
        return