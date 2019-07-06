import logging

import coloredlogs

from gbemulator.cpu import CPU

log = logging.getLogger(__name__)


def main():
    cpu = CPU()

    log.debug("I am the CPU")

    print(cpu.registers)

    cpu.LD_SP_nn()

    print(cpu.registers)

    # bios:
    # 0x31, 0xFE, 0xFF,
    # LD SP,$fffe

    # 0xAF,
    # XOR A

    # 0x21, 0xFF, 0x9F,
    # LD HL,$9fff

    # 0x32,
    # LD (HL-),A

    # 0xCB, 0x7C,
    # BIT 7,H

    # 0x20, 0xFB,
    # JR NZ $00FB

    # 0x21, 0x26, 0xFF, 0x0E,


if __name__ == "__main__":
    coloredlogs.install(
        level="DEBUG",
        fmt="%(asctime)s %(name)s[%(funcName)s] %(levelname)s %(message)s",
    )

    main()
