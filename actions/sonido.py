import pygame

pygame.init()
pygame.mixer.init()

def sonidoOn(fileName):
    audio_file = fileName
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

def sonidoOff():
    pygame.mixer.music.stop()

