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

OPCODE_MOV_REG_RM = 0b100010


with open("l_39", "rb") as f:
    print("; This is the python test")
    print("bits 16")
    instructions = f.read()

    for byte in instructions:
        opcode = (byte >> 2) & 0b111111
