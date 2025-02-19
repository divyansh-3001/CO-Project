import re
register_names = {"zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"}

# Dictionary of instruction types
instruction_dict = {
    "R": ["ADD", "SUB", "AND", "OR", "XOR", "SLL", "SRL", "SRA", "MUL", "DIV", "REM"],
    "I": ["ADDI", "ANDI", "ORI", "XORI", "SLLI", "SRLI", "SRAI", "LW", "LH", "LB", "JALR"],
    "S": ["SW", "SH", "SB"],
    "B": ["BEQ", "BNE", "BLT", "BGE"],
    "U": ["LUI", "AUIPC"],
    "J": ["JAL"]}
# funct3 Dictionary
register_map = {
("x0", "zero"):  "00000",
("x1", "ra"):    "00001",
("x2", "sp"):    "00010",
("x3", "gp"):    "00011",
("x4", "tp"):    "00100",
("x5", "t0"):    "00101",
("x6", "t1"):    "00110",
("x7", "t2"):    "00111",
("x8", "s0"):    "01000",
("x9", "s1"):    "01001",
("x10", "a0"):   "01010",
("x11", "a1"):   "01011",
("x12", "a2"):   "01100",
("x13", "a3"):   "01101",
("x14", "a4"):   "01110",
("x15", "a5"):   "01111",
("x16", "a6"):   "10000",
("x17", "a7"):   "10001",
("x18", "s2"):   "10010",
("x19", "s3"):   "10011",
("x20", "s4"):   "10100",
("x21", "s5"):   "10101",
("x22", "s6"):   "10110",
("x23", "s7"):   "10111",
("x24", "s8"):   "11000",
("x25", "s9"):   "11001",
("x26", "s10"):  "11010",
("x27", "s11"):  "11011",
("x28", "t3"):   "11100",
("x29", "t4"):   "11101",
("x30", "t5"):   "11110",
("x31", "t6"):   "11111",
}



instruction_info = {
    # R-type Instructions
    "ADD":  {"opcode": "0110011", "funct3": "000", "funct7": "0000000"},
    "SUB":  {"opcode": "0110011", "funct3": "000", "funct7": "0100000"},
    "AND":  {"opcode": "0110011", "funct3": "111", "funct7": "0000000"},
    "OR":   {"opcode": "0110011", "funct3": "110", "funct7": "0000000"},
    "XOR":  {"opcode": "0110011", "funct3": "100", "funct7": "0000000"},
    "SLL":  {"opcode": "0110011", "funct3": "001", "funct7": "0000000"},
    "SRL":  {"opcode": "0110011", "funct3": "101", "funct7": "0000000"},
    "SRA":  {"opcode": "0110011", "funct3": "101", "funct7": "0100000"},
    "MUL":  {"opcode": "0110011", "funct3": "000", "funct7": "0000001"},
    "DIV":  {"opcode": "0110011", "funct3": "100", "funct7": "0000001"},
    "REM":  {"opcode": "0110011", "funct3": "110", "funct7": "0000001"},
    
    # I-type Instructions
    "ADDI":  {"opcode": "0010011", "funct3": "000", "funct7": None},
    "ANDI":  {"opcode": "0010011", "funct3": "111", "funct7": None},
    "ORI":   {"opcode": "0010011", "funct3": "110", "funct7": None},
    "XORI":  {"opcode": "0010011", "funct3": "100", "funct7": None},
    "SLLI":  {"opcode": "0010011", "funct3": "001", "funct7": "0000000"},
    "SRLI":  {"opcode": "0010011", "funct3": "101", "funct7": "0000000"},
    "SRAI":  {"opcode": "0010011", "funct3": "101", "funct7": "0100000"},
    "LW":    {"opcode": "0000011", "funct3": "010", "funct7": None},
    "LH":    {"opcode": "0000011", "funct3": "001", "funct7": None},
    "LB":    {"opcode": "0000011", "funct3": "000", "funct7": None},
    "JALR":  {"opcode": "1100111", "funct3": "000", "funct7": None},
    
    # S-type Instructions
    "SW":    {"opcode": "0100011", "funct3": "010", "funct7": None},
    "SH":    {"opcode": "0100011", "funct3": "001", "funct7": None},
    "SB":    {"opcode": "0100011", "funct3": "000", "funct7": None},
    
    # B-type Instructions
    "BEQ":   {"opcode": "1100011", "funct3": "000", "funct7": None},
    "BNE":   {"opcode": "1100011", "funct3": "001", "funct7": None},
    "BLT":   {"opcode": "1100011", "funct3": "100", "funct7": None},
    "BGE":   {"opcode": "1100011", "funct3": "101", "funct7": None},
    
    # U-type Instructions
    "LUI":   {"opcode": "0110111", "funct3": None, "funct7": None},
    "AUIPC": {"opcode": "0010111", "funct3": None, "funct7": None},
    
    # J-type Instructions
    "JAL":   {"opcode": "1101111", "funct3": None, "funct7": None},
}

def tokenize_instruction(line):
 
    line = line.split("#")[0].strip()
    if not line:  # Ignore empty lines
        return None

    # This is to handle offset values like 100(x7) 
    line = re.sub(r'(\d+)\((x\d+|a\d+|s\d+|t\d+|zero|sp|gp|tp|ra)\)', r'\1 \2', line)

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
    for inst_type, inst_list in instruction_dict.items():
        for instr in tokens:
            if instr.upper() in inst_list:
                return inst_type


def find_registers_binary(tokens):
    """
    Searches for register names in the token list and returns a list of their 5-bit binary values.
    
    Example:
    tokens = ["ADDI", "x1", "x2", "10"] → ['00001', '00010']
    tokens = ["LW", "a0", "100", "s1"] → ['01010', '10001']
    """

    binary_values = []
    
    for token in tokens:
        token = token.lower()  # Normalize case
        
        # Check if token matches any key in register_map
        for (x_name, abi_name), binary in register_map.items():
            if token == x_name or token == abi_name:
                binary_values.append(binary)
                break  # Stop checking once a match is found
    
    return binary_values

def format_instruction(instruction_type, opcode, funct3, funct7, rd_bin, rs1_bin, rs2_bin, immediate):
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
    

    if instruction_type == "R":
        return f"{funct7}{rs2_bin}{rs1_bin}{funct3}{rd_bin}{opcode}"
    
    elif instruction_type == "I":
        imm_bin = to_signed_binary(immediate, 12)
        return f"{imm_bin}{rs1_bin}{funct3}{rd_bin}{opcode}"
    
    elif instruction_type == "S":
        imm_bin = to_signed_binary(immediate, 12)
        return f"{imm_bin[:7]}{rs1_bin}{rs2_bin}{funct3}{imm_bin[7:]}{opcode}"
    
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

def to_signed_binary(value, bits):
    """Converts an integer to a signed two’s complement binary representation."""
    if value < 0:
        value = (1 << bits) + value  # Two's complement conversion for negative numbers
    return format(value, f'0{bits}b')  # Ensures correct bit width

def get_nearest_label_offset(lines, target_index):
    register_names = {"zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"}
    
    tokenized_lines = [re.split(r'[\s,]+', line) for line in lines]
    label_positions = {}
    
    for i, tokens in enumerate(tokenized_lines):
        if tokens[0].endswith(":"):
            label = tokens[0][:-1]
            if label not in label_positions:
                label_positions[label] = []
            label_positions[label].append(i)
    
    if target_index < len(tokenized_lines):
        tokens = tokenized_lines[target_index]
        if tokens and tokens[-1] not in register_names and not tokens[-1].isdigit():
            label = tokens[-1]
            possible_positions = label_positions.get(label, [])
            
            print("Target Label:", label)
            print("Possible Positions:", possible_positions)
            
            if possible_positions:
                nearest_position = min(possible_positions, key=lambda x: abs(x - target_index))  # Pick the closest label
                print("Nearest Position:", nearest_position)
                return (nearest_position - target_index) * 4
    
    return None  # Return None if no valid label is found

def find_immediate(tokens, instr_type):
    """
    Extracts the immediate value if the instruction is not R-type.
    Looks for any integer value in the tokens.
    """

    target_index = next((i for i, line in enumerate(lines) if re.split(r'[ ,]+', line) == tokens), -1)
    



    if tokens and tokens[-1] not in register_names and not tokens[-1].lstrip('-').isdigit():
        return get_nearest_label_offset(lines, target_index)
    else:
        
        if instr_type == "R":
            return None  # R-type instructions do not have an immediate value

        for token in tokens:
            if token.lstrip('-').isdigit():  # Check if token is a number (allowing negative values)
                return int(token)  # Convert to integer
        return None  # No immediate found
def find_instruction_info(tokens):
    """
    Searches for an instruction in the token list and returns its opcode, funct3, and funct7.
    Example: ["ADDI", "x1", "x2", "10"] → {'opcode': '0010011', 'funct3': '000', 'funct7': None}
    """
    if not tokens:
        return None

    for token in tokens:
        token_upper = token.upper()  # Normalize case
        if token_upper in instruction_info:
            return instruction_info[token_upper]
    
    return None  # Return None if no instruction matches
import re
def process_file(input_filename, output_filename):
    errors = []  # Store errors
    binary_output = []
    
    with open(input_filename, 'r') as file:
        lines = file.readlines()
    
    for line_number, line in enumerate(lines, start=1):
        try:
            tokens = tokenize_instruction(line)
            if tokens:
                instr_type = get_instruction_type(tokens)
                dic = find_instruction_info(tokens)
                
                if dic is None:
                    errors.append(f"[Error at line {line_number}] Instruction not found: {tokens}")
                    continue
                
                opcode, funct3, funct7 = dic["opcode"], dic["funct3"], dic["funct7"]
                immediate = find_immediate(tokens, instr_type)
                r_list = find_registers_binary(tokens)
                
                if instr_type == "R":
                    binary_instr = format_instruction(instr_type, opcode, funct3, funct7, r_list[0], r_list[1], r_list[2], None)
                elif instr_type == "I":
                    binary_instr = format_instruction(instr_type, opcode, funct3, None, r_list[0], r_list[1], None, immediate)
                elif instr_type == "S":
                    binary_instr = format_instruction(instr_type, opcode, funct3, None, None, r_list[0], r_list[1], immediate)
                elif instr_type == "B":
                    binary_instr = format_instruction(instr_type, opcode, funct3, None, None, r_list[0], r_list[1], immediate)
                elif instr_type == "U":
                    binary_instr = format_instruction(instr_type, opcode, None, None, r_list[0], None, None, immediate)
                elif instr_type == "J":
                    binary_instr = format_instruction(instr_type, opcode, None, None, r_list[0], None, None, immediate)
                
                binary_output.append(binary_instr)
            else:
                continue
        except Exception as e:
            errors.append(f"[Error at line {line_number}] {str(e)}")
            break  # Stop processing further lines if an error occurs
    
    # Write to output file
    with open(output_filename, 'w') as output_file:
        if errors:
            for error in errors:
                output_file.write(error + '\n')
                print(error)
        else:
            for binary in binary_output:
                output_file.write(binary + '\n')
                print(binary)



def read_file(filepath):
    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    return lines
           


filename = input("Enter file name: ")
lines=read_file(filename)
# Example usage
output_filename = "output.txt"  # Define the output file
process_file(filename, output_filename)

