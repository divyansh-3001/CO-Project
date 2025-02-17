#U TYPE INSTRUCTIONS
U_TYPE_INSTRUCTIONS = {
    "lui":   {"opcode": "0110111"},
    "auipc": {"opcode": "0010111"},
}

# U-type Encoding:
# Immediate[31:12], rd, opcode
U_TYPE_ENCODING_FORMAT = ["imm[31:12]", "rd", "opcode"]

#J TYPE INSTRUCTIONS
J_TYPE_INSTRUCTIONS = {
    "jal": {"opcode": "1101111"},
}

#J-TYPE_ENCODING
# Immediate[20], Immediate[10:1], Immediate[11], Immediate[19:12], rd, opcode
J_TYPE_ENCODING_FORMAT = ["imm[20]", "imm[10:1]", "imm[11]", "imm[19:12]", "rd", "opcode"]
