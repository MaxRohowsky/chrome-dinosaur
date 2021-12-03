import pygame
import os
import random
pygame.init()

# Global Constants
SET_SPEED = 20
INCREASE_RATE = 1
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_BG = (255, 255, 255)
FONT_COLOR = (0, 0, 0)

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
themeStatus = 0

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
        if self.jump_vel < - self.JUMP_VEL:
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

class Difficult:
    def difficult_menu(death_count):
        global SET_SPEED, INCREASE_RATE
        diff = 0
        while True:
            SCREEN.fill((255, 255, 255))
            main_font = pygame.font.Font('freesansbold.ttf', 40)
            diff_dis_font = pygame.font.Font('freesansbold.ttf', 25)
            theme_main_text = main_font.render("Change difficult", True, (0, 0, 0))
            theme_main_textRect = theme_main_text.get_rect()
            theme_main_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)
            SCREEN.blit(theme_main_text, theme_main_textRect)
            diff_dis1_text = diff_dis_font.render("Easy: press 1  Medium: press 2", True, (0, 0, 0))
            diff_dis1_textRect = diff_dis1_text.get_rect()
            diff_dis1_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2-30)
            SCREEN.blit(diff_dis1_text, diff_dis1_textRect)
            diff_dis2_text = diff_dis_font.render("Hard: press 3  VeryHard: press 4", True, (0, 0, 0))
            diff_dis2_textRect = diff_dis2_text.get_rect()
            diff_dis2_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
            SCREEN.blit(diff_dis2_text, diff_dis2_textRect)
            diff_end_text = diff_dis_font.render("If you wand to Exit, press e", True, (0, 0, 0))
            diff_end_textRect = diff_end_text.get_rect()
            diff_end_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(diff_end_text, diff_end_textRect)

            if(diff == 1):
                diff_font = pygame.font.Font('freesansbold.ttf', 20)
                # Easy 난이도
                diff_text = diff_font.render("Difficult change to Easy", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                # Easy Speed
                SET_SPEED = 20 # Start Speed
                INCREASE_RATE = 1 # 1 increase per 100 points.
            if(diff == 2):
                diff_font = pygame.font.Font('freesansbold.ttf', 20)
                # Medium 난이도
                diff_text = diff_font.render("Difficult change to Medium", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                # Medium Speed
                SET_SPEED = 30
                INCREASE_RATE = 1
            if(diff == 3):
                diff_font = pygame.font.Font('freesansbold.ttf', 20)
                # Hard 난이도
                diff_text = diff_font.render("Difficult change to Hard", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                # Hard Speed
                SET_SPEED = 40
                INCREASE_RATE = 2
            if(diff == 4):
                diff_font = pygame.font.Font('freesansbold.ttf', 20)
                # VeryHard 난이도
                diff_text = diff_font.render("Difficult change to VeryHard", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                # VeryHard Speed
                SET_SPEED = 50
                INCREASE_RATE = 3

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.KEYDOWN:
                    # 키보드 1을 눌렀을 때
                    if(pygame.key.name(event.key) == '1'):
                        diff = 1
                    if(pygame.key.name(event.key) == '2'):
                        diff = 2
                    if(pygame.key.name(event.key) == '3'):
                        diff = 3
                    if(pygame.key.name(event.key) == '4'):
                        diff = 4
                    if(pygame.key.name(event.key) == "e"):
                        menu(death_count)

class Theme:
    def selectTheme(death_count):
        global RUNNING, JUMPING, DUCKING, SMALL_CACTUS, LARGE_CACTUS, BIRD, CLOUD, BG, SCREEN_BG, themeStatus, FONT_COLOR

        while True:
            SCREEN.fill((255, 255, 255))
            main_font = pygame.font.Font('freesansbold.ttf', 40)
            diff_dis_font = pygame.font.Font('freesansbold.ttf', 25)
            theme_main_text = main_font.render("Change Theme", True, (0, 0, 0))
            theme_main_textRect = theme_main_text.get_rect()
            theme_main_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)
            SCREEN.blit(theme_main_text, theme_main_textRect)
            diff_dis1_text = diff_dis_font.render("Default: press 1  Supermario: press 2", True, (0, 0, 0))
            diff_dis1_textRect = diff_dis1_text.get_rect()
            diff_dis1_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
            SCREEN.blit(diff_dis1_text, diff_dis1_textRect)
            diff_dis2_text = diff_dis_font.render("???: press 3  Night: press 4", True, (0, 0, 0))
            diff_dis2_textRect = diff_dis2_text.get_rect()
            diff_dis2_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
            SCREEN.blit(diff_dis2_text, diff_dis2_textRect)
            diff_end_text = diff_dis_font.render("Exit : press E", True, (0, 0, 0))
            diff_end_textRect = diff_end_text.get_rect()
            diff_end_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(diff_end_text, diff_end_textRect)

            if (themeStatus == 1):
                diff_font = pygame.font.Font('freesansbold.ttf', 20)
                # 1번 : Default
                diff_text = diff_font.render("Changed to Default Theme", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                # Assets Setting
                SCREEN_BG = (255, 255, 255)
                RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
                           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
                JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
                DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
                           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

                SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
                LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

                BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
                        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

                CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

                BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
                Dinosaur.Y_POS_DUCK = 340
                FONT_COLOR = (0, 0, 0)

            if (themeStatus == 2):
                diff_font = pygame.font.Font('freesansbold.ttf', 20)
                # 2번 : Supermario
                diff_text = diff_font.render("Changed to Supermario Theme", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                SCREEN_BG = (77, 184, 255)
                RUNNING = [pygame.image.load(os.path.join("Assets/Mario_Theme/Mario", "MarioRun1.png")),
                           pygame.image.load(os.path.join("Assets/Mario_Theme/Mario", "MarioRun2.png"))]
                JUMPING = pygame.image.load(os.path.join("Assets/Mario_Theme/Mario", "MarioJump.png"))
                DUCKING = [pygame.image.load(os.path.join("Assets/Mario_Theme/Mario", "MarioDuck1.png")),
                           pygame.image.load(os.path.join("Assets/Mario_Theme/Mario", "MarioDuck2.png"))]

                SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Mario_Theme/M_Obstacle", "SmallTree.png")),
                                pygame.image.load(os.path.join("Assets/Mario_Theme/M_Obstacle", "SmallTree2.png")),
                                pygame.image.load(os.path.join("Assets/Mario_Theme/M_Obstacle", "LargeTree.png"))]
                LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Mario_Theme/M_Obstacle", "GreenPipe.png")),
                                pygame.image.load(os.path.join("Assets/Mario_Theme/M_Obstacle", "LargePipe.png")),
                                pygame.image.load(os.path.join("Assets/Mario_Theme/M_Obstacle", "LargePipe2.png"))]

                BIRD = [pygame.image.load(os.path.join("Assets/Mario_Theme/M_Bird", "Bird1.png")),
                        pygame.image.load(os.path.join("Assets/Mario_Theme/M_Bird", "Bird2.png"))]

                CLOUD = pygame.image.load(os.path.join("Assets/Mario_Theme/M_Other", "M_Cloud.png"))
                BG = pygame.image.load(os.path.join("Assets/Mario_Theme/M_Other", "M_Track.png"))
                Dinosaur.Y_POS_DUCK = 320
                FONT_COLOR = (0, 0, 0)

            if (themeStatus == 3):
                diff_font = pygame.font.Font('freesansbold.ttf', 20)
                # 3번 :
                diff_text = diff_font.render("Changed to ??", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)

            if (themeStatus == 4):
                diff_font = pygame.font.Font('freesansbold.ttf', 20)
                # 4번 :
                diff_text = diff_font.render("Changed to Night Theme", True, (0, 0, 0))
                diff_textRect = diff_text.get_rect()
                diff_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                SCREEN.blit(diff_text, diff_textRect)
                # Assets Setting
                SCREEN_BG = (53, 53, 53)
                RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
                           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
                JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
                DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
                           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

                SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Night/Cactus", "SmallCactus1.png")),
                                pygame.image.load(os.path.join("Assets/Night/Cactus", "SmallCactus2.png")),
                                pygame.image.load(os.path.join("Assets/Night/Cactus", "SmallCactus3.png"))]
                LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Night/Cactus", "LargeCactus1.png")),
                                pygame.image.load(os.path.join("Assets/Night/Cactus", "LargeCactus2.png")),
                                pygame.image.load(os.path.join("Assets/Night/Cactus", "LargeCactus3.png"))]

                BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
                        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

                CLOUD = pygame.image.load(os.path.join("Assets/Night/Other", "Cloud.png"))

                BG = pygame.image.load(os.path.join("Assets/Night/Other", "Track.png"))
                Dinosaur.Y_POS_DUCK = 340
                FONT_COLOR = (255, 255, 255)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.KEYDOWN:
                    # 키보드 1을 눌렀을 때
                    if (pygame.key.name(event.key) == '1'):
                        themeStatus = 1
                    if (pygame.key.name(event.key) == '2'):
                        themeStatus = 2
                    if (pygame.key.name(event.key) == '3'):
                        themeStatus = 3
                    if (pygame.key.name(event.key) == '4'):
                        themeStatus = 4
                    if (pygame.key.name(event.key) == "e"):
                        menu(death_count)


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
    global themeStatus
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        if(themeStatus == 0 or themeStatus == 1):
            self.rect.y = 325
        elif(themeStatus == 2):
            self.rect.y = 290
        elif(themeStatus == 3):
            self.rect.y = 325
        elif(themeStatus == 4):
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
        if(yrand == 0):
            self.rect.y = 150
        if(yrand == 1):
            self.rect.y = 250
        if(yrand == 2):
            self.rect.y = 300
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
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
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed, INCREASE_RATE
        points += 1
        if points % 100 == 0:
            game_speed += INCREASE_RATE

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
                run = False

        SCREEN.fill(SCREEN_BG) # 스크린 배경
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
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        theme_text = font.render("Change Difficulty : D", True, (0, 0, 0))
        theme_textRect = theme_text.get_rect()
        theme_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        SCREEN.blit(theme_text, theme_textRect)

        theme2_text = font.render("Change Theme : T", True, (0, 0, 0))
        theme2_textRect = theme2_text.get_rect()
        theme2_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
        SCREEN.blit(theme2_text, theme2_textRect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if(pygame.key.name(event.key) == 'd'):
                    Difficult.difficult_menu(death_count)
                if (pygame.key.name(event.key) == 't'):
                    Theme.selectTheme(death_count)
                main()


menu(death_count=0)
