import re

def read_file(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def write_file(filepath, lines):
    with open(filepath, 'w') as file:
        for line in lines:
            file.write(line + '\n')  

def instruction_type(binary_instr):
    opcode = binary_instr[-7:]
    for instr_type, opcodes in opcode_dict.items():
        if opcode in opcodes:
            return instr_type
    return None

def decode_instruction(binary_instr):
    instr_type = instruction_type(binary_instr)
    opcode = binary_instr[-7:]
    funct3 = binary_instr[17:20] if instr_type in {'R', 'I', 'S', 'B'} else None
    funct7 = binary_instr[:7] if instr_type == 'R' else None
    rd = binary_instr[20:25] if instr_type in {'R', 'I', 'U', 'J'} else None
    rs1 = binary_instr[12:17] if instr_type in {'R', 'I', 'S', 'B'} else None
    rs2 = binary_instr[7:12] if instr_type in {'R', 'S', 'B'} else None
    imm = extract_immediate(binary_instr, instr_type)

    decoded_instr = match_instruction(instr_type, opcode, funct3, funct7)
    
    if decoded_instr:
        return format_decoded_instruction(decoded_instr, rd, rs1, rs2, imm)
    
    return "Unknown Instruction"

def extract_immediate(binary_instr, instr_type):
    if instr_type == 'I':  # Immediate for I-type
        return sign_extend(binary_instr[:12], 12)
    elif instr_type == 'S':  # Immediate for SW (S-type)
        return sign_extend(binary_instr[:7] + binary_instr[20:25], 12)
    elif instr_type == 'B':  # Immediate for BEQ/BNE (B-type)
        return sign_extend(binary_instr[0] + binary_instr[24] + binary_instr[1:7] + binary_instr[20:24] + '0', 13)
    elif instr_type == 'J':  # Immediate for JAL (J-type)
        return sign_extend(binary_instr[0] + binary_instr[12:20] + binary_instr[11] + binary_instr[1:11] + '0', 21)
    return "No immediate"

def sign_extend(value, bits):
    return int(value, 2) - (1 << bits) if value[0] == '1' else int(value, 2)

def match_instruction(instr_type, opcode, funct3, funct7):
    for instr, details in instruction_info.items():
        if (details['opcode'] == opcode and 
            (funct3 is None or details.get('funct3') == funct3) and 
            (funct7 is None or details.get('funct7') == funct7)):
            return instr
    return "no_match_instruction"

def format_decoded_instruction(instr, rd, rs1, rs2, imm):
    if instr in {'ADD', 'SUB', 'AND', 'OR', 'SLT', 'SRL'}:
        return f"{instr.lower()} {registers[rd]}, {registers[rs1]}, {registers[rs2]}"
    elif instr in {'LW'}:
        return f"{instr.lower()} {registers[rd]}, {registers[rs1]}, {imm}"  # Imm last
    elif instr in {'SW'}:
        return f"{instr.lower()} {registers[rs2]}, {registers[rs1]}, {imm}"  # Imm last
    elif instr in {'ADDI'}:
        return f"{instr.lower()} {registers[rd]}, {registers[rs1]}, {imm}"  # Imm last
    elif instr in {'JALR'}:
        return f"{instr.lower()} {registers[rd]}, {registers[rs1]}, {imm}"  # Imm last
    elif instr in {'BEQ', 'BNE'}:
        return f"{instr.lower()} {registers[rs1]}, {registers[rs2]}, {imm}"  # Imm last
    elif instr == 'JAL':
        return f"{instr.lower()} {registers[rd]}, {imm}"  # Imm last
    return "Unknown Instruction"

def process_file(input_file, output_file):
    binary_instructions = read_file(input_file)
    decoded_instructions = [decode_instruction(instr) for instr in binary_instructions]
    write_file(output_file, decoded_instructions)

registers = {format(i, '05b'): f"x{i}" for i in range(32)}
opcode_dict = {
    'R': ['0110011'], 'I': ['0010011', '0000011', '1100111'], 
    'S': ['0100011'], 'B': ['1100011'], 'U': ['0110111'], 'J': ['1101111']
}
instruction_info = {
    "ADD": {"opcode": "0110011", "funct3": "000", "funct7": "0000000"},
    "SUB": {"opcode": "0110011", "funct3": "000", "funct7": "0100000"},
    "AND": {"opcode": "0110011", "funct3": "111", "funct7": "0000000"},
    "OR": {"opcode": "0110011", "funct3": "110", "funct7": "0000000"},
    "SLT": {"opcode": "0110011", "funct3": "010", "funct7": "0000000"},
    "SRL": {"opcode": "0110011", "funct3": "101", "funct7": "0000000"},
    "LW": {"opcode": "0000011", "funct3": "010"},
    "SW": {"opcode": "0100011", "funct3": "010"},
    "ADDI": {"opcode": "0010011", "funct3": "000"},
    "JALR": {"opcode": "1100111", "funct3": "000"},
    "BEQ": {"opcode": "1100011", "funct3": "000"},
    "BNE": {"opcode": "1100011", "funct3": "001"},
    "JAL": {"opcode": "1101111"}
}

# Run the program
input_filename = input("Enter input file name: ")
output_filename = "hello1.txt"
process_file(input_filename, output_filename)

print(f"Decoded instructions written to '{output_filename}' successfully.")


#part 2
import re

# Initialize registers (x0 to x31), with x2 (sp) set to 380
registers = {f"x{i}": 0 for i in range(32)}
registers["x2"] = 380  # Stack pointer

# Initialize memory from 0x00010000 to 0x0001007C (word-aligned addresses) with 0
memory = {
    0x00010000: 0,
    0x00010004: 0,
    0x00010008: 0,
    0x0001000C: 0,
    0x00010010: 0,
    0x00010014: 0,
    0x00010018: 0,
    0x0001001C: 0,
    0x00010020: 0,
    0x00010024: 0,
    0x00010028: 0,
    0x0001002C: 0,
    0x00010030: 0,
    0x00010034: 0,
    0x00010038: 0,
    0x0001003C: 0,
    0x00010040: 0,
    0x00010044: 0,
    0x00010048: 0,
    0x0001004C: 0,
    0x00010050: 0,
    0x00010054: 0,
    0x00010058: 0,
    0x0001005C: 0,
    0x00010060: 0,
    0x00010064: 0,
    0x00010068: 0,
    0x0001006C: 0,
    0x00010070: 0,
    0x00010074: 0,
    0x00010078: 0,
    0x0001007C: 0
}


# Function to find the first available memory location
def get_available_memory():
    for addr in memory:
        if memory[addr] == 0:  # Unused memory location
            return addr
    return None  # No available memory

def read_file(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]



def assign_addresses(instructions):
    return {i * 4: instructions[i] for i in range(len(instructions))}

def detect_halt(parts):
    return parts[0] == "beq" and parts[1] == "x0" and parts[2] == "x0" and parts[3] == "0"

def calculate_pc(pc, parts):
    op = parts[0]
    if op == "beq" and registers[parts[1]] == registers[parts[2]]:
        return pc + int(parts[3])
    elif op == "bne" and registers[parts[1]] != registers[parts[2]]:
        return pc + int(parts[3])
    elif op == "jal":
        registers[parts[1]] = pc + 4
        return pc + int(parts[2])
    elif op == "jalr":
        if parts[1] != "x0":
            registers[parts[1]] = pc + 4
        return (registers[parts[2]] + int(parts[3])) & ~1
    return pc + 4  # Default: move to next instruction

def to_binary_32bit(value):
    """Convert an integer to a signed 32-bit two's complement binary representation."""
    return "0b" + format(value & 0xFFFFFFFF, '032b')

def execute_instruction(instruction, pc):
    parts = re.split(r'[ ,\s]+', instruction)
    if detect_halt(parts):
        return None  # Stop execution

    new_pc = calculate_pc(pc, parts)
    op = parts[0]

    if op == "add":
        registers[parts[1]] = registers[parts[2]] + registers[parts[3]]
    elif op == "sub":
        registers[parts[1]] = registers[parts[2]] - registers[parts[3]]
    elif op == "slt":
        registers[parts[1]] = int(registers[parts[2]] < registers[parts[3]])
    elif op == "srl":
        registers[parts[1]] = registers[parts[2]] >> (registers[parts[3]] & 0x1F)
    elif op == "or":
        registers[parts[1]] = registers[parts[2]] | registers[parts[3]]
    elif op == "and":
        registers[parts[1]] = registers[parts[2]] & registers[parts[3]]
    elif op == "addi":
        registers[parts[1]] = registers[parts[2]] + int(parts[3])
    elif op == "lw":
        address = registers[parts[2]] + int(parts[3])
        if address not in memory:  
            available_addr = get_available_memory()
            if available_addr is not None:
                memory[address] = memory[available_addr]
                memory[available_addr] = 0 
        registers[parts[1]] = memory.get(address, 0)  
    elif op == "sw":
        address = registers[parts[2]] + int(parts[3])
        if address not in memory:  
            available_addr = get_available_memory()
            if available_addr is not None:
                memory[address] = memory[available_addr]  
                memory[available_addr] = 0  
        memory[address] = registers[parts[1]]  

    registers["x0"] = 0  
    return new_pc

def execute_program(input_file, output_file):
    instructions = read_file(input_file)
    address_map = assign_addresses(instructions)
    pc = 0
    output_lines = []
    first_execution = True  # Track if it's the first instruction execution

    while pc in address_map:
        if not first_execution:  # Skip first execution (pc = 0)
            # Convert PC and registers to 32-bit two's complement binary format
            binary_values = f"{to_binary_32bit(pc)} " + " ".join(to_binary_32bit(registers[f"x{i}"]) for i in range(32)) + " "
            output_lines.append(binary_values)

        first_execution = False  # Mark first execution as done
        
        # Execute instruction and calculate next PC
        instruction = address_map[pc]
        new_pc = execute_instruction(instruction, pc)

        if new_pc is None:  # If halt detected, repeat last line and stop
            output_lines.append(binary_values)
            break

        pc = new_pc  # Move to next instruction

    # Write memory contents to output
# Write only memory contents within the allowed range
    for addr in sorted(memory.keys()):
        if 0x00010000 <= addr <= 0x0001007C:  # Only include addresses within this range
            output_lines.append(f"0x{addr:08X}:{to_binary_32bit(memory[addr])} ")


    # Write all the output to the file
    write_file(output_file, output_lines)

# Run program
input_filename = "hello1.txt"
output_filename = input("Enter output file name: ")
execute_program(input_filename, output_filename)
print(f"Register values and memory contents written to '{output_filename}' successfully.")
