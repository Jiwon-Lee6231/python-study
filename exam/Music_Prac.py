import sys
import random
import pygame

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 300))
screen.fill((255, 255, 255))
pygame.display.set_caption("Music Player")

file_names = ['horse', 'cat', 'caw', 'dog', 'chicken']

def initMixer():
    pygame.mixer.init()
    freq = 16000
    size = -16
    channels = 1
    buffer = 2048
    pygame.mixer.init(freq, size, channels, buffer)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            random_names = random.sample(file_names, len(file_names))
            print(file_names)
            print(random_names)
            
            initMixer()
            for file_name in random_names:
               file_dir = 'C:\\dongdong\\Musices' + '\\' + file_name + '.mp3'
               pygame.mixer.music.load(file_dir)
               pygame.mixer.music.play()
               
               clock = pygame.time.Clock()
               while pygame.mixer.music.get_busy():
                   clock.tick(30)
               pygame.mixer.music.stop()
                    
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.flip()