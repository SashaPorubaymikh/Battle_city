import sys, random

import pygame

from dead import Dead
from Levels import levels
from Blocks import Blocks
from Player import Player
from Bullet import Bullet
from Controls import Controls
from Enemy import Enemy
from Friend import Friend
from status_bar import Status_bar
from timer import Timer, New_timer
from menu import Menu
from flag import Flag
from Dynamite import Dynamite

pygame.init()
pygame.font.init()

#Создание игрового окна
infos = pygame.display.Info()
screen_size = (infos.current_w, infos.current_h)
scr_w = infos.current_w
scr_h = infos.current_h
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.Surface((1366, 768))
pygame.display.set_icon(pygame.image.load("Tanks.png"))
full_screen = True

#Создание перснaжа
sprite_group = []
bullets_group = []
boom_group = []
dead_group = []

#Персонаж, вргаги и друзья
                    
enemies = friends = 0
                    

#Создание меню
menu = Menu()
difficulty = 0

#Создание строки состояния
status_bar = Status_bar(0, 0)

#Создание Таймера
timer = Timer()
bomb_boom_timer = New_timer()

#Создание уровня
max_enemies = 0
spavned_enemies = 0
total_enemies = 0
stage = 0
bricks_group = []
enemy_spavner_group = []
level_num = 0
lvl_w = lvl_h = 0
player_spavn = []
def make_level(level_num, diff, mode):
    x = y = 0
    global bricks_group, sprite_group, lvl_w, lvl_h, enemies, \
        friends, max_enemies, total_enemies, spavned_enemies, enemy_spavner_group,\
            camera, bullets_group, boom_group, player_spavn, dead_group

    enemy_spavner_group = []
    bullets_group = []
    boom_group = []
    dead_group = []
    timer.timer = 0
    max_enemies = 6
    if mode == 'EL_Mode' or mode == 'BD_Mode':
        total_enemies = -1
    elif mode == 'ST_Mode':
        total_enemies = 20
    if diff == 1:
        max_enemies += 2
        total_enemies += 5
    if diff == 2:
        max_enemies += 4
        total_enemies += 10
    spavned_enemies = 0
    bricks_group = []
    sprite_group = []
    enemies = friends = 0
    lvl_h = len(levels[level_num]) * 40
    for row in levels[level_num]:
        lvl_w = len(row) * 40
        for col in row:
            if col == '0':
                b1 = Blocks(x, y, 'images/blocks/brick.png', 1)
                bricks_group.append(b1)
                sprite_group.append(b1)
            if col == '1':
                b1 = Blocks(x, y, 'images/blocks/experimentalbrick.png', 1000000)
                bricks_group.append(b1)
                sprite_group.append(b1)
            if col == 'e':
                enemy_spavner_group.append([x, y])
            if col == 'f':
                sprite_group.append(Friend(x, y))
                friends += 1
            if col == 'p':
                sprite_group = [Player(x, y)] + sprite_group
                friends += 1
                player_spavn = [x, y]
            if col == 'b' and mode == 'ST_Mode':
                sprite_group.append(Flag(x, y))
            if col == 'd' and mode == 'BD_Mode':
                sprite_group.append(Dynamite(x, y))
            x += 40
        y += 40
        x = 0

    camera = Camera(camera_func, lvl_w, lvl_h)


#Создание камеры
class Camera(object):
    def __init__(self, camera_func, widht, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, widht, height )
  
    def apply(self, target):
        return target.rect.move(self.state.topleft)
  
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
  
def camera_func(camera, target_rect):
    l = -target_rect.x + 1366/2
    t = -target_rect.y + 768/2
    w, h = camera.width, camera.height
 
    l = min(0, l)
    l = max(-(camera.width-1366), l)
    t = max(-(camera.height-768), t)
    t = min(0, t)
 
    return pygame.Rect(l, t, w, h)


#Отображениe управления
controls_list = ['Escape - меню',
                 'W, arrow up - ехать вверх',
                 'D, arrow right - ухать вправо',
                 'S, arrow down - ехать вниз',
                 'A, arrow left - ехать влево',
                 'F - включить/выключить полноэкранный режим',
                 'Space, mouse click - выстрел'
]

control = Controls(scr_w, scr_h, controls_list)
control.show()

#Конфигурации главного цикла
show_controls = False
done = True
launch_menu = False

clock = pygame.time.Clock()
mode_n_level = menu.main_menu(screen, win)
make_level(mode_n_level['level'], 0, mode_n_level['mode'])

pygame.key.set_repeat(10, 10)

while done:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_c:
                if show_controls == False:
                    show_controls = True
                else:
                    show_controls = False

            if e.key == pygame.K_f:
                if full_screen == True:
                    win = pygame.display.set_mode((scr_w, scr_h))
                    full_screen = False
                else:
                    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    full_screen = True

            if e.key == pygame.K_UP or e.key == pygame.K_w:
                sprite_group[0].dir = ''
            if e.key == pygame.K_DOWN  or e.key == pygame.K_s:
                sprite_group[0].dir = ''
            if e.key == pygame.K_LEFT or e.key == pygame.K_a:
                sprite_group[0].dir = ''
            if e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                sprite_group[0].dir = ''

        if e.type == pygame.MOUSEBUTTONDOWN  and sprite_group[0].isdead == False and sprite_group[0].ready == True:
            if e.button == 1:
                sprite_group[0].shoot(bullets_group)    

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        pause = menu.pause(screen, win)
        if pause == "MAIN_MENU":
            mode_n_level = menu.main_menu(screen, win)
            make_level(mode_n_level['level'], 0, mode_n_level['mode'])
        elif pause == 'RESTART':
            make_level(mode_n_level['level'], 0, mode_n_level['mode'])

            
        pygame.key.set_repeat(10, 10)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        sprite_group[0].dir = sprite_group[0].ldir = 'left'
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        sprite_group[0].dir = sprite_group[0].ldir = 'down'
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        sprite_group[0].dir = sprite_group[0].ldir = 'right'
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        sprite_group[0].dir = sprite_group[0].ldir = 'up'
    if keys[pygame.K_SPACE] and sprite_group[0].ready == True and sprite_group[0].isdead == False:
        sprite_group[0].shoot(bullets_group)
            
    screen.fill((5, 5, 5))

    #отрисовка объектов
    for i in bricks_group:
        i.update(bricks_group, sprite_group)
    for i in bricks_group:
        screen.blit(i.image, camera.apply(i))
    for i in bullets_group:
        if i.dir == 'up' or i.dir == 'down':
            screen.blit(i.image, camera.apply(i))
        else:
            screen.blit(pygame.transform.rotate(i.image, 90), camera.apply(i))
    
    #Обновление персонажей
    if len(sprite_group) > 0:
        camera.update(sprite_group[0])
    for i in bullets_group:
        i.update(i.dir, screen, sprite_group, bullets_group, lvl_w, lvl_h)
    for i in dead_group:
        i.update(sprite_group, bricks_group)
        screen.blit(i.image, camera.apply(i))
    for i in reversed(sprite_group):
        if isinstance(i, Enemy):
            if i.update(sprite_group, friends, enemies, bullets_group, lvl_w, lvl_h, boom_group, dead_group) == 0:
                enemies -= 1
                dead_group.append(Dead(i.rect.x, i.rect.y, 2, i.ldir))
            screen.blit(i.image, camera.apply(i))
        if isinstance(i, Player) and i.isdead == False:
            if i.update(sprite_group, screen, friends, boom_group, player_spavn) == 0:
                friends -= 1
                dead_group.append(Dead(i.rect.x, i.rect.y, 1, i.ldir))
            screen.blit(i.image, camera.apply(i))
            screen.blit(i.recharge, (camera.apply(i)[0], camera.apply(i)[1] - 10))
        elif isinstance(i, Player) and i.isdead == True:
            i.rect.x = i.rect.y = -40
        if isinstance(i, Friend):
            if i.update(sprite_group, enemies, friends, bullets_group, lvl_w, lvl_h, boom_group, dead_group) == 0:
                friends -= 1
            screen.blit(i.image, camera.apply(i))
        if isinstance(i, Flag):
            if i.update(sprite_group) == "game over":
                u_lose.menu(screen, win)
                launch_menu = True
            else:
                screen.blit(i.image, (camera.apply(i)[0], camera.apply(i)[1]))
        if isinstance(i, Dynamite):
            bomb_return = i.update(sprite_group, boom_group)
            if bomb_return == 'u win':
                mode_n_level['level'] += 1
                if stage < len(levels):
                    make_level(mode_n_level['level'] + 1, 0, mode_n_level['mode'])
            elif bomb_return == 'u lose':
                if bomb_boom_timer.update() == True:
                    pass        
            else:
                screen.blit(i.image, camera.apply(i))
    for i in boom_group:
        i.update(boom_group, clock.get_fps())
        screen.blit(i.image, camera.apply(i))

            
                
    if timer.update() == True:
        random.shuffle(enemy_spavner_group)
        for i in enemy_spavner_group:
            if enemies < max_enemies and (spavned_enemies < total_enemies or mode_n_level['mode'] == 'EL_Mode' or mode_n_level['mode'] == 'BD_Mode'):
                sprite_group.append(Enemy(i[0], i[1], 0))
                enemies += 1
                spavned_enemies += 1
    if mode_n_level['mode'] == 'ST_Mode': 
        status_bar.show(sprite_group[0].lifes, friends, total_enemies - spavned_enemies, mode_n_level['level'] + 1, screen, scr_w)
    elif mode_n_level['mode'] == 'EL_Mode' or mode_n_level['mode'] == 'BD_Mode':
        status_bar.show(sprite_group[0].lifes, friends, spavned_enemies, mode_n_level['level'] + 1, screen, scr_w)


    if friends == 0:
        u_lose.menu(screen, win)
        launch_menu = True
    if spavned_enemies == total_enemies and enemies == 0:
        u_win.menu(screen, win)
        stage += 1
        if stage < len(levels):
            make_level(stage, 0, mode_n_level['mode'])
    

    if show_controls == True:
        win.blit(control.surface, (0, 0))

    win.blit(pygame.transform.scale(screen, (scr_w, scr_h)), (0, 0))
    
    pygame.display.flip()
    
    clock.tick(40)
