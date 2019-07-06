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


if __name__ == "__main__":
    coloredlogs.install(
        level="DEBUG",
        fmt="%(asctime)s %(name)s[%(funcName)s] %(levelname)s %(message)s",
    )

    main()
