# Mantaining this as dict instead of array just because in manual
# the litteral bites are in the tables so for easy look up.
reg_map_word = {
    0b000: "ax",
    0b001: "cx",
    0b010: "dx",
    0b011: "bx",
    0b100: "sp",
    0b101: "bp",
    0b110: "si",
    0b111: "di",
}
reg_map_byte = {
    0b000: "al",
    0b001: "cl",
    0b010: "dl",
    0b011: "bl",
    0b100: "ah",
    0b101: "ch",
    0b110: "dh",
    0b111: "bh",
}
rm_map = {
    0b000: "bx + si",
    0b001: "bx + di",
    0b010: "bp + si",
    0b011: "bp + di",
    0b100: "si",
    0b101: "di",
    0b110: "bp",
    0b111: "bx",
}

OPCODE_MOV_REG_RM = 0b10001000
OPCODE_IMM_TO_REG = 0b10110000


class Reader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def read_u8(self):
        byte = self.data[self.pos]
        self.pos += 1
        return byte

    def read_u16(self):
        low = self.read_u8()
        high = self.read_u8()
        return low | (high << 8)

    def done(self):
        return self.pos >= len(self.data)


def decode_reg(reg, w):
    return reg_map_word[reg] if w else reg_map_byte[reg]


def decode_rm_operand(mod, rm, w, reader):
    if mod == 0b00:
        if rm == 0b110:
            value = reader.read_u16()
            return f"[{value}]"
        return f"[{rm_map[rm]}]"

    elif mod == 0b01:
        value = reader.read_u8()
        if value == 0:
            return f"[{rm_map[rm]}]"
        else:
            return f"[{rm_map[rm]} + {value}]"

    elif mod == 0b10:
        value = reader.read_u16()
        if value == 0:
            return f"[{rm_map[rm]}]"
        else:
            return f"[{rm_map[rm]} + {value}]"

    elif mod == 0b11:
        return decode_reg(rm, w)


def decode_mov_reg_rm(opcode, reader):
    d = (opcode >> 1) & 0b1
    w = opcode & 0b1

    modrm = reader.read_u8()
    mod = (modrm >> 6) & 0b11
    reg = (modrm >> 3) & 0b111
    rm = modrm & 0b111

    reg_operand = decode_reg(reg, w)
    rm_operand = decode_rm_operand(mod, rm, w, reader)

    dest, src = (reg_operand, rm_operand) if d else (rm_operand, reg_operand)
    return f"mov {dest}, {src}"


def decode_imm_to_reg(opcode, reader):
    w = (opcode >> 3) & 0b1
    reg = opcode & 0b111
    if w == 0b0:
        value = reader.read_u8()
    else:
        value = reader.read_u16()
    return f"mov {decode_reg(reg, w)}, {value}"


def decode_instruction(reader):
    opcode = reader.read_u8()
    if (opcode & 0b11111100) == OPCODE_MOV_REG_RM:
        return decode_mov_reg_rm(opcode, reader)
    elif (opcode & 0b11110000) == OPCODE_IMM_TO_REG:
        return decode_imm_to_reg(opcode, reader)


def main():
    with open("l_39", "rb") as f:
        data = f.read()
    reader = Reader(data)
    print("; This is the result of the cpu")
    print("bits 16")
    while not reader.done():
        asm = decode_instruction(reader)
        print(asm)


if __name__ == "__main__":
    main()
