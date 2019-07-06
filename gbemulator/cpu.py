import json
import logging

from .util import as_binary, as_hex, Bits

log = logging.getLogger(__name__)


class Registers:
    # flag register has 8 values (0-7). bits 0-3 aren't used.
    # Z flag - sets the 7th bit
    zero_flag = 0x80
    # N flag - sets the 6th bit
    subtract_flag = 0x40
    # H flag - sets the 5th bit
    half_carry_flag = 0x20
    # C flag - sets the 4th bit
    carry_flag = 0x10

    def __init__(self):
        # general purpose registers - (8-bit can hold value of 0-255)
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.h = 0
        self.l = 0

        # flag register (8-bit)
        self.f = 0

        # program counter
        self.pc = 0

        # stack pointer (16-bit)
        self.sp = 0

    @property
    def af(self):
        return self.a << 8 | self.f

    @af.setter
    def af(self, value):
        Bits.check_is_word(value)

        self.a = Bits.msb(value)
        self.f = Bits.lsb(value)

    @property
    def bc(self):
        return self.b << 8 | self.c

    @bc.setter
    def bc(self, value):
        Bits.check_is_word(value)

        self.b = Bits.msb(value)
        self.c = Bits.lsb(value)

    @property
    def de(self):
        return self.d << 8 | self.e

    @de.setter
    def de(self, value):
        Bits.check_is_word(value)

        self.d = Bits.msb(value)
        self.e = Bits.lsb(value)

    @property
    def hl(self):
        return self.h << 8 | self.l

    @hl.setter
    def hl(self, value):
        Bits.check_is_word(value)

        self.h = Bits.msb(value)
        self.l = Bits.lsb(value)

    def reset_flags(self):
        """
        Turn off all flags by setting them to 0

        :return:
        """
        self.f &= 0x00

    def set_flag(self, flag):
        """
        Turn a flag on by setting the appropriate bit

        :param flag: 8 bit number
        :return:
        """
        self.f |= flag

    def reset_flag(self, flag):
        """
        Set a flag to 0
        :param flag:
        :return:
        """
        self.f &= ~flag

    def get_flag(self, flag):
        return self.f & flag == flag

    def set_Z(self):
        self.set_flag(self.zero_flag)

    def reset_Z(self):
        self.set_flag(self.zero_flag)

    def get_Z(self):
        return self.get_flag(self.zero_flag)

    def set_N(self):
        self.set_flag(self.subtract_flag)

    def reset_N(self):
        self.set_flag(self.subtract_flag)

    def get_N(self):
        return self.get_flag(self.subtract_flag)

    def set_H(self):
        self.set_flag(self.half_carry_flag)

    def reset_H(self):
        self.set_flag(self.half_carry_flag)

    def get_H(self):
        return self.get_flag(self.half_carry_flag)

    def set_C(self):
        self.set_flag(self.carry_flag)

    def reset_C(self):
        self.set_flag(self.carry_flag)

    def get_C(self):
        return self.get_flag(self.carry_flag)

    def __str__(self):
        data = self.__dict__.copy()

        for key in data.keys():
            if key == "f":
                data["f"] = "b" + as_binary(data["f"])
            else:
                data[key] = "0x" + as_hex(data[key])

        for i in "af", "bc", "de", "hl":
            data[i] = "0x" + as_hex(getattr(self, i))

        return json.dumps(data, indent=4, sort_keys=True)


class Clock:
    def __init__(self):
        self.m = 0
        self.t = 0


class MMU:
    """Mock MMU until it is implemented"""

    def __init__(self, registers):
        self.registers = registers

    def read_byte(self, addr):
        return 0xFF

    def read_word(self, addr):
        return 0xFFFF

    def write_byte(self, addr, value):
        pass


class CPU:
    """
    Class representing the Z80 CPU
    """

    def __init__(self):
        self.registers = Registers()
        self.clock = Clock()

        self.mmu = MMU(self.registers)

    def __getattribute__(self, name):
        if name[0].isupper():
            log.debug(f"{name} called")

        # Default behaviour
        return object.__getattribute__(self, name)

    def _read_and_increment_pc(self, num_bytes):
        value = 0x00

        for i in range(num_bytes):
            next_byte = self.mmu.read_word(self.registers.pc)
            value = value << 8 | next_byte

        self.registers.pc += num_bytes

        return value

    # 0x31
    def LD_SP_nn(self):
        # read next 2 bytes from the program counter
        value = self._read_and_increment_pc(2)

        # put value into SP
        self.registers.sp = value

    # 0xAF
    def XOR_A(self):
        self.registers.a ^= self.registers.a

    # 0x21
    def LD_HL_nn(self):
        # read next 2 bytes from the program counter
        value = self._read_and_increment_pc(2)

        self.registers.hl = value

    # 0x32
    def LDD_HL_A(self):
        """
        Put the value of A into the _address_ pointed to by HL, then decrement.
        :return:
        """

        self.mmu.write_byte(self.registers.hl, self.registers.a)
        self.registers.hl -= 1

    # 0xCB 0x7C - may need a single BIT method
    def BIT_H_b(self):
        # Z - Set if bit b of register r is 0.
        # N - Reset.
        # H - Set.
        # C - Not affected.
        bit = self._read_and_increment_pc(1)

        self.registers.reset_Z()
        if (self.registers.h >> bit) & 0x00:
            self.registers.set_Z()

        self.registers.reset_N()

        self.registers.set_H()
