import sys
import time
import serial_ui
import threading

import numpy as np

from qthread_serial import Serial_Qthread

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtSerialPort import QSerialPortInfo

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import multiprocessing
import random

matplotlib.use("Qt5Agg")  # 声明使用QT5

def toHex(byte_data, split):
    hex_data = ''
    for elem in byte_data:
        hex_data = hex_data + '{:02x}'.format(elem) + split
    
    return hex_data

import krige_impl


'''
    
'''
import demo
class SerialFrom(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = serial_ui.Ui_Serial_Form()

        self.ui.setupUi(self)

        self.ports = []
        self.counter = 0

        self.qthread_init()
        self.ui_init()
        self.serial_option_init()

        self.start_timer()


    '''
        set basic layout of checkbox
        it include baud ratio, stop bit, data bit, check modle ...
    '''
    def serial_option_init(self):
        baud = ('4800', '9600', '57600', '115200')
        stop = ('1', '1.5', '2')
        data = ('8', '7', '6', '5')
        check = ('None', 'Odd', 'Even')
        frequence = ('5K', '10K', '20K', '50K')
        self.ui.comboBox_baud.addItems(baud)
        self.ui.comboBox_stop.addItems(stop)
        self.ui.comboBox_data.addItems(data)
        self.ui.comboBox_check.addItems(check)
        self.ui.comboBox_freq.addItems(frequence)

        self.ui.checkBox_rts.stateChanged.connect(self.checkBox_rts)
        # self.ui.checkBox_timestamp.stateChanged.connect(self.checkBox_timestamp)

        self.ui.checkBox_send_hex.stateChanged.connect(self.checkBox_hex_send)


    # def serial_btn_connect(self):
        # self.ui.btn_open_serial.clicked.connect(self.open_serial)

        # self.ui.checkBox_rts.stateChanged.connect(self.checkBox_rts)
        # self.ui.checkBox_rtx.stateChanged.connect(self.checkBox_rtx)
        # self.ui.checkBox_timestamp.stateChanged.connect(self.checkBox_timestamp)

        # self.ui.hex.stateChanged.connect(self.checkBox_hexsend)

    def qthread_init(self):
        self.qthread = QThread()
        self.serial_qthread = Serial_Qthread()
        self.serial_qthread.moveToThread(self.qthread)
        self.qthread.start()

        # connect signal and slot
        self.serial_qthread.signal_open_serial.connect(self.serial_qthread.serial_init_port)
        self.serial_qthread.signal_open_serial.emit()

        # connect open button to slot function
        self.serial_qthread.signal_pushbButton_open.connect(self.serial_qthread.slot_pushbButton_open)
        self.serial_qthread.signal_pushbButton_open_flags.connect(self.slot_pushButton_open_flags)
        self.serial_qthread.signal_read_data.connect(self.slot_read_data)

        self.serial_qthread.signal_rts.connect(self.serial_qthread.slot_rts)
        self.serial_qthread.signal_rtx.connect(self.serial_qthread.slot_rtx)
        # self.serial_qthread.signal_timestamp.connect(self.serial_qthread.slot_timestamp)
        self.serial_qthread.signal_send_data.connect(self.serial_qthread.slot_send_data)
        

    def ui_init(self):
        self.ui.btn_open_serial.clicked.connect(self.pushButton_open)
        self.ui.btn_send.clicked.connect(self.pushButton_send)
        self.ui.btn_clear.clicked.connect(self.pushButton_clear_recv)

    '''
        timer will active timeout scan per seconds
        actually, it will scan avaliable ports and update com port list per second
    '''
    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout_scan)
        self.timer.start(1000)

    def checkBox_rts(self, state):
        print("Serial Window: RTS: ", state)
        self.serial_qthread.signal_rts.emit(state)

    def checkBox_rtx(self, state):
        print("Serial Window: RTX: ", state)
        self.serial_qthread.signal_rtx.emit(state)

    def checkBox_hex_send(self, state):
        # hex state
        if state == 2:
            send_text = self.ui.textEdit_send.toPlainText()
            byte_text = str.encode(send_text)
            hex_data = toHex(byte_text, ' ')
            self.ui.textEdit_send.setText(hex_data)
            print('send:', send_text)

        else:
            send_list = []
            send_text = self.ui.textEdit_send.toPlainText()
            while send_text != '':
                try:
                    num = int(send_text[0:2], 16)
                except:
                    QMessageBox.warning(self, 'warning', 'input hex data')
                
                send_text = send_text[2:].strip()
                send_list.append(send_list)
    '''

    '''
    def timeout_scan(self):
        ava_port = QSerialPortInfo.availablePorts()
        new_port = []
        for port in ava_port:
            new_port.append(port.portName())
        
        if len(self.ports) != len(new_port):
            self.ports = new_port
            self.ui.comboBox_com.clear()
            self.ui.comboBox_com.addItems(self.ports)


    '''

    '''
    def pushButton_open(self):
        print("push button open")
        self.set_parameter = {}
        self.set_parameter['comboBox_com'] = self.ui.comboBox_com.currentText()
        self.set_parameter['comboBox_baud'] = self.ui.comboBox_baud.currentText()
        self.set_parameter['comboBox_stop'] = self.ui.comboBox_stop.currentText()
        self.set_parameter['comboBox_data'] = self.ui.comboBox_data.currentText()
        self.set_parameter['comboBox_freq'] = self.ui.comboBox_freq.currentText()
        self.set_parameter['comboBox_check'] = self.ui.comboBox_check.currentText()
       
        self.serial_qthread.signal_pushbButton_open.emit(self.set_parameter)

    def pushButton_clear_recv(self):
        self.ui.textEdit_recv.clear()

    def slot_pushButton_open_flags(self, state):
        print("state of serial port", state)
        if state == 0:
            QMessageBox.warning(self, 'warnning tips:', 'serial port can not use')
        
        elif state == 1:
            self.ui.btn_open_serial.setStyleSheet('color:red')
            self.ui.btn_open_serial.setText('关闭串口')
            self.timer.stop()

        else:
            self.ui.btn_open_serial.setStyleSheet('color:black')
            self.ui.btn_open_serial.setText('打开串口')
            self.timer.start(1000)

    def pushButton_send(self):
        print('send data clicked')
        send_data = {}
        send_data['data'] = self.ui.textEdit_send.toPlainText()
        send_data['hex'] = self.ui.checkBox_hex.stateChanged

        # next line       
        if self.ui.checkBox_hex.checkState():
            send_data['data'] += '\r\n'
 
        self.serial_qthread.signal_send_data.emit(send_data)


    def process_data(self, data):
        self.ui.groupBox_signals.update_image(data)

    def slot_read_data(self, data):
        if self.ui.checkBox_timestamp.checkState():
            tm = time.strftime('%Y-%m-%d %h:%M:%S', time.localtime())
            self.ui.textEdit_recv.setTextColor(QColor(255, 100, 100)) # red
            self.ui.textEdit_recv.insertPlainText(tm)
            self.ui.textEdit_recv.setTextColor(QColor(0, 0, 0))

        # data is float list, can't trans too byte, TODO fIx bug here   
        # byte_data = data.tobyte()
        
        # 2024-01-12: data is numpy array -> str(data)

        '''
            TODO: fork a process to imageing using byte_data         
                  thread is too slow, porcess will be a better choice
        '''
        # shared_matrix = multiprocessing.Array('d', data.flatten(), lock=False)
        # shared_shape = data.shape

        # 创建进程
        # p = multiprocessing.Process(target=self.process_matrix, args=(shared_matrix, shared_shape))
        # p.start()
        # with multiprocessing .Pool(5) as p:
            # p.map(self.ui.groupBox_signals.update_image, data)
        # p = multiprocessing.Process(target=self.ui.groupBox_signals.update_image, args=(data,))
        # p.start()

        # self.ui.groupBox_signals.update_image(data)

        # self.ui.textEdit_recv.clear()

        print('len:', len(data))
        if self.counter % 10 == 0:
            # start_time = time.time()
            print(len(data))
            self.ui.groupBox_signals.update_image(data)
            # end_time = time.time()
            # print("耗时: {:.2f}秒".format(end_time - start_time))
        
        # self.ui.groupBox_slice.plot_example()
        
        rand_data = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        random_integer = random.randint(5, 8)
        for i in range(random_integer):
            rand_data[i] = 1
        self.ui.groupBox_slice.update_image(rand_data)

        # if self.counter % 5 == 0:
        # self.ui.groupBox_slice.plot_data(np.random.randint(0, 256, size=(250, 250), dtype=np.uint8))

        self.counter += 1

        array_str = np.array2string(data)
        self.ui.textEdit_recv.setPlainText(array_str)
        # self.ui.textEdit_recv.moveCursor(QTextCursor.End)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SerialFrom()
    w.show()

    sys.exit(app.exec_())
