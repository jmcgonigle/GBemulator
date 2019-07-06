import logging


log = logging.getLogger(__name__)


class Registers:
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


class CPU:
    def __init__(self):
        self.registers = Registers()
