import pygame
import Bot
from Map import *
filename = 'testsave9.txt'
save_filename = 'testsave9.txt'
load = True
mapsize = (120,90)
scale = 8
screensize = (mapsize[0]*scale, mapsize[1]*scale)
sc = pygame.display.set_mode(screensize)
pygame.display.set_caption('Bacteria life')
clock = pygame.time.Clock()

def exp(num):
    return 1/(1+2.7182818284**(-num/200))

def draw_map(mapp):
    for i in range(len(mapp)):
        for o in range(len(mapp[0])):
            if type(mapp[i][o]) != Bot.Bot:
                if type(mapp[i][o]) == Bot.Organic:
                    pygame.draw.rect(sc, (100,100,100), (i*scale,o*scale,scale,scale))
                else:
                    pygame.draw.rect(sc, (mapp[i][o] * 250,0,0), (i*scale,o*scale,scale,scale))
            else:
                pygame.draw.rect(sc, (0,int(exp(mapp[i][o].energy)*250),0), (i*scale,o*scale,scale,scale))
    pygame.display.update()

mp = Map(mapsize)
mbd = False
mp.spawn_bot([2,2])
mp.spawn_bot([2,60], [45, 18, 55, 32, 31, 54, 30, 0, 58, 14, 8, 22, 18, 20, 41, 30, 33, 35, 61, 62, 34, 13, 37, 13, 39, 10, 19, 47, 33, 62, 7, 50, 5, 31, 45, 63, 41, 27, 38, 60, 38, 52, 22, 40, 30, 26, 12, 20, 33, 19, 34, 9, 0, 24, 4, 42, 45, 19, 21, 33, 11, 13, 5, 48])
if load:
    mp.load(filename)
running = True
paused = False
mode = 0
modes = ['Show info', 'Draw walls', 'Erase']
while running:
    draw_map(mp.map)
    pygame.display.set_caption(f'Bacteria life Mode: {modes[mode]}')
    if mbd:
        if mode == 1:
            mp.map[int(position[0]/scale)][int(position[1]/scale)] = 1
        elif mode == 2:
            mp.map[int(position[0]/scale)][int(position[1]/scale)] = 0
    if not paused:
        clock.tick(60)
        mp.main_cycle()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEMOTION:
            position = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            mbd = True
            if mode == 0:
                print(mp.map[int(position[0]/scale)][int(position[1]/scale)])
        if event.type == pygame.MOUSEBUTTONUP:
            mbd = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                mp.save(save_filename)
            if event.key == pygame.K_p:
                if paused:
                    paused = False
                else:
                    paused = True
            if event.key == pygame.K_c:
                mode += 1
                if mode > 2:
                    mode = 0