from enum import Enum, auto

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

OPCODE_MOV_REG_RM = 0b10001000
OPCODE_IMM_TO_REG = 0b10110000


class Ins(Enum):
    """Insrtucion Enum."""

    MOV_REG_MEM_TO_FROM_REG = auto()
    MOV_IMM_TO_REG = auto()


with open("test", "rb") as f:
    print("; This is the python test")
    print("bits 16")
    instructions = f.read()
    ins = None

    for byte in instructions:
        if ins == Ins.MOV_REG_MEM_TO_FROM_REG:
            mod = (byte >> 6) & 0b11
            reg = (byte >> 3) & 0b111
            r_m = byte & 0b111
            if mod == 0b11:
                reg_map = reg_map_word if w else reg_map_byte
                dest, src = (reg, r_m) if d else (r_m, reg)
                print(f"mov {reg_map[dest]}, {reg_map[src]}")
                ins = None
            # elif mod == 0b01:
            #
            # elif mod == 0b10:
            #
            # elif mod == 0b00:
        elif ins == Ins.MOV_IMM_TO_REG:
            if w == 0b0:
                print(f"mov {reg_map_byte[reg]}, {byte}")
                ins = None

        elif (byte & 0b11111100) == OPCODE_MOV_REG_RM:
            ins = Ins.MOV_REG_MEM_TO_FROM_REG
            d = (byte >> 1) & 0b1
            w = byte & 0b1
            continue
        elif (byte & 0b11110000) == OPCODE_IMM_TO_REG:
            ins = Ins.MOV_IMM_TO_REG
            w = (byte >> 3) & 0b1
            reg = byte & 0b111
            continue
