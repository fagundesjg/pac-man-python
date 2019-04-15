import pygame, os, threading

# DIMENSOES DO TABULEIRO
LINES = 31
COLUMNS = 28
running = True

# ESCALA DO JOGO
sx = sy = 20

# VARIAVEIS DO MAPA .TXT
BLOCK = 1
FOOD = 2
EMPTY = 3
SPAWN = 4
BIG_FOOD = 5

# LISTAS 
spawn_list = []
block_list = []
food_list = []
big_food_list = []

# VARIAVEIS BOOLEANAS
isOpen = True
big_food_flag = False

# VARIAVEIS DIRECIONAIS DO PLAYER
LEFT = 0
RIGHT = 1
UP = 0
DOWN = 0

# POSICAO DO PLAYER NO MAPA
player = (1,1)

# INFO DOS FANTASMAS
ghosts = {
    "RED": {
        "pos": (12,14),
        "before": None,
        "last_move": None,
        "direction": "RIGHT",
        "down": 0,
    },
    "ORANGE": {
        "pos": (13,14),
        "before": None,
        "last_move": None,
        "direction": "RIGHT",
        "down": 0,
    },
    "PINK": {
        "pos": (14,14),
        "before": None,
        "last_move": None,
        "direction": "RIGHT",
        "down": 0,
    },
    "AQUA": {
        "pos": (15,14),
        "before": None,
        "last_move": None,
        "direction": "RIGHT",
        "down": 0,
    }
}

# DEFINIÇÃO DAS SKINS

WALL_SKIN = pygame.transform.scale(pygame.image.load('imgs/block.bmp'),(sx,sy))
FOOD_SKIN = pygame.transform.scale(pygame.image.load('imgs/food.bmp'),(sx,sy))
BIG_FOOD_SKIN = pygame.transform.scale(pygame.image.load('imgs/big-food.bmp'),(sx,sy))
EMPTY_SKIN = pygame.transform.scale(pygame.image.load('imgs/empty.bmp'),(sx,sy))


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
    },
    "DOWN": pygame.transform.scale(pygame.image.load('imgs/ghost-down.bmp'),(sx,sy)),
}

pygame.init()
screen = pygame.display.set_mode((COLUMNS*sx,LINES*sy))
pygame.display.set_caption('Pac Man')
pygame.mixer.pre_init(frequency=44100, size=-16, channels=3, buffer=4096)
screen.fill((0,0,0))    # desenha a tela preta
music_intro = pygame.mixer.Sound(os.path.join('sounds','pacman_beginning.wav'))
music_eat = pygame.mixer.Sound(os.path.join('sounds','pacman_chomp.wav'))
music_eat_ghost = pygame.mixer.Sound(os.path.join('sounds','pacman_eatghost.wav'))
music_eat_big_food = pygame.mixer.Sound(os.path.join('sounds','pacman_intermission.wav'))
music_pac_death = pygame.mixer.Sound(os.path.join('sounds','pacman_death.wav'))
music_ghost_move = pygame.mixer.Sound(os.path.join('sounds','ghost-move.wav'))
clock = pygame.time.Clock()