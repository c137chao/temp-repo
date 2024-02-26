import sys
import serial_ui
import threading
from time import sleep

from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal, QObject 
from PyQt5.QtSerialPort import (
    QSerialPortInfo,
    QSerialPort,
)

class Serial_Qthread_function(QObject):

    signal_start_function = pyqtSignal()
    signal_readdata = pyqtSignal(object)
    signal_rts = pyqtSignal(object)
    signal_rtx = pyqtSignal(object)
    signal_timestamp = pyqtSignal(object)
    signal_senddata = pyqtSignal(object)

    signal_pushbButton_open = pyqtSignal(object)
    signal_pushbButton_open_flags = pyqtSignal(object)

    def __init__(self, parent=None):
        super(Serial_Qthread_function, self).__init__(parent)
        print("init thread id:", threading.currentThread().ident)
        self.state = 0 # 0 未打开, 1 打开， 2 占用/错误

    def slot_pushButton_open(self, parameter):
        if self.state == 0:
            print('press button:', parameter)
            self.serial.setPortName(parameter['comboBox_com'])
            self.serial.setBaudRate(int(parameter['comboBox_baud']))
            if parameter['comboBox_stop'] == '1.5':
                self.serial.setStopBits(3)
            else:
                self.serial.setStopBits(int(parameter['comboBox_stop']))

            self.serial.setDataBits(int(parameter['comboBox_data']))

            setParity = 0
            if parameter['comboBox_check'] == 'Odd':
                setParity = 3
            elif parameter['comboBox_check'] == 'Even':
                setParity = 2
            self.serial.setParity(setParity)
              
            if self.serial.open(QSerialPort.ReadWrite) == True:
                print('open serial success')
                self.state = 1
                self.signal_pushbButton_open_flags.emit(self.state)
            else:
                print("port is int using")
                self.signal_pushbButton_open_flags.emit(0)
        else:
            self.state = 0
            self.serial.close()
            self.signal_pushbButton_open_flags.emit(2)

    def slot_rts(self, state):
        send = False
        if state == 2:
            send = True
        self.serial.setDataTerminalReady(send) 
    
    def slot_rtx(self, state):
        terminal = False
        if state == 2:
            terminal = True
        self.serial.setDataTerminalReady(terminal)


    def slot_timestamp(self, state):
        pass

    def slot_senddata(self, send_data):
        print('send data', send_data)
        if self.state != 1:
            return
        if send_data['hex'] == 2:
            send_list = []
            send_text = self.ui.textEdit_send.toPlainText()
            while send_text != '':
                try:
                    num = int(send_text[0:2], 16)
                except:
                    QMessageBox.warning(self, 'warning', 'please input hex data')
                    return

                send_text = send_text[2:].strip()
                send_list.append(num)

            input_s = bytes(send_list)
            self.serial.write(input_s)

        else:
            byte_data = str.encode(send_data['data'])
            self.serial.write(byte_data)


    def serial_receive_data(self):
        # print("recv thread id:", threading.current_thread().ident)
        # print(self.serial.readAll())
        self.signal_readdata.emit(self.serial.readAll())


    def serial_init_function(self):
        print("running thread id:", threading.currentThread().ident)
        self.serial = QSerialPort()
        self.serial.readyRead.connect(self.serial_receive_data)