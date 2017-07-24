
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
            mu.mem_write(profile_._textstart + 0x34, code)
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


    def emulateKeyFunc(self, profile_, entry_, steps_):
        try:
            with open(profile_._bin, "rb") as fr:
                code = fr.read()

            mu = Uc(UC_ARCH_ARM64, UC_MODE_ARM)

            mu.mem_map(profile_._textstart, profile_._codemem + profile_._stackmem)
            mu.mem_map(profile_._heapstart, profile_._heapmem)
            mu.mem_write(profile_._textstart + 0x34, code)
            #mu.mem_write(entry_, code)
            sp = profile_._textstart + profile_._codemem + 0x500
            fp = sp + 0x10

            #startProvisioningWithDSID(-2LL, g_spim, sizeof(g_spim), &outCPIM, &outCPIMLength, &outSession)
            x0 = -2
            x1 = profile_._heapstart + 0x100
            x2 = 0
            x3 = profile_._heapstart + 0x500
            x4 = profile_._heapstart + 0x1000
            x5 = profile_._heapstart + 0x1000 + 0x100

            spim = binascii.unhexlify("00000004000000F0DA8878277D5C102B43C20884BD1492E16BA055FB304D1AAF658F9158FB3EB395CA4521998D911A7C32DAB89B2FF9FFDB6BEF0A479E5A311C6569E4AE1B45EF51632AFBBD31269860215AE3CD42A5E98EADBF9B5FCC04558AB5200923700E81CDC8140CBB28495619B2CFC9D1B7079044C75CE5844A103B6CF1DA2A7E25F4F83ED2134ACFF0FB8ABA2C9C2C14AD14F43115EA3CFB88499BF6FC4758C6D8CC3FF0DDFCCF0EFE31555E70008040E409D7F35CAD8FC81A88859EDCEC626C2CA9D94A137EE9694185C18324AFD88A9C9E3042F9A9485C249230F994814DAEDC9BB1EB622BAA2649207587E93D77F22C1FF42BF3C5E6E42FC4AE7890F88173DAE71BB300000034000000041ED32190AA92B0CC39C853B5BAAE1676E53930E3A4D523C6A70FBBB49D614A16D65B2606D872D385280774B227156C54ED9281D8F04A122105ED13044CD1E0DCA17A09066D992FB79C2A12")
            mu.mem_write(x1, spim)
            x2 = len(spim)

            mu.reg_write(UC_ARM64_REG_X0, x0)
            mu.reg_write(UC_ARM64_REG_X1, x1)
            mu.reg_write(UC_ARM64_REG_X2, x2)
            mu.reg_write(UC_ARM64_REG_X3, x3)
            mu.reg_write(UC_ARM64_REG_X4, x4)
            mu.reg_write(UC_ARM64_REG_X5, x5)


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