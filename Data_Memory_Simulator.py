# input_file_name = input("Enter input file name: ")
input_file = open("input_file.txt", "r")
output_file = open("output_file.txt" , "w")
lines = input_file.read().split()

PC = 4

Register_file = { "x0": [0 , "zero"], "x1": [0 , "ra"], "x2": [0 , "sp"], "x3": [0 , "gp"], "x4": [0 , "tp"], "x5": [0 , "t0"], "x6": [0 , "t1"], "x7": [0, "t2"], "x8": [0, "s0" , "fp"], "x9": [0, "s1"], "x10": [0 , "a0"], "x11": [0 , "a1"], "x12": [0 , "a2"], "x13": [0 , "a3"], "x14": [0 , "a4"], "x15": [0 , "a5"], "x16": [0 , "a6"], "x17": [0 , "a7"], "x18": [0 , "s2"], "x19": [0 , "s3"], "x20": [0 , "s4"], "x21": [0 , "s5"], "x22": [0 , "s6"], "x23": [0 , "s7"], "x24": [0 , "s8"], "x25": [0 , "s9"], "x26": [0 , "s10"], "x27": [0 , "s11"], "x28": [0 , "t3"], "x29": [0 , "t4"], "x30": [0 , "t5"], "x31": [0 , "t6"]  }


memory = {"0x00010000":0, "0x00010004":0, "0x00010008":0, "0x0001000C":0, "0x00010010":0, "0x00010014":0, "0x00010018":0, "0x0001001C":0, "0x00010020":0, "0x00010024":0, "0x00010028":0, "0x0001002C":0, "0x00010030":0, "0x00010034":0, "0x00010038":0, "0x0001003C":0, "0x00010040":0, "0x00010044":0, "0x00010048":0, "0x0001004C":0, "0x00010050":0, "0x00010054":0, "0x00010058":0, "0x0001005C":0, "0x00010060":0, "0x00010064":0, "0x00010068":0, "0x0001006C":0, "0x00010070":0, "0x00010074":0, "0x00010078":0, "0x0001007C":0}



def type_and_name(opcode , reverse_line):
    name = ""
    type = ""
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
        type = "R"
        return type, name

    elif (opcode == "0000011") or (opcode == "0010011") or (opcode == "1100111"):
        type = "I"
        if opcode == "0000011":
            name = "lw"
        elif opcode == "0010011":
            name = "addi"
        elif opcode == "1100111":
            name = "jalr"
        return type, name
    
    elif (opcode == "0100011"):
        type = "S"
        name = "sw"
        return type, name

    elif (opcode == "1100011"):
        funct3 = (reverse_line[12:15])[::-1]
        type = "B"
        if funct3 == "000":
            name = "beq"
        elif funct3 == "001":
            name = "bne"
        elif funct3 == "100":
            name = "blt"
        return type, name

    elif opcode == "1101111":
        type = "J"
        name = "jal"
        return type, name



def extend_imm(type, imm_to_extend, reverse_line):
    ImmSrc = ""
    if ((ImmSrc == "00") or (type == "I")):
        ImmExt2 = 20 * reverse_line[31] + imm_to_extend[::-1]
    elif ((type == "S") or (ImmSrc == "01")):
        ImmExt2 = 20 * reverse_line[31] + (reverse_line[25:])[::-1] + (reverse_line[7: 12])[::-1]
    elif ((type == "B") or (ImmSrc == "10")):
        ImmExt2 = 19 * reverse_line[31] + reverse_line[31] + reverse_line[7] + (reverse_line[25: 31])[::-1] + (reverse_line[8:12])[::-1] + "0"
    elif ((type == "J") or (ImmSrc == "11")):
        ImmExt2 = 12 * reverse_line[31] + (reverse_line[12:20])[::-1] + reverse_line[20] + (reverse_line[21:31])[::-1] + "0"
    elif (type == "R"):
        ImmExt2 = None
    return ImmExt2


def fetch(PC, type, name, zero_condition, ImmExt , rs1, rs2):
    if type == "B" or "J":
        if name == "beq":
            if zero_condition == True:
                return PC + ImmExt
            else:
                return PC + 4
        elif name == "bne":
            if zero_condition == False:
                return PC + ImmExt
            else:
                return PC + 4
        elif name == "blt":
            if Register_file[rs2][0] - Register_file[rs1][0] > 0:
                return PC + ImmExt
            else:
                return PC + 4
        elif name == "jal":
            return PC + ImmExt
    else:
        return PC + 4


def binary_to_decimal(binary_string):
    ans = 0
    count = 0
    for i in binary_string[::-1]:
        ans = ans + ((2**count) * int(i))
        count = count + 1

    return ans





def ALU2(ImmExt, RD2, type):
    if ((type == "R") or (type == "B")):
        return Register_file[RD2][0]

    if ((type == "I") or (type == "S") or (type == "J")):
        return ImmExt
    
def or_and(instruction , val1, val2):
    if instruction == "or":
        return (bin(val1))[2:] | (bin(val2))[2:]
    else:
        return (bin(val1))[2:] & (bin(val2))[2:]
        
def ALU(SRC1, SRC2, type, name, ImmExt):
    zero_condition = None
    if type == "R":
        if name == "add":
            aluresult = SRC1 + SRC2
        elif name == "sub":
            aluresult = SRC1 - SRC2
        elif name == "slt":
            if SRC1 < SRC2:
                aluresult = 1
            else:
                aluresult = 0
        elif name == "srl":
            shift = int (((bin(SRC2))[2:])[-5::1])
            x = len(str(SRC2))
            aluresult = binary_to_decimal(int (shift * "0" + str(SRC2)[0: x - shift]))
        elif name == "or":
            aluresult = binary_to_decimal(or_and("or", SRC1, SRC2))
        elif name == "and":
            aluresult = binary_to_decimal(or_and("and", SRC1, SRC2))

    elif (type == "I") or (type == "S"):
        aluresult = bin(SRC1) + ImmExt
    elif type == "B":
        if SRC1 - SRC2 == 0:
            zero_condition = True
        else:
            zero_condition = False
    elif type == "J":
        aluresult = None

    return aluresult, zero_condition
            





    return aluresult, zero_condition


def writeback_value(type, aluresult, memory, PC):
    if type == "lw":
        return memory[aluresult] 

    elif (type == "jal") or (type == "jalr"):
        return PC + 4
    else:
        return aluresult



for line in lines:
    reverse_line = line[::-1]
    opcode = (reverse_line[0:7])[::-1]
    (type , name) = type_and_name(opcode, reverse_line)

    
    A1 = (reverse_line[15:20])[::-1]
    A2 = (reverse_line[20:25])[::-1]
    A3 = (reverse_line[7:12])[::-1]  #=rd
    print(A1, A2, A3)
    print(type, name)

    RD1 = "x" + str(binary_to_decimal(A1))
    RD2 = "x" + str(binary_to_decimal(A2))
    A3 = "x" + str(binary_to_decimal(A3))

    imm_to_extend = (reverse_line[7:32])[::-1]

    ImmExt = extend_imm(type, imm_to_extend, reverse_line)

    SRC1 = Register_file[RD1][0]
    SRC2 = ALU2(ImmExt, RD2, type)

    aluresult, zero_condition = ALU(SRC1, SRC2, type, name, ImmExt)

    Writedata = Register_file[RD2][0]
    
    if type == "sw":  # etc
        write = True
        string_for_updating = str(hex((16 ** 4) + (4 * int(Writedata[1:]))))
        string_for_updating = string_for_updating[0:2] + "000" + string_for_updating[2:]

        memory[string_for_updating] = aluresult

    else:
        write = False


    writeback = False
    if (type == "R") or (type == "I") or (type == "J"):
        writeback = True

    if writeback == True:
        Register_file[A3][0] = writeback_value(type, aluresult, memory, PC)


    output_file.write(str(Register_file) + "\n")
    output_file.write(str(memory) + "\n")
    PC = fetch(PC, type, name, zero_condition, ImmExt, RD1, RD2)


output_file.close()
input_file.close()
