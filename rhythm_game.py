import pygame as pg
import os
import sys
import time
import math
import random


### default setting
TITLE = "Rhythm Game"
WIDTH = 1600
HEIGHT = WIDTH * (9 / 16)
FPS = 60

### color setting
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
RED = (246, 36, 74)
BLUE = (32, 105, 246)
BLACK = (0, 0, 0)
# ALPHA_MAX = 255

### time setting
SPEED = 2


class Game:
    # 프로그램 실행
    def __init__(self):
        pg.init()
        pg.font.init()
        pg.mixer.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen_mode = 0 #screen mode (0: logo, 1: logo2, 2: main, 3: stage select, 4: play, 5: score)
        # self.screen_value = [-ALPHA_MAX, 0, 0, 0]       #screen management value
        self.clock = pg.time.Clock()        #FPS timer
        self.start_tick = 0     #game timer
        self.running = True     #game initialize Boolean value
        self.frame = self.clock.get_fps()

        ### note time setting
        self.start_time = time.time()

        ### combo setting
        self.combo = 0
        self.combo_time = time.time()
        self.combo_effect1 = 0
        self.combo_effect2 = 0
        self.last_combo = 0
        self.rate = "PERFECT"
        self.perfect = "PERFECT"
        self.good = "GOOD"
        self.miss = "MISS"

        ### key setting
        self.keys = [0, 0, 0]
        self.keyset = [0, 0, 0]
        self.spin = 0

        ### note setting
        self.note1 = []
        self.note2 = []
        self.note3 = []
        self.create_note_time = 0
        self.randnote = 0
        self.temp_randnote = 0

        ### path setting
        self.Cpath = os.path.dirname(__file__)
        self.FontPath = os.path.join(self.Cpath,"font")
        self.ingame_font_rate = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int(WIDTH / 23))
        self.ingame_font_combo = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int(WIDTH / 38) * self.combo_effect2)


        # self.song_select = 1    #select song
        # self.load_date()        #data loading
        # self.new()

    def run(self):
        self.playing = True

        while self.playing:
            self.Time = time.time() - self.start_time
            self.clock.tick(FPS)
            self.events()
            self.frame_set()
            self.update()
            self.random_create_note()
            self.draw()
            pg.display.flip() ## 화면 전체를 업데이트

    def frame_set(self):
        if self.frame == 0:
            self.frame = FPS
        self.key_frame_set()
        # self.rate_frame_set()

    
    def key_frame_set(self):
        self.keys[0] += (self.keyset[0] - self.keys[0]) / (3 * (FPS / self.frame))
        self.keys[1] += (self.keyset[1] - self.keys[1]) / (3 * (FPS / self.frame))
        self.keys[2] += (self.keyset[2] - self.keys[2]) / (3 * (FPS / self.frame))

    # def rate_frame_set(self):
    #     if self.Time > self.combo.time():
    #         self.combo

    def draw(self):
        self.background = pg.Surface((WIDTH, HEIGHT))           #white background
        self.background = self.background.convert()
        self.background.fill(BLACK)
        self.screen.blit(self.background, (0,0))
        self.draw_screen()
        self.draw_key()
        self.draw_note()
        self.draw_rate()
        pg.display.update() ## 화면 일부 또는 전체를 업데이트

    def draw_screen(self):
        
        # 플레이 화면 구성
        pg.draw.rect(self.screen, BLACK, (WIDTH / 2 - WIDTH / 8, -int(WIDTH / 100), WIDTH / 4, HEIGHT + int(WIDTH / 50)))

        # 흰색 직사각형 테두리
        pg.draw.rect(self.screen, WHITE, (WIDTH / 2 - WIDTH / 8, -int(WIDTH / 100), WIDTH / 4, HEIGHT + int(WIDTH / 50)), int(WIDTH / 200))

        # [A, S, D] 키 입력시 화면 구성
        # 색상 미 입력시 자동으로 흰색 직사각형 생성
        for i in range(7):
            i += 1
            pg.draw.rect(self.screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (WIDTH / 2 - WIDTH / 8.5 + WIDTH / 32 - (WIDTH / 32) * self.keys[0], (HEIGHT / 12) * 9 - (HEIGHT / 30) * self.keys[0] * i, WIDTH / 12.7 * self.keys[0], (HEIGHT / 35) / i))
        
        for i in range(7):
            i += 1
            pg.draw.rect(self.screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (WIDTH / 2 - WIDTH / 25.8 + WIDTH / 32 - (WIDTH / 32) * self.keys[1], (HEIGHT / 12) * 9 - (HEIGHT / 30) * self.keys[1] * i, WIDTH / 12.7 * self.keys[1], (HEIGHT / 35) / i))
        
        for i in range(7):
            i += 1
            pg.draw.rect(self.screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (WIDTH / 2 + WIDTH / 14.1 - (WIDTH / 32) * self.keys[2], (HEIGHT / 12) * 9 - (HEIGHT / 30) * self.keys[2] * i, WIDTH / 12.7 * self.keys[2], (HEIGHT / 35) / i))

        # 노트 판정 선
        pg.draw.rect(self.screen, BLACK, (WIDTH / 2 - WIDTH / 8, (HEIGHT / 12) * 9, WIDTH / 4, HEIGHT /2))
        pg.draw.rect(self.screen, WHITE, (WIDTH / 2 - WIDTH / 8, (HEIGHT / 12) * 9, WIDTH / 4, HEIGHT), int(HEIGHT / 100))

    def set_note(self, note):
        if note == 1:
            self.noteY = 0
            self.note_time = self.Time + SPEED
            self.note1.append([self.noteY, self.note_time])
        elif note == 2:
            self.noteY = 0
            self.note_time = self.Time + SPEED
            self.note2.append([self.noteY, self.note_time])
        elif note == 3:
            self.noteY = 0
            self.note_time = self.Time + SPEED
            self.note3.append([self.noteY, self.note_time])

    def random_create_note(self):
        if self.Time > 0.2 * self.create_note_time:
            self.create_note_time += 1
            while self.randnote == self.temp_randnote:
                self.randnote = random.randint(1,3)
            self.set_note(self.randnote)
            self.temp_randnote = self.randnote

    def draw_note(self):
        for note_data in self.note1:
            note_data[0] = (HEIGHT / 12) * 9 + (self.Time - note_data[1]) * 350 * SPEED * (HEIGHT / 900)
            pg.draw.rect(self.screen, WHITE, (WIDTH / 2 - WIDTH / 8.5, note_data[0] - HEIGHT / 100, WIDTH / 12.7, HEIGHT / 50))
            if note_data[0] > (HEIGHT / 12.2) * 9:
                self.note1.remove(note_data)

        for note_data in self.note2:
            note_data[0] = (HEIGHT / 12) * 9 + (self.Time - note_data[1]) * 350 * SPEED * (HEIGHT / 900)
            pg.draw.rect(self.screen, WHITE, (WIDTH / 2 - WIDTH / 25.8, note_data[0] - HEIGHT / 100, WIDTH / 12.7, HEIGHT / 50))
            if note_data[0] > (HEIGHT / 12.2) * 9:
                self.note2.remove(note_data)

        for note_data in self.note3:
            note_data[0] = (HEIGHT / 12) * 9 + (self.Time - note_data[1]) * 350 * SPEED * (HEIGHT / 900)
            pg.draw.rect(self.screen, WHITE, (WIDTH / 2 + WIDTH / 25.6, note_data[0] - HEIGHT / 100, WIDTH / 12.7, HEIGHT / 50))
            if note_data[0] > (HEIGHT / 12.2) * 9:
                self.note3.remove(note_data)

    def draw_key(self):
        pg.draw.rect(self.screen, (255 - 100 * self.keys[0],255 - 100 * self.keys[0], 255 - 100 * self.keys[0]), (WIDTH / 2 - WIDTH / 9.7, (HEIGHT / 24) * 19 + (HEIGHT / 48) * self.keys[0], WIDTH / 20, HEIGHT / 8), int(HEIGHT / 150))
        pg.draw.rect(self.screen, (255 - 100 * self.keys[1],255 - 100 * self.keys[1], 255 - 100 * self.keys[1]), (WIDTH / 2 - WIDTH / 42, (HEIGHT / 24) * 19 + (HEIGHT / 48) * self.keys[1], WIDTH / 20, HEIGHT / 8), int(HEIGHT / 150))
        pg.draw.rect(self.screen, (255 - 100 * self.keys[2],255 - 100 * self.keys[2], 255 - 100 * self.keys[2]), (WIDTH / 2 + WIDTH / 18.5, (HEIGHT / 24) * 19 + (HEIGHT / 48) * self.keys[2], WIDTH / 20, HEIGHT / 8), int(HEIGHT / 150))

        # pg.draw.circle(self.screen, (150, 150, 150), (WIDTH / 2, (HEIGHT / 24) * 21), (WIDTH / 20), int(HEIGHT / 200))
        # pg.draw.line(self.screen, (150, 150, 150), (WIDTH / 2 - math.sin(self.spin) * 25 * (WIDTH / 1600), (HEIGHT / 24) * 21 - math.cos(self.spin) * 25 * (WIDTH / 1600)), (WIDTH / 2 + math.sin(self.spin) * 25 * (WIDTH / 1600), (HEIGHT / 24) * 21 + math.cos(self.spin) * 25 * (WIDTH / 1600)), int(WIDTH / 400))
        # self.spin = self.Time * -2


        # pg.draw.rect(self.screen, (255 - 100 * self.keys[1], 255 - 100 * self.keys[1], 255 - 100 * self.keys[1]), (WIDTH / 2 - WIDTH / 50, (HEIGHT / 48) * 39 + (HEIGHT / 48) * self.keys[1], WIDTH / 27, HEIGHT / 8))
        # pg.draw.rect(self.screen, (0,0, 0), (WIDTH / 2 - WIDTH / 50, (HEIGHT / 48) * 43 + (HEIGHT / 48) * (self.keys[1] * 1.2), WIDTH / 27, HEIGHT / 64), int(HEIGHT / 150))
        # pg.draw.rect(self.screen, (50,50, 50), (WIDTH / 2 - WIDTH / 50, (HEIGHT / 48) * 39 + (HEIGHT / 48) * self.keys[1], WIDTH / 27, HEIGHT / 8), int(HEIGHT / 150))

        # pg.draw.rect(self.screen, (255 - 100 * self.keys[2], 255 - 100 * self.keys[2], 255 - 100 * self.keys[2]), (WIDTH / 2 + WIDTH / 58, (HEIGHT / 48) * 39 + (HEIGHT / 48) * self.keys[2], WIDTH / 27, HEIGHT / 8))
        # pg.draw.rect(self.screen, (0,0, 0), (WIDTH / 2 + WIDTH / 58, (HEIGHT / 48) * 43 + (HEIGHT / 48) * (self.keys[2] * 1.2), WIDTH / 27, HEIGHT / 64), int(HEIGHT / 150))
        # pg.draw.rect(self.screen, (50,50, 50), (WIDTH / 2 + WIDTH / 58, (HEIGHT / 48) * 39 + (HEIGHT / 48) * self.keys[2], WIDTH / 27, HEIGHT / 8), int(HEIGHT / 150))

    def draw_rate(self):
        self.perfect_text = self.ingame_font_rate.render(str(self.perfect), False, BLUE)
        self.good_text = self.ingame_font_rate.render(str(self.good), False, GREEN)
        self.miss_text = self.ingame_font_rate.render(str(self.last_combo), False, RED)
        self.rate_text = self.ingame_font_rate.render(str(self.combo), False, WHITE)
        self.rate_text = pg.transform.scale(self.rate_text, (int(WIDTH / 110 * len(self.rate) * self.combo_effect2), int(WIDTH / 58 * self.combo_effect1 * self.combo_effect2)))

        self.screen.blit(self.perfect_text, (WIDTH / 2 - self.perfect_text.get_width() / 2, (HEIGHT / 3) * 2 - self.perfect_text.get_height() / 2))



    # def rating(self, n):
    #     if abs(self.Time - rate_data[n - 1]) < 2 and abs(self.Time - rate_data[n - 1]) >= 1:
    #         last_combo = combo
    #         miss_anim = 1
    #         combo = 0 
    #         combo_effect = 0.2
    #         combo_time = self.Time + 1
    #         combo_effect2 = 1.3
    #         rate = "WORST"
    #     if abs(self.Time - rate_data[n - 1]) < 1 and abs(self.Time - rate_data[n - 1]) >= 0.35:
    #         last_combo = combo
    #         miss_anim = 1
    #         combo = 0 
    #         combo_effect = 0.2
    #         combo_time = self.Time + 1
    #         combo_effect2 = 1.3
    #         rate = "BAD"
    #     if abs(self.Time - rate_data[n - 1]) < 0.35 and abs(self.Time - rate_data[n - 1]) >= 0.07:
    #         combo_effect = 0.2
    #         combo_time = self.Time + 1
    #         combo_effect2 = 1.3
    #         rate = "GOOD"
    #         combo += 1
    #     if abs(self.Time - rate_data[n - 1]) < 0.07 and abs(self.Time - rate_data[n - 1]) >= 0.035:
    #         combo_effect = 0.2
    #         combo_time = self.Time + 1
    #         combo_effect2 = 1.3
    #         rate = "GREAT"
    #         combo += 1
    #     if abs(self.Time - rate_data[n - 1]) < 0.035 and abs(self.Time - rate_data[n - 1]) >= 0:
    #         combo_effect = 0.2
    #         combo_time = self.Time + 1
    #         combo_effect2 = 1.3
    #         rate = "PERFECT"
    #         combo += 1



    def update(self):
        # self.all_sprites.update()
        self.game_tick = pg.time.get_ticks() - self.start_tick

    def events(self):
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
                    if len(self.note1) > 0:
                        if self.note1[0][0] > (HEIGHT / 12) * 9:
                            del self.note1[0]
                if event.key == pg.K_s:
                    self.keyset[1] = 1
                    if len(self.note2) > 0:
                        if self.note2[0][0] > (HEIGHT / 12) * 9:
                            del self.note2[0]
                if event.key == pg.K_d:
                    self.keyset[2] = 1
                    if len(self.note3) > 0:
                        if self.note3[0][0] > (HEIGHT / 12) * 9:
                            del self.note3[0]

            if event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    self.keyset[0] = 0
                if event.key == pg.K_s:
                    self.keyset[1] = 0
                if event.key == pg.K_d:
                    self.keyset[2] = 0

game = Game()

while game.running:
    game.run()

pg.quit()
