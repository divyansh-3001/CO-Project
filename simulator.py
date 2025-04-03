import re

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
    print("Invalid opcode")
    return None
def decode_instruction(binary_instr):
    
    instr_type = instruction_type(binary_instr)
    opcode = binary_instr[-7:]
    
    if instr_type in {'R', 'I', 'S', 'B'}:
        funct3 = binary_instr[17:20]
    else:
        funct3 = None

    
    if instr_type == 'R':
        funct7 = binary_instr[:7]
    else:
        funct7 = None

    
    if instr_type in {'R', 'I', 'U', 'J'}:
        rd = binary_instr[20:25]
    else:
        rd = None

   
    if instr_type in {'R', 'I', 'S', 'B'}:
        rs1 = binary_instr[12:17]
    else:
        rs1 = None

    
    if instr_type in {'R', 'S', 'B'}:
        rs2 = binary_instr[7:12]
    else:
        rs2 = None

   
    imm = extract_immediate(binary_instr, instr_type)

    
    decoded_instr = match_instruction(instr_type, opcode, funct3, funct7)

  
    if decoded_instr:
        return format_decoded_instruction(decoded_instr, rd, rs1, rs2, imm)
    
    return "Unknown Instruction"


def extract_immediate(binary_instr, instr_type):
    if instr_type == 'I':  
        return sign_extend(binary_instr[:12], 12)
    
    elif instr_type == 'S': 
        return sign_extend(binary_instr[:7] + binary_instr[20:25], 12)
    
    elif instr_type == 'B':  
        return sign_extend(binary_instr[0] + binary_instr[24] + binary_instr[1:7] + binary_instr[20:24] + '0', 13)
    
    elif instr_type == 'J': 
        return sign_extend(binary_instr[0] + binary_instr[12:20] + binary_instr[11] + binary_instr[1:11] + '0', 21)
    return "No immediate"

def sign_extend(value, bits):
    num = int(value, 2)  
    if num & (1 << (bits - 1)): 
        num -= (1 << bits) 
    return num


def match_instruction(instr_type, opcode, funct3, funct7):
    for instr, details in instruction_info.items():
        if (details['opcode'] == opcode and 
            (funct3 is None or details.get('funct3') == funct3) and 
            (funct7 is None or details.get('funct7') == funct7)):
            return instr
    print(f"Invalid combination of {{opcode: {opcode}, funct3: {funct3}, funct7: {funct7}}}")
    return None

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
    
    
input_filename = input("Enter input file name: ")
output_filename = "hello1.txt"
process_file(input_filename, output_filename)

print(f"Decoded instructions written to '{output_filename}' successfully.")
import re

def to_binary(value):
    if value < 0:
        value = (1 << 32) + value  # Convert negative value to 32-bit two's complement
    return "0b" + f"{value:032b}"



# Initialize registers (x0 to x31), with x2 (sp) set to 380
registers = {f"x{i}": 0 for i in range(32)}
registers["x2"] = 380  # Stack pointer

# availaible memory dictionary 
memory = {mem: 0 for mem in range(0x00010000, 0x00010080, 4)}


def get_available_memory():#function to check the next availaible memory for sw operand to store in 
    for addr in memory:
        if memory[addr] == 0:
            return addr
    return None



def assign_addresses(instructions):
    return {i * 4: instructions[i] for i in range(len(instructions))}

def detect_halt(parts):
    return parts[0] == "beq" and parts[1] == "x0" and parts[2] == "x0" and parts[3] == "0"

def calculate_pc(pc, parts):
    new_pc = None
    op = parts[0]
    if op == "beq" and registers[parts[1]] == registers[parts[2]]:
        new_pc = pc + int(parts[3])
    elif op == "bne" and registers[parts[1]] != registers[parts[2]]:
        new_pc = pc + int(parts[3])
    elif op == "jal":
        registers[parts[1]] = pc + 4
        new_pc = pc + int(parts[2])
    elif op == "jalr":
        if parts[1] != "x0":
            registers[parts[1]] = pc + 4
        new_pc = (registers[parts[2]] + int(parts[3])) & ~1
    else:
        new_pc = pc + 4
    
    if new_pc % 4 != 0:
        print(f"Error: PC update to address {new_pc}, which is not a multiple of four")
        return None
    return new_pc

def execute_instruction(instruction, pc):
    parts = re.split(r'[ ,\s]+', instruction)
    if detect_halt(parts):
        return None
    new_pc = calculate_pc(pc, parts)
    if new_pc is None:
        return None
    
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
        if address < 0x00010000 or address > 0x0001007C:
            print(f"Error: Invalid address to read memory from:{hex(address)}")
            return None
        registers[parts[1]] = memory.get(address, 0)
    elif op == "sw":
        address = registers[parts[2]] + int(parts[3])
        if address < 0x00010000 or address > 0x0001007C:
            print(f"Invalid address to read memory from: {hex(address)}")
            return None
        memory[address] = registers[parts[1]]
    
    registers["x0"] = 0  # x0 is always 0
    return new_pc


def execute_program(input_file, output_file):
    instructions = read_file(input_file)
    address_map = assign_addresses(instructions)

    pc = 0
    output_lines = []

    while pc in address_map:
        binary_values = [to_binary(pc)]
        for i in range(32):  
            binary_values.append(to_binary(registers[f"x{i}"]))
            
        formatted_values = []
        for i in range(0, len(binary_values), 5):
            formatted_values.append(' '.join(binary_values[i:i+5]))

        output_lines.append('\n'.join(formatted_values))

        
        instruction = address_map[pc]
        new_pc = execute_instruction(instruction, pc)

       
        if new_pc is None:
            output_lines.append('\n'.join(formatted_values))
            break

       
        pc = new_pc

    
    for addr in sorted(memory.keys()):
        output_lines.append(f"0x{addr:08X}:{to_binary(memory[addr])}")

   
    write_file(output_file, output_lines)


input_filename = "hello1.txt"
output_filename = input("Enter output file name: ")
execute_program(input_filename, output_filename)
print(f"Binary register values and memory contents written to '{output_filename}' successfully.")
