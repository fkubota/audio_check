# from mutagen.mp3 import MP3 as mp3
import pygame
import time

filename = '../data/test/window_broken.wav' #再生したいmp3ファイル
# filename = 'eine.mp3' #再生したいmp3ファイル
# filename = 'window_broken.wav' #再生したいmp3ファイル
pygame.mixer.init()
pygame.mixer.music.load(filename) #音源を読み込み
# mp3_length = mp3(filename).info.length #音源の長さ取得
pygame.mixer.music.play(1) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
# time.sleep(mp3_length + 0.25) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
time.sleep(5)
pygame.mixer.music.stop() #音源の長さ待ったら再生停止