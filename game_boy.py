import argparse
import logging
import coloredlogs

log = logging.getLogger(__name__)


class PyGameBoy:
    def __init__(self, ROM):
        with open(ROM, 'rb') as byte_rom:
            self.ROM = byte_rom.read()

    def print_hex_range(self, i, j):
        log.debug(','.join([format(value, '02x') for value in self.ROM[i:j]]))


def get_args():
    description = 'GAMEBOY EMULATOR.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--insert-rom', required=True,
                        help='Path to rom.')
    return parser.parse_args()


def main():
    args = get_args()
    emulator = PyGameBoy(ROM=args.insert_rom)
    emulator.print_hex_range(0, 14)


if __name__ == '__main__':

    coloredlogs.install(level="DEBUG",
                        fmt="%(asctime)s %(name)s[%(funcName)s] %(levelname)s %(message)s",
                        logger=log)

    main()
