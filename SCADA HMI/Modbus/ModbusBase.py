import ctypes
import socket

"""
Svaka klasa u okviru protokola sadrzi ovaj deo.
Request za read,write
Response na odredjeni read,write 
TransactionID - > broj transakcije 
ProtocolID ->  0 uvek za Modbus 
Length - > 
unitID - > ID slave-a(postrojenja) kojem saljemo poruku 
functionCode - >Procitaj digitalni izlaz 0x01  
                Procitaj digitalni input 0x02 
                Procitaj analogni output 0x03 
                Procitaj analogni input 0x04 
                Upisi digitalnu vrednost 0x05 
                Upisi analognu vrednost 0x06 
                Length -> unit byte + function code + remaining data 
"""

class ModbusBase:
    def __init__(self,
                 UnitID:ctypes.c_byte,
                 FunctionCode:ctypes.c_byte):
        self.TransactionID = 0 #ushort
        self.ProtocolID = 0 #ushort
        self.Length = 2 #ushort
        self.UnitID = UnitID
        self.FunctionCode = FunctionCode
    def __str__(self):
        return f"TransactionID:{self.TransactionID},ProtocolID:{self.ProtocolID},Length:{self.Length},UnitID:{self.UnitID},FunctionCode:{self.FunctionCode}"


    def setTransactionID(self, value):
        self.TransactionID = value


    def setProtocolID(self, value):
        self.ProtocolID = value


    def setLength(self, value):
        self.Length = value


    def setUnitID(self, value):
        self.UnitID = value

    def setFunctionCode(self, value):
        self.FunctionCode = value