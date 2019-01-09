# audio_check_test2
# 音声のグラフを表示する試み

import sys
import PyQt4.QtGui as QG
import PyQt4.QtCore as QC
import wave
import pyaudio
import threading
import numpy as np
import pandas as pd
import pyqtgraph as pg

class MakeGui(QG.QMainWindow):
    def __init__(self, parent = None):
        super(MakeGui, self).__init__(parent)  # superclassのコンストラクタを使用。

        self.count = 0

        self.resize(1000, 500)

        self.w = QG.QWidget(self)
        self.setCentralWidget(self.w)

        self.lbl1 = QG.QLabel('wav')
        self.lbl1.setFixedWidth(30)
        self.lbl2 = QG.QLabel('csv')
        self.lbl2.setFixedWidth(30)

        self.le0 = QG.QLineEdit(self)
        self.le0.setText("hello")
        self.le1 = QG.QLineEdit(self)
        self.le1.setText('../data/test/window_broken.wav')
        self.le2 = QG.QLineEdit(self)
        self.le2.setText('../data/test/window_broken.csv')

        self.btn0 = QG.QPushButton('play')
        self.btn0.clicked.connect(self.thread_play)
        self.btn1 = QG.QPushButton('...')
        self.btn1.setFixedWidth(30)
        self.btn1.clicked.connect(self.get_path_wav)
        self.btn2 = QG.QPushButton('...')
        self.btn2.setFixedWidth(30)
        self.btn2.clicked.connect(self.get_path_csv)

        # pyqtgraph
        self.w_plot = pg.GraphicsWindow()
        self.p0 = self.w_plot.addPlot()
        self.p0.setYRange(-40000,40000)
        self.p0.setXRange(0, 2000000)
        self.plot0 = self.p0.plot(pen=(250, 255, 55, 50))
        self.infline0 = pg.InfiniteLine(pen='r')

        # layout
        self.hbox1 = QG.QHBoxLayout(self)
        self.hbox1.addWidget(self.lbl1)
        self.hbox1.addWidget(self.le1)
        self.hbox1.addWidget(self.btn1)

        self.hbox2 = QG.QHBoxLayout(self)
        self.hbox2.addWidget(self.lbl2)
        self.hbox2.addWidget(self.le2)
        self.hbox2.addWidget(self.btn2)

        self.vbox0 = QG.QVBoxLayout(self)
        self.vbox0.addWidget(self.w_plot)
        self.vbox0.addWidget(self.le0)
        self.vbox0.addLayout(self.hbox1)
        self.vbox0.addLayout(self.hbox2)
        self.vbox0.addWidget(self.btn0)
        self.w.setLayout(self.vbox0)


    def play(self):
        # wav_path = '../data/test/window_broken.wav'
        wav_path = self.le1.text()
        self.wf = wave.open(wav_path, 'rb')
        y = self.wf.readframes(self.wf.getnframes())
        y = np.frombuffer(y, dtype = 'int16')
        self.plot0.setData(y)
        self.p0.addItem(self.infline0)
        self.wf.close()

        self.wf = wave.open(wav_path, 'rb')


        CHUNK = int(1024*4)
        RATE = 44100
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True)

        data = self.wf.readframes(CHUNK)
        while len(data) > 0:
            stream.write(data)
            data = self.wf.readframes(CHUNK)

        stream.close()
        p.terminate()
        self.wf.close()

    def timer(self):
        # csv_path = '../data/test/window_broken.csv'
        csv_path = self.le2.text()
        data = pd.read_csv(csv_path)
        self.data = data['0']

        def change_gui():
            self.le0.setText(str(self.data[self.count]))
            self.infline0.setValue((self.count+1)*44100*0.25)
            if self.data[self.count] == 1:
                self.le0.setStyleSheet("background-color: rgb(255, 0, 0);")
            else :
                self.le0.setStyleSheet('background-color: rgb(255, 255, 255);')
            self.count += 1

        self.timer=QC.QTimer()
        self.timer.timeout.connect(change_gui)
        self.timer.start(250)    #250msごとにupdateを呼び出し

    def thread_play(self):
        self.timer()
        thread_obj2 = threading.Thread(target=self.play)
        thread_obj2.start()


    def get_path_wav(self):
        self.wav_path = QG.QFileDialog.getOpenFileName(self, 'Get Wav File', '/home/')
        self.le1.setText(self.wav_path)

    def get_path_csv(self):
        self.csv_path = QG.QFileDialog.getOpenFileName(self, 'Get CSV File', '/home/')
        self.le1.setText(self.csv_path)



def main():
    app = QG.QApplication(sys.argv)

    ui = MakeGui()
    ui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()