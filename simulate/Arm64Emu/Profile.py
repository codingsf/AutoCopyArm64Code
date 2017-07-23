

class Profile(object):
    def __init__(self, binstr_, textstart_, heapstart_, stackmem_, heapmem_, codemem_):
        self._bin = binstr_
        self._textstart = textstart_
        self._heapstart = heapstart_
        self._stackmem = stackmem_
        self._heapmem = heapmem_
        self._codemem = codemem_
        self._tls = heapstart_  # my custom IPC TLS hook