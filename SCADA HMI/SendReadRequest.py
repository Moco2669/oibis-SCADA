import socket
from Modbus.ReadResponse import *
from DataBase import *
from Modbus.ModbusBase import *
from Modbus.ReadRequest import *
from Modbus.Signal import *
import time


def packRequest(base_info, signal_info):

    unitID = base_info["station_address"]
    signals_in_list = list(signal_info.values())
    list_of_request = list()
    for i in range(0, len(signals_in_list)):
        function_code = -1
        match signals_in_list[i].SignalType:
            case "DO":
                function_code = 1
            case "DI":
                function_code = 2
            case "AO":
                function_code = 3
            case "AI":
                function_code = 4
        base = ModbusBase(unitID, function_code)
        request = ModbusReadRequest(base, signals_in_list[i].StartAddress, signals_in_list[i].Num_reg)
        list_of_request.append(repack(request))

    return list_of_request


def ResponseMessage(responseMessage) -> bytearray:
    base = ModbusBase(responseMessage[7], responseMessage[8])
    data = socket.ntohs(responseMessage[9:])
    return ModbusReadReasponse(base, responseMessage[9], data)


def parseResponse(ModbusReadResponse: ModbusReadReasponse, address, signals_info):
    signals_info[address].currentValue(ModbusReadResponse.Data)
