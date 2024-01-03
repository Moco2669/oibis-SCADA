from Modbus.ModbusBase import *
import ctypes
import struct
import socket

"""
startAdress - > sa koje adrese zeli da se procita 
quantity - > sa koliko uzastopnih registara treba da cita 
Primer: start adress 1000 
        quantity 2 
        => citace sa adrese 1000 i 1001 na svakoj adresi je 16bit registar 
"""


class ModbusReadRequest(ModbusBase):
    value = 0
    def __init__(self,
                 base: ModbusBase,
                 StartAddress: ctypes.c_ushort,
                 Quantity: ctypes.c_ushort):
        super().__init__(base.UnitID, base.FunctionCode)
        ModbusReadRequest.value +=1
        self.TransactionID = ModbusReadRequest.value
        if(ModbusReadRequest.value==65535):
            ModbusReadRequest.value = 0
        self.Length += 4 # Start address and quantity is always 4 bytes
        self.StartAddress = StartAddress
        self.Quantity = Quantity
    def __str__(self):
        return f"{super().__str__()},StartAdress:{self.StartAddress},Quantity:{self.Quantity}"
def repack(ReadRequest: ModbusReadRequest) -> bytearray:
    request = bytearray(12)
    request[0:2] = socket.htons(ReadRequest.TransactionID).to_bytes(2, "little")
    request[2:4] = socket.htons(ReadRequest.ProtocolID).to_bytes(2, "little")
    request[4:6] = socket.htons(ReadRequest.Length).to_bytes(2, "little")
    request[6] = int(ReadRequest.UnitID)
    request[7] = int(ReadRequest.FunctionCode)
    request[8:10] = socket.htons(ReadRequest.StartAddress).to_bytes(2, "little")
    request[10:12] = socket.htons(ReadRequest.Quantity).to_bytes(2, "little")
    return request


