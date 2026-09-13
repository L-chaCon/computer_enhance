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

r_m_map = {
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


class Ins(Enum):
    """Insrtucion Enum."""

    MOV_REG_MEM_TO_FROM_REG = auto()
    MOV_IMM_TO_REG = auto()


with open("test", "rb") as f:
    print("; This is the python test")
    print("bits 16")
    instructions = f.read()
    ins = None
    w: bytes = 0b0
    d: bytes = 0b0
    data = []

    for byte in instructions:
        if ins == Ins.MOV_REG_MEM_TO_FROM_REG:
            data.append(byte)
            mod = (data[0] >> 6) & 0b11
            reg = (data[0] >> 3) & 0b111
            r_m = data[0] & 0b111
            if mod == 0b11:
                reg_map = reg_map_word if w else reg_map_byte
                dest, src = (reg, r_m) if d else (r_m, reg)
                print(f"mov {reg_map[dest]}, {reg_map[src]}")
                ins = None
                data = []
                continue

            elif mod == 0b00:
                if r_m == 0b110:
                    # direct address case
                    ins = None
                    continue
                reg_map = reg_map_word if w else reg_map_byte
                if d == 0b1:
                    print(f"mov {reg_map[reg]}, [{r_m_map[r_m]}]")
                else:
                    print(f"mov [{r_m_map[r_m]}], {reg_map[reg]}")
                ins = None
                data = []
                continue

            elif mod == 0b01:
                if len(data) == 2:
                    reg_map = reg_map_word if w else reg_map_byte
                    if data[1] != 0:
                        if d == 0b1:
                            print(f"mov {reg_map[reg]}, [{r_m_map[r_m]} + {data[1]}]")
                        else:
                            print(f"mov [{r_m_map[r_m]} + {data[1]}], {reg_map[reg]}")
                    else:
                        if d == 0b1:
                            print(f"mov {reg_map[reg]}, [{r_m_map[r_m]}]")
                        else:
                            print(f"mov [{r_m_map[r_m]}], {reg_map[reg]}")
                    ins = None
                    data = []
                    continue

            elif mod == 0b10:
                if len(data) == 3:
                    reg_map = reg_map_word if w else reg_map_byte
                    value = data[1] | data[2] << 8
                    if value != 0:
                        if d == 0b1:
                            print(f"mov {reg_map[reg]}, [{r_m_map[r_m]} + {value}]")
                        else:
                            print(f"mov [{r_m_map[r_m]} + {value}], {reg_map[reg]}")
                    else:
                        if d == 0b1:
                            print(f"mov {reg_map[reg]}, [{r_m_map[r_m]}]")
                        else:
                            print(f"mov [{r_m_map[r_m]}], {reg_map[reg]}")
                    ins = None
                    data = []
                    continue

        elif ins == Ins.MOV_IMM_TO_REG:
            if w == 0b0:
                print(f"mov {reg_map_byte[reg]}, {byte}")
                ins = None
                continue
            if w == 0b1:
                data.append(byte)
                if len(data) == 2:
                    value = data[0] | data[1] << 8
                    print(f"mov {reg_map_word[reg]}, {value}")
                    data = []
                    ins = None
                    continue
                continue

        # If there is no instruction found. Check for instruction.
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
