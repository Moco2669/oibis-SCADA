import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QLineEdit
import threading

import pydivert
import re
import random
from fileFormatString import *
from grabPort import *
from sniff import *
import time as t
from replayAttack import *
from commandInjection import *
import threadManagement


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 100, 320, 240)
        self.setWindowTitle("SCADA Attacker")
        self.btnSniff = QPushButton(self)
        self.numOfPackets = QLineEdit(self)
        self.btnReplayAttack = QPushButton(self)
        self.btnStopReplay = QPushButton(self)
        self.btnCommandInjection = QPushButton(self)
        self.btnStopInjection = QPushButton(self)
        self.labelStatus = QLabel(self)
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.central_widget)

        self.btnSniff.setText("Perform Sniffing")
        self.btnReplayAttack.setText("Replay Attack")
        self.btnStopReplay.setText("Stop Replay Attack")
        self.btnCommandInjection.setText("Command Injection")
        self.btnStopInjection.setText("Stop Command Injection")

        self.labelStatus.setText("Enter the amount of packets you want to sniff:")

        self.btnStopReplay.setEnabled(False)
        self.btnStopInjection.setEnabled(False)

        self.btnSniff.clicked.connect(self.sniff_action)
        self.btnReplayAttack.clicked.connect(self.replay_attack_action)
        self.btnStopReplay.clicked.connect(self.stop_replay)
        self.btnCommandInjection.clicked.connect(self.command_injection_action)
        self.btnStopInjection.clicked.connect(self.stop_injection)

        self.layout.addWidget(self.labelStatus)
        self.layout.addWidget(self.numOfPackets)
        self.layout.addWidget(self.btnSniff)
        self.layout.addWidget(self.btnReplayAttack)
        self.layout.addWidget(self.btnStopReplay)
        self.layout.addWidget(self.btnCommandInjection)
        self.layout.addWidget(self.btnStopInjection)

        self.central_widget.setLayout(self.layout)

    def sniff_action(self):
        sniff_thread = threading.Thread(target=self.sniff_thread)
        sniff_thread.daemon = True
        sniff_thread.start()

    def sniff_thread(self):
        try:
            num_of_packets = int(self.numOfPackets.text())
        except ValueError:
            return
        self.btnSniff.setEnabled(False)
        self.btnSniff.setText("Performing Packet Sniffing...")
        source_port = grabSourcePort()
        sniffPackageForReplayAttack(source_port, num_of_packets)
        self.btnSniff.setText("Perform Sniffing")
        self.btnSniff.setEnabled(True)

    def replay_attack_action(self):
        rattack_thread = threading.Thread(target=self.replay_attack_thread)
        rattack_thread.daemon = True
        rattack_thread.start()

    def replay_attack_thread(self):
        self.btnReplayAttack.setEnabled(False)
        self.btnReplayAttack.setText("Performing Replay Attack...")
        self.btnStopReplay.setEnabled(True)
        with threadManagement.ThreadManagement.replayLock:
            threadManagement.ThreadManagement.stopReplay = False
        replayAttack(grabSourcePort(), fileInject)
        self.btnReplayAttack.setEnabled(True)
        self.btnReplayAttack.setText("Replay Attack")
        self.btnStopReplay.setEnabled(False)

    def stop_replay(self):
        with threadManagement.ThreadManagement.replayLock:
            threadManagement.ThreadManagement.stopReplay = True

    def command_injection_action(self):
        cinjection_thread = threading.Thread(target=self.command_injection_thread)
        cinjection_thread.daemon = True
        cinjection_thread.start()

    def command_injection_thread(self):
        self.btnCommandInjection.setEnabled(False)
        self.btnCommandInjection.setText("Performing Command Injection...")
        self.btnStopInjection.setEnabled(True)
        with threadManagement.ThreadManagement.injectionLock:
            threadManagement.ThreadManagement.stopInject = False
        comandInjection(grabSourcePort())
        self.btnCommandInjection.setEnabled(True)
        self.btnCommandInjection.setText("Command Injection")
        self.btnStopInjection.setEnabled(False)

    def stop_injection(self):
        with threadManagement.ThreadManagement.injectionLock:
            threadManagement.ThreadManagement.stopInject = True

    """def grabSourcePortAction(self):
        sourcePort = grabSourcePort()"""


if __name__ == "__main__":
    fileInject = loadMessagesForAttack()
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

