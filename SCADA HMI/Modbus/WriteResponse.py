from Modbus.ModbusBase import *
import ctypes
"""
Klasa je samo kako bi se razlikovali Request Write i Response za Write sustinski su isti objekti
"""
class ModbusWriteResponse(ModbusBase):
    def __init__(self,
                 base : ModbusBase,
                 RegisterAdress : ctypes.c_ushort,
                 RegisterValue : ctypes.c_ushort):
        super().__init__(base.UnitID,base.FunctionCode)
        self.RegisterAdress = RegisterAdress
        self.RegisterValue  = RegisterValue

    def __str__(self):
        return f"{super().__str__()},RegisterAdress:{self.RegisterAdress},RegisterValue:{self.RegisterValue}"

    def getFunctionCode(self):
        return self.FunctionCode

def repackResponse(bytes : bytearray):
    base = ModbusBase(int.from_bytes(bytes[6:7], byteorder="big", signed=False),
                      int.from_bytes(bytes[7:8], byteorder="big", signed=False))
    base.setTransactionID(int.from_bytes(bytes[0:2],byteorder="big",signed=False))
    writeResponse = ModbusWriteResponse(base,int.from_bytes(bytes[8:10],byteorder="big",signed=False),
                                        int.from_bytes(bytes[10:12],byteorder="big",signed=False))
    return writeResponse