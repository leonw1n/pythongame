# https://elthen.itch.io/2d-pixel-art-cat-sprites
# https://www.looperman.com/loops/detail/285612/cute-loop-that-attracts-the-hoes-free-134bpm-pop-synth-loop
# https://ansimuz.itch.io/mountain-dusk-parallax-background
# https://free-game-assets.itch.io/free-sky-with-clouds-background-pixel-art-set
# https://www.youtube.com/watch?v=R4yhC5dV_LQ
# https://www.jdwasabi.com/store/8-bit-16-bit-sound-effects-x25-pack

import pygame
from pygame.locals import *
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

app_icon = pygame.image.load('images/cat1.png')
pygame.display.set_icon(app_icon)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Catty Flappy')


# define font
font = pygame.font.SysFont('Archivo Black', 60)

# define colors
white = (255, 255, 255)

# define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
high_score = 0

# load images
bg = pygame.image.load('images/bg3.png')
ground_img = pygame.image.load('images/ground2.png')
button_img = pygame.image.load('images/restartnew.png')
start_img = pygame.image.load('images/go.png')
exit_img = pygame.image.load('images/quit.png')

# music/sounds 
pygame.mixer.init()
pygame.mixer.music.load('music/chipbgm.wav')
pygame.mixer.music.play(-1,0.0)

sound_played = False
hit_pipe_sfx_played = False

go_sfx = pygame.mixer.Sound('music/confirm_sfx.wav')
restart_sfx = pygame.mixer.Sound('music/restart_sfx.wav')
exit_sfx = pygame.mixer.Sound('music/cancel_sfx.wav')
point_sfx = pygame.mixer.Sound('music/meow_sfx.mp3')
hit_sfx = pygame.mixer.Sound('music/hit_sfx.wav')

def draw_text(text, font, text_col, outline_col, x, y):
    #render text with black outline
    text_surface = font.render(text, True, outline_col)
    #offset
    text_rect = text_surface.get_rect(center= (x + 2, y + 2))
    screen.blit(text_surface, text_rect)
    
    #renders actual text
    text_surface = font.render(text, True, text_col)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'images/cat{num}.png')
            w = img.get_width()
            h = img.get_height()
            img2 = pygame.transform.scale(img, (51, 36))
            self.images.append(img2)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
    
    def update(self):
        
        #gravity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
        
        if game_over == False: 
            #handles the jump, if mouse 1 is pressed velocity is added
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #handles the animation
            self.counter += 1
            flap_cooldown = 5
            
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            
            #rotates the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            #rotates bird 90 degree clockwise onto the ground
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        # loads the pipe image
        self.image = pygame.image.load('images/logpipes.png')
        # creates a rectangle around the image
        self.rect = self.image.get_rect()
        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
            
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
        
    
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))        

bird_group.add(flappy)

# create restart button instance
restart_button = button.Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img, 4)

# create button instances
start_button = button.Button(screen_width // 2 - 50, screen_height // 2 - 100, start_img, 4)
exit_button = button.Button(screen_width // 2 - 50, screen_height // 2 - 10, exit_img, 4)


run = True
while run:
    
    clock.tick(fps)
    
    # draws the background
    screen.blit(bg, (0,0))
    
    # draws the bird
    bird_group.draw(screen)
    bird_group.update()
    
    # draws the pipes
    pipe_group.draw(screen)
        
    # draws the ground
    screen.blit(ground_img, (ground_scroll, 768))
    
    # draws the score
    draw_text(str(score), font, white, (0, 0, 0), int(screen_width / 2), 20)

    if not flying and not game_over:
        if start_button.draw(screen):
            go_sfx.play()
            flying = True
            game_over = False
            score = reset_game()      
                 
    
    # checks the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
                point_sfx.set_volume(0.2)
                point_sfx.play()

        
    # look for collision
    if (pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0) and not hit_pipe_sfx_played:
        hit_sfx.play()
        hit_pipe_sfx_played = True
        game_over = True
        
    # check if bird has hit the ground
    if flappy.rect.bottom >= 768 and not sound_played:
        hit_sfx.play()
        sound_played = True
        game_over = True
        flying = False
    
    if game_over == False and flying == True:
        
        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
    
       # draws and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    # check for game over and reset
    if game_over:
        pygame.mixer.music.stop()
        if restart_button.draw(screen):
            restart_sfx.play()
            game_over = False
            score = reset_game()
            flying = True
            sound_played = False
            hit_pipe_sfx_played = False
            pygame.mixer.music.play(-1,0.0)
        
        if exit_button.draw(screen):
            run = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()



 