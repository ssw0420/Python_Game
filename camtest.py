# game
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

FPS = 60

# 프레임 간격 (16ms = 1000ms / 60)
FRAME_INTERVAL = 16

### color setting
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
RED = (246, 36, 74)
BLUE = (32, 105, 246)
YELLOW = (242, 182, 80)
GRAY = (115, 115, 115)
BLACK = (0, 0, 0)
# ALPHA_MAX = 255

### play setting
PLAY_COLOR = (130, 105, 236)


### note setting

NOTE_COLOR = (120, 150, 200)

### hit setting

HIT_COLOR = (50, 50, 50)


### key setting


### font setting

COMBO_COLOR = (80, 40, 140)




### speed, time setting
SPEED = 5

### rating setting
PERFECT = "PERFECT"
GREAT = "GREAT"
GOOD = "GOOD"
BAD = "BAD"
MISS = "MISS"

### hit line setting


### score setting
SCORE = 0

# ### rank setting
# RANK_SS = "S+"
# RANK_S = "S"
# RANK_A = "A"
# RANK_B = "B"
# RANK_C = "C"
# RANK_F = "F"

### life setting
LIFE_COLOR = (160, 155, 240)

### cam setting
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# 웹캠, 영상 파일의 경우 이것을 사용하세요.:
cap = cv2.VideoCapture(0)
# w = cap.get(cv2.CAP_PROP_FRAME_self.width)
# h = cap.get(cv2.CAP_PROP_FRAME_self.height)
# a = w//3 
# hi = h//3
# 동영상 크기 변환
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # 가로
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # 세로

# 변환된 동영상 크기 정보
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
a = w//3 
hi = h//3

hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# 영상 제작
# fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# out = cv2.VideoWriter('output.avi', fourcc, 30.0, (int(w), int(h)))


class Game:
    # 프로그램 실행
    def __init__(self):
        pg.init()
        pg.font.init()
        # pg.mixer.init() # 음악 사용하는 경우
        pg.display.set_caption(TITLE) # 제목 표시
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN) # 화면 표시
        # self.screen_mode = 0 #screen mode (0: logo, 1: logo2, 2: main, 3: stage select, 4: play, 5: score)
        # # self.screen_value = [-ALPHA_MAX, 0, 0, 0]       #screen management value
        self.width, self.height = self.screen.get_size()
        print(self.width, self.height)

        self.play_x = self.width / 2 - self.width / 3
        print(self.play_x)
        self.play_y = -int(self.width / 100)
        print(self.play_y)
        self.play_width = self.width / 1.505
        print(self.play_width)
        self.play_height = self.height + int(self.width / 50)
        print(self.play_height)
        self.play_line = int(self.width / 200)
        print(self.play_line)
        self.note_height = (self.height / 30)
        print(self.note_height)
        self.note_width = self.width / 4.61
        print(self.note_width)
        self.note_first_x = self.play_x + self.play_line
        print(self.note_first_x)
        self.note_second_x = self.note_first_x + self.note_width + 3
        print(self.note_second_x)
        self.note_third_x = self.note_second_x + self.note_width + 3
        print(self.note_third_x)

        self.hit_y = (self.height / 12) * 10
        print(self.hit_y)
        self.hit_height = self.note_height + 30
        print(self.hit_height)
        self.hit_line = int(self.width / 400)
        print(self.hit_line)
        self.play_color_height = self.play_height - self.hit_height
        print(self.play_color_height)

        self.key_effect_width = self.width / 4.61
        print(self.key_effect_width)
        self.key_effect_height = self.height / 33
        print(self.key_effect_height)
        self.key_effect_first_x = self.play_x + self.play_line
        print(self.key_effect_first_x)
        self.key_effect_second_x = self.key_effect_first_x + self.key_effect_width + 5
        print(self.key_effect_second_x)
        self.key_effect_third_x = self.key_effect_second_x + self.key_effect_width + 5
        print(self.key_effect_third_x)
        self.key_effect_y = self.hit_y + 50
        print(self.key_effect_y)

        self.font_y = (self.height / 12)
        print(self.font_y)
        self.note_end_y = self.height
        print(self.note_end_y)

        self.hit_end_line = self.hit_y + 40 + self.hit_height + 30
        print(self.hit_end_line)
        self.perfect_hit_line = self.hit_y
        print(self.perfect_hit_line)
        self.great_hit_line = self.hit_y * (0.85)
        print(self.great_hit_line)
        self.good_hit_line = self.hit_y * (0.83)
        print(self.good_hit_line)
        self.bad_hit_line = self.hit_y * (0.8)
        print(self.bad_hit_line)
        
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

        ### score setting
        self.score = 0

        ### life setting
        self.life = 10

        ### path setting
        self.Cpath = os.path.dirname(__file__)
        self.FontPath = os.path.join(self.Cpath,"font")

        ### font setting
        self.ingame_font_rate = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int(self.width / 23))
        self.ingame_font_combo = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int(self.width / 38))
        self.ingame_font_miss = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int(self.width / 38))
        self.ingame_font_score = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int(self.width / 48))
        self.ingame_font_score_eng = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int(self.width / 48))
        self.ingame_font_life_eng = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int(self.width / 48))

        ### background setting
        self.background = pg.Surface((0, 0), pg.FULLSCREEN)           #white background
        self.background = self.background.convert()
        self.background.fill(BLACK)
        self.screen.blit(self.background, (0,0))


        # self.song_select = 1    #select song
        # self.load_date()        #data loading
        # self.new()

    def run(self):
        self.playing = True

        while self.playing:
            success, self.image = cap.read()
            if not success:
                print("카메라를 찾을 수 없습니다.")
                # 동영상을 불러올 경우는 'continue' 대신 'break'를 사용합니다.
                continue
            self.image.flags.writeable = False
            self.results = hands.process(self.image)
            # self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            # self.image = cv2.flip(self.image,1)
            cv2.line(self.image, (int(a), 0), (int(a), int(h)), (0, 0, 0), 2)
            cv2.line(self.image, (int(2 * a), 0), (int(2 * a), int(h)), (0, 0, 0), 2)
            cv2.line(self.image, (0, int(hi * 2)), (int(w), int(hi * 2)), (0, 0, 0), 2)
            self.Time = time.time() - self.start_time
            self.combo_time = self.Time + 1
            self.dt = self.clock.tick(FPS)
            self.events()
            self.frame_set()
            # self.update()
            self.random_create_note()
            self.draw()
            # pg.display.update(self.image)
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
        self.draw_screen()
        self.draw_cam()
        self.draw_play_line()
        # self.draw_key()
        self.draw_effect()
        self.draw_note()
        self.draw_rate()
        self.draw_score()
        self.draw_life()
        # pg.display.update() ## 화면 일부 또는 전체를 업데이트

    def draw_screen(self):        
        # 플레이 전체 화면
        pg.draw.rect(self.screen, BLACK, (self.play_x, self.play_y, self.play_width, self.play_color_height))


        # 플레이 화면 구성
        pg.draw.rect(self.screen, BLACK, (self.play_x, self.hit_y + 40 + self.hit_height + 30, self.play_width, self.height / 2))


    def draw_play_line(self):
        # 노트 판정 선
        pg.draw.rect(self.screen, HIT_COLOR, (self.play_x, self.hit_y + 40, self.play_width, self.hit_height + 30), 0)

        # 플레이 양측 끝 선
        pg.draw.rect(self.screen, PLAY_COLOR, (self.play_x, self.play_y, self.play_width, self.play_height), self.hit_line)

        # 3분할 선
        pg.draw.line(self.screen, GRAY, [self.note_first_x + self.note_width + 1, 0],[self.note_first_x + self.note_width + 1, self.height], 1)
        pg.draw.line(self.screen, GRAY, [self.note_second_x + self.note_width + 1, 0],[self.note_second_x + self.note_width + 1, self.height], 1)




        # 키 입력 선
        # pg.draw.rect(self.screen, BLACK, (self.play_x, self.hit_y, self.play_self.width, self.height / 2))
        # pg.draw.rect(self.screen, WHITE, (self.play_x, self.hit_y, self.play_self.width, self.height / 2), self.hit_line)

    def draw_effect(self):
                # [A, S, D] 키 입력시 화면 구성
        # 색상 미 입력시 자동으로 흰색 직사각형 생성
        # 키 입력시 이펙트 생성
        for i in range(5):
            i += 1
            pg.draw.rect(self.screen, (115 - (6 * i), 90 - (15 * i), 220 - (25 * i)), (self.key_effect_first_x, self.key_effect_y + 110 - (self.height / 25) * i * self.keys[0], self.key_effect_width, self.key_effect_height / i * self.keys[0]))
        
        for i in range(5):
            i += 1
            pg.draw.rect(self.screen, (115 - (6 * i), 90 - (15 * i), 220 - (25 * i)), (self.key_effect_second_x, self.key_effect_y + 110 - (self.height / 25) * i * self.keys[1], self.key_effect_width, self.key_effect_height / i * self.keys[1]))
        
        for i in range(5):
            i += 1
            pg.draw.rect(self.screen, (115 - (6 * i), 90 - (15 * i), 220 - (25 * i)), (self.key_effect_third_x, self.key_effect_y + 110 - (self.height / 25) * i * self.keys[2], self.key_effect_width, self.key_effect_height / i * self.keys[2]))

    def draw_cam(self):
            # self.image.flags.writeable = False
            # # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # self.image = cv2.flip(self.image,1)
            # self.results = hands.process(self.image)
            self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
            self.image = pg.surfarray.make_surface(self.image)
            self.image = pg.transform.rotate(self.image,-90)

            # self.image.flags.writeable = True
            # if self.results.multi_hand_landmarks:
            #     for hand_landmarks in self.results.multi_hand_landmarks:
            #         mp_drawing.draw_landmarks(
            #             self.image,
            #             hand_landmarks,
            #             mp_hands.HAND_CONNECTIONS,
            #             mp_drawing_styles.get_default_hand_landmarks_style(),
            #             mp_drawing_styles.get_default_hand_connections_style())
            # out.write(self.image)
            
            self.screen.blit(self.image,(self.play_x, self.height / 2 - 300))
            #보기 편하게 이미지를 좌우 반전합니다.
            
            # cv2.imshow(cv2.flip(self.image, 1))
            # out.write(self.image)

    def draw_score(self):
        self.score_box = pg.draw.rect(self.screen, BLACK, (self.play_x + self.play_width + 10, 255, 310, 500))
        self.score_box_edge = pg.draw.rect(self.screen, PLAY_COLOR, (self.play_x + self.play_width + 10, 255, 310, 500), 2)
        self.score_text = self.ingame_font_score.render(str(self.score), False, WHITE)
        self.score_text_eng = self.ingame_font_score_eng.render("SCORE", False, WHITE)
        self.screen.blit(self.score_text_eng, (self.play_x + self.play_width + 170 - self.score_text_eng.get_width() / 2, 280 - self.score_text_eng.get_height() / 2))
        self.screen.blit(self.score_text, (self.play_x + self.play_width + 240 - self.score_text.get_width() / 2, 350 - self.score_text.get_height() / 2))
        
    def draw_life(self):
        self.life_text_eng = self.ingame_font_life_eng.render("LIFE", False, WHITE)
        self.screen.blit(self.life_text_eng, (self.play_x + self.play_width + 170 - self.life_text_eng.get_width() / 2, 450 - self.life_text_eng.get_height() / 2))
        for i in range (self.life):
            self.life_box = pg.draw.rect(self.screen, (245 - (i * 18), 35 + (i * 5), 75 + (i * 8)), (self.play_x + self.play_width + 45 + (i * 25), 500, 25, 30))
        pg.display.update(self.life_box)

    # 노트의 Y축 좌표 값과 생성 시간을 각 노트별 배열에 추가
    def set_note(self, note):
        if note == 1:
            self.noteY = 0
            self.note_time = self.Time
            # 1번 줄의 모든 노트의 정보를 가지는 배열 : note1
            self.note1.append([self.noteY, self.note_time])
        elif note == 2:
            self.noteY = 0
            self.note_time = self.Time
            self.note2.append([self.noteY, self.note_time])
        elif note == 3:
            self.noteY = 0
            self.note_time = self.Time
            self.note3.append([self.noteY, self.note_time])

    def random_create_note(self):
        if self.Time > 3 and self.Time - 3 > 1.1 * self.create_note_time: # 노트 생성 주기
            self.create_note_time += 1
            while self.randnote == self.temp_randnote:
                self.randnote = random.randint(1,3)
            self.set_note(self.randnote) # 노트 생성
            self.temp_randnote = self.randnote

    def draw_note(self):
        self.speed_per_second = SPEED * (self.dt / 10)
        for note_data in self.note1:
            # 노트가 내려오도록 함
            # 각 노트별 Y 좌표 : note_data[0] -> 이를 변경시킴으로써 note의 위치를 이동시킴
            # note_data[0] = (self.Time - note_data[1]) * 350 * SPEED * (self.height / 900)
            note_data[0] += self.speed_per_second
            # 노트 표현
            self.note1_rect = pg.draw.rect(self.screen, NOTE_COLOR, (self.note_first_x, note_data[0], self.note_width, self.note_height))
            pg.display.update(self.note1_rect)
            # MISS 노트 삭제
            if note_data[0] > self.note_end_y:
                self.last_combo = self.combo
                self.miss_animation = 1
                self.combo = 0
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = MISS
                self.miss_count += 1
                self.life -= 1
                self.note1.remove(note_data)

        for note_data in self.note2:
            # self.height -> 노트 도달 위치
            # note_data[0] += (0.5 * FPS)
            note_data[0] += self.speed_per_second
            self.note2_rect = pg.draw.rect(self.screen, NOTE_COLOR, (self.note_second_x, note_data[0], self.note_width, self.note_height))
            pg.display.update(self.note2_rect)
            if note_data[0] > self.note_end_y:
                self.last_combo = self.combo
                self.miss_animation = 1
                self.combo = 0
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = MISS
                self.miss_count += 1
                self.life -= 1
                self.note2.remove(note_data)

        for note_data in self.note3:
            note_data[0] += self.speed_per_second
            self.note3_rect = pg.draw.rect(self.screen, NOTE_COLOR, (self.note_third_x, note_data[0], self.note_width, self.note_height))
            pg.display.update(self.note3_rect)
            if note_data[0] > self.note_end_y:
                self.last_combo = self.combo
                self.miss_animation = 1
                self.combo = 0
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = MISS
                self.miss_count += 1
                self.life -= 1
                self.note3.remove(note_data)

# 임시 잠금
    # def draw_key(self):
    #     pg.draw.rect(self.screen, (255 - 100 * self.keys[0],255 - 100 * self.keys[0], 255 - 100 * self.keys[0]), (self.width / 2 - self.width / 9.7, (self.height / 24) * 19 + (self.height / 48) * self.keys[0], self.width / 20, self.height / 8), int(self.height / 150))
    #     pg.draw.rect(self.screen, (255 - 100 * self.keys[1],255 - 100 * self.keys[1], 255 - 100 * self.keys[1]), (self.width / 2 - self.width / 42, (self.height / 24) * 19 + (self.height / 48) * self.keys[1], self.width / 20, self.height / 8), int(self.height / 150))
    #     pg.draw.rect(self.screen, (255 - 100 * self.keys[2],255 - 100 * self.keys[2], 255 - 100 * self.keys[2]), (self.width / 2 + self.width / 18.5, (self.height / 24) * 19 + (self.height / 48) * self.keys[2], self.width / 20, self.height / 8), int(self.height / 150))

    #     # pg.draw.circle(self.screen, (150, 150, 150), (self.width / 2, (self.height / 24) * 21), (self.width / 20), int(self.height / 200))
    #     # pg.draw.line(self.screen, (150, 150, 150), (self.width / 2 - math.sin(self.spin) * 25 * (self.width / 1600), (self.height / 24) * 21 - math.cos(self.spin) * 25 * (self.width / 1600)), (self.width / 2 + math.sin(self.spin) * 25 * (self.width / 1600), (self.height / 24) * 21 + math.cos(self.spin) * 25 * (self.width / 1600)), int(self.width / 400))
    #     # self.spin = self.Time * -2


    #     # pg.draw.rect(self.screen, (255 - 100 * self.keys[1], 255 - 100 * self.keys[1], 255 - 100 * self.keys[1]), (self.width / 2 - self.width / 50, (self.height / 48) * 39 + (self.height / 48) * self.keys[1], self.width / 27, self.height / 8))
    #     # pg.draw.rect(self.screen, (0,0, 0), (self.width / 2 - self.width / 50, (self.height / 48) * 43 + (self.height / 48) * (self.keys[1] * 1.2), self.width / 27, self.height / 64), int(self.height / 150))
    #     # pg.draw.rect(self.screen, (50,50, 50), (self.width / 2 - self.width / 50, (self.height / 48) * 39 + (self.height / 48) * self.keys[1], self.width / 27, self.height / 8), int(self.height / 150))

    #     # pg.draw.rect(self.screen, (255 - 100 * self.keys[2], 255 - 100 * self.keys[2], 255 - 100 * self.keys[2]), (self.width / 2 + self.width / 58, (self.height / 48) * 39 + (self.height / 48) * self.keys[2], self.width / 27, self.height / 8))
    #     # pg.draw.rect(self.screen, (0,0, 0), (self.width / 2 + self.width / 58, (self.height / 48) * 43 + (self.height / 48) * (self.keys[2] * 1.2), self.width / 27, self.height / 64), int(self.height / 150))
    #     # pg.draw.rect(self.screen, (50,50, 50), (self.width / 2 + self.width / 58, (self.height / 48) * 39 + (self.height / 48) * self.keys[2], self.width / 27, self.height / 8), int(self.height / 150))


    def draw_rate(self):
        self.ingame_font_combo = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int((self.width / 38) * self.combo_effect2))
        self.ingame_font_miss = pg.font.Font(os.path.join(self.FontPath, "pdark.ttf"), int((self.width / 38) * self.miss_animation))
        self.combo_text = self.ingame_font_combo.render(str(self.combo), False, COMBO_COLOR)
        self.miss_text = self.ingame_font_rate.render(str(self.last_combo), False, RED)
        # self.perfect_text = self.ingame_font_rate.render(str(PERFECT), False, BLUE)
        # # self.perfect_text = pg.transform.scale(self.perfect_text, (int(self.width / 110 * len(self.rate) * self.combo_effect2), int(self.width / 58 * self.combo_effect1 * self.combo_effect2)))
        # self.great_text = self.ingame_font_rate.render(str(GREAT),False, GREEN)
        # # self.great_text = pg.transform.scale(self.great_text, (int(self.width / 110 * len(self.rate) * self.combo_effect2), int(self.width / 58 * self.combo_effect1 * self.combo_effect2)))
        # self.good_text = self.ingame_font_rate.render(str(GOOD), False, YELLOW)
        # # self.good_text = pg.transform.scale(self.good_text, (int(self.width / 110 * len(self.rate) * self.combo_effect2), int(self.width / 58 * self.combo_effect1 * self.combo_effect2)))
        # self.bad_text = self.ingame_font_rate.render(str(BAD), False, RED)
        # # self.bad_text = pg.transform.scale(self.bad_text, (int(self.width / 110 * len(self.rate) * self.combo_effect2), int(self.width / 58 * self.combo_effect1 * self.combo_effect2)))
        # self.miss_text = self.ingame_font_rate.render(str(MISS), False, GRAY)
        # self.miss_text = pg.transform.scale(self.miss_text, (int(self.width / 110 * len(self.rate) * self.combo_effect2), int(self.width / 58 * self.combo_effect1 * self.combo_effect2)))
        self.rate_text = self.ingame_font_rate.render(str(self.rate), False, WHITE)
        if (self.rate == PERFECT):
            self.rate_text = self.ingame_font_rate.render(str(PERFECT), False, BLUE)     
        elif (self.rate == GREAT):
            self.rate_text = self.ingame_font_rate.render(str(GREAT),False, GREEN)
        elif (self.rate == GOOD):
            self.rate_text = self.ingame_font_rate.render(str(GOOD), False, YELLOW)
        elif (self.rate == BAD):
            self.rate_text = self.ingame_font_rate.render(str(BAD), False, RED)
        elif (self.rate == MISS):
            self.rate_text = self.ingame_font_rate.render(str(MISS), False, GRAY)
            # self.rate_text = pg.transform.scale(self.miss_text, (int(self.width / 110 * len(self.rate) * self.combo_effect2), int(self.width / 58 * self.combo_effect1 * self.combo_effect2)))
        # self.rate_text = pg.transform.scale(self.rate_text, (int(self.width / 110 * len(self.rate) * self.combo_effect2), int(self.width / 58 * self.combo_effect1 * self.combo_effect2)))

        self.miss_text.set_alpha(255 - (255 / 4) * self.miss_animation)
        if self.combo != 0:
            self.screen.blit(self.combo_text, (self.width / 2 - self.combo_text.get_width() / 2, self.font_y * 4 - self.combo_text.get_height() / 2))
        self.rate_text = pg.transform.scale(self.rate_text, (int(self.width / 110 * len(self.rate) * self.combo_effect2), int(self.width / 58 * self.combo_effect1 * self.combo_effect2)))
        if self.miss_count == 1:
            self.screen.blit(self.miss_text, (self.width / 2 - self.miss_text.get_width() / 2, self.font_y * 4 - self.miss_text.get_height() / 2))

        self.screen.blit(self.rate_text, (self.width / 2 - self.rate_text.get_width() / 2, self.font_y * 8 - self.rate_text.get_height() / 2))


    def rating(self, n):
        if n == 1:
            if self.rate_data[n - 1] >= self.bad_hit_line and self.rate_data[n - 1] < self.good_hit_line:
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = BAD
                self.miss_count = 0
                self.combo += 1
                self.score += (self.combo + 10)
                del self.note1[0]
                

            elif self.rate_data[n - 1] >= self.good_hit_line and self.rate_data[n - 1] < self.great_hit_line:
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = GOOD
                self.miss_count = 0
                self.combo += 1
                self.score += (self.combo + 20)
                del self.note1[0]

            elif self.rate_data[n - 1] >= self.great_hit_line and self.rate_data[n - 1] < self.perfect_hit_line:
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = GREAT
                self.miss_count = 0
                self.combo += 1
                self.score += (self.combo + 50)
                del self.note1[0]

            
            elif self.rate_data[n - 1] >= self.perfect_hit_line and self.rate_data[n - 1] < self.hit_end_line:
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = PERFECT
                self.miss_count = 0
                self.combo += 1
                self.score += (self.combo + 100)
                del self.note1[0]

        elif n == 2:
            if self.rate_data[n - 1] >= self.bad_hit_line and self.rate_data[n - 1] < self.good_hit_line:
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = BAD
                self.miss_count = 0
                self.combo += 1
                self.score += (self.combo + 10)
                del self.note2[0]
                

            elif self.rate_data[n - 1] >= self.good_hit_line and self.rate_data[n - 1] < self.great_hit_line:
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = GOOD
                self.miss_count = 0
                self.combo += 1
                self.score += (self.combo + 20)
                del self.note2[0]

            elif self.rate_data[n - 1] >= self.great_hit_line and self.rate_data[n - 1] < self.perfect_hit_line:
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = GREAT
                self.miss_count = 0
                self.combo += 1
                self.score += (self.combo + 50)
                del self.note2[0]

            
            elif self.rate_data[n - 1] >= self.perfect_hit_line and self.rate_data[n - 1] < self.hit_end_line:
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = PERFECT
                self.miss_count = 0
                self.combo += 1
                self.score += (self.combo + 100)
                del self.note2[0]

        elif n == 3:
            if self.rate_data[n - 1] >= self.bad_hit_line and self.rate_data[n - 1] < self.good_hit_line:
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = BAD
                self.miss_count = 0
                self.combo += 1
                self.score += (self.combo + 10)
                del self.note3[0]
                

            elif self.rate_data[n - 1] >= self.good_hit_line and self.rate_data[n - 1] < self.great_hit_line:
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = GOOD
                self.miss_count = 0
                self.combo += 1
                self.score += (self.combo + 20)
                del self.note3[0]

            elif self.rate_data[n - 1] >= self.great_hit_line and self.rate_data[n - 1] < self.perfect_hit_line:
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = GREAT
                self.miss_count = 0
                self.combo += 1
                self.score += (self.combo + 50)
                del self.note3[0]

            
            elif self.rate_data[n - 1] >= self.perfect_hit_line and self.rate_data[n - 1] < self.hit_end_line:
                self.combo_effect1 = 0.2
                self.combo_time = self.Time + 1
                self.combo_effect2 = 1.3
                self.rate = PERFECT
                self.miss_count = 0
                self.combo += 1
                self.score += (self.combo + 100)
                del self.note3[0]
            

        # if abs(self.Time - self.rate_data[n - 1]) < 0.1 and abs(self.Time - self.rate_data[n - 1]) >= 0:
        #     self.combo_effect1 = 0.2
        #     self.combo_time = self.Time + 1
        #     self.combo_effect2 = 1.3
        #     self.rate = PERFECT
        #     self.miss_count = 0
        #     self.combo += 1


    def rating_data(self):
        if len(self.note1) > 0:
            self.rate_data[0] = self.note1[0][0]
        if len(self.note2) > 0:
            self.rate_data[1] = self.note2[0][0]
        if len(self.note3) > 0:
            self.rate_data[2] = self.note3[0][0]

        

    # def update(self):
    #     # self.all_sprites.update()
    #     self.game_tick = pg.time.get_ticks() - self.start_tick

    def events(self):
        if self.results.multi_hand_landmarks is not None:

            for res in self.results.multi_hand_landmarks:   
                for j, lm in enumerate(res.landmark):
                    if j==0:
                        # print((lm.x*w, lm.y*h, lm.z))
                        if 0 <= lm.x*w and a >= lm.x*w:
                            if hi * 2 <= lm.y*h:
                                self.keyset[2] = 1
                                if len(self.note3) > 0:
                                    self.rating_data()
                                    if self.note3[0][0] > self.bad_hit_line:
                                        self.rating(3)
                            else:
                                self.keyset[2] = 0

                        elif a <lm.x*w and 2 * a >= lm.x*w: # b
                            if hi * 2 <= lm.y*h:
                                self.keyset[1] = 1
                                if len(self.note2) > 0:
                                    self.rating_data()
                                    if self.note2[0][0] > self.bad_hit_line:
                                        self.rating(2)
                            else:
                                self.keyset[1] = 0
                        else: # a
                            if hi * 2 <= lm.y*h:
                                self.keyset[0] = 1
                                if len(self.note1) > 0:
                                    self.rating_data()
                                    if self.note1[0][0] > self.bad_hit_line:
                                        self.rating(1)
                            else:
                                self.keyset[0] = 0
                    
        # else:
        #     self.keyset[0], self.keyset[1], self.keyset[2] = 0, 0, 0




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
                        if self.note1[0][0] > self.bad_hit_line:
                            self.rating(1)
                if event.key == pg.K_s:
                    self.keyset[1] = 1
                    if len(self.note2) > 0:
                        self.rating_data()
                        if self.note2[0][0] > self.bad_hit_line:
                            self.rating(2)
                if event.key == pg.K_d:
                    self.keyset[2] = 1
                    if len(self.note3) > 0:
                        self.rating_data()
                        if self.note3[0][0] > self.bad_hit_line:
                            self.rating(3)

            if event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    self.keyset[0] = 0
                if event.key == pg.K_s:
                    self.keyset[1] = 0
                if event.key == pg.K_d:
                    self.keyset[2] = 0

        if self.life == 0:
            self.playing, self.running = False, False

game = Game()

while game.running:
    game.run()

pg.quit()