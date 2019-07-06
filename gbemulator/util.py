def as_binary(value):
    return f"{value:b}".zfill(8)


def as_hex(value):
    return f"{value:X}"


class Bits:
    @staticmethod
    def msb(word):
        # shift right to move the most significant byte to the first 8 bits
        return word >> 8

    @staticmethod
    def lsb(word):
        # truncate all but the first 8 bits
        return word & 0xFF

    @staticmethod
    def is_word(value):
        return 0 <= value <= 0xFFFF

    @staticmethod
    def is_byte(value):
        return 0 <= value <= 0xFF

    @staticmethod
    def check_is_word(value):
        if not Bits.is_word(value):
            raise ValueError(f"{value} is not a word")

    @staticmethod
    def check_is_byte(value):
        if not Bits.is_byte(value):
            raise ValueError(f"{value} is not a byte")
