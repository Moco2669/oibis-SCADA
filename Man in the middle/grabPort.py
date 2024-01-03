import pydivert

"""
Proverava da li je dest port od paketa 25252 
Ako je source != 0 vratice source port od onoga ko salje na port 25252 
"""


def grabSourcePort():
    with pydivert.WinDivert("tcp.DstPort == 25252") as w:
        for packet in w:
            return packet.src_port
