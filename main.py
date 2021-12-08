import os
import random

# from pygame.constants import MOUSEBUTTONDOWN
import pygame
import requests
import uuid

ch = uuid.getnode()
mac = ":".join(("%12X" % ch)[i : i + 2] for i in range(0, 12, 2))

pygame.init()

# Global Constants
DIFF = 1
SELECT_MENU = 1
SELECT_MENU_END = 0
SET_SPEED = 20
INCREASE_RATE = 1

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_BG = (255, 255, 255)
FONT_COLOR = (0, 0, 0)

RUNNING = [
    pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("Assets/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
themeStatus = 1
JUMP_SOUND = pygame.mixer.Sound(os.path.join("Assets/Soundtrack", "jump.mp3"))
SPEEDUP_SOUND = pygame.mixer.Sound(os.path.join("Assets/Soundtrack", "speedup.mp3"))
BG_MUSIC = pygame.mixer.Sound(os.path.join("Assets/Soundtrack", "Main_BGM.mp3"))

SCORE = []


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
            JUMP_SOUND.play()  # 점프 사운드 한번 재생
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Option:
    def option(death_count):
        global SELECT_MENU, SELECT_MENU_END
        SELECT_MENU = 1
        SELECT_MENU_END = 4
        while True:
            SCREEN.fill((255, 255, 255))
            font = pygame.font.Font("freesansbold.ttf", 30)
            title_font = pygame.font.Font("freesansbold.ttf", 40)
            option_text = title_font.render("Option", True, (0, 0, 0))
            option_textRect = option_text.get_rect()
            option_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 180)
            SCREEN.blit(option_text, option_textRect)

            if SELECT_MENU == 1:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 140,
                    SCREEN_HEIGHT // 2 - 5,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)

            if SELECT_MENU == 2:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 130,
                    SCREEN_HEIGHT // 2 + 45,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)

            if SELECT_MENU == 3:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 120,
                    SCREEN_HEIGHT // 2 + 95,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)

            if SELECT_MENU == 4:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 120,
                    SCREEN_HEIGHT // 2 + 145,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)

            diff_text = font.render("Change Difficult", True, (0, 0, 0))
            diff_textRect = diff_text.get_rect()
            diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(diff_text, diff_textRect)

            theme_text = font.render("Change Theme", True, (0, 0, 0))
            theme_textRect = theme_text.get_rect()
            theme_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(theme_text, theme_textRect)

            reader_text = font.render("Readerboard", True, (0, 0, 0))
            reader_textRect = reader_text.get_rect()
            reader_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(reader_text, reader_textRect)

            back_text = font.render("Back to Menu", True, (0, 0, 0))
            back_textRect = back_text.get_rect()
            back_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
            SCREEN.blit(back_text, back_textRect)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        SELECT_MENU = SELECT_MENU - 1
                        if SELECT_MENU <= 0:
                            SELECT_MENU = SELECT_MENU_END

                    if event.key == pygame.K_DOWN:
                        SELECT_MENU = SELECT_MENU + 1
                        if SELECT_MENU > SELECT_MENU_END:
                            SELECT_MENU = 1

                    if event.key == pygame.K_RETURN:
                        if SELECT_MENU == 1:
                            Option.difficult_menu(death_count)

                        if SELECT_MENU == 2:
                            Option.selectTheme(death_count)

                        if SELECT_MENU == 3:
                            Option.score(death_count)

                        if SELECT_MENU == 4:
                            menu(death_count)

    def difficult_menu(death_count):
        global SET_SPEED, INCREASE_RATE, SELECT_MENU, SELECT_MENU_END, DIFF
        SELECT_MENU_END = 5
        while True:
            SCREEN.fill((255, 255, 255))
            font = pygame.font.Font("freesansbold.ttf", 30)
            main_font = pygame.font.Font("freesansbold.ttf", 40)
            diff_dis_font = pygame.font.Font("freesansbold.ttf", 25)
            title_font = pygame.font.Font("freesansbold.ttf", 40)
            theme_main_text = main_font.render("Change difficult", True, (0, 0, 0))
            theme_main_textRect = theme_main_text.get_rect()
            theme_main_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)
            SCREEN.blit(theme_main_text, theme_main_textRect)
            if SELECT_MENU == 1:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 140,
                    SCREEN_HEIGHT // 2 - 55,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)
            if SELECT_MENU == 2:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 140,
                    SCREEN_HEIGHT // 2 - 5,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)
            if SELECT_MENU == 3:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 140,
                    SCREEN_HEIGHT // 2 + 45,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)
            if SELECT_MENU == 4:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 140,
                    SCREEN_HEIGHT // 2 + 95,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)
            if SELECT_MENU == 5:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 140,
                    SCREEN_HEIGHT // 2 + 145,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)
            easy_text = font.render("Easy", True, (0, 0, 0))
            easy_textRect = easy_text.get_rect()
            easy_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            SCREEN.blit(easy_text, easy_textRect)
            medium_text = font.render("Medium", True, (0, 0, 0))
            medium_textRect = medium_text.get_rect()
            medium_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(medium_text, medium_textRect)
            hard_text = font.render("Hard", True, (0, 0, 0))
            hard_textRect = hard_text.get_rect()
            hard_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(hard_text, hard_textRect)
            veryhard_text = font.render("VeryHard", True, (0, 0, 0))
            veryhard_textRect = veryhard_text.get_rect()
            veryhard_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(veryhard_text, veryhard_textRect)
            back_text = font.render("Back to Option", True, (0, 0, 0))
            back_textRect = back_text.get_rect()
            back_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
            SCREEN.blit(back_text, back_textRect)
            if DIFF == 1:
                diff_font = pygame.font.Font("freesansbold.ttf", 20)
                # Easy 난이도
                diff_text = diff_font.render("Difficulty: Easy", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                Menu_selected = font.render(chr(64), True, (0, 0, 0))
                Menu_selectedRect = Menu_selected.get_rect()
                Menu_selectedRect.center = (
                    SCREEN_WIDTH // 2 - 100,
                    SCREEN_HEIGHT // 2 - 55,
                )
                SCREEN.blit(Menu_selected, Menu_selectedRect)
                # Easy Speed
                SET_SPEED = 20  # Start Speed
                INCREASE_RATE = 1  # 1 increase per 100 points.
            if DIFF == 2:
                diff_font = pygame.font.Font("freesansbold.ttf", 20)
                # Medium 난이도
                diff_text = diff_font.render("Difficulty: Medium", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                Menu_selected = font.render(chr(64), True, (0, 0, 0))
                Menu_selectedRect = Menu_selected.get_rect()
                Menu_selectedRect.center = (
                    SCREEN_WIDTH // 2 - 100,
                    SCREEN_HEIGHT // 2 - 5,
                )
                SCREEN.blit(Menu_selected, Menu_selectedRect)
                # Medium Speed
                SET_SPEED = 30
                INCREASE_RATE = 1
            if DIFF == 3:
                diff_font = pygame.font.Font("freesansbold.ttf", 20)
                # Hard 난이도
                diff_text = diff_font.render("Difficulty: Hard", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                Menu_selected = font.render(chr(64), True, (0, 0, 0))
                Menu_selectedRect = Menu_selected.get_rect()
                Menu_selectedRect.center = (
                    SCREEN_WIDTH // 2 - 100,
                    SCREEN_HEIGHT // 2 + 45,
                )
                SCREEN.blit(Menu_selected, Menu_selectedRect)
                # Hard Speed
                SET_SPEED = 40
                INCREASE_RATE = 2
            if DIFF == 4:
                diff_font = pygame.font.Font("freesansbold.ttf", 20)
                # VeryHard 난이도
                diff_text = diff_font.render("Difficulty: VeryHard", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                Menu_selected = font.render(chr(64), True, (0, 0, 0))
                Menu_selectedRect = Menu_selected.get_rect()
                Menu_selectedRect.center = (
                    SCREEN_WIDTH // 2 - 100,
                    SCREEN_HEIGHT // 2 + 95,
                )
                SCREEN.blit(Menu_selected, Menu_selectedRect)
                # VeryHard Speed
                SET_SPEED = 50
                INCREASE_RATE = 3

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        SELECT_MENU = SELECT_MENU - 1
                        if SELECT_MENU <= 0:
                            SELECT_MENU = SELECT_MENU_END
                    if event.key == pygame.K_DOWN:
                        SELECT_MENU = SELECT_MENU + 1
                        if SELECT_MENU > SELECT_MENU_END:
                            SELECT_MENU = 1
                    if event.key == pygame.K_RETURN:
                        if SELECT_MENU == 1:
                            DIFF = 1
                        if SELECT_MENU == 2:
                            DIFF = 2
                        if SELECT_MENU == 3:
                            DIFF = 3
                        if SELECT_MENU == 4:
                            DIFF = 4
                        if SELECT_MENU == 5:
                            Option.option(death_count)

    def selectTheme(death_count):
        global RUNNING, JUMPING, DUCKING, SMALL_CACTUS, LARGE_CACTUS, BIRD, CLOUD, BG, SCREEN_BG, themeStatus, FONT_COLOR, JUMP_SOUND, BG_MUSIC, SPEEDUP_SOUND, SELECT_MENU, SELECT_MENU_END
        SELECT_MENU = 1
        SELECT_MENU_END = 5
        while True:
            SCREEN.fill((255, 255, 255))
            font = pygame.font.Font("freesansbold.ttf", 30)
            main_font = pygame.font.Font("freesansbold.ttf", 40)
            diff_dis_font = pygame.font.Font("freesansbold.ttf", 25)
            theme_main_text = main_font.render("Change Theme", True, (0, 0, 0))
            theme_main_textRect = theme_main_text.get_rect()
            theme_main_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)
            SCREEN.blit(theme_main_text, theme_main_textRect)
            if SELECT_MENU == 1:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 140,
                    SCREEN_HEIGHT // 2 - 55,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)
            if SELECT_MENU == 2:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 140,
                    SCREEN_HEIGHT // 2 - 5,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)
            if SELECT_MENU == 3:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 140,
                    SCREEN_HEIGHT // 2 + 45,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)
            if SELECT_MENU == 4:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 140,
                    SCREEN_HEIGHT // 2 + 95,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)
            if SELECT_MENU == 5:
                Menu_select = font.render(">", True, (0, 0, 0))
                Menu_selectRect = Menu_select.get_rect()
                Menu_selectRect.center = (
                    SCREEN_WIDTH // 2 - 140,
                    SCREEN_HEIGHT // 2 + 145,
                )
                SCREEN.blit(Menu_select, Menu_selectRect)
            easy_text = font.render("Default", True, (0, 0, 0))
            easy_textRect = easy_text.get_rect()
            easy_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            SCREEN.blit(easy_text, easy_textRect)
            medium_text = font.render("Supermario", True, (0, 0, 0))
            medium_textRect = medium_text.get_rect()
            medium_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(medium_text, medium_textRect)
            hard_text = font.render("???", True, (0, 0, 0))
            hard_textRect = hard_text.get_rect()
            hard_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(hard_text, hard_textRect)
            veryhard_text = font.render("Night", True, (0, 0, 0))
            veryhard_textRect = veryhard_text.get_rect()
            veryhard_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(veryhard_text, veryhard_textRect)
            back_text = font.render("Back to Option", True, (0, 0, 0))
            back_textRect = back_text.get_rect()
            back_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
            SCREEN.blit(back_text, back_textRect)
            if themeStatus == 1:
                diff_font = pygame.font.Font("freesansbold.ttf", 20)
                # 1번 : Default
                diff_text = diff_font.render(
                    "Changed to Default Theme", True, (0, 0, 0)
                )
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                # Assets Setting
                SCREEN_BG = (255, 255, 255)
                RUNNING = [
                    pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
                    pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png")),
                ]
                JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
                DUCKING = [
                    pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
                    pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png")),
                ]

                SMALL_CACTUS = [
                    pygame.image.load(
                        os.path.join("Assets/Cactus", "SmallCactus1.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Cactus", "SmallCactus2.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Cactus", "SmallCactus3.png")
                    ),
                ]
                LARGE_CACTUS = [
                    pygame.image.load(
                        os.path.join("Assets/Cactus", "LargeCactus1.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Cactus", "LargeCactus2.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Cactus", "LargeCactus3.png")
                    ),
                ]

                BIRD = [
                    pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
                    pygame.image.load(os.path.join("Assets/Bird", "Bird2.png")),
                ]

                CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

                BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

                JUMP_SOUND = pygame.mixer.Sound(
                    os.path.join("Assets/Soundtrack", "jump.mp3")
                )
                SPEEDUP_SOUND = pygame.mixer.Sound(
                    os.path.join("Assets/Soundtrack", "speedup.mp3")
                )
                BG_MUSIC = pygame.mixer.Sound(
                    os.path.join("Assets/Soundtrack", "Main_BGM.mp3")
                )

                Dinosaur.Y_POS_DUCK = 340
                FONT_COLOR = (0, 0, 0)
                Menu_selected = font.render(chr(64), True, (0, 0, 0))
                Menu_selectedRect = Menu_selected.get_rect()
                Menu_selectedRect.center = (
                    SCREEN_WIDTH // 2 - 100,
                    SCREEN_HEIGHT // 2 - 55,
                )
                SCREEN.blit(Menu_selected, Menu_selectedRect)
            if themeStatus == 2:
                diff_font = pygame.font.Font("freesansbold.ttf", 20)
                # 2번 : Supermario
                diff_text = diff_font.render(
                    "Changed to Supermario Theme", True, (0, 0, 0)
                )
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                SCREEN_BG = (77, 184, 255)
                RUNNING = [
                    pygame.image.load(
                        os.path.join("Assets/Mario_Theme/Mario", "MarioRun1.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Mario_Theme/Mario", "MarioRun2.png")
                    ),
                ]
                JUMPING = pygame.image.load(
                    os.path.join("Assets/Mario_Theme/Mario", "MarioJump.png")
                )
                DUCKING = [
                    pygame.image.load(
                        os.path.join("Assets/Mario_Theme/Mario", "MarioDuck1.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Mario_Theme/Mario", "MarioDuck2.png")
                    ),
                ]

                SMALL_CACTUS = [
                    pygame.image.load(
                        os.path.join("Assets/Mario_Theme/M_Obstacle", "SmallTree.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Mario_Theme/M_Obstacle", "SmallTree2.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Mario_Theme/M_Obstacle", "LargeTree.png")
                    ),
                ]
                LARGE_CACTUS = [
                    pygame.image.load(
                        os.path.join("Assets/Mario_Theme/M_Obstacle", "GreenPipe.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Mario_Theme/M_Obstacle", "LargePipe.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Mario_Theme/M_Obstacle", "LargePipe2.png")
                    ),
                ]

                BIRD = [
                    pygame.image.load(
                        os.path.join("Assets/Mario_Theme/M_Bird", "Bird1.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Mario_Theme/M_Bird", "Bird2.png")
                    ),
                ]

                CLOUD = pygame.image.load(
                    os.path.join("Assets/Mario_Theme/M_Other", "M_Cloud.png")
                )
                BG = pygame.image.load(
                    os.path.join("Assets/Mario_Theme/M_Other", "M_Track.png")
                )

                JUMP_SOUND = pygame.mixer.Sound(
                    os.path.join("Assets/Mario_Theme/Soundtrack", "M_Jump.mp3")
                )
                SPEEDUP_SOUND = pygame.mixer.Sound(
                    os.path.join("Assets/Mario_Theme/Soundtrack", "Coin.mp3")
                )
                BG_MUSIC = pygame.mixer.Sound(
                    os.path.join("Assets/Mario_Theme/Soundtrack", "M_BGM.mp3")
                )
                Dinosaur.Y_POS_DUCK = 320
                FONT_COLOR = (0, 0, 0)
                Menu_selected = font.render(chr(64), True, (0, 0, 0))
                Menu_selectedRect = Menu_selected.get_rect()
                Menu_selectedRect.center = (
                    SCREEN_WIDTH // 2 - 100,
                    SCREEN_HEIGHT // 2 - 5,
                )
                SCREEN.blit(Menu_selected, Menu_selectedRect)
            if themeStatus == 3:
                diff_font = pygame.font.Font("freesansbold.ttf", 20)
                # 3번 :
                diff_text = diff_font.render("ComingSoon", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                Menu_selected = font.render(chr(64), True, (0, 0, 0))
                Menu_selectedRect = Menu_selected.get_rect()
                Menu_selectedRect.center = (
                    SCREEN_WIDTH // 2 - 100,
                    SCREEN_HEIGHT // 2 + 45,
                )
                SCREEN.blit(Menu_selected, Menu_selectedRect)
            if themeStatus == 4:
                diff_font = pygame.font.Font("freesansbold.ttf", 20)
                # 4번 :
                diff_text = diff_font.render("Changed to Night Theme", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                # Assets Setting
                SCREEN_BG = (53, 53, 53)
                RUNNING = [
                    pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
                    pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png")),
                ]
                JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
                DUCKING = [
                    pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
                    pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png")),
                ]

                SMALL_CACTUS = [
                    pygame.image.load(
                        os.path.join("Assets/Night/Cactus", "SmallCactus1.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Night/Cactus", "SmallCactus2.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Night/Cactus", "SmallCactus3.png")
                    ),
                ]
                LARGE_CACTUS = [
                    pygame.image.load(
                        os.path.join("Assets/Night/Cactus", "LargeCactus1.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Night/Cactus", "LargeCactus2.png")
                    ),
                    pygame.image.load(
                        os.path.join("Assets/Night/Cactus", "LargeCactus3.png")
                    ),
                ]

                BIRD = [
                    pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
                    pygame.image.load(os.path.join("Assets/Bird", "Bird2.png")),
                ]

                CLOUD = pygame.image.load(
                    os.path.join("Assets/Night/Other", "Cloud.png")
                )

                BG = pygame.image.load(os.path.join("Assets/Night/Other", "Track.png"))

                JUMP_SOUND = pygame.mixer.Sound(
                    os.path.join("Assets/Soundtrack", "jump.mp3")
                )
                SPEEDUP_SOUND = pygame.mixer.Sound(
                    os.path.join("Assets/Soundtrack", "speedup.mp3")
                )
                BG_MUSIC = pygame.mixer.Sound(
                    os.path.join("Assets/Soundtrack", "Main_BGM.mp3")
                )
                Dinosaur.Y_POS_DUCK = 340
                FONT_COLOR = (255, 255, 255)
                Menu_selected = font.render(chr(64), True, (0, 0, 0))
                Menu_selectedRect = Menu_selected.get_rect()
                Menu_selectedRect.center = (
                    SCREEN_WIDTH // 2 - 100,
                    SCREEN_HEIGHT // 2 + 95,
                )
                SCREEN.blit(Menu_selected, Menu_selectedRect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        SELECT_MENU = SELECT_MENU - 1
                        if SELECT_MENU <= 0:
                            SELECT_MENU = SELECT_MENU_END
                    if event.key == pygame.K_DOWN:
                        SELECT_MENU = SELECT_MENU + 1
                        if SELECT_MENU > SELECT_MENU_END:
                            SELECT_MENU = 1
                    if event.key == pygame.K_RETURN:
                        if SELECT_MENU == 1:
                            themeStatus = 1
                        if SELECT_MENU == 2:
                            themeStatus = 2
                        if SELECT_MENU == 3:
                            themeStatus = 3
                        if SELECT_MENU == 4:
                            themeStatus = 4
                        if SELECT_MENU == 5:
                            Option.option(death_count)

    def score(death_count):
        font = pygame.font.Font("freesansbold.ttf", 40)
        score_font = pygame.font.Font("freesansbold.ttf", 20)
        datas = {"uid": mac}
        url = "http://ec2-54-180-119-201.ap-northeast-2.compute.amazonaws.com/user/v1/info"
        response = requests.post(url, data=datas)
        SCORE = response.json()["Message"]
        while True:
            SCREEN.fill((255, 255, 255))
            title_text = font.render("Score Board", True, (0, 0, 0))
            title_textRect = title_text.get_rect()
            title_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 180)
            SCREEN.blit(title_text, title_textRect)
            for i in range(5):
                if len(SCORE) <= i:
                    score_text = score_font.render(
                        (str)(i + 1) + ". empty", True, (0, 0, 0)
                    )
                    score_textRect = score_text.get_rect()
                    score_textRect.center = (
                        SCREEN_WIDTH // 2,
                        SCREEN_HEIGHT // 2 - 80 + (i * 50),
                    )
                    SCREEN.blit(score_text, score_textRect)
                else:
                    score_text = score_font.render(
                        (str)(i + 1) + ". " + (str)(SCORE[i]), True, (0, 0, 0)
                    )
                    score_textRect = score_text.get_rect()
                    score_textRect.center = (
                        SCREEN_WIDTH // 2,
                        SCREEN_HEIGHT // 2 - 80 + (i * 50),
                    )
                    SCREEN.blit(score_text, score_textRect)
            title_text = score_font.render("Press Enter to Back", True, (0, 0, 0))
            title_textRect = title_text.get_rect()
            title_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
            SCREEN.blit(title_text, title_textRect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        Option.option(death_count)
            pygame.display.update()


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        if themeStatus == 0 or themeStatus == 1:
            self.rect.y = 325
        elif themeStatus == 2:
            self.rect.y = 290
        elif themeStatus == 3:
            self.rect.y = 325
        elif themeStatus == 4:
            self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        yrand = random.randint(0, 2)
        if yrand == 0:
            self.rect.y = 150
        if yrand == 1:
            self.rect.y = 250
        if yrand == 2:
            self.rect.y = 300
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global SET_SPEED, game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = SET_SPEED
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    BG_MUSIC.play(-1)  # BGM 무한재생

    def score():
        global points, game_speed, INCREASE_RATE
        points += 1
        if points % 100 == 0:
            game_speed += INCREASE_RATE
            # 100점 마다 Alert Sound
            SPEEDUP_SOUND.play()
        text = font.render("Points: " + str(points), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                BG_MUSIC.stop()
                run = False

        SCREEN.fill(SCREEN_BG)
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                datas = {"uid": mac, "data": points}
                url = "http://ec2-54-180-119-201.ap-northeast-2.compute.amazonaws.com/user/v1/data"
                response = requests.post(url, data=datas)
                BG_MUSIC.stop()
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points, SELECT_MENU, SELECT_MENU_END
    run = True
    SELECT_MENU = 1
    SELECT_MENU_END = 2
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font("freesansbold.ttf", 30)
        info_font = pygame.font.Font("freesansbold.ttf", 20)
        if death_count > 0:
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        title_text = font.render("Dinosaur Game!", True, (0, 0, 0))
        title_textRect = title_text.get_rect()
        title_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(title_text, title_textRect)
        text = info_font.render("UP, DOWN: Move, Enter: Select", True, (0, 0, 0))
        if SELECT_MENU == 1:
            Menu_select = font.render(">", True, (0, 0, 0))
            Menu_selectRect = Menu_select.get_rect()
            Menu_selectRect.center = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 95)
            SCREEN.blit(Menu_select, Menu_selectRect)
        if SELECT_MENU == 2:
            Menu_select = font.render(">", True, (0, 0, 0))
            Menu_selectRect = Menu_select.get_rect()
            Menu_selectRect.center = (SCREEN_WIDTH // 2 - 65, SCREEN_HEIGHT // 2 + 145)
            SCREEN.blit(Menu_select, Menu_selectRect)
        play_text = font.render("Play", True, (0, 0, 0))
        play_textRect = play_text.get_rect()
        play_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        SCREEN.blit(play_text, play_textRect)
        option_text = font.render("Option", True, (0, 0, 0))
        option_textRect = option_text.get_rect()
        option_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
        SCREEN.blit(option_text, option_textRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2 - 250)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        click = False
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    SELECT_MENU = SELECT_MENU - 1
                    if SELECT_MENU <= 0:
                        SELECT_MENU = SELECT_MENU_END
                if event.key == pygame.K_DOWN:
                    SELECT_MENU = SELECT_MENU + 1
                    if SELECT_MENU > SELECT_MENU_END:
                        SELECT_MENU = 1
                if event.key == pygame.K_RETURN:
                    if SELECT_MENU == 1:
                        main()
                    if SELECT_MENU == 2:
                        Option.option(death_count)


menu(death_count=0)
