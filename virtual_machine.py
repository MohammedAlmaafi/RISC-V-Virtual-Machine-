import os
from memoryfile import Memory_class
from vbusfile import vbus_class 
from UARTfile import UART_class
from cpufile import CPU
import Assembler
import PySimpleGUI as gui
from sys import argv



def run(source_code, memory_size):
    
    # check for correct input
    if (memory_size % 4) != 0:
        raise("memory size need to be Multiplication of 4\n like 4,8,16 ....")
    
     # 1024 size of 1 killobyte
    memory_size = memory_size * 1024

    # assmble source code
    # output from ammbler will be in NEW folder(child folder) in source code folder
    Assembler.run(source_code, memory_size)
    
    
    Memory    = Memory_class(memory_size) 
    UART      = UART_class(memory_size) # there are extra address for UART after sp(Stack)
    Vbus      = vbus_class(Memory, UART)

    # take refernce of vbus 
    UART.vbus = Vbus

    # load memory usiong generated files from assmbler
    # it takes the source code only for the path
    # to access the folder made by the assmbler (assmbler output)
    Memory.load(source_code)
    
    # make object from CPU 
    RV32 = CPU(Vbus)
    RV32.registers[2] = memory_size # at the end of memeory
    RV32.registers[3] = memory_size // 2 # start of static data

    # pass reference of CPU to Vbus
    Vbus.cpu = RV32

    #########Array############
    temp = Memory.size//2
    string = "Before Sorting:"
    string += "\n\t\t["
    for i in range(8):
        if i == 7:
            string += str(int.from_bytes(Memory.memory[temp:temp+4] ,byteorder='little',signed=False))
        else:
            string += str(int.from_bytes(Memory.memory[temp:temp+4] ,byteorder='little',signed=False)) + ","
        temp +=4
    string += "]"

    temp = Memory.size//2+32
    # print("[",end="")
    string += "\n\t\t["
    for i in range(8):
        if i == 7:
            string += str(int.from_bytes(Memory.memory[temp:temp+4] ,byteorder='little',signed=False))
        else:
            string += str(int.from_bytes(Memory.memory[temp:temp+4] ,byteorder='little',signed=False)) + ","
        temp +=4
    string += "]\n\nThe program output:\n\t\t"
            
    UART.string= string
    while 1:
        RV32.fetch()
        RV32.decode()
        RV32.execute()
    

if __name__ == "__main__":
    # from terimnal 
    # source_code  = argv[1] # take path for source code
    # memory_size  = int(argv[2]) # number of killobytes for the memory (4,8,16,32 .....)


    #################################GUI#################################### 
    gui.theme("TealMono")
    layout = [[gui.Text('\t\tPlease insert your assembly file:')],
    [gui.Text("Choose a file: "),
        gui.Input(key="-IN2-" ,change_submits=True),
        gui.FileBrowse(key="-IN-")],[gui.Button("Submit")]]


    layout2 = [ 
        [gui.Text('\t\t\tPlease enter your Memory Size (x4): ')], 
        [gui.Text('Size', size =(15, 1)), gui.InputText()], 
        [gui.Submit()] 
    ] 
    ###Building Window
    window = gui.Window('Assembly File', layout, size=(600,150))
    window2 = gui.Window('Memory Size', layout2, size=(600,150))
    list = [0,0]
    while 1:
        event, values = window.read()
        window.close()
        if event == gui.WIN_CLOSED or event=="Submit":
            break
        list[0] = values["-IN-"]

        event, values = window2.read()
        window2.close()
        # if event == sg.WIN_CLOSED or event=="Submit":
        #     break
        list[1] = values[0]
    ##########################################################################
    run(list[0], int(list[1]))
    