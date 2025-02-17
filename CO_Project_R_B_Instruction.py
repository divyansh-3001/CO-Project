# R-type Instructions Dictionary (RISC-V)
R_TYPE_INSTRUCTIONS = {
    "add":  {"funct7": "0000000", "funct3": "000", "opcode": "0110011"},
    "sub":  {"funct7": "0100000", "funct3": "000", "opcode": "0110011"},
    "sll":  {"funct7": "0000000", "funct3": "001", "opcode": "0110011"},
    "slt":  {"funct7": "0000000", "funct3": "010", "opcode": "0110011"},
    "sltu": {"funct7": "0000000", "funct3": "011", "opcode": "0110011"},
    "xor":  {"funct7": "0000000", "funct3": "100", "opcode": "0110011"},
    "srl":  {"funct7": "0000000", "funct3": "101", "opcode": "0110011"},
    "sra":  {"funct7": "0100000", "funct3": "101", "opcode": "0110011"},
    "or":   {"funct7": "0000000", "funct3": "110", "opcode": "0110011"},
    "and":  {"funct7": "0000000", "funct3": "111", "opcode": "0110011"},
}

# R-type Encoding Format:
# funct7, rs2, rs1, funct3, rd, opcode
R_TYPE_ENCODING_FORMAT = ["funct7", "rs2", "rs1", "funct3", "rd", "opcode"]
# B-type Instructions Dictionary (RISC-V)
B_TYPE_INSTRUCTIONS = {
    "beq":  {"funct3": "000", "opcode": "1100011"},
    "bne":  {"funct3": "001", "opcode": "1100011"},
    "blt":  {"funct3": "100", "opcode": "1100011"},
    "bge":  {"funct3": "101", "opcode": "1100011"},
    "bltu": {"funct3": "110", "opcode": "1100011"},
    "bgeu": {"funct3": "111", "opcode": "1100011"},
}
# Immediate[12], Immediate[10:5], rs2, rs1, funct3, Immediate[4:1], Immediate[11], opcode
B_TYPE_ENCODING_FORMAT = ["imm[12]", "imm[10:5]", "rs2", "rs1", "funct3", "imm[4:1]", "imm[11]", "opcode"]
