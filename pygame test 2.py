import pygame as pg
import os
import sys
import time
import math
import random

# cv
import numpy as np
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt

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
YELLOW = (242, 182, 80)
GRAY = (115, 115, 115)
BLACK = (0, 0, 0)
# ALPHA_MAX = 255


### note setting
NOTE = (HEIGHT / 40)


### play setting
PLAY_X = WIDTH / 2 - WIDTH / 3
PLAY_Y = -int(WIDTH / 100)
PLAY_WIDTH = WIDTH / 1.5
PLAY_HEIGHT = HEIGHT + int(WIDTH / 50)
PLAY_COLOR = (130, 105, 236)
PLAY_COLOR_HEIGHT = PLAY_HEIGHT - 165
PLAY_LINE = int(WIDTH / 200)


### hit setting
HIT_Y = (HEIGHT / 12) * 10
HIT_HEIGHT = NOTE + 30
HIT_LINE = int(WIDTH / 400)
HIT_COLOR = (100, 100, 135)

### key setting
KEY_EFFECT_WIDTH = WIDTH / 4.61
KEY_EFFECT_HEIGHT = HEIGHT / 15
KEY_EFFECT_FIRST_X = PLAY_X + PLAY_LINE
KEY_EFFECT_SECOND_X = KEY_EFFECT_FIRST_X + KEY_EFFECT_WIDTH + 5
KEY_EFFECT_THIRD_X = KEY_EFFECT_SECOND_X + KEY_EFFECT_WIDTH + 5
KEY_EFFECT_Y = HIT_Y + 50

### time setting
SPEED = 2

### rating setting
PERFECT = "PERFECT"
GREAT = "GREAT"
GOOD = "GOOD"
BAD = "BAD"
MISS = "MISS"

### score setting
SCORE = 0

### rank setting
RANK_SS = "S+"
RANK_S = "S"
RANK_A = "A"
RANK_B = "B"
RANK_C = "C"
RANK_F = "F"

### life setting
LIFE = 100
### cam setting
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# 웹캠, 영상 파일의 경우 이것을 사용하세요.:
cap = cv2.VideoCapture(0)
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
a = w//3 
hi = h//3

hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)


class Game:
    # 프로그램 실행
    def __init__(self):
        pg.init()
        pg.font.init()
        pg.mixer.init() # 음악 사용하는 경우
        pg.display.set_caption(TITLE) # 제목 표시
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # 화면 표시
        # self.screen_mode = 0 #screen mode (0: logo, 1: logo2, 2: main, 3: stage select, 4: play, 5: score)
        # # self.screen_value = [-ALPHA_MAX, 0, 0, 0]       #screen management value
        self.clock = pg.time.Clock()        #FPS timer
        self.start_tick = 0     #game timer
        self.running = True     #game initialize Boolean value
        self.frame = self.clock.get_fps() # 현재 fps
        
        ### note time setting
        self.start_time = time.time()

        ### combo setting
        self.combo = 0
        self.combo_effect1 = 0
        self.combo_effect2 = 0
        self.last_combo = 0
        self.rate = ""
        self.rate_text = ""
        self.miss_animation = 0
        self.miss_count = 0
        self.rate_data = [0, 0, 0]

        ### key setting
        self.keys = [0, 0, 0]
        self.keyset = [0, 0, 0]

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
        self.ingame_font_combo = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int(WIDTH / 38))
        self.ingame_font_miss = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int(WIDTH / 38))


        # self.song_select = 1    #select song
        # self.load_date()        #data loading
        # self.new()

    def run(self):
        self.playing = True

        while self.playing:
            success, image = cap.read()
            if not success:
                print("카메라를 찾을 수 없습니다.")
                # 동영상을 불러올 경우는 'continue' 대신 'break'를 사용합니다.
                continue
            self.Time = time.time() - self.start_time
            self.combo_time = self.Time + 1
            self.clock.tick(FPS)
            self.events()
            self.frame_set()
            self.update()
            self.random_create_note()
            self.draw()
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            image= pg.surfarray.make_surface(image)
            image = pg.transform.rotate(image,-90)
            self.screen.blit(image,(250,0))
            pg.display.update()
            pg.display.flip() ## 화면 전체를 업데이트

    def frame_set(self):
        if self.frame == 0:
            self.frame = FPS
        self.key_frame_set()
        self.rate_frame_set()

    
    def key_frame_set(self):
        self.keys[0] += (self.keyset[0] - self.keys[0]) / (3 * (FPS / self.frame))
        self.keys[1] += (self.keyset[1] - self.keys[1]) / (3 * (FPS / self.frame))
        self.keys[2] += (self.keyset[2] - self.keys[2]) / (3 * (FPS / self.frame))

    def rate_frame_set(self):
        if self.Time > self.combo_time:
            self.combo_effect1 += (0 - self.combo_effect1) / (7 * (FPS / self.frame))

        if self.Time < self.combo_time:
            self.combo_effect1 += (1 - self.combo_effect1) / (7 * (FPS / self.frame))

        self.combo_effect2 += (2 - self.combo_effect2) / (7 *(FPS / self.frame))

        self.miss_animation += (4 - self.miss_animation) / (14 * FPS / self.frame)

    def draw(self):
        self.background = pg.Surface((WIDTH, HEIGHT))           #white background
        self.background = self.background.convert()
        self.background.fill(BLACK)
        self.screen.blit(self.background, (0,0))
        self.draw_screen()
        # self.draw_key()
        self.draw_note()
        self.draw_rate()
        pg.display.update() ## 화면 일부 또는 전체를 업데이트

    def draw_screen(self):
        
        # 플레이 화면 구성
        pg.draw.rect(self.screen, BLACK, (PLAY_X, HIT_Y, PLAY_WIDTH, HEIGHT / 2))
        # 노트 판정 선
        pg.draw.rect(self.screen, HIT_COLOR, (PLAY_X, HIT_Y + 40, PLAY_WIDTH, HIT_HEIGHT + 30), 0)
        pg.draw.rect(self.screen, BLACK, (PLAY_X, PLAY_Y, PLAY_WIDTH, PLAY_COLOR_HEIGHT))

        # 판정 선
        pg.draw.rect(self.screen, PLAY_COLOR, (PLAY_X, PLAY_Y, PLAY_WIDTH, PLAY_HEIGHT), HIT_LINE)


        # [A, S, D] 키 입력시 화면 구성
        # 색상 미 입력시 자동으로 흰색 직사각형 생성
        # 키 입력시 이펙트 생성
        for i in range(4):
            i += 1
            pg.draw.rect(self.screen, (130 - (6 * i), 105 - (2 * i), 235 - (25 * i)), (KEY_EFFECT_FIRST_X *  self.keys[0], KEY_EFFECT_Y + 90 - (HEIGHT / 15) * i * self.keys[0], KEY_EFFECT_WIDTH , KEY_EFFECT_HEIGHT / i * self.keys[0]))
        
        for i in range(4):
            i += 1
            pg.draw.rect(self.screen, (130 - (6 * i), 105 - (15 * i), 235 - (25 * i)), (KEY_EFFECT_SECOND_X, KEY_EFFECT_Y + 90 - (HEIGHT / 15) * i * self.keys[1], KEY_EFFECT_WIDTH , KEY_EFFECT_HEIGHT / i * self.keys[1]))
        
        for i in range(4):
            i += 1
            pg.draw.rect(self.screen, (130 - (6 * i), 105 - (15 * i), 235 - (25 * i)), (KEY_EFFECT_THIRD_X, KEY_EFFECT_Y + 90 - (HEIGHT / 15) * i * self.keys[2], KEY_EFFECT_WIDTH , KEY_EFFECT_HEIGHT / i * self.keys[2]))

        # 키 입력 선
        # pg.draw.rect(self.screen, BLACK, (PLAY_X, HIT_Y, PLAY_WIDTH, HEIGHT / 2))
        # pg.draw.rect(self.screen, WHITE, (PLAY_X, HIT_Y, PLAY_WIDTH, HEIGHT / 2), HIT_LINE)


    # 노트의 Y축 좌표 값과 생성 시간을 각 노트별 배열에 추가
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
        if self.Time > 0.3 * self.create_note_time: # 노트 생성 주기
            self.create_note_time += 1
            while self.randnote == self.temp_randnote:
                self.randnote = random.randint(1,3)
            self.set_note(self.randnote) # 노트 생성
            self.temp_randnote = self.randnote

    def draw_note(self):
        for note_data in self.note1:
            # 노트가 내려오도록 함
            note_data[0] = (HEIGHT / 12) * 9 + (self.Time - note_data[1]) * 350 * SPEED * (HEIGHT / 900)
            # 노트 표현
            pg.draw.rect(self.screen, PLAY_COLOR, (WIDTH / 2 - WIDTH / 8.5, note_data[0] - HEIGHT / 100, WIDTH / 12.7, NOTE))
            # MISS 노트 삭제
            if note_data[0] > (HEIGHT / 12.1) * 9:
                self.last_combo = self.combo
                self.miss_animation = 1
                self.combo = 0 
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = MISS
                self.miss_count += 1
                self.note1.remove(note_data)

        for note_data in self.note2:
            note_data[0] = (HEIGHT / 12) * 9 + (self.Time - note_data[1]) * 350 * SPEED * (HEIGHT / 900)
            pg.draw.rect(self.screen, PLAY_COLOR, (WIDTH / 2 - WIDTH / 25.8, note_data[0] - HEIGHT / 100, WIDTH / 12.7, NOTE))
            if note_data[0] > (HEIGHT / 12.1) * 9:
                self.last_combo = self.combo
                self.miss_animation = 1
                self.combo = 0 
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = MISS
                self.miss_count += 1
                self.note2.remove(note_data)

        for note_data in self.note3:
            note_data[0] = (HEIGHT / 12) * 9 + (self.Time - note_data[1]) * 350 * SPEED * (HEIGHT / 900)
            pg.draw.rect(self.screen, PLAY_COLOR, (WIDTH / 2 + WIDTH / 25.6, note_data[0] - HEIGHT / 100, WIDTH / 12.7, NOTE))
            if note_data[0] > (HEIGHT / 12.1) * 9:
                self.last_combo = self.combo
                self.miss_animation = 1
                self.combo = 0 
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = MISS
                self.miss_count += 1
                self.note3.remove(note_data)

# 임시 잠금
    # def draw_key(self):
    #     pg.draw.rect(self.screen, (255 - 100 * self.keys[0],255 - 100 * self.keys[0], 255 - 100 * self.keys[0]), (WIDTH / 2 - WIDTH / 9.7, (HEIGHT / 24) * 19 + (HEIGHT / 48) * self.keys[0], WIDTH / 20, HEIGHT / 8), int(HEIGHT / 150))
    #     pg.draw.rect(self.screen, (255 - 100 * self.keys[1],255 - 100 * self.keys[1], 255 - 100 * self.keys[1]), (WIDTH / 2 - WIDTH / 42, (HEIGHT / 24) * 19 + (HEIGHT / 48) * self.keys[1], WIDTH / 20, HEIGHT / 8), int(HEIGHT / 150))
    #     pg.draw.rect(self.screen, (255 - 100 * self.keys[2],255 - 100 * self.keys[2], 255 - 100 * self.keys[2]), (WIDTH / 2 + WIDTH / 18.5, (HEIGHT / 24) * 19 + (HEIGHT / 48) * self.keys[2], WIDTH / 20, HEIGHT / 8), int(HEIGHT / 150))

    #     # pg.draw.circle(self.screen, (150, 150, 150), (WIDTH / 2, (HEIGHT / 24) * 21), (WIDTH / 20), int(HEIGHT / 200))
    #     # pg.draw.line(self.screen, (150, 150, 150), (WIDTH / 2 - math.sin(self.spin) * 25 * (WIDTH / 1600), (HEIGHT / 24) * 21 - math.cos(self.spin) * 25 * (WIDTH / 1600)), (WIDTH / 2 + math.sin(self.spin) * 25 * (WIDTH / 1600), (HEIGHT / 24) * 21 + math.cos(self.spin) * 25 * (WIDTH / 1600)), int(WIDTH / 400))
    #     # self.spin = self.Time * -2


    #     # pg.draw.rect(self.screen, (255 - 100 * self.keys[1], 255 - 100 * self.keys[1], 255 - 100 * self.keys[1]), (WIDTH / 2 - WIDTH / 50, (HEIGHT / 48) * 39 + (HEIGHT / 48) * self.keys[1], WIDTH / 27, HEIGHT / 8))
    #     # pg.draw.rect(self.screen, (0,0, 0), (WIDTH / 2 - WIDTH / 50, (HEIGHT / 48) * 43 + (HEIGHT / 48) * (self.keys[1] * 1.2), WIDTH / 27, HEIGHT / 64), int(HEIGHT / 150))
    #     # pg.draw.rect(self.screen, (50,50, 50), (WIDTH / 2 - WIDTH / 50, (HEIGHT / 48) * 39 + (HEIGHT / 48) * self.keys[1], WIDTH / 27, HEIGHT / 8), int(HEIGHT / 150))

    #     # pg.draw.rect(self.screen, (255 - 100 * self.keys[2], 255 - 100 * self.keys[2], 255 - 100 * self.keys[2]), (WIDTH / 2 + WIDTH / 58, (HEIGHT / 48) * 39 + (HEIGHT / 48) * self.keys[2], WIDTH / 27, HEIGHT / 8))
    #     # pg.draw.rect(self.screen, (0,0, 0), (WIDTH / 2 + WIDTH / 58, (HEIGHT / 48) * 43 + (HEIGHT / 48) * (self.keys[2] * 1.2), WIDTH / 27, HEIGHT / 64), int(HEIGHT / 150))
    #     # pg.draw.rect(self.screen, (50,50, 50), (WIDTH / 2 + WIDTH / 58, (HEIGHT / 48) * 39 + (HEIGHT / 48) * self.keys[2], WIDTH / 27, HEIGHT / 8), int(HEIGHT / 150))

    def draw_rate(self):
        self.ingame_font_combo = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int((WIDTH / 38) * self.combo_effect2))
        self.ingame_font_miss = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int((WIDTH / 38) * self.miss_animation))
        self.combo_text = self.ingame_font_combo.render(str(self.combo), False, WHITE)
        self.miss_text = self.ingame_font_rate.render(str(self.last_combo), False, RED)
        # self.perfect_text = self.ingame_font_rate.render(str(PERFECT), False, BLUE)
        # # self.perfect_text = pg.transform.scale(self.perfect_text, (int(WIDTH / 110 * len(self.rate) * self.combo_effect2), int(WIDTH / 58 * self.combo_effect1 * self.combo_effect2)))
        # self.great_text = self.ingame_font_rate.render(str(GREAT),False, GREEN)
        # # self.great_text = pg.transform.scale(self.great_text, (int(WIDTH / 110 * len(self.rate) * self.combo_effect2), int(WIDTH / 58 * self.combo_effect1 * self.combo_effect2)))
        # self.good_text = self.ingame_font_rate.render(str(GOOD), False, YELLOW)
        # # self.good_text = pg.transform.scale(self.good_text, (int(WIDTH / 110 * len(self.rate) * self.combo_effect2), int(WIDTH / 58 * self.combo_effect1 * self.combo_effect2)))
        # self.bad_text = self.ingame_font_rate.render(str(BAD), False, RED)
        # # self.bad_text = pg.transform.scale(self.bad_text, (int(WIDTH / 110 * len(self.rate) * self.combo_effect2), int(WIDTH / 58 * self.combo_effect1 * self.combo_effect2)))
        # self.miss_text = self.ingame_font_rate.render(str(MISS), False, GRAY)
        # self.miss_text = pg.transform.scale(self.miss_text, (int(WIDTH / 110 * len(self.rate) * self.combo_effect2), int(WIDTH / 58 * self.combo_effect1 * self.combo_effect2)))
        self.rate_text = self.ingame_font_rate.render(str(self.rate), False, WHITE)
        if (self.rate == PERFECT):
            self.rate_text = self.ingame_font_rate.render(str(PERFECT), False, BLUE)
            # self.rate_text = pg.transform.scale(self.perfect_text, (int(WIDTH / 110 * len(self.rate) * self.combo_effect2), int(WIDTH / 58 * self.combo_effect1 * self.combo_effect2)))
        elif (self.rate == GREAT):
            self.rate_text = self.ingame_font_rate.render(str(GREAT),False, GREEN)
            # self.rate_text = pg.transform.scale(self.great_text, (int(WIDTH / 110 * len(self.rate) * self.combo_effect2), int(WIDTH / 58 * self.combo_effect1 * self.combo_effect2)))
        elif (self.rate == GOOD):
            self.rate_text = self.ingame_font_rate.render(str(GOOD), False, YELLOW)
            # self.rate_text = pg.transform.scale(self.good_text, (int(WIDTH / 110 * len(self.rate) * self.combo_effect2), int(WIDTH / 58 * self.combo_effect1 * self.combo_effect2)))
        elif (self.rate == BAD):
            self.rate_text = self.ingame_font_rate.render(str(BAD), False, RED)
            # self.rate_text = pg.transform.scale(self.bad_text, (int(WIDTH / 110 * len(self.rate) * self.combo_effect2), int(WIDTH / 58 * self.combo_effect1 * self.combo_effect2)))
        elif (self.rate == MISS):
            self.rate_text = self.ingame_font_rate.render(str(MISS), False, GRAY)
            # self.rate_text = pg.transform.scale(self.miss_text, (int(WIDTH / 110 * len(self.rate) * self.combo_effect2), int(WIDTH / 58 * self.combo_effect1 * self.combo_effect2)))
        # self.rate_text = pg.transform.scale(self.rate_text, (int(WIDTH / 110 * len(self.rate) * self.combo_effect2), int(WIDTH / 58 * self.combo_effect1 * self.combo_effect2)))

        self.miss_text.set_alpha(255 - (255 / 4) * self.miss_animation)
        if self.combo != 0:
            self.screen.blit(self.combo_text, (WIDTH / 2 - self.combo_text.get_width() / 2, (HEIGHT / 12) * 4 - self.combo_text.get_height() / 2))
        self.rate_text = pg.transform.scale(self.rate_text, (int(WIDTH / 110 * len(self.rate) * self.combo_effect2), int(WIDTH / 58 * self.combo_effect1 * self.combo_effect2)))
        if self.miss_count == 1:
            self.screen.blit(self.miss_text, (WIDTH / 2 - self.miss_text.get_width() / 2, (HEIGHT / 12) * 4 - self.miss_text.get_height() / 2))

        self.screen.blit(self.rate_text, (WIDTH / 2 - self.rate_text.get_width() / 2, (HEIGHT / 12) * 8 - self.rate_text.get_height() / 2))


    def rating(self, n):
        if abs(self.Time - self.rate_data[n - 1]) < 2 and abs(self.Time - self.rate_data[n - 1]) >= 0.7:
            self.miss_count = 1
            self.rate = ""

        if abs(self.Time - self.rate_data[n - 1]) < 0.3 and abs(self.Time - self.rate_data[n - 1]) >= 0.2:
            self.combo_effect1 = 0.2
            self.combo_time = self.Time + 1
            self.combo_effect2 = 1.3
            self.rate = BAD
            self.miss_count = 0
            self.combo += 1
            

        if abs(self.Time - self.rate_data[n - 1]) < 0.2 and abs(self.Time - self.rate_data[n - 1]) >= 0.15:
            self.combo_effect1 = 0.2
            self.combo_time = self.Time + 1
            self.combo_effect2 = 1.3
            self.rate = GOOD
            self.miss_count = 0
            self.combo += 1

        if abs(self.Time - self.rate_data[n - 1]) < 0.15 and abs(self.Time - self.rate_data[n - 1]) >= 0.1:
            self.combo_effect1 = 0.2
            self.combo_time = self.Time + 1
            self.combo_effect2 = 1.3
            self.rate = GREAT
            self.miss_count = 0
            self.combo += 1

        if abs(self.Time - self.rate_data[n - 1]) < 0.1 and abs(self.Time - self.rate_data[n - 1]) >= 0:
            self.combo_effect1 = 0.2
            self.combo_time = self.Time + 1
            self.combo_effect2 = 1.3
            self.rate = PERFECT
            self.miss_count = 0
            self.combo += 1


    def rating_data(self):
        if len(self.note1) > 0:
            self.rate_data[0] = self.note1[0][1]
        if len(self.note2) > 0:
            self.rate_data[1] = self.note2[0][1]
        if len(self.note3) > 0:
            self.rate_data[2] = self.note3[0][1]

        

    def update(self):
        # self.all_sprites.update()
        self.game_tick = pg.time.get_ticks() - self.start_tick

    def events(self):
        for event in pg.event.get():
            # 게임 종료
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing, self.running = False, False

            # 키 입력
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing, self.running = False, False
                if event.key == pg.K_a:
                    self.keyset[0] = 1
                    if len(self.note1) > 0:
                        self.rating_data()
                        self.rating(1)
                        if self.note1[0][0] > (HEIGHT / 15) * 9:
                            del self.note1[0]
                if event.key == pg.K_s:
                    self.keyset[1] = 1
                    if len(self.note2) > 0:
                        self.rating_data()
                        self.rating(2)
                        if self.note2[0][0] > (HEIGHT / 15) * 9:
                            del self.note2[0]
                if event.key == pg.K_d:
                    self.keyset[2] = 1
                    if len(self.note3) > 0:
                        self.rating_data()
                        self.rating(3)
                        if self.note3[0][0] > (HEIGHT / 15) * 9:
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