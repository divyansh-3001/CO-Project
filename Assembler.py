import re

# Dictionary of instruction types
instruction_dict = {
    "R": ["ADD", "SUB", "AND", "OR", "XOR", "SLL", "SRL", "SRA", "MUL", "DIV", "REM"],
    "I": ["ADDI", "ANDI", "ORI", "XORI", "SLLI", "SRLI", "SRAI", "LW", "LH", "LB", "JALR"],
    "S": ["SW", "SH", "SB"],
    "B": ["BEQ", "BNE", "BLT", "BGE"],
    "U": ["LUI", "AUIPC"],
    "J": ["JAL"]
}

def tokenize_instruction(line):
    """
    Tokenizes a RISC-V instruction by handling spaces, commas, and memory offsets (e.g., 100(x7) → ["100", "x7"]).
    Example: "ADDI x1, x2, 10" → ["ADDI", "x1", "x2", "10"]
             "LW x6, 100(x7)" → ["LW", "x6", "100", "x7"]
    """
    # Remove comments and extra spaces
    line = line.split("#")[0].strip()
    if not line:  # Ignore empty lines
        return None

    # Properly handle memory offsets like "100(x7)" → "100 x7"
    line = re.sub(r'(\d+)\((x\d+)\)', r'\1 \2', line)

    # Split by space or comma
    tokens = re.split(r'[,\s]+', line)
    return tokens

def get_instruction_type(tokens):
    """
    Determines the instruction type based on the instruction dictionary.
    Example: ["ADDI", "x1", "x2", "10"] → "I"
    """
    if not tokens:
        return None

    instr = tokens[0].upper()  # First token is always the instruction
    for inst_type, inst_list in instruction_dict.items():
        if instr in inst_list:
            return inst_type
    return "Unknown"

def find_immediate(tokens, instr_type):
    """
    Extracts the immediate value if the instruction is not R-type.
    Looks for any integer value in the tokens.
    """
    if instr_type == "R":
        return None  # R-type instructions do not have an immediate value

    for token in tokens:
        if token.lstrip('-').isdigit():  # Check if token is a number (allowing negative values)
            return int(token)  # Convert to integer
    return None  # No immediate found

def process_file(filename):
    """
    Reads a file line by line, processes instructions, classifies them, and extracts immediates.
    """
    with open(filename, 'r') as file:
        for line in file:
            tokens = tokenize_instruction(line)
            if tokens:  # Ignore blank lines
                instr_type = get_instruction_type(tokens)
                immediate = find_immediate(tokens, instr_type)
                
                print(f"Instruction: {line.strip()}")
                print(f"Tokens: {tokens}")
                print(f"Instruction Type: {instr_type}")
                if immediate is not None:
                    print(f"Immediate Value: {immediate}")
                print("-" * 40)

# Read instructions from 'instructions.txt'
filename = input("Enter file name: ")
process_file(filename)

def to_signed_binary(value, bits):
    """Converts an integer to a signed two’s complement binary representation."""
    if value < 0:
        value = (1 << bits) + value  # Two's complement conversion for negative numbers
    return format(value, f'0{bits}b')  # Ensures correct bit width


def format_instruction(instruction_type, opcode, funct3, funct7, rd=None, rs1=None, rs2=None, immediate=None):
    """
    Formats an instruction into its correct binary representation.
    
    Parameters:
    - instruction_type (str): Instruction type (R, I, S, B, U, J).
    - opcode (str): 7-bit opcode.
    - funct3 (str): 3-bit function code (used for differentiation in I, S, B, R types).
    - funct7 (str): 7-bit function code (used for R-type).
    - rd (int): Destination register.
    - rs1 (int): Source register 1.
    - rs2 (int): Source register 2.
    - immediate (int): Immediate value (if applicable).
    
    Returns:
    - str: Full 32-bit binary instruction.
    """
    
    # Convert registers to 5-bit binary
    rd_bin = format(rd, '05b') if rd is not None else "00000"
    rs1_bin = format(rs1, '05b') if rs1 is not None else "00000"
    rs2_bin = format(rs2, '05b') if rs2 is not None else "00000"
    
    if instruction_type == "R":
        return f"{funct7}{rs2_bin}{rs1_bin}{funct3}{rd_bin}{opcode}"
    
    elif instruction_type == "I":
        imm_bin = to_signed_binary(immediate, 12)
        return f"{imm_bin}{rs1_bin}{funct3}{rd_bin}{opcode}"
    
    elif instruction_type == "S":
        imm_bin = to_signed_binary(immediate, 12)
        return f"{imm_bin[:7]}{rs2_bin}{rs1_bin}{funct3}{imm_bin[7:]}{opcode}"
    
    elif instruction_type == "B":
        imm_bin = to_signed_binary(immediate, 13)
        return f"{imm_bin[0]}{imm_bin[2:8]}{rs2_bin}{rs1_bin}{funct3}{imm_bin[8:12]}{imm_bin[1]}{opcode}"
    
    elif instruction_type == "U":
        imm_bin = to_signed_binary(immediate, 20)
        return f"{imm_bin}{rd_bin}{opcode}"
    
    elif instruction_type == "J":
        imm_bin = to_signed_binary(immediate, 21)
        return f"{imm_bin[0]}{imm_bin[10:20]}{imm_bin[9]}{imm_bin[1:9]}{rd_bin}{opcode}"
    
    else:
        return "Invalid Instruction Type"


# ✅ **Example Usage**
test_instructions = [
    ("R", "0110011", "000", "0000000", 1, 2, 3, None),  # ADD x1, x2, x3
    ("I", "0010011", "000", None, 1, 2, None, 100),  # ADDI x1, x2, 100
    ("S", "0100011", "010", None, None, 2, 3, 100),  # SW x3, 100(x2)
    ("B", "1100011", "000", None, None, 2, 3, 100),  # BEQ x2, x3, 100
    ("U", "0110111", None, None, 1, None, None, 100000),  # LUI x1, 100000
    ("J", "1101111", None, None, 1, None, None, 1000)  # JAL x1, 1000
]

for instr in test_instructions:
    print(f"{instr[0]}-Type Instruction: {format_instruction(*instr)}")
