# audio_check
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

class audio_check(QG.QMainWindow):
    def __init__(self, parent = None):
        super(audio_check, self).__init__(parent)  # superclassのコンストラクタを使用。

        self.resize(300, 600)

        # widget
        self.w0 = QG.QWidget()
        self.setCentralWidget(self.w0)
        self.lbl0 = QG.QLabel('wav')
        self.lbl1 = QG.QLabel('feat')
        self.le0 = QG.QLineEdit()
        self.le1 = QG.QLineEdit()
        self.btn0 = QG.QPushButton('...')
        self.btn0.setFixedWidth(30)
        self.btn1 = QG.QPushButton('...')
        self.btn1.setFixedWidth(30)

        # plot
        self.w_plot = pg.GraphicsWindow()



        # layout
        self.hbox0 = QG.QHBoxLayout()
        self.hbox0.addWidget(self.w_plot)
        self.hbox1 = QG.QHBoxLayout()
        self.hbox1.addWidget(self.lbl0)
        self.hbox1.addWidget(self.le0)
        self.hbox1.addWidget(self.btn0)
        self.hbox2 = QG.QHBoxLayout()
        self.hbox2.addWidget(self.lbl1)
        self.hbox2.addWidget(self.le1)
        self.hbox2.addWidget(self.btn1)
        self.vbox0 = QG.QVBoxLayout()
        self.vbox0.addLayout(self.hbox0)
        self.vbox0.addLayout(self.hbox1)
        self.vbox0.addLayout(self.hbox2)
        self.w0.setLayout(self.vbox0)


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

    ui = audio_check()
    ui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
