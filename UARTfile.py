class UART_class():
    def __init__(self, address, width = 8):
        self.width = width
        self.byte  = 0 # buffer
        self.byte2 = 0 # buffer
        self.byte3 = 0 # buffer
        self.byte4 = 0 # buffer
        self.vbus  = 0 # object
        self.address = address
        self.length = 0
        self.counter = 0
        self.counter2 = 0
        self.string = ""
        

    def readByte(self):
        
        if self.byte == 0:
            self.byte = chr( self.vbus.readUART(self.counter))
        elif self.byte2 == 0:
            self.byte2 = chr( self.vbus.readUART(self.counter))
        elif self.byte3 == 0:
            self.byte3 = chr( self.vbus.readUART(self.counter))
        else:
            self.byte4 = chr( self.vbus.readUART(self.counter))

        self.counter += 1
          
    def writeIO(self):

        if self.counter2 == 3:
            self.string += self.byte4 + self.byte3 + self.byte2 + self.byte 
            self.counter2 = 0
            self.byte  = 0
            self.byte2 = 0
            self.byte3 = 0
            self.byte4 = 0
        else:
            self.counter2 +=1

       

    def RUN(self):
        self.counter = self.address
        while self.counter <= self.length + self.address  :
            self.readByte()# it terminates the loop when there's a null termintor
            self.writeIO()
            
        