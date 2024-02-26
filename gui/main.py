import sys
import serial_ui
import threading
import time

import numpy as np

from qthread_serial import Serial_Qthread_function

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtSerialPort import QSerialPortInfo

def toHex(byte_data, split):
    hex_data = ''
    for elem in byte_data:
        hex_data = hex_data + '{:02x}'.format(elem) + split
    
    return hex_data

import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class SerialFrom(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = serial_ui.Ui_Serial()
        self.ui.setupUi(self)

        self.port_name = []
        self.interface_init()
        self.Ui_init()

        print("main thread id:", threading.current_thread().ident)

        self.qthread_init()

        self.start()
        
    def tabchange(self):
        index = self.ui.tabWidget.currentIndex()
        print('index:', index)
        if self.tabWidget.index == 3:
            self.ui.page3.plot_example()
            

    def timeout_scan(self):
        ava_port = QSerialPortInfo.availablePorts()
        new_port = []
        for port in ava_port:
            new_port.append(port.portName())
        
        if len(self.port_name) != len(new_port):
            self.port_name = new_port
            self.ui.comboBox_com.clear()
            self.ui.comboBox_com.addItems(self.port_name)
        
        self.check = ('None', 'Odd', 'Even')


    def interface_init(self):
        self.Baud = ('4800', '9600', '57600', '115200')
        self.stop = ('1', '1.5', '2')
        self.data = ('8', '7', '6', '5')
        self.check = ('None', 'Odd', 'Even')
        self.ui.comboBox_baud.addItems(self.Baud)
        self.ui.comboBox_stopbit.addItems(self.stop)
        self.ui.comboBox_databit.addItems(self.data)
        self.ui.comboBox_checkbit.addItems(self.check)

        self.ui.checkBox_rts.stateChanged.connect(self.checkBox_rts)
        self.ui.checkBox_rtx.stateChanged.connect(self.checkBox_rtx)
        self.ui.checkBox_timestamp.stateChanged.connect(self.checkBox_timestamp)

        self.ui.hex.stateChanged.connect(self.checkBox_hexsend)
        # self.ui.tabWidget.


    def Ui_init(self):
        self.ui.btn_open_serial.clicked.connect(self.pushButton_Open)
        self.ui.btn_send.clicked.connect(self.pushButton_Send)
    

    def qthread_init(self):
        # create a serial collecting thread
        self.serial_qthread = QThread()
        self.serial_qthread_function = Serial_Qthread_function()
        self.serial_qthread_function.moveToThread(self.serial_qthread)
        self.serial_qthread.start()

        # connect serial_init_function(a function) to signal_start_function(a signal)
        self.serial_qthread_function.signal_start_function.connect(self.serial_qthread_function.serial_init_function)
        self.serial_qthread_function.signal_start_function.emit()

        # connect open button to slot function
        self.serial_qthread_function.signal_pushbButton_open.connect(self.serial_qthread_function.slot_pushButton_open)
        self.serial_qthread_function.signal_pushbButton_open_flags.connect(self.slot_pushButton_Open_flags)
        self.serial_qthread_function.signal_readdata.connect(self.slot_readdata)

        self.serial_qthread_function.signal_rts.connect(self.serial_qthread_function.slot_rts)
        self.serial_qthread_function.signal_rtx.connect(self.serial_qthread_function.slot_rtx)
        self.serial_qthread_function.signal_timestamp.connect(self.serial_qthread_function.slot_timestamp)
        self.serial_qthread_function.signal_senddata.connect(self.serial_qthread_function.slot_senddata)


    def start(self):
        self.time_scan = QTimer()
        self.time_scan.timeout.connect(self.timeout_scan)
        self.time_scan.start(1000)


    def pushButton_Open(self):
        print("push button open")
        self.set_parameter = {}
        self.set_parameter['comboBox_com'] = self.ui.comboBox_com.currentText()
        self.set_parameter['comboBox_baud'] = self.ui.comboBox_baud.currentText()
        self.set_parameter['comboBox_stop'] = self.ui.comboBox_stopbit.currentText()
        self.set_parameter['comboBox_data'] = self.ui.comboBox_databit.currentText()
        self.set_parameter['comboBox_check'] = self.ui.comboBox_checkbit.currentText()
        self.serial_qthread_function.signal_pushbButton_open.emit(self.set_parameter)
    
    def pushButton_Send(self):
        print('send data clicked')
        send_data = {}
        send_data['data'] = self.ui.textEdit_send.toPlainText()
        if self.ui.hex.checkState():
            send_data['data'] += '\r\n'
        send_data['hex'] = self.ui.hex.stateChanged
        self.serial_qthread_function.signal_senddata.emit(send_data)


    def slot_pushButton_Open_flags(self, state):
        print("state of serial port", state)
        if state == 0:
            QMessageBox.warning(self, 'warnning tips:', 'serial port can not use')
        elif state == 1:
            self.ui.btn_open_serial.setStyleSheet('color:red')
            self.ui.btn_open_serial.setText('关闭串口')
            self.time_scan.stop()
        
        else:
            self.ui.btn_open_serial.setStyleSheet('color:black')
            self.ui.btn_open_serial.setText('打开串口')
            self.time_scan.start(1000)

    def slot_readdata(self, data):
        # print(data)
        if self.ui.checkBox_timestamp.stateChanged:
            tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.ui.textEdit_recvdata.setTextColor(QColor(255, 100, 100))
            self.ui.textEdit_recvdata.insertPlainText(tm)
            self.ui.textEdit_recvdata.setTextColor(QColor(0, 0, 0))

        byte_data = bytes(data)
        if self.ui.checkBox_hex_show.checkState():
            print("hex view")
            hex_data = toHex(byte_data, ' ')
            self.ui.textEdit_recvdata.insertPlainText(hex_data)
            # print(hex_data)
        else:
            print("dec view")
            self.ui.textEdit_recvdata.insertPlainText(byte_data.decode('utf-8', 'ignore'))
            # print(data)

        self.ui.textEdit_recvdata.moveCursor(QTextCursor.End)

    def checkBox_rts(self, state):
        print('RTS:', state)
        self.serial_qthread_function.signal_rts.emit(state)

    def checkBox_rtx(self, state):
        self.serial_qthread_function.signal_rtx.emit(state)

    def checkBox_timestamp(self, state):
        self.serial_qthread_function.signal_timestamp.emit(state)

    def checkBox_hexsend(self, state):
        if state == 2:
            send_text = self.ui.textEdit_send.toPlainText()
            byte_text = str.encode(send_text)
            hex_data = toHex(byte_text, ' ')
            self.ui.textEdit_send.setText(hex_data)
            print(send_text)
        else:
            send_list = []
            send_text = self.ui.textEdit_send.toPlainText()
            while send_text != '':
                try:
                    num = int(send_text[0:2], 16)
                except:
                    QMessageBox.warning(self, 'warnning', 'input hex data')
                    return
                send_text = send_text[2:].strip()
                send_list.append(num)

            input_s = bytes(send_list)
            self.ui.textEdit_send.setText(input_s.decode())


class MyFigure(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)

    def plotsin(self):
        self.axes0 = self.fig.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.axes0.plot(t, s)

    def plotcos(self):
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.axes.plot(t, s)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(718, 515)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(370, 470, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QWidget(Dialog)
        self.widget.setGeometry(QRect(10, 10, 691, 451))
        self.widget.setObjectName("widget")
        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setGeometry(QRect(0, 0, 691, 451))
        self.groupBox.setObjectName("groupBox")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "GroupBox_Matplotlib的图形显示："))

class MainDialogImgBW(SerialFrom):
    def __init__(self):
        super().__init__()
       

    def show_recv_data(self):
        print("switch recv data page")
        pass

    def show_plt(self):
        self.ui.groupBox.close()
        self.ui.setWindowTitle("显示matplotlib绘制图形")
        self.ui.setMinimumSize(0,0)


        #第五步：定义MyFigure类的一个实例
        self.F = MyFigure(width=3, height=2, dpi=100)
        #self.F.plotsin()
        self.plotcos()
        #第六步：在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。
        self.gridlayout = QGridLayout(self.groupBox)  # 继承容器groupBox
        self.gridlayout.addWidget(self.F,0,1)

        #补充：另创建一个实例绘图并显示
        self.plotother()
        pass

    def plotcos(self):
        t = np.arange(0.0, 5.0, 0.01)
        s = np.cos(2 * np.pi * t)
        self.F.axes.plot(t, s)
        self.F.fig.suptitle("cos")

    def plotother(self):
        F1 = MyFigure(width=5, height=4, dpi=100)
        F1.fig.suptitle("Figuer_4")
        F1.axes1 = F1.fig.add_subplot(221)
        x = np.arange(0, 50)
        y = np.random.rand(50)
        F1.axes1.hist(y, bins=50)
        F1.axes1.plot(x, y)
        F1.axes1.bar(x, y)
        F1.axes1.set_title("hist")
        F1.axes2 = F1.fig.add_subplot(222)

        ## 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y = [23, 21, 32, 13, 3, 132, 13, 3, 1]
        F1.axes2.plot(x, y)
        F1.axes2.set_title("line")
        # 散点图
        F1.axes3 = F1.fig.add_subplot(223)
        F1.axes3.scatter(np.random.rand(20), np.random.rand(20))
        F1.axes3.set_title("scatter")
        # 折线图
        F1.axes4 = F1.fig.add_subplot(224)
        x = np.arange(0, 5, 0.1)
        F1.axes4.plot(x, np.sin(x), x, np.cos(x))
        F1.axes4.set_title("sincos")
        self.gridlayout.addWidget(F1, 0, 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    # MainWindow = QMainWindow()  # 创建主窗口
    # ui = serial_ui.Ui_Serial()
    # ui.setupUi(MainWindow)
    # MainWindow.show()  # 显示主窗口
    
    # main = MainDialogImgBW()
    # main.show()

    w = SerialFrom()
    w.show()
 
    sys.exit(app.exec_())  # 在主线程中退出
