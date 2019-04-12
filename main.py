import pygame, time, threading, random
from random import randint
from pygame.locals import *

sx = sy = 20
isOpen = True
LEFT = 0
RIGHT = 1
UP = 0
DOWN = 0
BLOCK = 1
FOOD = 2
EMPTY = 3
SPAWN = 4
player = (1,1)
ghosts = {
    "RED": {
        "pos": (12,14),
        "before": None,
        "last_move": None,
        "direction": "RIGHT",
    },
    "ORANGE": {
        "pos": (13,14),
        "before": None,
        "last_move": None,
        "direction": "RIGHT",
    },
    "PINK": {
        "pos": (14,14),
        "before": None,
        "last_move": None,
        "direction": "RIGHT",
    },
    "AQUA": {
        "pos": (15,14),
        "before": None,
        "last_move": None,
        "direction": "RIGHT",
    }
}

LINES = 31
COLUMNS = 28

spawn_list = []
block_list = []
food_list = []

lock = threading.Lock()

PAC_SKINS = {
    "OPEN": {   
        "LEFT": pygame.transform.scale(pygame.image.load('imgs/pacman.bmp'),(sx,sy)),
        "RIGHT": pygame.transform.scale(pygame.transform.rotate(pygame.image.load('imgs/pacman.bmp'), 180),(sx,sy)),
        "UP": pygame.transform.scale(pygame.transform.rotate(pygame.image.load('imgs/pacman.bmp'), -90),(sx,sy)),
        "DOWN": pygame.transform.scale(pygame.transform.rotate(pygame.image.load('imgs/pacman.bmp'), 90),(sx,sy)),
    },
    "CLOSED": pygame.transform.scale(pygame.image.load('imgs/pacman-closed.bmp'),(sx,sy))
}

GHOST_SKIN = {
    "RED": {
        "LEFT": pygame.transform.scale(pygame.image.load('imgs/red-ghost-left.bmp'),(sx,sy)),
        "RIGHT": pygame.transform.scale(pygame.image.load('imgs/red-ghost-right.bmp'),(sx,sy)),
        "UP": pygame.transform.scale(pygame.image.load('imgs/red-ghost-up.bmp'),(sx,sy)),
        "DOWN": pygame.transform.scale(pygame.image.load('imgs/red-ghost-down.bmp'),(sx,sy)),
    },
    "ORANGE": {
        "LEFT": pygame.transform.scale(pygame.image.load('imgs/orange-ghost-left.bmp'),(sx,sy)),
        "RIGHT": pygame.transform.scale(pygame.image.load('imgs/orange-ghost-right.bmp'),(sx,sy)),
        "UP": pygame.transform.scale(pygame.image.load('imgs/orange-ghost-up.bmp'),(sx,sy)),
        "DOWN": pygame.transform.scale(pygame.image.load('imgs/orange-ghost-down.bmp'),(sx,sy)),
    },
    "AQUA": {
        "LEFT": pygame.transform.scale(pygame.image.load('imgs/aqua-ghost-left.bmp'),(sx,sy)),
        "RIGHT": pygame.transform.scale(pygame.image.load('imgs/aqua-ghost-right.bmp'),(sx,sy)),
        "UP": pygame.transform.scale(pygame.image.load('imgs/aqua-ghost-up.bmp'),(sx,sy)),
        "DOWN": pygame.transform.scale(pygame.image.load('imgs/aqua-ghost-down.bmp'),(sx,sy)),
    },
    "PINK": {
        "LEFT": pygame.transform.scale(pygame.image.load('imgs/pink-ghost-left.bmp'),(sx,sy)),
        "RIGHT": pygame.transform.scale(pygame.image.load('imgs/pink-ghost-right.bmp'),(sx,sy)),
        "UP": pygame.transform.scale(pygame.image.load('imgs/pink-ghost-up.bmp'),(sx,sy)),
        "DOWN": pygame.transform.scale(pygame.image.load('imgs/pink-ghost-down.bmp'),(sx,sy)),
    }
}

WALL_SKIN = pygame.transform.scale(pygame.image.load('imgs/block.bmp'),(sx,sy))
FOOD_SKIN = pygame.transform.scale(pygame.image.load('imgs/food.bmp'),(sx,sy))
EMPTY_SKIN = pygame.transform.scale(pygame.image.load('imgs/empty.bmp'),(sx,sy))

def ghosts_collide(destiny):
    for ghost,info in ghosts.items():
        if(destiny == info["pos"]): return True
    return False


def getContain(position):
    if position in food_list:
        return FOOD
    else: return EMPTY

def draw(contain, position):
    if contain == FOOD:
        screen.blit(FOOD_SKIN, (position[0]*sx,position[1]*sy) )
    else:
        screen.blit(EMPTY_SKIN, (position[0]*sx,position[1]*sy) )

def ghosts_move(color, seconds):
    while True:
        time.sleep(seconds)
        flag = False
        possible_moves = [("UP",(ghosts[color]["pos"][0], ghosts[color]["pos"][1] - 1)),
        ("DOWN",(ghosts[color]["pos"][0],ghosts[color]["pos"][1] + 1)),
        ("LEFT",(ghosts[color]["pos"][0] - 1,ghosts[color]["pos"][1])),
        ("RIGHT",(ghosts[color]["pos"][0] + 1,ghosts[color]["pos"][1]))]
        random.shuffle(possible_moves)
        while not flag:
            for position in possible_moves:
                if (position[1] not in block_list) and (not ghosts_collide(position[1])) and (not (ghosts[color]["last_move"] == position[1])):
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
            else:
                screen.blit(EMPTY_SKIN,(i*sx,j*sy))

pygame.init()
screen = pygame.display.set_mode((COLUMNS*sx,LINES*sy))
pygame.display.set_caption('Pac Man')
clock = pygame.time.Clock()

screen.fill((0,0,0))    # desenha a tela preta
loadMap('maps/level1.txt')

threading.Thread(target=ghosts_move, args=("RED",0.5,)).start()
threading.Thread(target=ghosts_move, args=("ORANGE",0.5,)).start()
threading.Thread(target=ghosts_move, args=("PINK",0.5,)).start()
threading.Thread(target=ghosts_move, args=("AQUA",0.5,)).start()


while True:
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
            if (player[0] + 1, player[1]) not in block_list:
                screen.blit(EMPTY_SKIN,(player[0]*sx,player[1]*sy)) # pinta de preto onde o pacman estava
                player = (player[0] + 1, player[1]) # define nova posição
                if(player[0] > COLUMNS): player = (0, player[1])
            screen.blit(PAC_SKINS["OPEN"]["RIGHT"], (player[0]*sx,player[1]*sy)) # pinta o pacman na nova posicao
        elif LEFT:
            if (player[0] - 1, player[1]) not in block_list:
                screen.blit(EMPTY_SKIN,(player[0]*sx,player[1]*sy))
                player = (player[0] - 1, player[1])
                if(player[0] < 0): player = (COLUMNS, player[1])
            screen.blit(PAC_SKINS["OPEN"]["LEFT"], (player[0]*sx,player[1]*sy))
        elif UP:
            if (player[0], player[1] - 1) not in block_list:
                screen.blit(EMPTY_SKIN,(player[0]*sx,player[1]*sy))
                player = (player[0], player[1] - 1)
                if(player[1] < 0): player = (player[0], LINES)
            screen.blit(PAC_SKINS["OPEN"]["UP"], (player[0]*sx,player[1]*sy))
        elif DOWN:
            if (player[0], player[1] + 1) not in block_list:
                screen.blit(EMPTY_SKIN,(player[0]*sx,player[1]*sy))
                player = (player[0], player[1] + 1)
                if(player[1] > LINES): player = (player[0], 0)
            screen.blit(PAC_SKINS["OPEN"]["DOWN"], (player[0]*sx,player[1]*sy))
    else:
        screen.blit(PAC_SKINS["CLOSED"], (player[0]*sx,player[1]*sy))

    if player in food_list:
        food_list.remove((player[0],player[1]))

    isOpen = not isOpen

    for ghost,info in ghosts.items():
        screen.blit(GHOST_SKIN[ghost][info["direction"]], (info["pos"][0]*sx,info["pos"][1]*sy))

    pygame.display.update()
                


if __name__ == "__main__":
    pass