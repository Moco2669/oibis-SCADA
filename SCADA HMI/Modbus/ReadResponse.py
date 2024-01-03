import socket

from Modbus.ModbusBase import *
import ctypes
"""
Objekat koji ce primati read odgovore 
"""

class ModbusReadReasponse(ModbusBase):
    def __init__(self,
                 base : ModbusBase,
                 ByteCount : ctypes.c_byte,
                 Data : bytearray ):
        super().__init__(base.UnitID,base.FunctionCode)
        self.ByteCount = ByteCount
        self.Data = Data
    def __str__(self):
        return f"{super().__str__()},ByteCount:{self.ByteCount},Data:{self.Data}"

    def getData(self):
        return self.Data
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

"""
Summary how to repack this message from scada sim 

1. ushort transactionID 
2. ushort protocolID 
3. ushort length 
4. byte unit id 
5. byte function code 
6. byte byteCount 
7. n-bytes data  
"""
def repackReadResponse(bytes : bytearray):
    base = ModbusBase(int.from_bytes(bytes[6:7], byteorder="big", signed=False),
                      int.from_bytes(bytes[7:8], byteorder="big", signed=False))
    readResponse = ModbusReadReasponse(base,int.from_bytes(bytes[8:9],byteorder="big", signed=False),
                                       int.from_bytes(bytes[9:],byteorder="big",signed=False))
    readResponse.setTransactionID(int.from_bytes(bytes[0:2],byteorder="big",signed=False))
    readResponse.setLength(int.from_bytes(bytes[4:6],byteorder="big",signed=False)) # treba da se setuje ne znamo duzinu odgovora [data] == n bytes
    return readResponse
