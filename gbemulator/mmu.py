BIOS = [
    0x31, 0xFE, 0xFF, 0xAF, 0x21, 0xFF, 0x9F, 0x32, 0xCB, 0x7C, 0x20, 0xFB, 0x21, 0x26, 0xFF, 0x0E,
    0x11, 0x3E, 0x80, 0x32, 0xE2, 0x0C, 0x3E, 0xF3, 0xE2, 0x32, 0x3E, 0x77, 0x77, 0x3E, 0xFC, 0xE0,
    0x47, 0x11, 0x04, 0x01, 0x21, 0x10, 0x80, 0x1A, 0xCD, 0x95, 0x00, 0xCD, 0x96, 0x00, 0x13, 0x7B,
    0xFE, 0x34, 0x20, 0xF3, 0x11, 0xD8, 0x00, 0x06, 0x08, 0x1A, 0x13, 0x22, 0x23, 0x05, 0x20, 0xF9,
    0x3E, 0x19, 0xEA, 0x10, 0x99, 0x21, 0x2F, 0x99, 0x0E, 0x0C, 0x3D, 0x28, 0x08, 0x32, 0x0D, 0x20,
    0xF9, 0x2E, 0x0F, 0x18, 0xF3, 0x67, 0x3E, 0x64, 0x57, 0xE0, 0x42, 0x3E, 0x91, 0xE0, 0x40, 0x04,
    0x1E, 0x02, 0x0E, 0x0C, 0xF0, 0x44, 0xFE, 0x90, 0x20, 0xFA, 0x0D, 0x20, 0xF7, 0x1D, 0x20, 0xF2,
    0x0E, 0x13, 0x24, 0x7C, 0x1E, 0x83, 0xFE, 0x62, 0x28, 0x06, 0x1E, 0xC1, 0xFE, 0x64, 0x20, 0x06,
    0x7B, 0xE2, 0x0C, 0x3E, 0x87, 0xF2, 0xF0, 0x42, 0x90, 0xE0, 0x42, 0x15, 0x20, 0xD2, 0x05, 0x20,
    0x4F, 0x16, 0x20, 0x18, 0xCB, 0x4F, 0x06, 0x04, 0xC5, 0xCB, 0x11, 0x17, 0xC1, 0xCB, 0x11, 0x17,
    0x05, 0x20, 0xF5, 0x22, 0x23, 0x22, 0x23, 0xC9, 0xCE, 0xED, 0x66, 0x66, 0xCC, 0x0D, 0x00, 0x0B,
    0x03, 0x73, 0x00, 0x83, 0x00, 0x0C, 0x00, 0x0D, 0x00, 0x08, 0x11, 0x1F, 0x88, 0x89, 0x00, 0x0E,
    0xDC, 0xCC, 0x6E, 0xE6, 0xDD, 0xDD, 0xD9, 0x99, 0xBB, 0xBB, 0x67, 0x63, 0x6E, 0x0E, 0xEC, 0xCC,
    0xDD, 0xDC, 0x99, 0x9F, 0xBB, 0xB9, 0x33, 0x3E, 0x3c, 0x42, 0xB9, 0xA5, 0xB9, 0xA5, 0x42, 0x4C,
    0x21, 0x04, 0x01, 0x11, 0xA8, 0x00, 0x1A, 0x13, 0xBE, 0x20, 0xFE, 0x23, 0x7D, 0xFE, 0x34, 0x20,
    0xF5, 0x06, 0x19, 0x78, 0x86, 0x23, 0x05, 0x20, 0xFB, 0x86, 0x20, 0xFE, 0x3E, 0x01, 0xE0, 0x50
]

class MMU:

    READ_CALLBACKS = {
        # ROM bank 0
        0x0000: _rom_bank_0_0,

        0x1000: _rom_bank_0_1,
        0x2000: _rom_bank_0_1,
        0x3000: _rom_bank_0_1,

        # ROM bank 1
        0x3000: _rom_bank_1,
        0x4000: _rom_bank_1,
        0x5000: _rom_bank_1,
        0x6000: _rom_bank_1,

        # VRAM
        0x8000: _vram,
        0x9000: _vram,

        # External RAM
        0xA000: _external_ram,
        0xB000: _external_ram,

        # work RAM and echo
        0xC000: _work_ram_and_echo,
        0xD000: _work_ram_and_echo,
        0xE000: _work_ram_and_echo,

        # default
        0xF000: _default,
    }

    WRITE_CALLBACKS = {
        # ROM bank 0
        0x0000: _write_rom_bank_0_0,
        0x1000: _write_rom_bank_0_0,

        0x2000: _write_rom_bank_0_1,
        0x3000: _write_rom_bank_0_1,

        0x4000: _write_rom_bank_1,
        0x5000: _write_rom_bank_1,
    }

    def __init__(self, rom, z80_registers, gpu_vram, gpu_oam):

        self._rom = rom
        self._z80 = z80_registers
        self._gpu_vram = gpu_vram
        self._gpu_oam = gpu_oam

        self._in_bios = True

        self._ie = 0
        self._if = 0

        self._mbc = [{}, {"rombank": 0, "rambank": 0, "ramon": 0, "mode": 0}]

        self._wram = [0] * 8192
        self._vram = [0] * 32768
        self._zram = [0] * 127

        self.ram_offset = 0x4000
        self.rom_offset = 0

    @property
    def cartridge_type(self):
        return self._rom[0x0147] 

    def read_byte(self, addr):
        return self.READ_CALLBACKS[addr & 0xF000](addr)

    def read_word(self, addr):
        return self.read_byte(addr) + (self.read_byte(addr + 1) << 8)

    def write_byte(self, addr, value):
        self.WRITE_CALLBACKS[addr & 0xF000](addr) = value

    def write_word(self, addr, value):
        self.write_byte(addr, value & 255)
        self.write_byte(addr + 1, value >> 8)

    def reset(self):
        self._wram = [0] * len(self._wram)
        self._vram = [0] * len(self._vram)
        self._zram = [0] * len(self._zram)
        self._in_bios = True

    # -------------------------------------------------------------------------
    # callbacks for read address

    # TODO: refactor

    def _rom_bank_0_0(self, addr):

        if self._in_bios:

            if addr < 0x0100:
                return self._bios[addr]

            if self.z80_registers.pc == 0x0100:
                self._in_bios = False
                return 0

        else:
            return self._rom[addr]

    def _rom_bank_0_1(self, addr):
        return self._rom[addr]

    def _vram(self, addr):
        return self._vram[addr & 0x1FFF]

    def _external_ram(self, addr):
        return self._eram[RAM_OFFSET + (addr & 0x1FFF)]

    def _work_ram_and_echo(self, addr):
        return self._wram[addr & 0x1FFF]

    def _default(self, addr):

        # echo RAM
        if (addr & 0x1FFF) in {
            0x000, 0x100, 0x200, 0x300, 0x400, 0x500, 0x600,
            0x700, 0x800, 0x900, 0xA00, 0xB00, 0xC00, 0xD00
        }:
            return self._wram[addr & 0x1FFF]

        # OAM
        if (addr & 0x1FFF) == 0xE00:
            if (addr & 0xFF) < 0xA0:
                return self.gpu_oam[addr & 0xFF]
            else:
                return 0

        # Zeropage RAM, IO, Interrupts
        if (addr & 0x1FFF) == 0xF00:

            if addr == 0xFFFF:
                return self._ie

            elif addr > 0xFF7F:
                return self._zram[addr & 0x7F]

            else:
                if (addr & 0xF0) == 0x00:
                    if addr & 0xF == 0:
                        return # KEY.rb()

                    elif (addr & 0xF) in {4, 5, 6, 7}:
                        return # TIMER.rb(addr)

                    elif (addr & 0xF) == 15:
                        return self._if

                    else:
                        return 0

                if (addr & 0xF0) in {0x10, 0x20, 0x30}:
                    return 0

                if (addr & 0xF0) in {0x40, 0x50, 0x60, 0x70}:
                    self.gpu_vram[addr]

    # -------------------------------------------------------------------------
    # callbacks for write address

    # TODO: refactor

    def _write_rom_bank_0_0(self, addr, value):
        if self._cartridge_type == 1:
            self._mbc[1]["ramon"] = int((value & 0xF) == 0xA)

    def _write_rom_bank_0_1(self, addr, value):
        if self._cartridge_type == 1:
            MMU._mbc[1]["rombank"] &= 0x60
	    value &= 0x1F

	    if not value:
		 value = 1

            MMU._mbc[1]["rombank"] |= value
            MMU.rom_offset = self._mbc[1]["rombank"] * 0x4000

    def _write_rom_bank_1(self, addr, value):
        if self._cartridge_type == 1:

            if self._mbc[1]["mode"]:
                self._mbc[1]["rambank"] = value & 3
                self.ram_offset = self._mbc[1]["rambank"] * 0x2000;

            else:
                self._mbc[1]["rombank"] &= 0x1F
                self._mbc[1]["rombank"] |= (value & 3) << 5)
                self.rom_offset = self._mbc[1]["rombank"] * 0x4000

