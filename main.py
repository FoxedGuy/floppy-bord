import pygame as pg
import sys
import random


def more_pipes():
    new_pipe2 = pipedown.get_rect(midtop=(700, random.randint(300, 700)))
    new_pipe1 = pipeup.get_rect(midbottom=(700, new_pipe2.y-210))
    new_pipe = [new_pipe1, new_pipe2]
    return new_pipe


def move_pipe(pipes, flag1):
    buf = flag1
    if len(pipes) >= 1:
        if pipes[0][0].midright[0] <= 0:
            pipes.pop(0)
            buf = False
        for pip in pipes:
            pip[0].centerx -= 3
            pip[1].centerx -= 3
    return buf, pipes


def draw_pipe(pipes):
    for pip in pipes:
        screen.blit(pipeup, pip[0])
        screen.blit(pipedown, pip[1])


def check_coll(pipes):
    for pip in pipes:
        if bird_rect.colliderect(pip[0]) or bird_rect.colliderect(pip[1]):
            return True
    if bird_rect.centery <= -100 or bird_rect.midbottom[1] >= 894:
        return True
    else:
        return False


def rotate_bird(bird):
    new_bird = pg.transform.rotozoom(bird, -bird_speed*3, 1)
    return new_bird


pg.init()
fps = 100
clock = pg.time.Clock()
pg.display.set_caption('Floppy Bord')
screen = pg.display.set_mode([600, 1000], pg.DOUBLEBUF)

# font
font = pg.font.Font('FlappyBirdRegular-9Pq0.ttf', 80)

# background
bg = pg.image.load('assets/bg2.png')
floor = pg.image.load('assets/floor.png')
# =========

# bird
bird = pg.image.load('assets/flappy_bird.png').convert_alpha()
bird_rect = bird.get_rect(center=(300, 500))
# =========

# pipe
pipeup = pg.image.load('assets/pipe_up.png')
pipedown = pg.image.load('assets/pipe_down.png')
pipe_list = []
NEWPIPE = pg.USEREVENT
pg.time.set_timer(NEWPIPE, 1500)
# =========


# death screen
death = pg.image.load('assets/Death_title.png')
death_rect = death.get_rect()
death_rect = (0, 0)

# movement
movement = pg.image.load('assets/how_to_start.png')
movement = pg.transform.scale(movement,(160,200))
movement_rect = movement.get_rect()
movement_rect.center = (300, 800)

dead = False
floor_x = 0
gravity = 0.25
bird_speed = 0
score = 0
flag = False
start = False

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN and not dead:
            if event.button == 1:
                if not start:
                    start = True
                bird_speed = 0
                bird_speed -= 7.5
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key == pg.K_SPACE and not dead:
                if not start:
                    start = True
                bird_speed = 0
                bird_speed -= 7.5
            elif event.key == pg.K_r and dead:
                dead = False
                flag = False
                start = False
                score = 0
                bird_speed = 0
                pipe_list.clear()
                bird_rect.center = (300, 500)
        if event.type == NEWPIPE and start:
            pipe_list.append(more_pipes())
    if not dead:

        if not start:
            screen.blit(bg, (0, 0))
            screen.blit(floor, (floor_x, 894))
            screen.blit(bird, bird_rect)
            text = font.render('Floppy Bord ', True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (300, 100)
            screen.blit(text, textRect)
            screen.blit(movement,movement_rect)

            pg.display.update()
            clock.tick(fps)
        else:
            # prepare score
            text = font.render('SCORE '+str(score), True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (300, 100)

            # draw background
            screen.blit(bg, (0, 0))

            # move and draw pipes
            flag, pipe_list = move_pipe(pipe_list, flag)
            draw_pipe(pipe_list)

            # draw and move floor
            screen.blit(floor, (floor_x, 894))

            floor_x -= 1
            screen.blit(floor, (floor_x + 600, 894))
            if floor_x == -600:
                screen.blit(floor, (0, 894))
                floor_x = 0

            # move/rotate/draw bird
            bird_speed += gravity
            rot_bird = rotate_bird(bird)
            bird_rect.centery += bird_speed
            screen.blit(rot_bird, bird_rect)

            # add to score if conditions met
            if len(pipe_list) > 0 and pipe_list[0][0].centerx <= bird_rect.centerx and not flag:
                flag = True
                score += 1

            # check for collisions
            dead = check_coll(pipe_list)

            if dead:
                screen.blit(death,death_rect)
            # draw score
            screen.blit(text, textRect)
            # update screen
            pg.display.update()
            clock.tick(fps)
    else:
        pass
