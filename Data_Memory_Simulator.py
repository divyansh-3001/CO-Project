memory = {"0x00010000":0, "0x00010004":0, "0x00010008":0, "0x0001000C":0, "0x00010010":0, "0x00010014":0, "0x00010018":0, "0x0001001C":0, "0x00010020":0, "0x00010024":0, "0x00010028":0, "0x0001002C":0, "0x00010030":0, "0x00010034":0, "0x00010038":0, "0x0001003C":0, "0x00010040":0, "0x00010044":0, "0x00010048":0, "0x0001004C":0, "0x00010050":0, "0x00010054":0, "0x00010058":0, "0x0001005C":0, "0x00010060":0, "0x00010064":0, "0x00010068":0, "0x0001006C":0, "0x00010070":0, "0x00010074":0, "0x00010078":0, "0x0001007C":0}


# False Initialization
aluresult = ""
Writedata = "" #rd
PC = 0
str (type)

if type == "sw": #etc
    write = True
    rd = Writedata
    string_for_updating = str(hex((16 ** 4) + (4 * int(rd[1:]))))
    
    string_for_updating = string_for_updating[0:2] + "000" + string_for_updating[2:].upper()             
    memory[string_for_updating] = aluresult

else:
    write = False


def writeback(type, aluresult, memory, PC):
    if type == "lw":
        return memory[aluresult] 

    elif (type == "jal") or (type == "jalr"):
        return PC + 4
    else:
        return aluresult
for i in range(0,len(memory.keys())):
    p=memory[list(memory.keys())[i]]
    print(f"{list(memory.keys())[i]}: {p}")


