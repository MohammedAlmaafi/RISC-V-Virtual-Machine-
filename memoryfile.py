import os
class Memory_class():
    def __init__(self, size):
        self.size        = size

        # byte addressable memory
        # text segemnet
            # 0.50% of memory(every address have 4 bytes(32bits))
            # 4 bytes between instructions
        # data segements
            # 0.50% of memory (every address have 32 bytes)
            # 32 bytes between data
        self.memory      = bytearray(self.size)

    # to load instructions and data
    def load(self, path):
        folder_name = os.path.dirname(path)
        folder_name= folder_name + "\\" + "asmmbler output"
        
        with open(folder_name + "\out.bin",'rb') as file:
            instructions_bytes = file.read()
            self.memory[:self.size//2] = instructions_bytes  
       
        with open(folder_name + "\data.bin", 'rb') as file:
            data_bytes = file.read()
            self.memory[self.size//2:] = data_bytes       

        # # This is for UART
        for item in range(len(self.memory), self.size+32):             
            self.memory.append(0x00)


    def read(self, address):
        return self.memory[address:address+4] 

    def readHalf(self, address):
        return self.memory[address:address+2] 

    def readByte(self, address):
        return self.memory[address] 

    def readData(self, address):
        return self.memory[address:address+32] 


    def write(self,  address, instruction):
        # to make it into 4 bytes
        self.memory[address:address+4] = int.to_bytes(instruction, 4, byteorder='little', signed=False)

    def writeData(self, address, data):
        self.memory[address:address+32] = data

# if __name__ == "__main__":
#     obj = Memory_class(4096*8)
#     Mcodepath = r"C:\Users\Mohammed Almaafi\Documents\WSforVS\EE361Project1\New\here.bin"
#     datapath  = r"C:\Users\Mohammed Almaafi\Documents\WSforVS\EE361Project1\New\data.bin"
#     obj.load(Mcodepath, datapath)
