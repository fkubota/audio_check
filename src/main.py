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
import pickle
import pygame
import time

class audio_check(QG.QMainWindow):
    def __init__(self, parent = None):
        super(audio_check, self).__init__(parent)  # superclassのコンストラクタを使用。

        self.resize(600, 600)

        # widget
        self.w0 = QG.QWidget()
        self.setCentralWidget(self.w0)
        self.lbl0 = QG.QLabel('wav')
        self.lbl1 = QG.QLabel('feat')
        self.le0 = QG.QLineEdit()
        self.le1 = QG.QLineEdit()
        self.btn0 = QG.QPushButton('...')
        self.btn0.setFixedWidth(30)
        self.btn0.clicked.connect(self.get_path_wav)
        self.btn1 = QG.QPushButton('...')
        self.btn1.setFixedWidth(30)
        self.btn1.clicked.connect(self.get_path_feat)
        self.btn_play = QG.QPushButton('Play')
        self.btn_play.clicked.connect(self.thread)
        self.scroll = QG.QScrollArea()

        # graph_wav
        self.w_plot_wav = pg.GraphicsWindow()
        self.w_plot_wav.setFixedHeight(200)
        self.w_plot_wav.setBackground('#FFFFFF00')
        self.p_wav = self.w_plot_wav.addPlot()
        self.p_wav.setLabel('bottom', 'Time', 'hour')
        self.p_wav.showGrid(x=True, y=True, alpha=0.7)
        self.curve_wav = self.p_wav.plot(pen=(255, 0, 0, 50))
        self.infline_wav = pg.InfiniteLine(pen=(0, 0, 0), movable=True, hoverPen=(0, 0, 255))
        self.p_wav.addItem(self.infline_wav)
        self.p_wav.setYRange(-40000,40000)
        self.p_wav.setXRange(0, 2000000)


        # graph_feat
        self.w_plot_feat = pg.GraphicsWindow()
        self.w_plot_feat.resize(1000, 6000)
        self.w_plot_feat.setBackground('#FFFFFF00')
        self.p_featV = []
        self.curve_featV = []
        self.infline_featV = []
        for idx in range(34):
            self.p_featV.append(self.w_plot_feat.addPlot())
            self.p_featV[idx].setLabel('bottom', 'Time', 'hour')
            self.p_featV[idx].showGrid(x=True, y=True, alpha=0.7)
            self.p_featV[idx].setXRange(0, 200)
            self.curve_featV.append(self.p_featV[idx].plot(pen=(255, 0, 0, 100)))
            self.infline_featV.append(pg.InfiniteLine(pen=(0, 0, 0), movable=True, hoverPen=(0, 0, 255)))
            self.p_featV[idx].addItem(self.infline_featV[idx])
            self.w_plot_feat.nextRow()

        # self.p_feat = self.w_plot_feat.addPlot()
        # self.p_feat.setLabel('bottom', 'Time', 'hour')
        # self.p_feat.showGrid(x=True, y=True, alpha=0.7)
        # self.curve_feat = self.p_feat.plot(pen=(255, 0, 0, 50))
        # self.infline_feat = pg.InfiniteLine(pen=(0, 0, 0), movable=True, hoverPen=(0, 0, 255))
        # self.p_feat.addItem(self.infline_feat)
        # self.p_feat.setYRange(-40000,40000)
        # self.p_feat.setXRange(0, 2000000)
        self.scroll.setWidget(self.w_plot_feat)
        self.hbox_plot_feat = QG.QHBoxLayout()
        self.hbox_plot_feat.addWidget(self.scroll)



        # layout
        self.hbox0 = QG.QHBoxLayout()
        self.hbox0.addWidget(self.w_plot_wav)
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
        self.vbox0.addLayout(self.hbox_plot_feat)
        self.vbox0.addLayout(self.hbox1)
        self.vbox0.addLayout(self.hbox2)
        self.vbox0.addWidget(self.btn_play)
        self.w0.setLayout(self.vbox0)


        self.get_path_wav()
        self.get_path_feat()


    def play(self):
        filename = self.wav_path

        pygame.mixer.init()
        pygame.mixer.music.load(filename) #音源を読み込み
        # mp3_length = mp3(filename).info.length #音源の長さ取得
        pygame.mixer.music.play(1) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
        # time.sleep(mp3_length + 0.25) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
        # time.sleep(5)
        # pygame.mixer.music.stop() #音源の長さ待ったら再生停止


    def timer(self):
        self.time = 0
        self.a = time.time()
        def change_infline():
            self.infline_wav.setPos(self.time*44100/4)
            for idx in range(34):
                self.infline_featV[idx].setPos(self.time)

            self.time += 1
            self.now = time.time()- self.a
            print(self.now)


        self.timer = QC.QTimer()
        self.timer.timeout.connect(change_infline)
        self.timer.start(250)  # 250 ms 毎


    def thread(self):
        self.timer()
        thread_obj2 = threading.Thread(target=self.play)
        thread_obj2.start()


    def get_path_wav(self):
        # self.wav_path = QG.QFileDialog.getOpenFileName(self, 'Get Wav File', '/home/')
        self.wav_path = '../data/test/window_broken.wav'
        self.le0.setText(self.wav_path)

        self.wav_file = wave.open(self.wav_path, 'rb')
        y = self.wav_file.readframes(self.wav_file.getnframes())
        y = np.frombuffer(y, dtype='int16')
        # y = np.frombuffer(y, dtype='float16')
        self.curve_wav.setData(y)



    def get_path_feat(self):
        # self.feat_path = QG.QFileDialog.getOpenFileName(self, 'Get Feature File', '/home/')
        self.feat_path = '../data/sample.pkl'
        self.le1.setText(self.feat_path)
        with open(self.feat_path, mode='rb') as f:
            self.feat = pickle.load(f)
        try:
            self.feat = self.feat['data']
        except:
            pass

        for idx in range(10):
            self.curve_featV[idx].setData(self.feat[:, idx])


def main():
    app = QG.QApplication(sys.argv)

    ui = audio_check()
    ui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
