import logging

import coloredlogs

from gbemulator.cpu import CPU

log = logging.getLogger(__name__)


def main():
    cpu = CPU()
    log.debug("I am the CPU")


if __name__ == "__main__":
    coloredlogs.install(
        level="DEBUG",
        fmt="%(asctime)s %(name)s[%(funcName)s] %(levelname)s %(message)s",
        logger=log,
    )

    main()
