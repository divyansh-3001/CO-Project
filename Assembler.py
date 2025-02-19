import re

#first we define all the important dictionaries etc containing data
register_names_set = {"zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"}
instruction_types_list_dict = {
    "R": ["ADD", "SUB", "AND", "OR", "XOR", "SLL", "SRL", "SRA", "MUL", "DIV", "REM"],
    "I": ["ADDI", "ANDI", "ORI", "XORI", "SLLI", "SRLI", "SRAI", "LW", "LH", "LB", "JALR"],
    "S": ["SW", "SH", "SB"],
    "B": ["BEQ", "BNE", "BLT", "BGE"],
    "U": ["LUI", "AUIPC"],
    "J": ["JAL"]}
register_to_binary_dict = {
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



instruction_info_main_dict = {
    # for R-type
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
    
    # for I-type
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
    
    # for S-type
    "SW":    {"opcode": "0100011", "funct3": "010", "funct7": None},
    "SH":    {"opcode": "0100011", "funct3": "001", "funct7": None},
    "SB":    {"opcode": "0100011", "funct3": "000", "funct7": None},
    
    # for B-type
    "BEQ":   {"opcode": "1100011", "funct3": "000", "funct7": None},
    "BNE":   {"opcode": "1100011", "funct3": "001", "funct7": None},
    "BLT":   {"opcode": "1100011", "funct3": "100", "funct7": None},
    "BGE":   {"opcode": "1100011", "funct3": "101", "funct7": None},
    
    # for -type 
    "LUI":   {"opcode": "0110111", "funct3": None, "funct7": None},
    "AUIPC": {"opcode": "0010111", "funct3": None, "funct7": None},
    
    # for J-type 
    "JAL":   {"opcode": "1101111", "funct3": None, "funct7": None},
}

def create_tokens_from_line(line):
 
    line = line.split("#")[0].strip()

    if not line:  
        return None #Empty lines
    
    line = re.sub(r'(\d+)\((x\d+|a\d+|s\d+|t\d+|zero|sp|gp|tp|ra)\)', r'\1 \2', line) #for offsets like 100(x1) etc

    
    tokens = re.split(r'[,\s]+', line)
    
    return tokens #This is a list of important terms extracted from a line

def instruction_type_func(tokens): #For determining type of instruction like I R etc
    if not tokens:
        return None
    for type, list in instruction_types_list_dict.items():
        for i in tokens:
            if i.upper() in list:
                return type


def convert_register_to_binary(tokens): #Registers in a token are first searched for then converted to binary


    binary_list = []
    
    for token in tokens:
        token = token.lower()  
        

        for (x, abi), binary in register_to_binary_dict.items():
            if token == x or token == abi: #search
                binary_list.append(binary) #converted to binary
                break  
    
    return binary_list

def format_instruction(type, opcode, funct3, funct7, rd, rs1, rs2, imm): #This returns encoding for a type of instruction


    if type == "R":
        return f"{funct7}{rs2}{rs1}{funct3}{rd}{opcode}"
    
    elif type == "I":
        imm_bin = binary_to_signed_binary(imm, 12)
        return f"{imm_bin}{rs1}{funct3}{rd}{opcode}"
    
    elif type == "S":
        imm_bin = binary_to_signed_binary(imm, 12)
        return f"{imm_bin[:7]}{rs1}{rs2}{funct3}{imm_bin[7:]}{opcode}"
    
    elif type == "B":
        imm_bin = binary_to_signed_binary(imm, 13)
        return f"{imm_bin[0]}{imm_bin[2:8]}{rs2}{rs1}{funct3}{imm_bin[8:12]}{imm_bin[1]}{opcode}"
    
    elif type == "U":
        imm_bin = binary_to_signed_binary(imm, 20)
        return f"{imm_bin}{rd}{opcode}"
    
    elif type == "J":
        imm_bin = binary_to_signed_binary(imm, 21)
        return f"{imm_bin[0]}{imm_bin[10:20]}{imm_bin[9]}{imm_bin[1:9]}{rd}{opcode}"
    
    else:
        return "Instruction Type is Invalid"

def binary_to_signed_binary(value, bits): #This simply converts a binary to signed 2's complement representation

    if value < 0:
        value = (1 << bits) + value  
    return format(value, f'0{bits}b')  

def get_nearest_label_offset(lines, target_index): #This is for label handling
    global register_names_set
    
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
        if tokens and tokens[-1] not in register_names_set and not tokens[-1].isdigit():
            label = tokens[-1]
            possible_positions = label_positions.get(label, [])
            
            
            
            
            if possible_positions:
                nearest_position = min(possible_positions, key=lambda x: abs(x - target_index))  # Pick the closest label
                
                return (nearest_position - target_index) * 4
    
    return None  #if no label is found

def find_immediate_value(tokens, type): #This function finds the immediate value


    target = next((i for i, line in enumerate(lines) if re.split(r'[ ,]+', line) == tokens), -1)
    



    if tokens and tokens[-1] not in register_names_set and not tokens[-1].lstrip('-').isdigit(): #label is involved
        return get_nearest_label_offset(lines, target)
    else: #label is not involved
        
        if type == "R":
            return None  

        for token in tokens:
            if token.lstrip('-').isdigit():  
                return int(token)  
        return None  
    
def func_for_instruction_info(tokens): #This function gets all the info for an instruction as you can see in the dictionary also

    if not tokens:
        return None

    for token in tokens:
        token_u = token.upper()  
        if token_u in instruction_info_main_dict:
            return instruction_info_main_dict[token_u]
    
    return None  

def process_file(input_file, output_filename): #main function of our program where we will use all the above defined functions to get to the final binary output
    errors = []  
    binary_output = []
    
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    for line_number, line in enumerate(lines, start=1):
        try: #In this we are basically getting all the data from a token(using above defined functions) into variables and finally getting its binary representation
            tokens = create_tokens_from_line(line)
            if tokens:
                instr_type = instruction_type_func(tokens)
                dic = func_for_instruction_info(tokens)
                
                if dic is None:
                    errors.append(f"[Error at line {line_number}] Instruction not found: {tokens}")
                    continue
                
                opcode, funct3, funct7 = dic["opcode"], dic["funct3"], dic["funct7"]
                imm = find_immediate_value(tokens, instr_type)
                r_list = convert_register_to_binary(tokens)
                
                if instr_type == "R":
                    binary_instr = format_instruction(instr_type, opcode, funct3, funct7, r_list[0], r_list[1], r_list[2], None)
                elif instr_type == "I":
                    binary_instr = format_instruction(instr_type, opcode, funct3, None, r_list[0], r_list[1], None, imm)
                elif instr_type == "S":
                    binary_instr = format_instruction(instr_type, opcode, funct3, None, None, r_list[0], r_list[1], imm)
                elif instr_type == "B":
                    binary_instr = format_instruction(instr_type, opcode, funct3, None, None, r_list[0], r_list[1], imm)
                elif instr_type == "U":
                    binary_instr = format_instruction(instr_type, opcode, None, None, r_list[0], None, None, imm)
                elif instr_type == "J":
                    binary_instr = format_instruction(instr_type, opcode, None, None, r_list[0], None, None, imm)
                
                binary_output.append(binary_instr)
            else:
                continue
        except Exception as e: #error handling with line number
            errors.append(f"[Error at line {line_number}] {str(e)}")
            break  
    
    
    with open(output_filename, 'w') as output_file: #writing in the output file
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
           

#main executable body of our program
filename = input("Enter input file name: ")
lines=read_file(filename)

output_filename = input("Enter output file name: ")  
process_file(filename, output_filename)

