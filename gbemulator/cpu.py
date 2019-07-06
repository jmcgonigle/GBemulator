import logging
import time

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
        self.start_time = time.process_time()
        self.total_cycles = 0

    def estimate_clock_cycle(self):
        """
        A hacky attempt to estimate the clock speed of the computer, and return it based on the time elapsed and the
        number of cycles cleared.
        :return: clocks per second in MHz
        """
        time_elapsed = time.process_time() - self.start_time

        # Handle the divide by 0 errors
        if time_elapsed == 0:
            return 0

        clock_per_second = self.total_cycles/time_elapsed

        return clock_per_second / 1000000
