import pydivert
from fileFormatString import  *
"""
Imamo source port onoga ko je slao paket na DstPort 25252 
Na osnovu toga trazimo pakete koji idu na taj port i koji su duzine 11 zbog samog formata Modbus poruke
Ti pobaci se cuvaju u data.txt
"""


def sniffPackageForReplayAttack(sourcePort, num_of_packets):
    reWriteFile()  # fajl se re writeuje svaki put kad se pokrene
    current_packet = 0
    with pydivert.WinDivert(f"tcp.DstPort == {sourcePort} and tcp.PayloadLength == 11") as w:
        for packet in w:
            dicForSave = ForFileAnalitics(packet.payload)  # pravi se dic od paketa
            result = modbusBaseAnalitics(dicForSave)
            saveOldData(result)
            w.send(packet)
            current_packet = current_packet + 1
            print(current_packet)
            if current_packet >= num_of_packets:
                return
