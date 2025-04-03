input_file_name = input("Enter input file name: ")
input_file_str = "/Users/divyanshgoel/Downloads/final_valuation_framework_mar30_2025_students_v5 2/automatedTesting/tests/bin/simple/" + input_file_name
input_file = open(input_file_str, "r")
output_file_str = "/Users/divyanshgoel/Downloads/final_valuation_framework_mar30_2025_students_v5 2/automatedTesting/tests/user_traces/simple/" + input_file_name
output_file = open(output_file_str, "w")
lines = input_file.read().split()

PC = 4

Register_file = { "x0": [0 , "zero"], "x1": [0 , "ra"], "x2": [380 , "sp"], "x3": [0 , "gp"], "x4": [0 , "tp"], "x5": [0 , "t0"], "x6": [0 , "t1"], "x7": [0, "t2"], "x8": [0, "s0" , "fp"], "x9": [0, "s1"], "x10": [0 , "a0"], "x11": [0 , "a1"], "x12": [0 , "a2"], "x13": [0 , "a3"], "x14": [0 , "a4"], "x15": [0 , "a5"], "x16": [0 , "a6"], "x17": [0 , "a7"], "x18": [0 , "s2"], "x19": [0 , "s3"], "x20": [0 , "s4"], "x21": [0 , "s5"], "x22": [0 , "s6"], "x23": [0 , "s7"], "x24": [0 , "s8"], "x25": [0 , "s9"], "x26": [0 , "s10"], "x27": [0 , "s11"], "x28": [0 , "t3"], "x29": [0 , "t4"], "x30": [0 , "t5"], "x31": [0 , "t6"]  }

memory = {"0x00010000":0, "0x00010004":0, "0x00010008":0, "0x0001000C":0, "0x00010010":0, "0x00010014":0, "0x00010018":0, "0x0001001C":0, "0x00010020":0, "0x00010024":0, "0x00010028":0, "0x0001002C":0, "0x00010030":0, "0x00010034":0, "0x00010038":0, "0x0001003C":0, "0x00010040":0, "0x00010044":0, "0x00010048":0, "0x0001004C":0, "0x00010050":0, "0x00010054":0, "0x00010058":0, "0x0001005C":0, "0x00010060":0, "0x00010064":0, "0x00010068":0, "0x0001006C":0, "0x00010070":0, "0x00010074":0, "0x00010078":0, "0x0001007C":0}

def type_and_name(opcode , reverse_line):
    name = ""
    inst_type = ""
    if opcode == "0110011":
        funct3 = (reverse_line[12:15])[::-1]
        funct7 = (reverse_line[25:])[::-1]
        
        if funct3 == "000":
            if funct7 == "0000000":
                name = "add"
            else:
                name = "sub"
        elif funct3 == "010":
            name = "slt"
        elif funct3 == "101":
            name = "srl"
        elif funct3 == "110":
            name = "or"
        elif funct3 == "111":
            name = "and"
        inst_type = "R"
        return inst_type, name

    elif opcode in ["0000011", "0010011", "1100111"]:
        inst_type = "I"
        if opcode == "0000011":
            name = "lw"
        elif opcode == "0010011":
            name = "addi"
        elif opcode == "1100111":
            name = "jalr"
        return inst_type, name
    
    elif opcode == "0100011":
        inst_type = "S"
        name = "sw"
        return inst_type, name

    elif opcode == "1100011":
        funct3 = (reverse_line[12:15])[::-1]
        inst_type = "B"
        if funct3 == "000":
            name = "beq"
        elif funct3 == "001":
            name = "bne"
        elif funct3 == "100":
            name = "blt"
        return inst_type, name

    elif opcode == "1101111":
        inst_type = "J"
        name = "jal"
        return inst_type, name

def extend_imm(inst_type, reverse_line):
    # Use string multiplication to replicate sign bit
    if inst_type == "I":
        ImmExt2 = reverse_line[31] * 20 + (reverse_line[20:])[::-1]
    elif inst_type == "S":
        ImmExt2 = reverse_line[31] * 20 + (reverse_line[25:])[::-1] + (reverse_line[7:12])[::-1]
    elif inst_type == "B":
        ImmExt2 = reverse_line[31] * 19 + reverse_line[31] + reverse_line[7] + (reverse_line[25:31])[::-1] + (reverse_line[8:12])[::-1] + "0"
    elif inst_type == "J":
        ImmExt2 = reverse_line[31] * 12 + (reverse_line[12:20])[::-1] + reverse_line[20] + (reverse_line[21:31])[::-1] + "0"
    elif inst_type == "R":
        ImmExt2 = None
    return ImmExt2

def fetch(PC, inst_type, name, zero_condition, ImmExt , rs1, rs2):
    if inst_type in ["B", "J"]:
        if name == "beq":
            if zero_condition:
                return PC + binary_to_decimal(ImmExt)
            else:
                return PC + 4
        elif name == "bne":
            if not zero_condition:
                return PC + binary_to_decimal(ImmExt)
            else:
                return PC + 4
        elif name == "blt":
            if Register_file[rs2][0] - Register_file[rs1][0] > 0:
                return PC + binary_to_decimal(ImmExt)
            else:
                return PC + 4
        elif name == "jal":
            return PC + binary_to_decimal(ImmExt)
    else:
        return PC + 4

def binary_to_decimal(binary_string):
    if binary_string[0:2] == "0b":
        binary_string_2 = binary_string[2:]
    else:
        binary_string_2 = binary_string
    ans = 0
    count = 0
    for i in binary_string_2[::-1]:
        ans += (2 ** count) * int(i)
        count += 1
    return ans

def ALU2(ImmExt, RD2, inst_type):
    if inst_type in ["R", "B"]:
        return Register_file[RD2][0]
    if inst_type in ["I", "S", "J"]:
        return binary_to_decimal(ImmExt)

def or_and(instruction, val1, val2):
    if instruction == "or":
        return val1 | val2
    else:
        return val1 & val2

def to_signed32(x):
    # Convert a 32-bit unsigned integer to a signed integer.
    if x & (1 << 31):
        return x - (1 << 32)
    return x

def ALU(SRC1, SRC2, inst_type, name, ImmExt):
    zero_condition = None
    if inst_type == "R":
        if name == "add":
            aluresult = (SRC1 + SRC2) & 0xFFFFFFFF
        elif name == "sub":
            aluresult = to_signed32((SRC1 - SRC2) & 0xFFFFFFFF)
        elif name == "slt":
            aluresult = 1 if SRC1 < SRC2 else 0
        elif name == "srl":
            shift = 5
            aluresult = SRC1 >> shift
        elif name == "or":
            aluresult = SRC1 | SRC2
        elif name == "and":
            aluresult = SRC1 & SRC2
    elif inst_type in ["I", "S"]:
        aluresult = (SRC1 + binary_to_decimal(ImmExt)) & 0xFFFFFFFF
    elif inst_type == "B":
        zero_condition = (SRC1 - SRC2 == 0)
        aluresult = None
    elif inst_type == "J":
        aluresult = None
    return aluresult, zero_condition


def writeback_value(inst_type, aluresult, memory, PC):
    if inst_type == "lw":
        return memory[aluresult] 
    elif inst_type in ["jal", "jalr"]:
        return PC + 4
    else:
        return aluresult


condition = False
while True:
    try:
        index = (int(PC / 4)) - 1
        if 0 <= index < len(lines):
            line = lines[index]
        else:
            break

        reverse_line = line[::-1]
        opcode = (reverse_line[0:7])[::-1]

        inst_type, name = type_and_name(opcode, reverse_line)
        
        A1 = (reverse_line[15:20])[::-1]
        A2 = (reverse_line[20:25])[::-1]
        A3 = (reverse_line[7:12])[::-1]  # rd

        RD1 = "x" + str(binary_to_decimal(A1))
        RD2 = "x" + str(binary_to_decimal(A2))
        A3 = "x" + str(binary_to_decimal(A3))

        ImmExt = extend_imm(inst_type, reverse_line)

        SRC1 = Register_file[RD1][0]
        SRC2 = ALU2(ImmExt, RD2, inst_type)

        aluresult, zero_condition = ALU(SRC1, SRC2, inst_type, name, ImmExt)
        Writedata = Register_file[RD2][0]
        
        if inst_type == "S":
            # Correct: convert Writedata to binary string then to int for address calc.
            string_for_updating = str(hex((16 ** 4) + (4 * int(bin(Writedata)[2:]))))
            string_for_updating = string_for_updating[0:2] + "000" + string_for_updating[2:]
            memory[string_for_updating] = aluresult

        writeback = inst_type in ["R", "I", "J"]
        if writeback:
            Register_file[A3][0] = writeback_value(inst_type, aluresult, memory, PC)

        if (PC / 4) == len(lines):
            PC = PC - 4
            condition = True

        no_2 = 34 - len(str(bin(PC)))
        s_f_pc = "0b" + no_2 * "0" + str(bin(PC))[2:]
        output_file.write(s_f_pc + " ")

        for reg in Register_file:
            reg_val = Register_file[reg][0]
            bin_val = bin(reg_val) if reg_val >= 0 else "-" + bin(abs(reg_val))
            if len(bin_val) == 34:
                output_file.write(bin_val + " ")
            else:
                st = "1" if reg_val < 0 else "0"
                no = 34 - len(bin_val)
                s_f = "0b" + no * st + bin_val[2:] if reg_val >= 0 else "-" + "0b" + no * st + bin_val[3:]
                output_file.write(s_f + " ")

        output_file.write("\n")
        x = fetch(PC, inst_type, name, zero_condition, ImmExt, RD1, RD2)

        if condition:
            PC = PC + 4
            break

        if x == PC:
            condition = False
            break
        else:
            PC = x
    except Exception as e:
        print("Error occurred")
        print("Please check assembly code")
        print("At line number ", int(PC / 4))
        output_file.write("Error occurred. Please check assembly code. At line number " + str(int(PC/4)))
        break

for addr in memory:
    no_3 = 34 - len(str(bin(memory[addr])))
    s_f_mem = "0b" + no_3 * "0" + str(bin(memory[addr]))[2:]
    output_file.write(str(addr) + ":" + s_f_mem + "\n")
output_file.close()
input_file.close()
