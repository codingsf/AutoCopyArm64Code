
from __future__ import print_function
from unicorn import *
from unicorn.arm64_const import *
import sys

from Util import *
from Hook import *
from Profile import *

class Emulator(object):
    def __init__(self):
        self._tag = "Emulator"

    def getTag(self):
        return self._tag

    def breakpoint(self, uc_, addr_):
        pc = uc_.reg_read(UC_ARM64_REG_PC)
        if pc == addr_:
            self.stopEmu(uc_, "Breakpoint!")

    def stopEmu(self, reason_):
        print(reason_)
        uc_.emu_stop()

    def emulate(self, profile_, entry_, steps_):
        try:
            with open(profile_._bin, "rb") as fr:
                code = fr.read()

            mu = Uc(UC_ARCH_ARM64, UC_MODE_ARM)

            mu.mem_map(profile_._textstart, profile_._codemem + profile_._stackmem)
            mu.mem_map(profile_._heapstart, profile_._heapmem)
            mu.mem_write(profile_._textstart, code)
            sp = profile_._textstart + profile_._codemem + 0x500
            fp = sp + 0x10

            mu.reg_write(UC_ARM64_REG_SP, sp)
            mu.reg_write(UC_ARM64_REG_FP, fp)

            mu.hook_add(UC_HOOK_CODE, Hook().hookCode, user_data=profile_._textstart)
            mu.hook_add(UC_HOOK_INTR, Hook().hookInst)
            mu.hook_add(UC_HOOK_MEM_INVALID, Hook().hookMemInvalid)
            mu.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, Hook().hookMemRw)

            mu.emu_start(entry_, profile_._textstart + len(code), count=steps_)

            print("Emulator done!")

        except UcError as e:
            Util().dumpData(mu, profile_._heapstart, profile_._tls)
            print("ERROR: %s" % e)
            print("SP = %x\nPC = %x" % (mu.reg_read(UC_ARM64_REG_SP), mu.reg_read(UC_ARM64_REG_PC)))