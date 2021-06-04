import os
from sys import path
from AssemblerData import reg_dict, collectdata

# global
instruction = 0

def offset(PC,vlabel):
    delta = vlabel-PC
    delta2 = vlabel-(PC-4)
    imm = vlabel-PC
    jimm = vlabel-PC
    
    # zero extension
    if delta >= 0 or delta2 >=0 or imm >= 0 or jimm>=0 :
        if '0010111' in instruction:
            delta = delta +32#add word(4bytes) to convert to 2's complement for the higher-bits imm 
        delta = bin(delta)[2:].zfill(32)
        delta2 = bin(delta2)[2:].zfill(32)#to avoid delta using previous PC
        imm = bin(imm)[2:].zfill(13)
        jimm = bin(jimm)[2:].zfill(21)
        low  = delta2[20:]
        high = delta[0:20]#+delta[20]

    
    # ones extension
    else:
        if '0010111' in instruction:
            delta = delta +1 
        delta = bin((1 << 32) + delta)[2:]
        delta2 = bin((1 << 32) +delta2)[2:]
        imm = bin((1 << 13 ) + imm)[2:]
        jimm = bin((1 << 21 ) + jimm)[2:]
        low  = delta2[20:]
        high = delta[0:20]#+delta[20]
    return [high,low,imm,jimm]

#sb, uj format
def special(imm): 
    imm1 = imm[0]+imm[2:8]
    imm2 = imm[8:12]+imm[1]
    jimm = imm[0]+imm[10:20]+imm[9]+imm[1:9]#j imm
    return [imm1,imm2,jimm]



# here we write
# text segement files
    # binary file
    # binary string file
# data sgement file
# in same folder for the source code
def write_to_files(path, memory):

    # make child folder in folder of the source code
    folder_name = os.path.dirname(path)
    folder_name= folder_name + "\\" + "asmmbler output"
    if  os.path.isdir(folder_name) == False:
        os.mkdir(folder_name)
    
    with open(folder_name+ "\out.txt", "w") as output_file: # text output file
        for i in memory[1].values():
            output_file.write(i+'\n')

    with open(folder_name + "\out.bin", "wb") as file:
        for i in memory[1].values():
            o = int(i, 2)
            file.write(o.to_bytes(4, byteorder="little", signed=False))
   
    with open(folder_name+ "\data.bin", "wb") as file:
        for i in memory[2].values():
            # data = []
            if isinstance(i, str):
                file.write(i.encode('ascii'))
            else:
                for j in range(8):
                    i[j] = int(i[j])
                    file.write(i[j].to_bytes(4, byteorder="little", signed=False))

def run(path, memory_size):
    # this is from AssmblerData
    labels, memory = collectdata(path, memory_size) 
        # count = 0x10040000 # in heap
    PC    = 0x0
    while 1:
        string = ""
        global instruction
        instruction = memory[1].get(PC)
        try:
            len(instruction)
        except:
            # when we read none thats we mean we finished
            # print("Done...")
            break 
        for chunk in range(1,len(instruction), 2): 
            n = instruction[chunk-1]
            if instruction[chunk] in labels.keys():
                if '1101111' in instruction:# to apply special method for uj format 
                        imm =  special(offset(PC,labels.get(instruction[chunk]))[3])[2]
                elif n == 20:
                    imm =  offset(PC,labels.get(instruction[chunk]))[0]  
                elif '1100011' in instruction:## to apply special method for sb format 
                    if n == 7:
                        imm =  special(offset(PC,labels.get(instruction[chunk]))[2])[0]
                    else:
                        imm = special(offset(PC,labels.get(instruction[chunk]))[2])[1]
                elif n == 12: 
                    imm =  offset(PC,labels.get(instruction[chunk]))[1]
                string += imm 
            elif instruction[chunk] in reg_dict.keys():#to get registers binary value
                reg_address = reg_dict.get(instruction[chunk])
                string += reg_address
            elif isinstance(instruction[chunk], int):
                string += bin(instruction[chunk])[2:].zfill(n)
            elif '-' in instruction[chunk]:#to get negative imm binary value
                string += bin((1 << n) + int(instruction[chunk]))[2:]
            elif len(instruction[chunk]) != n  :#to get imm binary value
                string += bin(int(instruction[chunk]))[2:].zfill(n)
            else:
                string += instruction[chunk]
        memory[1].update({PC:string})
        PC += 4
    write_to_files(path, memory)

# # this is for testing
# if __name__ == '__main__':
#     path = r # source code
#     run(path, 4 *1024)
                
    
        

    
    
    

            