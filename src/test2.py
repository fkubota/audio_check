# from mutagen.mp3 import MP3 as mp3
import pygame
import time

# filename = '../data/test/window_broken.wav' #再生したいmp3ファイル
filename = '/home/fkubota/Music/futta-lifetime.ogg' #再生したいmp3ファイル
# filename = '/home/fkubota/Project/Yokogawa/徳山防爆エリア201812/data/徳山防爆エリア201812/record_20181221_162632_環境音/20181221_162632.mp3'
# filename = 'eine.mp3' #再生したいmp3ファイル
# filename = 'window_broken.wav' #再生したいmp3ファイル
pygame.mixer.init()
pygame.mixer.music.load(filename) #音源を読み込み
# mp3_length = mp3(filename).info.length #音源の長さ取得


while True :
    pygame.mixer.init()
    pygame.mixer.music.load(filename) #音源を読み込み

    pygame.mixer.music.play()
    time.sleep(3)
    pygame.mixer.music.rewind()
    time.sleep(3)
    pygame.mixer.music.stop()
    # pygame.mixer.music.pause()
    #
    # while pygame.mixer.music.get_busy() == True:
    #     print('a')
    #     time.sleep(1)

    pygame.mixer.music.play()
    pygame.mixer.music.rewind()
    # pygame.mixer.music.unpause()
    print('ok')
    pygame.mixer.music.set_pos(10)

    time.sleep(3)
    pygame.mixer.music.stop()

