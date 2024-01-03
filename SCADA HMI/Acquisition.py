import socket
import time as t
import numpy as np
from Modbus.ReadResponse import *
from DataBase import *
from Modbus.ModbusBase import *
from Modbus.ReadRequest import *
from Modbus.Signal import *
from Modbus.WriteRequest import *
from Modbus.WriteResponse import *
from SendReadRequest import *
from Modbus.ReadResponse import *
import threading
from AutomationManager import *
import Connection
import pandas as pd
from mlModel import *
controlRodsList = list()
waterThermometerList = list()
predictionList = list()
counter = 0
xgboostModel = loadModel()
systemStateCounter = 0
systemStatePrevious = list()


class StateHolder(object):
    state = "NORMAL STATE"


def findAddres(repackRequest):
    address = int.from_bytes(repackRequest[8:10], byteorder="big", signed=False)
    return address

def Acquisition(base_info, signal_info):
    global controlRodsList
    global waterThermometerList
    global counter
    global predictionList
    global systemStateCounter
    global systemStatePrevious
    while True:
        pack_request = packRequest(base_info, signal_info)
        for message in pack_request:
            address = findAddres(message)
            functionCode = int.from_bytes(message[7:8], byteorder="big", signed=False)
            with Connection.ConnectionHandler.connection_lock:
                try:
                    Connection.ConnectionHandler.client.send(message)
                    response = Connection.ConnectionHandler.client.recv(1024)
                except:
                    Connection.ConnectionHandler.isConnected = False
                    Connection.ConnectionHandler.lostConnection.notify_all()
                    Connection.ConnectionHandler.connected.wait()
                    continue
            op = eOperation(response, functionCode)
            if op == False:
                modbusresponse = repackReadResponse(response)
                signal_info[address].setcurrentValue(modbusresponse.getData())

        #ovde se pozivao log
        #dataForCSV(signal_info)

        takeValuesForPredict(signal_info)
        if len(predictionList) == 6:
            pred = xgboostModel.predict(np.array(predictionList).reshape(1, 6))
            systemStatePrevious.append(pred) # dodacu predikciju da proveravam
            systemStateCounter += 1
            predictionList.clear()
        if systemStateCounter == 2 and np.all(systemStatePrevious[0] == systemStatePrevious[1]):
            if systemStatePrevious[0][0][0] == 1:
                StateHolder.state = "REPLAY ATTACK"
            elif systemStatePrevious[0][0][1] == 1:
                StateHolder.state = "COMMAND INJECTION"
            elif systemStatePrevious[0][0][2] == 1:
                StateHolder.state = "NORMAL STATE"
            else:
                StateHolder.state = "FINDING STATE"
            systemStatePrevious.clear()
            systemStateCounter = 0
        elif systemStateCounter == 2 and np.any(systemStatePrevious[0] != systemStatePrevious[1]):
            systemStatePrevious.clear()
            systemStateCounter = 0

        Automation(signal_info, base_info)
        t.sleep(1)


"""
Uzima poslednje 3 vrednosti za prediktovanje 
"""


def takeValuesForPredict(signal_info:dict):
    global counter
    global controlRodsList
    global waterThermometerList
    global predictionList
    if counter != 3:
        for key,value in signal_info.items():
            match signal_info[key].getSignalType():
                case "DO":
                    controlRodsList.append(signal_info[key].getcurrentValue())
                case "AI":
                    waterThermometerList.append(signal_info[key].getcurrentValue())
        counter+=1
    else:
        counter = 0
        predictionList.extend(waterThermometerList)
        predictionList.extend(controlRodsList)
        waterThermometerList.clear()
        controlRodsList.clear()



"""
Korisceno kako bi se skupljali podaci za treniranje 
"""
def dataForCSV(signal_info : dict):
    global counter
    global controlRodsList
    global waterThermometerList
    if counter != 3:
        for key,value in signal_info.items():
            match signal_info[key].getSignalType():
                case "DO":
                    controlRodsList.append(signal_info[key].getcurrentValue())
                case "AI":
                    waterThermometerList.append(signal_info[key].getcurrentValue())
        counter+=1
    else:
        counter = 0
        # Read existing CSV file if it exists
        try:
            df = pd.read_csv('learningDataNew.csv')
        except FileNotFoundError:
            # If the file doesn't exist, create a new DataFrame with the updated header
            columns = [
                'WT_VALUE01', 'WT_VALUE02', 'WT_VALUE03',
                'CR_VALUE01', 'CR_VALUE02', 'CR_VALUE03',
                'REPLAY_ATTACK', 'COMMAND_INJECTION', 'NORMAL_STATE'
            ]
            df = pd.DataFrame(columns=columns)

        new_row = {
            'WT_VALUE01': int(waterThermometerList[0]),
            'WT_VALUE02': int(waterThermometerList[1]),
            'WT_VALUE03': int(waterThermometerList[2]),
            'CR_VALUE01': int(controlRodsList[0]),
            'CR_VALUE02': int(controlRodsList[1]),
            'CR_VALUE03': int(controlRodsList[2]),
            'REPLAY_ATTACK': 0,  # Replace with the actual values
            'COMMAND_INJECTION': 0,  # Replace with the actual values
            'NORMAL_STATE': 1  # Replace with the actual values
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Convert relevant columns to integers
        int_columns = ['WT_VALUE01', 'WT_VALUE02', 'WT_VALUE03','CR_VALUE01', 'CR_VALUE02', 'CR_VALUE03']
        df[int_columns] = df[int_columns].astype(int)

        # Write the updated DataFrame back to the CSV file
        df.to_csv('learningDataNew.csv', index=False)

        controlRodsList.clear()
        waterThermometerList.clear()
