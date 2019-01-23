# from mutagen.mp3 import MP3 as mp3
import pygame
import time

# filename = '../data/test/window_broken.wav' #再生したいmp3ファイル
# filename = '/home/fkubota/Music/futta-lifetime.ogg' #再生したいmp3ファイル
filename = '/home/fkubota/Project/Yokogawa/徳山防爆エリア201812/data/徳山防爆エリア201812/record_20181221_162632_環境音/20181221_162632_01.ogg'
# filename = 'eine.mp3' #再生したいmp3ファイル
# filename = 'window_broken.wav' #再生したいmp3ファイル
pygame.mixer.init()
pygame.mixer.music.load(filename) #音源を読み込み
# mp3_length = mp3(filename).info.length #音源の長さ取得

i = 0
while True:
    print(i)
    pygame.mixer.music.play(start=0) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
    time.sleep(3)
    pygame.mixer.music.stop()
    pygame.mixer.music.play(start=10+i*1000)
    # time.sleep(3)
    # pygame.mixer.music.stop()
    # time.sleep(1)
    # pygame.mixer.music.load(filename) #音源を読み込み
    # pygame.mixer_music.play(1, 3600)
    # time.sleep(mp3_length + 0.25) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
    time.sleep(3)
    pygame.mixer.music.stop() #音源の長さ待ったら再生停止
    i += 1