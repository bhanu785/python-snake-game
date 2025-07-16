import pygame,sys,random
from pygame.math import Vector2
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10),]
        self.direction = Vector2(0,0)
        self.new_block = False
        self.snowman_down = pygame.image.load('snowman_head.png').convert_alpha()
        self.snowman_up = pygame.image.load('snowman_head.png').convert_alpha()
        self.snowman_left = pygame.image.load('snowman_head.png').convert_alpha()
        self.snowman_right = pygame.image.load('snowman_head.png').convert_alpha()
        self.snowman_body = pygame.image.load('snowman_body.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('snake_crunch.wav')
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index,block in enumerate(self.body):
            snake_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            if index == 0:
                screen.blit(self.snowman_right,snake_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.snowman_body,snake_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x or previous_block.y == next_block.y:
                    screen.blit(self.snowman_body,snake_rect)
    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10),]
        self.direction = Vector2(0,0)
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): 
            self.head = self.snowman_left
        if head_relation == Vector2(1,0): 
            self.head = self.snowman_right
        if head_relation == Vector2(0,1): 
            self.head = self.snowman_up
        if head_relation == Vector2(-1,0): 
            self.head = self.snowman_down
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
    def add_block(self):
        self.new_block = True
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): 
            self.tail = self.snowman_body
        if tail_relation == Vector2(-1,0): 
            self.tail = self.snowman_body
        if tail_relation == Vector2(0,1): 
            self.tail = self.snowman_body
        if tail_relation == Vector2(-1,0): 
            self.tail = self.snowman_body
    def snake_crunch(self):
        self.crunch_sound.play()
class FRUIT:
    def __init__(self):
        self.randomize()
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(snowflake,fruit_rect)
        #pygame.draw.rect(screen,(255,255,255), fruit_rect)
    def randomize(self):
        self.x = random.randint(0,cell_number - 1) #(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1) #(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)
class MAIN:
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    def draw_grass(self):
        grass_color = (204,229,255)
        for row in range(cell_size):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.snake_crunch()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number:
            self.game_over()
        if not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    def game_over(self):
        self.snake.reset()
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (255,255,255))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_number * cell_size - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        snowflake_rect = snowflake.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(snowflake_rect.left, snowflake_rect.top, snowflake_rect.width + score_rect.width + 6, snowflake_rect.height)
        pygame.draw.rect(screen, (0,0,0), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(snowflake, snowflake_rect)
        pygame.draw.rect(screen, (255,255,255), bg_rect, 2)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
snowflake = pygame.image.load('snowflake.png').convert_alpha()
background_music = pygame.mixer.Sound('background_music.mp3')
game_font = pygame.font.Font(None, 25)
main_game = MAIN()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and main_game.snake.direction != Vector2(0,1):
                main_game.snake.direction = Vector2(0,-1)
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and main_game.snake.direction != Vector2(0,-1):
                main_game.snake.direction = Vector2(0,1)
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and main_game.snake.direction != Vector2(1,0):
                main_game.snake.direction = Vector2(-1,0)
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and main_game.snake.direction != Vector2(-1,0):
                main_game.snake.direction = Vector2(1,0)
    screen.fill(pygame.Color(51,153,255))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)