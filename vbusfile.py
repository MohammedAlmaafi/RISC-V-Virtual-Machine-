class vbus_class():
    # width is 32-bit
    def __init__(self,memory, UART, width = 32):
        self.width  = width
        self.cpu = 0
        self.memory = memory
        self.UART = UART


    def readMEM(self, address):
        return self.memory.read(address)

    def writeMEM(self, address, value):
        self.memory.write(address, value)

    def readUART(self, address):
        return self.memory.readByte(address)

    def readData(self, address):
        return self.memory.readData(address)

    def writeData(self, address ,  data):
        self.memory.writeData(address, data)