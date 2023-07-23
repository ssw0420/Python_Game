import pygame as pg
import os
import sys
import time
import math


### default setting
TITLE = "Rhythm Game"
WIDTH = 1600
HEIGHT = 900
FPS = 60

### color setting
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
RED = (246, 36, 74)
BLUE = (32, 105, 246)
BLACK = (0, 0, 0)
ALPHA_MAX = 255

class Game:
    # 프로그램 실행
    def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen_mode = 0 #screen mode (0: logo, 1: logo2, 2: main, 3: stage select, 4: play, 5: score)
        self.screen_value = [-ALPHA_MAX, 0, 0, 0]       #screen management value
        self.clock = pg.time.Clock()        #FPS timer
        self.start_tick = 0     #game timer
        self.running = True     #game initialize Boolean value
        self.frame = self.clock.get_fps()
        # self.song_select = 1    #select song
        # self.load_date()        #data loading
        self.new()

    def run(self):
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.frame_set()
            self.key_frame_set()
            self.update()
            self.draw()
            pg.display.flip() ## 화면 전체를 업데이트

    def frame_set(self):
        if self.frame == 0:
            self.frame = FPS

    
    def key_frame_set(self):
        self.keys[0] += (self.keyset[0] - self.keys[0]) / (2 * (FPS / self.frame))
        self.keys[1] += (self.keyset[1] - self.keys[1]) / (2 * (FPS / self.frame))
        self.keys[2] += (self.keyset[2] - self.keys[2]) / (2 * (FPS / self.frame))

    def load_data(self):
        self.song_dir = os.path.join(self.dir, 'music')
        music_type = ["ogg", "mp3", "wav"]
        song_lists = [i for i in os.listdir(self.sng_dir) if i.split('.')[-1] in music_type]

    def draw(self):     ########################## Game Loop - Draw
        self.background = pg.Surface((WIDTH, HEIGHT))           #white background
        self.background = self.background.convert()
        self.background.fill(BLACK)
        self.screen.blit(self.background, (0,0))
        self.draw_screen()
        pg.display.update() ## 화면 일부 또는 전체를 업데이트

    def draw_screen(self):
        
        # 플레이 화면 구성
        pg.draw.rect(self.screen, BLACK, (WIDTH / 2 - WIDTH / 8, -int(WIDTH / 100), WIDTH / 4, HEIGHT + int(WIDTH / 50)))

        # 흰색 직사각형 테두리
        pg.draw.rect(self.screen, WHITE, (WIDTH / 2 - WIDTH / 8, -int(WIDTH / 100), WIDTH / 4, HEIGHT + int(WIDTH / 50)), int(WIDTH / 200))

        # 노트 판정 선
        pg.draw.rect(self.screen, BLACK, (WIDTH / 2 - WIDTH / 8, (HEIGHT / 12) * 9, WIDTH / 4, HEIGHT /2))
        pg.draw.rect(self.screen, WHITE, (WIDTH / 2 - WIDTH / 8, (HEIGHT / 12) * 9, WIDTH / 4, HEIGHT), int(HEIGHT / 200))


        # [A, S, D] 키 입력시 화면 구성
        # 색상 미 입력시 자동으로 흰색 직사각형 생성
        for i in range(7):
            i += 1
            pg.draw.rect(self.screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (WIDTH / 2 - WIDTH / 8 + WIDTH / 32 - (WIDTH / 32) * self.keys[0], (HEIGHT / 12) * 9 - (HEIGHT / 30) * self.keys[0] * i, WIDTH / 16 * self.keys[0], (HEIGHT / 35) / i))
        
        for i in range(7):
            i += 1
            pg.draw.rect(self.screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (WIDTH / 2 - WIDTH / 16 + WIDTH / 32 - (WIDTH / 32) * self.keys[1], (HEIGHT / 12) * 9 - (HEIGHT / 30) * self.keys[1] * i, WIDTH / 16 * self.keys[1], (HEIGHT / 35) / i))
        
        for i in range(7):
            i += 1
            pg.draw.rect(self.screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (WIDTH / 2 + WIDTH / 32 - (WIDTH / 32) * self.keys[2], (HEIGHT / 12) * 9 - (HEIGHT / 30) * self.keys[2] * i, WIDTH / 16 * self.keys[2], (HEIGHT / 35) / i))
                     
    def update(self):
        # self.all_sprites.update()
        self.game_tick = pg.time.get_ticks() - self.start_tick

    def events(self):
        mouse_coord = pg.mouse.get_pos()
        mouse_mover = False
        mouse_click = 0
        key_click = 0
        
        ### key setting
        self.keys = [0, 0, 0]
        self.keyset = [0, 0, 0]

        for event in pg.event.get():
            # 게임 종료
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing, self.running = False, False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing, self.running = False, False
                if event.key == pg.K_a:
                    self.keyset[0] = 1
                if event.key == pg.K_s:
                    self.keyset[1] = 1
                if event.key == pg.K_d:
                    self.keyset[2] = 1

            if event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    self.keyset[0] = 0
                if event.key == pg.K_s:
                    self.keyset[1] = 0
                if event.key == pg.K_d:
                    self.keyset[2] = 0



    # def loading(self): # song, image 호출

    # 게임 초기화
    def new(self):
        self.score = 0

game = Game()

while game.running:
    game.run()

pg.quit()
