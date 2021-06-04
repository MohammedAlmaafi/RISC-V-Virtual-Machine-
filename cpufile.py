import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import Submit

class CPU():
    def __init__(self, vbus):

        # next instruction to be executed
        self.PC    = 0
        self.bytes = 0 # this used in fetch method
        self.vbus  = vbus # this is reference for vbus to use it

        # register number same as list index
        self.registers = [0 for i in range(32)]

        # sp start of stack (growing down)
        self.registers[2] = 0

        # gp start of static 
        self.registers[3] = 0 #6144

        # bytes fetched decoded to its part
        self.instruction = []
        
        # after decoding instruction to its parts
        self.opcode = 0
        self.rd     = 0
        self.func3  = 0
        self.rs1    = 0
        self.rs2    = 0
        self.func7  = 0
        

        # for GUI
        self.string = ""
        
        # function call automation
        # this act like big switch with values of functions names
        # using opcode as key we get function name 
        # if there are funct 3 and funct7
        # it will keep chaining to reach the correct function then execute it 
        # this helps alot performnce wise
        self.selector = {51:self._0110011, 19:self._0010011, 3:self._0000011, 35:self._0100011, 
                         99:self._1100011, 111:self.JAL, 103:self.JALR, 55:self.LUI, 23:self.AUIPC, 115:self.ECALL
                         }
     
    # R-format
    # some R-format have same opcode it
    # using selevtor attribute we come here and find the correct function to execute 
    def _0110011(self):
        
        # this continue the selector attribute chain
        dictionary = {0x0:{0x0:self.ADD, 0x20:self.SUB, 0x01:self.MUL}, 0x4:{0x0:self.XOR, 0x01:self.DIV},
                      0x6:{0x0:self.OR, 0x01:self.REM}, 0x7:{0x0:self.AND, 0x01: self.REMU}, 0x1:{0x0:self.SLL, 0x01:self.MULH},
                      0x5:{0x0:self.SRL, 0x20:self.SRL, 0x01:self.DIVU}, 0x2:{0x0:self.SLT, 0x01:self.MULSU}, 
                      0x3:{0x0:self.SLTU, 0x01:self.MULU,}}
        
        # calling the function using func3 and func7
        dictionary.get(self.func3).get(self.func7)()
        
    
    #I-format
    # some I-format have same opcode it jump using selevtor attribute
    # using selevtor attribute we come here and find the correct function to execute 
    def _0010011(self):

        # needs to check for func7
        dictionary = {0x0:self.ADDI, 0x4:self.XORI, 0x6: self.ORI ,0x7:self.ANDI, 0x1:{self.func7:self.SLLI}, 
                      0x5:{self.func7:self.SRLI, self.func7:self.SRAI}, 0x2:self.SLTI, 0x3:self.SLTIU}

        
        # check for func3 in only 2 cases
        if (self.func3 == 0x1 or self.func3 == 0x5):
            dictionary.get(self.func3).get(self.func7)()
        else:
            dictionary.get(self.func3)()
        

    #I2-format ---> load
    def _0000011(self):
        dictionary = {0x0: self.LB, 0x1: self.LH, 0x2: self.LW, 0x4: self.LBU, 0x5: self.LHU}
        
        dictionary.get(self.func3)()
        

    #S-format 
    def _0100011(self):
        dictionary = {0x0: self.SB, 0x1: self.SH, 0x2: self.SW}
        
        dictionary.get(self.func3)()
        

    #B-format
    def _1100011(self):
        dictionary = {0x0: self.BEQ, 0x1: self.BNE, 0x4: self.BLT, 0x5: self.BGE,
        0x6: self.BLTU, 0x7: self.BGEU}
        
        dictionary.get(self.func3)()
        

 
    ################################ R format ################################
    def ADD(self):        
        
        self.registers[self.rd] = self.registers[self.rs1] + self.registers[self.rs2]
        
        self.PC += 4
        

    def SUB(self):
        
        self.registers[self.rd] = self.registers[self.rs1] - self.registers[self.rs2]
        
        self.PC += 4
        

    def XOR(self):
        
        self.registers[self.rd] = self.registers[self.rs1] ^ self.registers[self.rs2]
        
        self.PC += 4
        

    def OR(self):
        
        self.registers[self.rd] = self.registers[self.rs1] | self.registers[self.rs2]
        
        self.PC += 4
        

    def AND(self):
        
        self.registers[self.rd] = self.registers[self.rs1] & self.registers[self.rs2]
        
        self.PC += 4
        

    def SLL(self):
        
        self.registers[self.rd] = self.registers[self.rs1] << self.registers[self.rs2]
        
        self.PC += 4

    def SRL(self):
        
        self.registers[self.rd] = self.registers[self.rs1] >> self.registers[self.rs2]
        
        self.PC += 4

    def SRA(self):
        
        self.registers[self.rd] = self.registers[self.rs1] >> self.registers[self.rs2]
        
        self.PC += 4

    def SLT(self):
        
        if(self.registers[self.rs1] < self.registers[self.rs2]):
            self.registers[self.rd] = 1
        else:
            self.registers[self.rd] = 0
        
        self.PC += 4

    def SLTU(self):
        
        if(self.registers[self.rs1] < self.registers[self.rs2]):
            self.registers[self.rd] = 1
        else:
            self.registers[self.rd] = 0
        
        self.PC += 4
        
    
    ################################ R format RV32M ################################
    def MUL(self):
        
        self.registers[self.rd] = (self.registers[self.rs1] * self.registers[self.rs2]) & 0xffffffff
        
        self.PC += 4
        

    def MULH(self):
        
        self.registers[self.rd] = (self.registers[self.rs1] * self.registers[self.rs2]) & 0xffffffff00000000
        
        self.PC += 4
 
    # S U
    def MULSU(self):
        
        self.registers[self.rd] = (self.registers[self.rs1] * self.registers[self.rs2]) & 0xffffffff00000000
        
        self.PC += 4
    # U
    def MULU(self):
        
        self.registers[self.rd] = (self.registers[self.rs1] * self.registers[self.rs2]) & 0xffffffff00000000
        
        self.PC += 4

    def DIV(self):
        
        self.registers[self.rd] = (self.registers[self.rs1 / self.rs2]) 
        
        self.PC += 4

    # U
    def DIVU(self):
        
        self.registers[self.rd] = (self.registers[self.rs1] / self.registers[self.rs2])
        
        self.PC += 4

    def REM(self):
        
        self.registers[self.rd] = (self.registers[self.rs1] % self.registers[self.rs2])
        
        self.PC += 4

    # U
    def REMU(self):
        
        self.registers[self.rd] = (self.registers[self.rs1] % self.registers[self.rs2]) 
        
        self.PC += 4
    
    
    ################################ I format ################################
    def ADDI(self):
        #imm for 12-bit
        imm = (self.func7 <<5) | self.rs2
        
        if (imm & (1 << (12 - 1))): # if sign bit is set e.g., 8bit: 128-255
            imm = imm - (1 << 12)
        
        self.registers[self.rd] = self.registers[self.rs1] + imm

        self.PC += 4
        

    def XORI(self):
        #imm for 12-bit
        imm = (self.func7 <<5) | self.rs2
        
        self.registers[self.rd] = self.registers[self.rs1] ^ imm
        
        self.PC += 4
        

    def ORI(self):
        #imm for 12-bit
        imm = (self.func7 <<5) | self.rs2
        
        self.registers[self.rd] = self.registers[self.rs1] | imm
        
        self.PC += 4
        

    def ANDI(self):
        # imm for 12-bit
        imm = (self.func7 <<5) | self.rs2
        
        self.registers[self.rd] = self.registers[self.rs1] & imm
        
        self.PC += 4
        

    def SLLI(self):
        self.registers[self.rd] = self.registers[self.rs1] >> self.registers[self.rs2]

        self.PC += 4

    def SRLI(self):
        self.registers[self.rd] = self.registers[self.rs1] >> self.registers[self.rs2]

        self.PC += 4

    def SRAI(self):# for 1 extends circular        
        self.registers[self.rd] = self.registers[self.rs1] >> self.registers[self.rs2]
        
        self.PC += 4
        

    def SLTI(self):
        imm = (self.func7 <<5) | self.rs2
        
        if(self.registers[self.rs1] < imm):
            self.registers[self.rd] = 1
        else:
            self.registers[self.rd] = 0
        
        self.PC += 4
        

    def SLTIU(self):
        imm = (self.func7 <<5) | self.rs2
        
        if(self.registers[self.rs1] < imm):
            self.registers[self.rd] = 1
        else:
            self.registers[self.rd] = 0
        
        self.PC += 4

    def LB(self):
        #imm for 12-bit
        imm = (self.func7 <<5) | self.rs2
        
        self.registers[self.rd] = (self.vbus.readMEM(self.registers[self.rs1] + imm)) & 255
        
        self.PC += 4
        

    def LH(self):
        imm = (self.func7 <<5) | self.rs2
        
        self.registers[self.rd] = (self.vbus.readMEM(self.registers[self.rs1] + imm)) & 0xffff # easier represnation 
        
        self.PC += 4

    def LW(self):
        #imm for 12-bit
        imm = (self.func7 <<5) | self.rs2
        self.registers[self.rd] = (self.vbus.readMEM(self.registers[self.rs1] + imm)) 
        self.registers[self.rd] = int.from_bytes((self.vbus.readMEM(self.registers[self.rs1] + imm)),byteorder='little',signed=False)
        
        self.PC += 4



    def LBU(self):#zero extends
        #imm for 12-bit
        imm = (self.func7 <<5) | self.rs2
        self.registers[self.rd] = (self.vbus.readMEM(self.registers[self.rs1] + imm)) & 255 
        self.PC += 4

    def LHU(self):#zero extends
        #imm for 12-bit
        imm = (self.func7 <<5) | self.rs2
        self.registers[self.rd] = (self.vbus.readMEM(self.registers[self.rs1] + imm)) & 0xffff # easier represnation 
        self.PC += 4
    
    def JALR(self):
        imm = self.func7 <<5 | self.rs2  

        if (imm & (1 << (12 - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            imm = imm - (1 << 12)

        if self.rd != 0:
            self.registers[self.rd] = self.PC + 4
        self.PC = self.registers[self.rs1] + imm

    ################################ U format ################################
    def LUI(self):
        imm = (self.func7 <<13) | (self.rs2 <<8) | (self.rs1 <<3) | (self.func3)
        self.registers[self.rd] = imm
        self.PC += 4

    def AUIPC(self):
        imm = (self.func7 <<13) | (self.rs2 <<8) | (self.rs1 <<3) | (self.func3)
        imm = imm << 12
        self.registers[self.rd] = self.PC + imm
        self.PC += 4

    ################################ B format ################################
    def BEQ(self):
        part1 = ( self.rd & 0x1e) >> 1
        part2 = (self.func7 & 0x3f) <<4
        part3 = (self.rd & 1) << 10
        part4 = (self.func7& 0x40) << 5
       
        
        imm = (part4)|(part3)|(part2)| part1
        if (imm & (1 << (12- 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            imm = imm - (1 <<12)
        imm = (imm << 1)
        if (self.registers[self.rs1] == self.registers[self.rs2]):
            self.PC = self.PC + imm 
        else:
            self.PC += 4
        

    def BNE(self):
        part1 = ( self.rd & 0x1e) >> 1
        part2 = (self.func7 & 0x3f) <<4
        part3 = (self.rd & 1) << 10
        part4 = (self.func7& 0x40) << 5
        
        
        imm = (part4)|(part3)|(part2)| part1
        if (imm & (1 << (12- 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            imm = imm - (1 <<12)
        imm = (imm << 1)

        if (self.registers[self.rs1] != self.registers[self.rs2]):
            self.PC = self.PC + imm 
        else:
            self.PC += 4


    def BLT(self):
        part1 = ( self.rd & 0x1e) >> 1
        part2 = (self.func7 & 0x3f) <<4
        part3 = (self.rd & 1) << 10
        part4 = (self.func7& 0x40) << 5
        
        imm = (part4)|(part3)|(part2)| part1
        if (imm & (1 << (12- 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            imm = imm - (1 <<12)
        imm = (imm << 1)
        
        if (self.registers[self.rs1]< self.registers[self.rs2]):
            self.PC = self.PC + imm 
        else:
            self.PC += 4

    def BGE(self):
        part1 = ( self.rd & 0x1e) >> 1
        part2 = (self.func7 & 0x3f) <<4
        part3 = (self.rd & 1) << 10
        part4 = (self.func7& 0x40) << 5
        
        imm = (part4)|(part3)|(part2)| part1
        if (imm & (1 << (12- 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            imm = imm - (1 <<12)
        imm = (imm << 1)
        if (self.registers[self.rs1] >= self.registers[self.rs2]):
            self.PC = self.PC + imm 
        else:
            self.PC += 4

    def BLTU(self):#zero extends
        part1 = ( self.rd & 0x1e) >> 1
        part2 = (self.func7 & 0x3f) <<4
        part3 = (self.rd & 1) << 10
        part4 = (self.func7& 0x40) << 5

        imm = (part4)|(part3)|(part2)| part1
        imm = (imm << 1)

        if (self.registers[self.rs1] < self.registers[self.rs2]):
            self.PC = self.PC + imm 
        else:
            self.PC += 4

    def BGEU(self):#zero extends
        part1 = ( self.rd & 0x1e) >> 1
        part2 = (self.func7 & 0x3f) <<4
        part3 = (self.rd & 1) << 10
        part4 = (self.func7& 0x40) << 5

        imm = (part4)|(part3)|(part2)| part1
        imm = (imm << 1)

        if (self.registers[self.rs1] >= self.registers[self.rs2]):
            self.PC = self.PC + imm
        else:
            self.PC += 4

    ################################ S format ################################
    def SB(self):
        imm = (self.func7 <<5) | self.rd
        value = self.registers[self.rs2] & 255
        address = (self.registers[self.rs1] + imm) 
        self.vbus.writeMEM(address,value) 
        self.PC += 4

    def SH(self):
        imm = (self.func7 <<5) | self.rd
        value = self.registers[self.rs2] & 0xffff
        address = (self.registers[self.rs1] + imm) 
        self.vbus.writeMEM(address,value)
        self.PC += 4

    def SW(self):
        imm = (self.func7 <<5) | self.rd
        value = self.registers[self.rs2] 
        address = (self.registers[self.rs1] + imm)
        if (address & (1 << (address.bit_length() - 1))) == 0 and self.registers[3] < 4095: # if sign bit is set e.g., 8bit: 128-255
            address = address + 4096 # if it is negative make it positive only in 4kilobytes case NEED FIX
        self.vbus.writeMEM(address, value)
        self.PC += 4
        
    def ECALL(self):
        # printing using UART
        if self.registers[17] == 64: 
            if (self.registers[11] & (1 << (self.registers[11].bit_length() - 1))) == 0 and self.registers[3] < 4095: # if sign bit is set e.g., 8bit: 128-255
                self.registers[11] = self.registers[11] + 4096 # if it is negative make it positive only in 4kilobytes case NEED FIX
            self.vbus.writeData(self.vbus.UART.address, self.vbus.readData(self.registers[11]))
            self.vbus.UART.length = self.registers[12]
            self.vbus.UART.RUN()
            
        # exit virtual machine
        elif self.registers[17] == 93:

            temp = self.vbus.memory.size//2
            self.string = self.vbus.UART.string
            string =  "The sorted Array:\n\t\t"
            
            string += "["
            for i in range(8):
                if i == 7:
                    string += str(int.from_bytes(self.vbus.memory.memory[temp:temp+4] ,byteorder='little',signed=False))
                else:
                    string += str(int.from_bytes(self.vbus.memory.memory[temp:temp+4] ,byteorder='little',signed=False)) + ","
                temp +=4
            string += "]"

            temp = self.vbus.memory.size//2+32
            
            string += "\n\t\t["
            for i in range(8):
                if i == 7:
                    string += str(int.from_bytes(self.vbus.memory.memory[temp:temp+4] ,byteorder='little',signed=False))
                else:
                    string += str(int.from_bytes(self.vbus.memory.memory[temp:temp+4] ,byteorder='little',signed=False)) + ","
                temp +=4
            string += "]"

            ###################GUI#########################
            gui.theme("TealMono")
            
            layout = [[gui.Text(self.string)],[gui.Text(string)],[gui.Exit()]]
            window = gui.Window("Virtual Machine",layout, size=(400,350) )
            
            event, values = window.read()
            window.close()
            ################################################
            exit(0)

        self.PC += 4

    def EBREAK(self):
        self.PC += 4
        pass
        

    ################################  UJ format ################################
    def JAL(self):
        '''
        reassemble the imm
        look for extension (2's comp) 
        needs to be shifted by 1 to the left similar to (multiply by 2)

        '''
        imm = (self.func7 <<13) | (self.rs2 <<8) | (self.rs1 <<3) | (self.func3)
        part1 = ( imm & 0x7FE00) >> 9
        part2 = (imm & 0x100) <<2
        part3 = (imm & 0xff) << 11
        part4 = (imm & 0x80000)
        imm = ((part4)|(part3)|(part2)| part1)
        if (imm & (1 << (20 - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            imm = imm - (1 << 20)
        imm = imm << 1
        if self.rd != 0:
            self.registers[self.rd] = self.PC + 4
        self.PC = self.PC + imm
        


    ##################################### main functions #######################################
    
    def fetch(self):
        self.instruction = []

        # read from memory using the vbus
        self.bytes  = self.vbus.readMEM(self.PC)

        # little endian
        for i in range(4):
            self.instruction.append(self.bytes[i])

    def decode(self):
        # >> taken 
        # << will take
        self.opcode= self.instruction[0] & 127 # 127 is opcode mask
        # 0-6bits taken
        bit = self.instruction[0] >> 7 # shifting 
        self.rd= (((self.instruction[1] << 1) & 30) | bit)
        # 7-11bits taken
        self.func3= (self.instruction[1] >> 4 ) & 7
        # 12-14bits taken
        bit2 = self.instruction[1] >> 7 
        self.rs1= (((self.instruction[2] << 1) & 30) | bit2)
        # 15-19bits taken
        bit3 = (self.instruction[3] & 1) # for the first bit 
        self.rs2= (bit3<< 4 | ((self.instruction[2] >> 4) & 15)) 
        # 20-24bits taken   
        self.func7= self.instruction[3] >> 1

    def execute(self):
        # this is will chain to reach correct function
        self.selector.get(self.opcode)()


