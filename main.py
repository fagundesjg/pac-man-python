import pygame, time, threading, random, os
from random import randint
from pygame.locals import *
from configs import *

def sound_eat_food():
    if pygame.mixer.Channel(0).get_busy():
        pass
    else: pygame.mixer.Channel(0).play(music_eat)


def getContain(position):
    if position in food_list:
        return FOOD
    else: return EMPTY


def draw(contain, position):
    if contain == FOOD:
        screen.blit(FOOD_SKIN, (position[0]*sx,position[1]*sy) )
    else:
        screen.blit(EMPTY_SKIN, (position[0]*sx,position[1]*sy) )


def toggleVisibilityBigFood():
    global running
    while running:
        time.sleep(0.6)
        for big_food in big_food_list:
            if big_food["visible"]:
                screen.blit(BIG_FOOD_SKIN,(big_food["pos"][0]*sx,big_food["pos"][1]*sy))
            else: 
                screen.blit(EMPTY_SKIN,(big_food["pos"][0]*sx,big_food["pos"][1]*sy))
            big_food["visible"] = not big_food["visible"]


def ghost_sound():
    global running
    while running:
        while pygame.mixer.Channel(2).get_busy(): pass
        pygame.mixer.Channel(2).play(music_ghost_move)

def ghosts_move(color, seconds):
    global running
    while running:
        time.sleep(seconds)
        flag = False
        possible_moves = [("UP",(ghosts[color]["pos"][0], ghosts[color]["pos"][1] - 1)),
        ("DOWN",(ghosts[color]["pos"][0],ghosts[color]["pos"][1] + 1)),
        ("LEFT",(ghosts[color]["pos"][0] - 1,ghosts[color]["pos"][1])),
        ("RIGHT",(ghosts[color]["pos"][0] + 1,ghosts[color]["pos"][1]))]
        random.shuffle(possible_moves)
        while not flag:
            for position in possible_moves:
                if (position[1] not in block_list) and (not (ghosts[color]["last_move"] == position[1])):
                    if position not in spawn_list:
                        flag = True
                        break
                    else:
                        flag = True
            if flag:
                ghosts[color]["direction"] = position[0]
                draw(ghosts[color]["before"], ghosts[color]["pos"])
                ghosts[color]["last_move"] = ghosts[color]["pos"]
                ghosts[color]["before"] = getContain(position[1])
                ghosts[color]["pos"] = position[1]
                if(ghosts[color]["pos"][0] > COLUMNS): ghosts[color]["pos"] = (0, ghosts[color]["pos"][1])
                elif(ghosts[color]["pos"][0] < 0): ghosts[color]["pos"] = (COLUMNS, ghosts[color]["pos"][1])
                elif(ghosts[color]["pos"][1] < 0): ghosts[color]["pos"] = (ghosts[color]["pos"][0], LINES)
                elif(ghosts[color]["pos"][1] > LINES): ghosts[color]["pos"] = (ghosts[color]["pos"][0], 0)
            

def loadMap(url):
    arq = open(url,"r")
    lines = arq.readlines()
    for j,line in enumerate(lines):
        splited = line.split(" ")
        for i,ch in enumerate(splited):
            ch = int(ch)
            if ch == BLOCK:
                screen.blit(WALL_SKIN,(i*sx,j*sy))
                block_list.append((i,j))
            elif ch == FOOD:
                screen.blit(FOOD_SKIN,(i*sx,j*sy))
                food_list.append((i,j))
            elif ch == SPAWN:
                spawn_list.append((i,j))
            elif ch == BIG_FOOD:
                screen.blit(BIG_FOOD_SKIN,(i*sx,j*sy))
                big_food_list.append({"pos": (i,j), "visible": True})
            else:
                screen.blit(EMPTY_SKIN,(i*sx,j*sy))

                
def main():
    global player, isOpen, spawn_list, block_list, big_food_list, big_food_flag, LEFT, RIGHT, UP, DOWN, running
    loadMap('maps/level1.txt')
    pygame.display.update()
    pygame.mixer.Channel(0).play(music_intro)
    while pygame.mixer.Channel(0).get_busy(): pass
    threading.Thread(target=ghosts_move, args=("RED",0.5,)).start()
    threading.Thread(target=ghosts_move, args=("ORANGE",0.5,)).start()
    threading.Thread(target=ghosts_move, args=("PINK",0.5,)).start()
    threading.Thread(target=ghosts_move, args=("AQUA",0.5,)).start()
    threading.Thread(target=toggleVisibilityBigFood, args=()).start()
    threading.Thread(target=ghost_sound, args=()).start()

    while running:
        time.sleep(0.15)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    RIGHT = DOWN = LEFT = 0
                    UP = 1
                elif event.key == K_DOWN:
                    RIGHT = UP = LEFT = 0
                    DOWN = 1
                elif event.key == K_LEFT:
                    RIGHT = UP = DOWN = 0
                    LEFT = 1
                elif event.key == K_RIGHT:
                    LEFT = UP = DOWN = 0
                    RIGHT = 1

        if isOpen:
            if RIGHT:
                if (player[0] + 1, player[1]) not in block_list and ((player[0] + 1, player[1]) not in spawn_list):
                    screen.blit(EMPTY_SKIN,(player[0]*sx,player[1]*sy)) # pinta de preto onde o pacman estava
                    player = (player[0] + 1, player[1]) # define nova posição
                    if(player[0] > COLUMNS): player = (0, player[1])
                screen.blit(PAC_SKINS["OPEN"]["RIGHT"], (player[0]*sx,player[1]*sy)) # pinta o pacman na nova posicao
            elif LEFT:
                if (player[0] - 1, player[1]) not in block_list and ((player[0] - 1, player[1]) not in spawn_list):
                    screen.blit(EMPTY_SKIN,(player[0]*sx,player[1]*sy))
                    player = (player[0] - 1, player[1])
                    if(player[0] < 0): player = (COLUMNS, player[1])
                screen.blit(PAC_SKINS["OPEN"]["LEFT"], (player[0]*sx,player[1]*sy))
            elif UP:
                if (player[0], player[1] - 1) not in block_list and ((player[0], player[1] - 1)) not in spawn_list:
                    screen.blit(EMPTY_SKIN,(player[0]*sx,player[1]*sy))
                    player = (player[0], player[1] - 1)
                    if(player[1] < 0): player = (player[0], LINES)
                screen.blit(PAC_SKINS["OPEN"]["UP"], (player[0]*sx,player[1]*sy))
            elif DOWN:
                if (player[0], player[1] + 1) not in block_list and ((player[0], player[1] + 1) not in spawn_list):
                    screen.blit(EMPTY_SKIN,(player[0]*sx,player[1]*sy))
                    player = (player[0], player[1] + 1)
                    if(player[1] > LINES): player = (player[0], 0)
                screen.blit(PAC_SKINS["OPEN"]["DOWN"], (player[0]*sx,player[1]*sy))
        else:
            screen.blit(PAC_SKINS["CLOSED"], (player[0]*sx,player[1]*sy))

        if player in food_list:
            food_list.remove((player[0],player[1]))
            sound_eat_food()
        for big_food in big_food_list:
            if player == big_food["pos"]:
                pygame.mixer.Channel(1).play(music_eat_big_food)
                big_food_flag = True
                big_food_list.remove(big_food)

        isOpen = not isOpen

        for ghost,info in ghosts.items():
            if big_food_flag:
                info["down"] = 60
            if info["down"] > 0:
                if player == info["pos"]:
                    pygame.mixer.Channel(1).play(music_eat_ghost)
                    info["down"] = 0
                    if ghost == "RED":
                        info["pos"] = (12,14)
                    elif ghost == "ORANGE":
                        info["pos"] = (13,14)
                    elif ghost == "PINK":
                        info["pos"] = (14,14)
                    elif ghost == "AQUA":
                        info["pos"] = (15,14)
                else:
                    info["down"] = info["down"] - 1
                    screen.blit(GHOST_SKIN["DOWN"], (info["pos"][0]*sx,info["pos"][1]*sy))
            else:
                if player == info["pos"]:
                    pygame.mixer.Channel(1).play(music_pac_death)
                    pygame.display.update()
                    running = False
                    while pygame.mixer.Channel(1).get_busy(): pass
                screen.blit(GHOST_SKIN[ghost][info["direction"]], (info["pos"][0]*sx,info["pos"][1]*sy))
        big_food_flag = False

        pygame.display.update()

if __name__ == "__main__":
    main()