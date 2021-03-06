from unicorn import *
from unicorn.arm64_const import *
import struct
import binascii

class UcInstModify(object):
    def __init__(self):
        self._tag = "UcInstModify"

    def getTag(self):
        return self._tag

    def modify(self, uc_, pc_, addr_, size_):
        if pc_ == 0x4408C:
            print("instruction 0x4408C is modified!")
            w10 = uc_.reg_read(UC_ARM64_REG_W10)
            print("w10 : %x", w10)
            jmptable = [
                0xC4, 0x90, 0x5C, 0x310, 0x80, 0x6C, 0x25FC, 0xB4,
                0x474, 0x2C, 0x2628, 0x40, 0x1808, 0x9C, 0x340, 0,
                0x70, 0x54, 0xAC, 0x1F4, 0x58, 0x108, 0, 0x54, 0x2C,
                0x198, 0x5C, 0xB0, 0x1D0, 0x40, 0x30, 0x64, 0, 0x34,
                0x44, 0x10A4, 0x34, 0x58, 0x5C, 0x28, 0x70, 0x10, 8,
                8, 0x3C, 0x4C, 0x38, 0x40, 0x50, 0x60, 0x38, 0x48,
                0x10, 0x10, 0x10, 0x44, 0x54, 0x140, 0x78, 0x64, 0x234,
                0x2BC, 0x88, 0x40, 0x1D0, 0x70, 0x32C, 0x500, 0x68,
                0x5C, 0x388, 0x88, 0x190, 0x5C, 0x110, 0x68, 0xAC,
                0xFFFFF62C, 0x5C, 0x108, 0x200, 0x44, 0x17C, 0x70,
                0x260, 0x4C, 8, 0x54, 0x74, 0x89C, 0x58, 0x60, 0x14,
                0, 0x30, 0x104, 0x4C, 0x3C, 0xCC, 0x48, 0x594, 0xEC,
                0x40, 0x48, 0x44, 0x7B8, 8, 0x504, 0x38, 0x774, 0x780,
                0x8A8, 0x9B0, 0xA0, 0x54, 0x6C, 0x28, 0x68, 0x1538,
                0x34, 0x44, 0x418, 0xCC, 0x48, 0x460, 0x22C, 0x84,
                0x58, 0x250, 0x974, 0x7C, 0x4C, 0x350, 0, 0x64, 0x50,
                0x4AC, 0x54, 0x3C, 0x388, 0x68, 0x208, 0x74, 0x18F8,
                0x38, 0x44, 0x2D8, 0, 0x88, 0x2C, 0x4C, 0x1E0, 0x78,
                0xDA4, 0x218, 0x7C, 0x6C, 0x78, 0x1C4C, 0x34, 0x5C,
                0x3C, 0x320, 0, 0x80, 0x54, 0x170, 0x10EC, 0x48, 0x268,
                0x30, 0xFFFFFD08, 0, 0x1CC, 0x4C, 0xEC, 0, 0x44, 0x40,
                0x20C, 0x30, 0x328, 0x5C, 0xA0, 0x44, 0x1FE8, 0x3C,
                0x4C, 0x2AC, 0x220, 0x78, 0x3C, 0x360, 0x98, 0x1474,
                0, 0x70, 0x20, 0x2500, 0x24E0, 0x5C, 0x1AC, 0, 0,
            ]

            jmpdata = b''
            for jmpitem in jmptable:
                itemdata = struct.pack("<I", jmpitem)
                jmpdata = jmpdata + itemdata

            uc_.mem_write(pc_ + 0x16db4, jmpdata)
            rawdata = uc_.mem_read(pc_ + 0x16db4, 100 * 4)
            print binascii.b2a_hex(rawdata)

        if pc_ == 0x44094:
            x10 = uc_.reg_read(UC_ARM64_REG_X10)
            print("x10 : %x" % x10)

        if pc_ == 0x440A8:
            x10 = uc_.reg_read(UC_ARM64_REG_X10)
            print("x10 : %x" % x10)

        if pc_ == 0x440E4:
            x8 = uc_.reg_read(UC_ARM64_REG_X8)
            print("x8 : %x" % x8)

        if pc_ == 0x440D0:
            x9 = uc_.reg_read(UC_ARM64_REG_X9)
            print("x9 : %x" % x9)