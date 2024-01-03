class Signal():
    def __init__(self, reg_type, num_reg, StartAddress, MinV, MaxV, StartV, SignalType, MinAlarm, MaxAlarm,name):
        self._Reg_type = reg_type
        self._Num_reg = num_reg
        self._StartAddress = StartAddress
        self._MinValue = MinV
        self._MaxValue = MaxV
        self._StartV = StartV
        self._SignalType = SignalType
        self._MinAlarm = MinAlarm
        self._MaxAlarm = MaxAlarm
        self._Name = name
        self._AlarmNow = "NO ALARM"
        self.CurrentValue = StartV
    def AlarmNow(self):
        return self._AlarmNow

    def Modify_Alrm(self,alarm):
        self._AlarmNow = alarm

    def Name(self):
        return self.Name

    def Name(self,name):
        self.Name = name

    def Reg_type(self):
        return self._Reg_type

    def Reg_type(self, value):
        self._Reg_type = value

    def getNum_reg(self):
        return self._Num_reg

    def setNum_reg(self, value):
        self._Num_reg = value

    Num_reg = property(getNum_reg,setNum_reg)

    def getStartAddress(self):
        return self._StartAddress

    def setStartAddress(self, value):
        self._StartAddress = value

    StartAddress = property(getStartAddress,setStartAddress)

    def MinValue(self):
        return self._MinValue

    def MinValue(self, value):
        self._MinValue = value

    def MaxValue(self):
        return self._MaxValue

    def MaxValue(self, value):
        self._MaxValue = value

    def StartV(self):
        return self._StartV

    def StartV(self, value):
        self._StartV = value

    def getSignalType(self):
        return self._SignalType

    def setSignalType(self, value):
        self._SignalType = value

    SignalType = property(getSignalType,setSignalType)

    def getMinAlarm(self):
        return self._MinAlarm

    def setMinAlarm(self, value):
        self._MinAlarm = value

    MinAlarm = property(getMinAlarm,setMinAlarm)
    def getMaxAlarm(self):
        return self._MaxAlarm
    def setMaxAlarm(self, value):
        self._MaxAlarm = value

    MaxAlarm = property(getMaxAlarm,setMaxAlarm)
    def getcurrentValue(self):
        return self.CurrentValue

    def setcurrentValue(self,value):
        self.CurrentValue = value

    currentValue = property(getcurrentValue,setcurrentValue)

    def __str__(self):
        return f"Signal Info: Reg_type: {self._Reg_type},Num_reg: {self._Num_reg},StartAddress: {self._StartAddress},MinValue: {self._MinValue},MaxValue: {self._MaxValue},StartV: {self._StartV},SignalType: {self._SignalType},MinAlarm: {self._MinAlarm},MaxAlarm: {self._MaxAlarm},Name:{self._Name}, CurrentValue:{self.CurrentValue}"
