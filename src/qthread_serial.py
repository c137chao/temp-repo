import threading

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort

import numpy as np



buf_cmd_50k = b'\x00\xFD\xFD\xFD\00\xCB\x00\x14\x00\x00\xFE\xFE\xFE\xFE'
# 指令，用于将采样频率设置为20k
buf_cmd_20k = b'\x00\xFD\xFD\xFD\00\xCB\x00\x32\x00\x00\xFE\xFE\xFE\xFE'
# 指令，用于将采样频率设置为10k
buf_cmd_10k = b'\x00\xFD\xFD\xFD\00\xCB\x00\x64\x00\x00\xFE\xFE\xFE\xFE'

buf_cmd_5k = b'\x00\xFD\xFD\xFD\00\xCB\x00\xC8\x00\x00\xFE\xFE\xFE\xFE'

buf_cmd_4k = b'\x00\xFD\xFD\xFD\00\xCB\x00\xFa\x00\x00\xFE\xFE\xFE\xFE'


offset = 4

def get_s16(val):
    if val < 0x8000:
        return val
    else:
        return val - 0x10000

'''

'''
class Serial_Qthread(QObject):
    signal_open_serial = pyqtSignal()
  
    signal_rts = pyqtSignal(object)
    signal_rtx = pyqtSignal(object)
    signal_timestamp = pyqtSignal(object)

    signal_read_data = pyqtSignal(object)
    signal_send_data = pyqtSignal(object)

    signal_pushbButton_open = pyqtSignal(object)
    signal_pushbButton_open_flags = pyqtSignal(object)

    def __init__(self, parent=None):
        super(Serial_Qthread, self).__init__(parent)
        print("init thread id:", threading.currentThread().ident)
        '''
            state: 0 is unopen, 1 is opened, 2 is occupied or error
        '''
        self.cmd = {'5K':buf_cmd_5k, '10K':buf_cmd_10k, '20K':buf_cmd_20k, '50K':buf_cmd_50k}
        self.state = 0 
        self.first_read_14 = True
        self.buffer = b""

        self.count = 0 # help for debug

    '''
        signal read data will be emit when receive data, more details in serial window
    '''
    def decode_frame(self, frame):
        result = np.zeros(len(frame)>>1)
        for i in range(len(frame)//2):
            result[i] = (get_s16((frame[i*2 + 1] << 8) + frame[2*i]) * 10 / (
                            1 << 16 -1))

        # result = np.zeros((len(frame)>>5, 16), dtype=float)
        # for i in range(len(frame)//2):
        #     result[i >> 4, i & 0xf] = (get_s16((frame[i*2 + 1] << 8) + frame[2*i]) * 5 / (
        #                     1 << 16))

        return result
    
    def test_frequence(self):
        if self.count % 1000 == 0:
            print(self.count)
        
        self.count += 1
            
    def serial_recv_data(self):
        data = self.serial.read(1924)

        if len(data) != 1924:
            return
        
        # self.test_frequence()

        self.buffer = self.buffer + data[offset:]
        if len(self.buffer) < 19200:
            return
       
        # print('buffer length:', len(self.buffer))
        decode_data = self.decode_frame(self.buffer)
        self.buffer = b'' 
        # print("recv data:", decode_data)
        self.signal_read_data.emit(decode_data)

    '''
        
    '''
    def serial_init_port(self):
        print("running thread id:", threading.currentThread().ident)
        self.serial = QSerialPort()
        self.serial.setReadBufferSize(1024*1024*128)
        self.serial.readyRead.connect(self.serial_recv_data)

    '''
    '''
    def slot_pushbButton_open(self, parameter):
        if self.state == 0: # normal case
            print('press button open, parameter:', parameter)
            # set port (such as COM3)
            self.serial.setPortName(parameter['comboBox_com'])
            # set baud ratio
            self.serial.setBaudRate(int(parameter['comboBox_baud']))

            if parameter['comboBox_stop'] == '1.5':
                self.serial.setStopBits(3)
            else:
                self.serial.setStopBits(int(parameter['comboBox_stop']))

            # set data bit 1~8 bit
            self.serial.setDataBits(int(parameter['comboBox_data']))

            # set check bit, odd or even
            setParity = 0
            if parameter['comboBox_check'] == 'Odd':
                setParity = 3
            elif parameter['comboBox_check'] == 'Even':
                setParity = 2
            self.serial.setParity(setParity)

            
            # state 
            if self.serial.open(QSerialPort.ReadWrite) == True:
                print('open serial success')
                self.state = 1

                '''
                    add: select frequence
                '''
                freq = parameter['comboBox_freq']
                self.serial.write(self.cmd[freq])
 
                first = self.serial.read(14)
                print('first:', first, ', len:', len(first))

                self.signal_pushbButton_open_flags.emit(self.state)

            else:
                print("port is int using")
                self.signal_pushbButton_open_flags.emit(0)


        else: # wrong case
            self.state = 0
            self.serial.close()
            self.signal_pushbButton_open_flags.emit(2)

    # require to send
    def slot_rts(self, state):
        send = False if state != 2 else True
        self.serial.setDataTerminalReady(send)

    # require to 
    def slot_rtx(self, state):
        terminal = False if state != 2 else  True
        self.serial.setDataTerminalReady(terminal)

    # send data to com
    def slot_send_data(self, send_data):
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
