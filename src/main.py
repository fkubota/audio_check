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
# region
import time
import pydub
import os
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_path + '/../'))

class audio_check(QG.QMainWindow):
    def __init__(self, parent = None):
        super(audio_check, self).__init__(parent)  # superclassのコンストラクタを使用。

        self.resize(600, 600)

        self.isStop = 1
        self.infline_pos = 0
        self.p_featV = []
        self.curve_featV = []
        self.infline_featV = []
        self.region_wavV = []
        self.region_id = -1

        # toolbar
        self.add_region_wav = QG.QAction(QG.QIcon(script_path+'/../icon_file/plus_icon2.png'),
                                     'resion', self)
        self.add_region_wav.triggered.connect(self.show_region)
        self.toolber = self.addToolBar('')
        self.toolber.addAction(self.add_region_wav)

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
        self.btn_play_stop = QG.QPushButton('Play')
        self.btn_play_stop.clicked.connect(self.thread)
        self.scroll = QG.QScrollArea()

        # graph_wav
        self.w_plot_wav = pg.GraphicsWindow()
        self.w_plot_wav.setFixedHeight(200)
        self.w_plot_wav.setBackground('#FFFFFF00')
        self.p_wav = self.w_plot_wav.addPlot()
        self.p_wav.setLabel('bottom', 'Time', 'sec')
        self.p_wav.showGrid(x=True, y=True, alpha=0.7)
        self.curve_wav = self.p_wav.plot(pen=(255, 0, 0, 50))
        self.infline_wav = pg.InfiniteLine(pen=(0, 0, 0), movable=True, hoverPen=(0, 0, 255))
        self.infline_wav.sigPositionChangeFinished.connect(self.infline_changed)
        self.p_wav.addItem(self.infline_wav)


        # graph_feat
        self.w_plot_feat = pg.GraphicsWindow()
        self.w_plot_feat.resize(1000, 6000)
        self.w_plot_feat.setBackground('#FFFFFF00')
        for idx in range(34):
            self.p_featV.append(self.w_plot_feat.addPlot())
            self.p_featV[idx].setLabel('bottom', 'Time', 'sec')
            self.p_featV[idx].showGrid(x=True, y=True, alpha=0.7)
            # self.p_featV[idx].setXRange(0, 200)
            self.curve_featV.append(self.p_featV[idx].plot(pen=(255, 0, 0, 100)))
            self.curve_featV[idx].id = idx
            self.infline_featV.append(pg.InfiniteLine(pen=(0, 0, 0), movable=True, hoverPen=(0, 0, 255)))
            self.infline_featV[idx].sigPositionChangeFinished.connect(self.infline_changed)
            self.p_featV[idx].addItem(self.infline_featV[idx])

            #region
            self.p_featV[idx].region_featV = []

            self.w_plot_feat.nextRow()

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
        self.vbox0.addWidget(self.btn_play_stop)
        self.w0.setLayout(self.vbox0)


        # self.get_path_wav()
        # self.get_path_feat()
        self.timer()
        # thread_obj2 = threading.Thread(target=self.play)
        # thread_obj2.start()


    def play(self):
        self.btn_play_stop.setEnabled(False)
        self.btn_play_stop.setText('loading')
        filename_wav = self.wav_path
        dir = os.path.dirname(filename_wav)
        base_name = os.path.basename(filename_wav).split('.')[0]
        # filename_mp3 = dir+'/'+base_name+".mp3"
        filename_ogg = dir + '/' + base_name+ '.ogg'
        if os.path.isfile(filename_ogg)==False:
            sound = pydub.AudioSegment.from_wav(filename_wav)
            sound.export(filename_ogg, format="ogg")
        # sound.export("output.mp3", format="mp3")
        self.btn_play_stop.setEnabled(True)
        self.btn_play_stop.setText('Play')


        pygame.mixer.init()
        pygame.mixer.music.load(filename_ogg) #音源を読み込み
        # mp3_length = mp3(filename).info.length #音源の長さ取得
        # pygame.mixer.music.play(1) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
        # time.sleep(mp3_length + 0.25) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
        # time.sleep(5)
        # pygame.mixer.music.stop() #音源の長さ待ったら再生停止


    def timer(self):
        # self.time = self.infline_pos
        self.a = time.time()
        def change_infline():
            # print('music: ' + str(pygame.mixer.music.get_pos()))
            # self.infline_wav.setPos(self.time*44100/4)
            self.infline_wav.setPos(self.infline_pos)
            for idx in range(34):
                self.infline_featV[idx].setPos(self.infline_pos)

            self.infline_pos += 0.25
            print(self.infline_pos)
            self.now = time.time()- self.a
            # print(self.now)


        self.timer = QC.QTimer()
        self.timer.timeout.connect(change_infline)
        # self.timer.start(250)  # 250 ms 毎


    def thread(self):
        if pygame.mixer.music.get_busy() == False:
            print('start play')
            pygame.mixer.music.play()
        # print('music: ' + str(pygame.mixer.music.get_pos()))
        self.isStop = int((self.isStop+1)%2)
        if self.isStop:
            pygame.mixer.music.stop()
            self.timer.stop()
            # self.timer.deleteLater()
            # self.timer.destroyed()
            self.btn_play_stop.setText('Play')
            # pygame.mixer.music.stop()
            return
        self.btn_play_stop.setText('Stop')


        # pygame.mixer.music.play(1) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
        print('inf : '+ str(self.infline_pos))
        pygame.mixer.music.play(start = self.infline_pos)
        # pygame.mixer.music.stop()
        # pygame.mixer.music.set_pos(10)
        # pygame.mixer.music.play(-1, self.infline_pos/4)
        # pygame.mixer.music.rewind()
        # pygame.mixer.music.set_pos(self.infline_pos)
        # pygame.mixer.music.unpause()
        # pygame.mixer.music.set_pos()
        # pygame.mixer.music.set_pos(1)
        # pygame.mixer.music.unpause()

        self.timer.start(250)  # 250 ms 毎



    def get_path_wav(self):
        self.wav_path = QG.QFileDialog.getOpenFileName(self, 'Get Wav File', '/home/')
        # self.wav_path = '../data/test/window_broken.wav'
        self.le0.setText(self.wav_path)

        self.wav_file = wave.open(self.wav_path, 'rb')
        # print(1, self.wav_file.getframerate())
        # print(2, self.wav_file.getnframes())
        y = self.wav_file.readframes(self.wav_file.getnframes())
        # print(3, len(y))
        y = np.frombuffer(y, dtype='int16')
        # print(4, len(y))
        y = y[::int(44100/4)]
        # print(5, len(y))
        x = np.arange(0, len(y))/4
        self.curve_wav.setData(x, y)
        self.wav_file.close()

        thread_obj2 = threading.Thread(target=self.play)
        thread_obj2.start()


    def get_path_feat(self):
        self.feat_path = QG.QFileDialog.getOpenFileName(self, 'Get Feature File', '/home/')
        # self.feat_path = '../data/sample.pkl'
        self.le1.setText(self.feat_path)
        with open(self.feat_path, mode='rb') as f:
            self.feat = pickle.load(f)
        try:
            self.feat = self.feat['data']
        except:
            pass

        for idx in range(34):
            x = np.arange(0, len(self.feat[:, idx]))/4
            self.curve_featV[idx].setData(x, self.feat[:, idx])

    def infline_changed(self):
        infline = self.sender()
        pos = infline.pos()[0]
        # print(infline.pos()[0])
        # print(pos)
        self.infline_pos = int(pos)

    def show_region(self):
        self.region_id += 1
        region_id = self.region_id
        self.region_wavV.append(pg.LinearRegionItem())
        region_wav = self.region_wavV[region_id]
        region_wav.
        self.p_wav.addItem(region_wav)

        for idx in range(34):
            self.p_featV[idx].region_featV.append(pg.LinearRegionItem())
            region_feat = self.p_featV[idx].region_featV[region_id]
            self.p_featV[idx].addItem(region_feat)

    def update_region(self):
        pass



def main():
    app = QG.QApplication(sys.argv)

    ui = audio_check()
    ui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
