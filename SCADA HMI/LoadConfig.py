from Modbus.Signal import *
def load_cfg(file_name):
    with open(file_name, 'r') as file:
        file_contents = file.readlines()
    o1,o2 = obradi(file_contents)
    return o1,o2

def obradi(file_contents):
    adresa_stanice = int(file_contents[0].split()[1])
    broj_porta = int(file_contents[1].split()[1])
    delay = int(file_contents[3].split()[1])
    base_info = {"station_address": adresa_stanice, "num_port": broj_porta, "dbc": delay}
    signals = {}
    for vrsta in file_contents[5:]:  # Start from the 5th row
        privremena = vrsta.split()
        reg_type = privremena[0]
        num_registers = int(privremena[1])
        address = int(privremena[2])
        min_value = int(privremena[3])
        max_value = int(privremena[4])
        start_value = int(privremena[5])
        signal_type = privremena[6]
        min_alarm = "NO ALARM" if not(privremena[7].isdigit()) else int(privremena[7])
        max_alarm = "NO ALARM" if not(privremena[8].isdigit()) else int(privremena[8])
        name = privremena[9].split(":")[1]
        signal = Signal(reg_type, num_registers, address, min_value, max_value, start_value, signal_type, min_alarm, max_alarm, name)
        signals[address] = signal
    return base_info, signals
