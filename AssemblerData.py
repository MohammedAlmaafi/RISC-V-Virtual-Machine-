import sys

# instruction and its format
all_insts = {'lui': 'u', 'auipc': 'u', 'jal': 'uj', 'jalr': 'i4', 'beq': 'sb',
             'bne': 'sb', 'blt': 'sb', 'bge': 'sb', 'bltu': 'sb', 'bgeu': 'sb',
             'lw': 'i1', 'lb': 'i1', 'lh': 'i1', 'lbu': 'i1', 'lhu': 'i1',
             'sb': 's', 'sh': 's', 'sw': 's', 'addi': 'i2', 'slti': 'i2',
             'sltiu': 'i2', 'xori': 'i2', 'ori': 'i2', 'andi': 'i2', 'slli': 'i3',
             'srli': 'i3', 'srai': 'i3', 'add': 'r', 'sub': 'r', 'sll': 'r', 'slt': 'r',
             'sltu': 'r', 'xor': 'r', 'srl': 'r', 'sra': 'r', 'or': 'r', 'and': 'r',
             'mul': 'r', 'mulh': 'r', 'mulhsu': 'r', 'mulhu': 'r', 'div': 'r',
             'divu': 'r', 'rem': 'r', 'remu': 'r', 'la': 'p', 'mv': 'p', 'call': 'p', 'ret': 'p',
             'bgtz': 'p', 'j': 'p', 'ble': 'p', 'beqz': 'p', 'blez': 'p', 'li': 'p', 'ecall': 'i5', 'ebreak': 'i5'
             }
# instruction types:
# both I type (1,2) they have funct3
# both I type (3) and R type they have funct3 and (shamt or funct7)
# inst: func3
i1_type = {'opcode': '0000011', 'lb': '000', 'lh': '001', 'lw': '010',
           'lbw': '100', 'lhu': '101'}

# inst: funct3
i2_type = {'opcode': '0010011', 'addi': '000', 'slti': '010', 'sltiu': '011',
           'xori': '100', 'ori': '110', 'andi': '111'}

# [inst,funct3,shamt]
i3_type = {'opcode': ['0010011', ''], 'slli': ['001', '0000000']
    , 'srli': ['101', '0000000'], 'srai': ['101', '0100000']}

i4_type = {'opcode': '1100111', 'jalr': '000'}


i5_type = {'opcode': '1110011', 'rd': '00000', 'funct3': '000', 'rs1': '00000', 'ecall': '000000000000',
           'ebreak': '000000000001'}

# [inst,funct3,funct7]
r_type = {'opcode': ['0110011', ''], 'add': ['000', '0000000'],
          'sub': ['000', '0100000'], 'sll': ['001', '0000000'],
          'slt': ['010', '0000000'], 'sltu': ['011', '0000000'],
          'xor': ['100', '0000000'], 'srl': ['101', '0000000'],
          'sra': ['101', '0100000'], 'or': ['110', '0000000'],
          'and': ['111', '0000000']}

# inst: funct3
s_type = {'opcode': '0100011', 'sb': '000', 'sh': '001', 'sw': '010'}
sb_type = {'opcode': '1100011', 'beq': '000', 'bne': '001', 'blt': '100', 'bge': '101', 'bltu': '110', 'bgeu': '111'}
u_type = {'opcode': '0010111', 'lui': None, 'auipc': None}
uj_type = {'opcode': '1101111', 'jal': None, 'jalr': None}

# Memory Section
# creating 3 arrays ( reserved, text, data) to be added into Memory section
data = {}
text = {}
reserved = []
memory = [reserved, text, data]
 

# fields
PC = 0  # last entry in text segement(addresses offest by 4 )
PCtemp = 0

# creating register dict
#registers dictionary with binary values
reg_dict = {
    'zero': bin(0)[2:].zfill(5),
    'x0': bin(0)[2:].zfill(5),
    'ra': bin(1)[2:].zfill(5),
    'x1': bin(1)[2:].zfill(5),
    'sp': bin(2)[2:].zfill(5),
    'x2': bin(2)[2:].zfill(5),
    'gp': bin(3)[2:].zfill(5),
    'x3': bin(3)[2:].zfill(5),
    'tp': bin(4)[2:].zfill(5),
    'x4': bin(4)[2:].zfill(5),
    't0': bin(5)[2:].zfill(5),
    'x5': bin(5)[2:].zfill(5),
    't1': bin(6)[2:].zfill(5),
    'x6': bin(6)[2:].zfill(5),
    't2': bin(7)[2:].zfill(5),
    'x7': bin(7)[2:].zfill(5),
    's0': bin(8)[2:].zfill(5),
    'x8': bin(8)[2:].zfill(5),
    's1': bin(9)[2:].zfill(5),
    'x9': bin(9)[2:].zfill(5),
    'a0': bin(10)[2:].zfill(5),
    'x10': bin(10)[2:].zfill(5),
    'a1': bin(11)[2:].zfill(5),
    'x11': bin(11)[2:].zfill(5),
    'a2': bin(12)[2:].zfill(5),
    'x12': bin(12)[2:].zfill(5),
    'a3': bin(13)[2:].zfill(5),
    'x13': bin(13)[2:].zfill(5),
    'a4': bin(14)[2:].zfill(5),
    'x14': bin(14)[2:].zfill(5),
    'a5': bin(15)[2:].zfill(5),
    'x15': bin(15)[2:].zfill(5),
    'a6': bin(16)[2:].zfill(5),
    'x16': bin(16)[2:].zfill(5),
    'a7': bin(17)[2:].zfill(5),
    'x17': bin(17)[2:].zfill(5),
    's2': bin(18)[2:].zfill(5),
    'x18': bin(18)[2:].zfill(5),
    's3': bin(19)[2:].zfill(5),
    'x19': bin(19)[2:].zfill(5),
    's4': bin(20)[2:].zfill(5),
    'x20': bin(20)[2:].zfill(5),
    's5': bin(21)[2:].zfill(5),
    'x21': bin(21)[2:].zfill(5),
    's6': bin(22)[2:].zfill(5),
    'x22': bin(22)[2:].zfill(5),
    's7': bin(23)[2:].zfill(5),
    'x23': bin(23)[2:].zfill(5),
    's8': bin(24)[2:].zfill(5),
    'x24': bin(24)[2:].zfill(5),
    's9': bin(25)[2:].zfill(5),
    'x25': bin(25)[2:].zfill(5),
    's10': bin(26)[2:].zfill(5),
    'x26': bin(26)[2:].zfill(5),
    's11': bin(27)[2:].zfill(5),
    'x27': bin(27)[2:].zfill(5),
    't3': bin(28)[2:].zfill(5),
    'x28': bin(28)[2:].zfill(5),
    't4': bin(29)[2:].zfill(5),
    'x29': bin(29)[2:].zfill(5),
    't5': bin(30)[2:].zfill(5),
    'x30': bin(30)[2:].zfill(5),
    't6': bin(31)[2:].zfill(5),
    'x31': bin(31)[2:].zfill(5),
}




def add_to_memory(*args):
    ''''
    stack     0x7fffeffc sub to for push, add to pop (grow to heap pointer)
    v
    ^
    heap      0x10040000 (grow to sp pointer)
    ^                               
    data/regs 0x10010000
    ^
    gp        0x10008000 it is  start of static varibales in data segement
    ^
    text      0x00400000

    this store every line the text segmant
    '''
    global PC
    global PCtemp # data segement pointer start with 0 them initialize by memory size //2 when reach .data dircetive
    
    if PCtemp < args[1]//2: # 0.50% of memory 
        memory[1].update({PC: args[0]})
        PC = PC + 4 # for instructions not complete and for labels addresses
    else:
        memory[2].update({PCtemp: args[0]})
        PCtemp += 32 # for static data and label dicitinary in heap
    

# to process all the basic instructions in the file 
def basic(line, Memory_size):
    x = line[0]
    if all_insts.get(x) == 'i1':
        op = i1_type.get('opcode')
        rd = line[1]
        funct3 = i1_type.get(x)
        rs1 = line[3]
        imm = line[2]
        add_to_memory([12,imm, 5,rs1, 3,funct3, 5,rd, 7,op], Memory_size)# the numbers were added to be used as a flag to tell the size of each element later in the second pass
    elif all_insts.get(x) == 'i2':
        op = i2_type.get('opcode')
        rd = line[1]
        funct3 = i2_type.get(x)
        rs1 = line[2]
        imm = line[3] 
        add_to_memory([12,imm,5, rs1, 3,funct3, 5,rd, 7,op], Memory_size)
    elif all_insts.get(x) == 'i3':
        op = i3_type.get('opcode')[0]
        rd = line[1]
        funct3 = i3_type.get(x)[0]
        rs1 = line[2]
        shamt = line[3]
        funct7 = i3_type.get(x)[1]
        add_to_memory([7,funct7, 5,shamt, 5,rs1, 3,funct3, 5,rd, 7,op], Memory_size)
    elif all_insts.get(x) == 'i4':
        op = i4_type.get('opcode')
        rd = line[1]
        funct3 = i4_type.get(x)
        rs1 = line[2]
        imm = line[3]  # offset
        add_to_memory([12,imm, 5,rs1, 3,funct3, 5,rd, 7,op], Memory_size)
    elif all_insts.get(x) == 'i5':
        op = i5_type.get('opcode')
        rd = i5_type.get('rd')
        rs1 = i5_type.get('rs1')
        funct3 = i5_type.get('funct3')
        if x == 'ecall':
            imm = i5_type.get(x)
        else:
            imm = i5_type.get(x)
        # ready form
        add_to_memory([12,imm, 5,rs1,3,funct3, 5,rd, 7,op], Memory_size)
    elif all_insts.get(x) == 'r':
        op = r_type.get('opcode')[0]
        rd = line[1]
        funct3 = r_type.get(x)[0]
        rs1 = line[2]
        rs2 = line[3]
        funct7 = r_type.get(x)[1]
        
        add_to_memory([7,funct7, 5,rs2, 5,rs1, 3,funct3, 5,rd, 7,op], Memory_size)
    elif all_insts.get(x) == 's':
        op = s_type.get('opcode')
        imm1 = line[2]
        funct3 = s_type.get(x)
        rs1 = line[3]
        rs2 = line[1]
        imm2 = 0
        
        add_to_memory([7,imm2, 5,rs2, 5,rs1, 3,funct3, 5,imm1, 7,op], Memory_size)
    elif all_insts.get(x) == 'sb':
        op = sb_type.get('opcode')
        imm1 = line[3]##################################################
        funct3 = sb_type.get(x)
        rs1 = line[1]
        rs2 = line[2]
        imm2 = line[3]
        
        add_to_memory([7,imm2, 5,rs2, 5,rs1, 3,funct3, 5,imm1, 7,op], Memory_size)
    elif all_insts.get(x) == 'u':
        op = u_type.get('opcode')
        rd = line[1]
        imm = line[2]
        
        add_to_memory([20,imm, 5,rd, 7,op], Memory_size)
    elif all_insts.get(x) == 'uj':
        op = uj_type.get('opcode')
        rd = line[1]
        imm = line[2]
        
        add_to_memory([20,imm, 5,rd, 7,op], Memory_size) 

# to convert the psedou instructions into basic instruction and get processed in basic()
def pseudo(line, Memory_size):
    if line[0] == 'la':
        x = ['auipc', line[1], line[2]]
        basic(x, Memory_size)
        y = ['addi', line[1], line[1], line[2]]
        basic(y, Memory_size)
    elif line[0] == 'mv':
        x = ['add', line[1], 'x0', line[2]]
        basic(x, Memory_size)
    elif line[0] == 'call':
        x = ['auipc', 'x6', bin(0)[2:].zfill(20)]
        basic(x, Memory_size)
        y = ['jalr', 'x1', 'x6', line[1]]
        basic(y, Memory_size)
    elif line[0] == 'ret':
        x = ['jalr', 'x0', 'x1', 0]
        basic(x, Memory_size)
    elif line[0] == 'bgtz':
        x = ['blt', 'x0', line[1], line[2]]
        basic(x, Memory_size)
    elif line[0] == 'j':
        x = ['jal', 'x0', line[1]]
        basic(x, Memory_size)
    elif line[0] == 'ble':
        x = ['bge', line[2], line[1], line[3]]
        basic(x, Memory_size)
    elif line[0] == 'beqz':
        x = ['beq', line[1], 'x0', line[2]]
        basic(x, Memory_size)
    elif line[0] == 'blez':
        x = ['bge', 'x0', line[1], line[2]]
        basic(x, Memory_size)
    elif line[0] == 'li':
        x = ['addi', line[1], 'x0', line[2]]
        basic(x, Memory_size)
    elif line[0] == 'nop':
        x = ['addi', 'x0', 'x0', 0]
        basic(x, Memory_size)
    elif line[0] == 'not':
        x = ['xori', line[1], line[2], -1]
        basic(x, Memory_size)
    elif line[0] == 'neg':
        x = ['sub', line[1], 'x0', line[2]]
        basic(x, Memory_size)
    elif line[0] == 'negw':
        x = ['subw', line[1], 'x0', line[2]]
        basic(x, Memory_size)
    elif line[0] == 'sext':
        x = ['addiw', line[1], line[2], 0]
        basic(x, Memory_size)
    


##############################################################
#                     PASS ONE                               #
##############################################################

#############################################################
# preprocess the file
# prepare the labels and directives and memory
##############################################################
def collectdata(path, Memory_size):
    with open(path) as file:
        delimters = {'\n', '\t', ' ', '', ',', '(', ')', '"'}  # set faster to search using (in) make common case faster
        delimter2 = {'\n', '\t'}
        labels = {}  # to store both label name and line number
        diretives = {"text": [], "data": [], "word": [], 'ascii': []}  # no need for it anymore
        the_line = []
        linenum = 1  # line in source code
        global PC
        global PCtemp

        for line in file:
            string   = ""
            isdire   = 0
            isascii  = 0
            count    = 0
            temp     = ""
            lineflag = 1
            for item in range(len(line)):
                if line[item] == '#':
                    break
                
                elif isascii: # add ascii string
                    if line[item] != '"' and line[item] not in delimter2:
                        if count == 4:
                            temp    = temp[::-1] # reverse it
                            string += temp 
                            temp    = ""
                            count   = 0
                        temp += line[item]
                        count +=1
                    if item == len(line)-1:# fill last 
                        if count != 4: 
                            for i in range(4 - len(temp)):
                                temp    += '\0'
                            temp    = temp[::-1] # reverse it
                            string += temp
                            add_to_memory(string, Memory_size)
                        else:
                            add_to_memory(string, Memory_size)


                elif line[item] == '.':
                    isdire = 1

                elif line[item] not in delimters and isdire == 1:
                    string += line[item]

                elif isdire:  # add dircetives
                    string = ''.join(string.split())
                    isdire = 0
                    try:
                        if string == "text" :
                            PC = 0x0
                        elif string == "data":
                            PCtemp = Memory_size //2
                            PC = Memory_size # we need it to be bigger than Memory_size //2
                        elif string == "ascii":
                            isascii = 1
                            string  = ""
                        diretives[string].append(linenum)
                        string = ""
                    except:
                        string = ""
                        pass

                elif line[item] == ':' and not isdire:  # add labels
                    string = line[0:item]
                    string = "".join(string.split())
                    if PC >= Memory_size //2: # 1024 decimal
                        labels.update({string: PCtemp}) # here in data segement
                    else:
                        labels.update({string: PC}) # in text segemenat
                    string = ""


                elif line[item] not in delimters:  # instrcutiona
                    string += line[item]

                elif string != '':
                    if lineflag == 1:  # line number
                        lineflag = 0
                    the_line.append(string)
                    string = ""
            if the_line != []:
                if all_insts.get(the_line[0]) == 'p':
                    pseudo(the_line, Memory_size)#invoking psuedo method
                elif PC < Memory_size//2:# we are in text segement
                    basic(the_line, Memory_size)#invoking basic method
                else: # we are in data segemnet now
                    add_to_memory(the_line, Memory_size) #invoking adding to memory method
                the_line = []
            isascii = 0
            linenum += 1
    return labels, memory
    