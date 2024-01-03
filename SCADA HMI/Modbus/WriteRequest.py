from Modbus.ModbusBase import *
import ctypes
import socket
"""Objekat koji se salje da bi se upisalo nesto
    RegisterAdress - > adresa registra na koji se upisuje vrednost 
    RegisterValue - > vrednost koja se upisuje u taj registar 
    Akko se uspesno izvrsi upravljanje u WriteResponse ce doci povratna poruka koja je ista kao poslata(WriteRequest)
"""


class ModbusWriteRequest(ModbusBase):
    value = 0
    def __init__(self,
                 base: ModbusBase,
                 RegisterAdress: ctypes.c_ushort,
                 RegisterValue: ctypes.c_ushort):
        super().__init__(base.UnitID, base.FunctionCode)
        ModbusWriteRequest.value +=1
        self.Length += 4 # zato sto je su registerAddres && register value fiksno 4 bajta
        self.TransactionID = ModbusWriteRequest.value
        self.RegisterAdress = RegisterAdress
        self.RegisterValue = RegisterValue
    def __str__(self):
        return f"{super().__str__()},RegisterAdress:{self.RegisterAdress},RegisterValue:{self.RegisterValue}"

def repackWrite(write : ModbusWriteRequest,newValue : ctypes.c_ushort):
    message = bytearray(12)
    message[0:2] = socket.htons(write.TransactionID).to_bytes(2,"little")
    message[2:4] = socket.htons(write.ProtocolID).to_bytes(2,"little")
    message[4:6] = socket.htons(write.Length).to_bytes(2,"little")
    message[6] = write.UnitID
    message[7] = write.FunctionCode
    message[8:10] = socket.htons(write.RegisterAdress).to_bytes(2,"little")
    message[10:12] = socket.htons(newValue).to_bytes(2,"little") # new value
    return message
