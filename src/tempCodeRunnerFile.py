d.connect(self.checkBox_hex_send)


    def qthread_init(self):
        self.qthread = QThread()
        self.serial_qthread = Serial_Qthread()
        self.serial_qthread.moveToThread(self.qthread)
        self.qthread.start()

        # connect signal and slot