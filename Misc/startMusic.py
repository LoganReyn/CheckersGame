"""
Functions for Game Music

Music Credit 
    "Laughing Love" by Charles Crawford Gorst, available on Free Music Archive, licensed under CC BY-NC.
"""
import pygame

def startMusic(filePath):
    pygame.mixer.init()
    pygame.mixer_music.load(filePath)
    pygame.mixer_music.play(-1)