import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QWidget,QDesktopWidget
import Connection
from DataBase import *
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from PyQt5.QtGui import QGuiApplication, QFont
from PyQt5.QtCore import Qt, QTimer, QDateTime, QTimeZone,pyqtSignal,QObject
from Connection import *
import socket
from Acquisition import *
import threading
import Connection


class TableExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('SCADA-HMI')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Create a QTableWidget with 5 columns and make it an instance variable
        self.tableWidget = QTableWidget(0, 5)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Type", "Address", "Value", "Alarm"])

        # Make the table non-editable
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(self.tableWidget)

        # Calculate the desired height (70% of screen height) and convert it to an integer

        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        table_height = int(screen_geometry.height() * 0.7)
        self.tableWidget.setGeometry(0, 0, screen_geometry.width(), table_height)

        central_widget.setLayout(layout)

        for col in range(self.tableWidget.columnCount()):
            self.tableWidget.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)

        tuplesForPrint = makeTuplesForPrint(signal_info)
        data = list()
        data.extend(tuplesForPrint)

        for row, item in enumerate(data):
            self.tableWidget.insertRow(row)
            for col, text in enumerate(item):
                self.tableWidget.setItem(row, col, QTableWidgetItem(text))

        self.show()

        # Create a QHBoxLayout to place the "CONNECTED" label and the time label side by side
        hbox = QHBoxLayout()

        # Create the "CONNECTED" label
        self.label = QLabel("CONNECTED")
        self.label1 = QLabel(f"STATE OF SYSTEM:{StateHolder.state}")
        self.label1.setFont(QFont("Helvetica", 10, QFont.Bold))
        self.label.setFont(QFont("Helvetica", 10, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        self.label1.setAlignment(Qt.AlignCenter)
        # Set a fixed height for the label
        self.label.setFixedHeight(30)
        hbox.addWidget(self.label)
        hbox.addWidget(self.label1)

        layout.addLayout(hbox)

        # okida na svake 0.5 sek update tabele
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTable)
        self.timer.start(500)

    def updateTable(self):
        print(StateHolder.state)
        if Connection.ConnectionHandler.isConnected:
            self.label.setStyleSheet("background-color: green;")
        else:
            self.label.setStyleSheet("background-color: red")

        if StateHolder.state in ("COMMAND INJECTION", "REPLAY ATTACK"):
            self.label1.setStyleSheet("background-color: red")
            self.label1.setText(f"STATE OF SYSTEM: {StateHolder.state}")
        else:
            self.label1.setStyleSheet("background-color: green;")
            self.label1.setText(f"STATE OF SYSTEM: {StateHolder.state}")

        tuples = makeTuplesForPrint(signal_info)  # fresh info
        data = list()
        data.extend(tuples)
        self.tableWidget.setRowCount(0)  # brise poslednje podatke
        for row, item in enumerate(data):  # update
            self.tableWidget.insertRow(row)
            for col, text in enumerate(item):
                # self.tableWidget.setItem(row, col, QTableWidgetItem(text))
                item_widget = QTableWidgetItem(text)
                if text == "HIGH ALARM":
                    # Set the text color to red
                    item_widget.setForeground(QColor(255, 0, 0))  # Red color

                    # Set the font to bold
                    font = QFont()
                    font.setBold(True)
                    item_widget.setFont(font)
                    self.tableWidget.setItem(row, col, item_widget)
                elif text == "LOW ALARM":
                    item_widget.setForeground(QColor(255, 0, 0))  # Red color

                    # Set the font to bold
                    font = QFont()
                    font.setBold(True)
                    item_widget.setFont(font)
                    self.tableWidget.setItem(row, col, item_widget)
                else:
                    item_widget.setForeground(QColor(0, 0, 0))
                    font = QFont()
                    font.setBold(False)
                    item_widget.setFont(font)
                    self.tableWidget.setItem(row, col, item_widget)

    def closeEvent(self, event):
        Connection.ConnectionHandler.client.close()


def main():
    app = QApplication(sys.argv)
    ex = TableExample()
    acquisition_thread = threading.Thread(target=Acquisition, args=(base_info, signal_info))
    acquisition_thread.daemon = True  # koristi se za niti koje rade u pozadini
    acquisition_thread.start()
    connect_thr = threading.Thread(target=Connection.connect_thread, args=(base_info, 1))
    connect_thr.daemon = True
    connect_thr.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
