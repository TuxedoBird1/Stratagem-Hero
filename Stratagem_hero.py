import pygame
import time
import Stratagem_Hero_Stratagems as stratagems
import random

def draw_arrow(surface, color, position, size, direction):
    x, y = position
    half_size = size // 2

    if direction == 'W':
        triangle_points = [
            (x, y - half_size), 
            (x - half_size, y),  
            (x + half_size, y)  
        ]
        rect = pygame.Rect(x - half_size // 2, y, half_size, half_size)
    elif direction == 'S':
        triangle_points = [
            (x, y + half_size),
            (x - half_size, y), 
            (x + half_size, y)
        ]
        rect = pygame.Rect(x - half_size // 2, y - half_size, half_size, half_size)
    elif direction == 'A':
        triangle_points = [
            (x - half_size, y),
            (x, y - half_size),
            (x, y + half_size)
        ]
        rect = pygame.Rect(x, y - half_size // 2, half_size, half_size)
    elif direction == 'D':
        triangle_points = [
            (x + half_size, y), 
            (x, y - half_size),
            (x, y + half_size)  
        ]
        rect = pygame.Rect(x - half_size, y - half_size // 2, half_size, half_size)
    else:
        raise ValueError(f"{direction} is a invalid direction. Choose from 'W', 'S', 'A', 'D'.")

    pygame.draw.polygon(surface, color, triangle_points)
    pygame.draw.rect(surface, color, rect)

def rescale_image(image, width, height): 
    image = image.convert_alpha() 
    return pygame.transform.scale(image, (width,height))

def strats_per_lvl(lvl):
    return lvl + 5

def get_centered_x(text, font, screen_width):
    text_surface = font.render(text, True, (0, 0, 0))  
    text_width = text_surface.get_width() 
    return (screen_width - text_width) // 2  

pygame.init()
width, height = 700, 500
font = pygame.font.Font('Fonts/Oxanium.TTF', 25)
bold_font = pygame.font.Font('Fonts/Oxanium-Bold.TTF', 35)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

stratagem_list = stratagems.Stratagem_list

super_earth_logo = rescale_image(pygame.image.load('Stratagem Hero imgs/Else/super_earth.png'), height - 75, height - 75)
super_earth_logo.set_alpha(75)

running = True

code = ''

time_limit = 20 * 1000
time_remaining = time_limit
start_time = pygame.time.get_ticks()
current_time = pygame.time.get_ticks()
elapsed_time = (current_time - start_time) // 1000  
time_regain = 1250
FPS = 60

points = 0
level = 1
index = 1
strats = strats_per_lvl(level)

random_stratagems = [random.choice(stratagem_list) for _ in range(strats)]

current_stratagem = random_stratagems[0]

start_menu = True
gameover = False
roundover = False

change_time = True
wrong = False
perfect_round = True

correct_sfxs = [pygame.mixer.Sound(f'Stratagem Hero Sfx/correct{i}.wav') for i in range(1,5)]
incorrect_sfxs = [pygame.mixer.Sound(f'Stratagem Hero Sfx/error{i}.wav') for i in range(1,5)]
hit_sfxs = [pygame.mixer.Sound(f'Stratagem Hero Sfx/hit{i}.wav') for i in range(1,5)]
success_sfxs = [pygame.mixer.Sound(f'Stratagem Hero Sfx/success{i}.wav') for i in range(1,3)]
failure_sfxs = [pygame.mixer.Sound('Stratagem Hero Sfx/failure.wav'), pygame.mixer.Sound(f'Stratagem Hero Sfx/failurefull.wav')]
coin_sfxs = [pygame.mixer.Sound(f'Stratagem Hero Sfx/coin{i}.wav') for i in range(1,2)]


ready_sfx = pygame.mixer.Sound('Stratagem Hero Sfx/ready.wav')
start_sfx = pygame.mixer.Sound('Stratagem Hero Sfx/start.wav')

playing_sfx = pygame.mixer.music.load('Stratagem Hero Sfx/playing.wav')
pygame.mixer.music.play(loops = -1)

ready_sfx_played = False

while running:
    if not start_menu:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000  
        time_remaining = max(0, time_limit - (current_time - start_time)) 


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  
            wrong = False
            random.choice(hit_sfxs).play()
            if event.key == pygame.K_w:  
                code += 'W'
            elif event.key == pygame.K_a:  
                code += 'A'
            elif event.key == pygame.K_s:  
                code += 'S'
            elif event.key == pygame.K_d: 
                code += 'D'
            elif event.key == pygame.K_g:
                gameover = True
            elif event.key == pygame.K_r:
                roundover = True
            
            if code != current_stratagem['Code'][:len(code)]:
                random.choice(incorrect_sfxs).play()
                code = ''
                wrong = True
                perfect_round = False
            else:
                random.choice(correct_sfxs).play()
            
            if start_menu:
                if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                    start_menu = False
                    random.choice(coin_sfxs).play()
                    code = ''
    
    screen.fill((0,0,0))
    screen.blit(super_earth_logo, ((width - (height - 75)) / 2, 40))
    pygame.draw.rect(screen, (150,150,150), pygame.Rect(0,5, width, 5))
    pygame.draw.rect(screen, (150,150,150), pygame.Rect(0,height - 10, width, 5))

    if not roundover and not gameover and not start_menu:
        for j, strat in enumerate(random_stratagems):
            size = (50,50) if j != 0 else (75,75)
            screen.blit(rescale_image(strat['img'], size[0], size[1]), (75 * j + ((width - (75*5 + 100))/2), 30))
            img_x = ((width - (75 * 5 + 100)) / 2) - 2
            img_y = 28

            rect = pygame.Rect(img_x, img_y, 77, 77)
            pygame.draw.rect(screen, (255,255,0), rect, 2)
            if j == 5:
                break
        
        pygame.draw.rect(screen, (150,150,150), pygame.Rect(0,5, width, 5))
        pygame.draw.rect(screen, (255,255,0), pygame.Rect(0,110, width, 40))
        stratagem_name = font.render(current_stratagem['Name'], True, (0,0,0))
        screen.blit(stratagem_name, ((width - stratagem_name.get_rect().w) / 2, 119))

        arrow_size, arrow_dist = 50, 25
        arrow_sequence_width = (arrow_size + arrow_dist) * len(current_stratagem['Code']) - arrow_dist
        start_x = (width - arrow_sequence_width) / 2

        for i, dir in enumerate(current_stratagem['Code']):
            x_position = start_x + i * (arrow_size + arrow_dist)
            try:
                color = (255, 255, 255) if code[i] != current_stratagem['Code'][i] else (255, 255, 0)
            except IndexError:
                color = (255, 255, 255)
            if wrong:
                color = (255,0,0) if elapsed_time % 2 == 0 else (200,0,0)
            
            draw_arrow(screen, color, (x_position, 200), arrow_size, dir)

        
        pygame.draw.rect(screen, (150,150,150), pygame.Rect(0,250, width, 30))
        pygame.draw.rect(screen, (255,255,0), pygame.Rect(0,250, (width * (time_remaining / time_limit)), 30))
        pygame.draw.rect(screen, (150,150,150), pygame.Rect(0,height-10, width, 5))
        if code == current_stratagem['Code']:
            if index == strats:
                strats = 6 if level < 2 else level + 4
                level += 1
                index = 1

                random_stratagems = [random.choice(stratagem_list) for _ in range(strats)]
                current_stratagem = random_stratagems[0]
                code = ''
                time_remaining = time_limit
                roundover = True

            else:
                points += len(current_stratagem) * 5
                code = ''
                random_stratagems.pop(0)
                current_stratagem = random_stratagems[0]
                start_time += time_regain 
                index += 1

        if time_remaining == 0:
            gameover = True

        screen.blit(font.render('Score: ', True, (255,255,255)), (50, 310))
        screen.blit(font.render(str(points), True, (255,255,0)), (50, 340))
        screen.blit(font.render('Round: ', True, (255,255,255)), (width - 100, 310))
        screen.blit(font.render(str(level), True, (255,255,0)), (width - 100, 340))

    elif start_menu:
        bold_font = pygame.font.Font('Fonts/Oxanium-Bold.TTF', 70)
        screen.blit(bold_font.render('Stratagem Hero', True, (255,255,255)), (get_centered_x('Stratagem Hero', bold_font, width), 150))
        bold_font = pygame.font.Font('Fonts/Oxanium-Bold.TTF', 35)
        screen.blit(font.render('Enter any stratagem input to start', True, (255,255,0)), (get_centered_x('Enter any stratagem input to start', font, width), 320))

    elif roundover:
        if change_time:
            pygame.mixer.music.pause()
            random.choice(success_sfxs).play()
            start_time = current_time
            time_bonus = time_remaining // 1000
            round_bonus = ((level-1)*25) + 75
            perfect_bonus = 100 if perfect_round else 0
            points += time_bonus + perfect_bonus + round_bonus
            change_time = False
        elif elapsed_time >= 6:
            roundover = False
            change_time = True
            perfect_round = True
            ready_sfx_played = False
            pygame.mixer.music.unpause()
        if elapsed_time >= 1:
            screen.blit(font.render('Round Bonus:', True, (255,255,255)), (50,50))
            screen.blit(font.render(str(round_bonus), True, (255,255,0)), (width - 50,50))
        if elapsed_time >= 2:
            screen.blit(font.render('Time Bonus:', True, (255,255,255)), (50,100))
            screen.blit(font.render(str(time_bonus), True, (255,255,0)), (width - 50,100))
        if elapsed_time >= 3:
            screen.blit(font.render('Perfect Bonus:', True, (255,255,255)), (50,150))
            screen.blit(font.render(str(perfect_bonus), True, (255,255,0)), (width - 50,150))
        if elapsed_time >= 4:
            screen.blit(font.render('Total Score:', True, (255,255,255)), (50,200))
            screen.blit(font.render(str(points), True, (255,255,0)), (width - 50,200))
        if elapsed_time >= 5:
            if not ready_sfx_played:
                ready_sfx.play()
                ready_sfx_played = True
            screen.fill((0,0,0))
            screen.blit(super_earth_logo, ((width - (height - 75)) / 2, 40))
            pygame.draw.rect(screen, (150,150,150), pygame.Rect(0,5, width, 5))
            pygame.draw.rect(screen, (150,150,150), pygame.Rect(0,height - 10, width, 5))
            font = pygame.font.Font('Fonts/Oxanium.TTF', 40)
            screen.blit(font.render('Get Ready!', True, (255,255,255)), (get_centered_x('Get Ready!', font, width), height / 2 - 50))
            font = pygame.font.Font('Fonts/Oxanium.TTF', 25)

    elif gameover:
        if change_time:
            pygame.mixer.music.pause()
            start_time = current_time
            change_time = False
            random.choice(failure_sfxs).play()
        with open('Stratagem_hero_highscore.txt', 'r') as file:
            data  = [data.strip() for data in file.readlines()]
        high_score = int(data[0])
        if high_score < points:
            high_score = points
        with open('Stratagem_hero_highscore.txt', 'w') as file:
            file.write(str(high_score))

        if elapsed_time >= 1:
            screen.blit(bold_font.render('High Score:', True, (255,255,255)), (get_centered_x('High Score:', bold_font, width), 80))
            screen.blit(bold_font.render(str(high_score), True, (255,255,0)), (get_centered_x(str(high_score), bold_font, width), 120))
        if elapsed_time >= 2:
            screen.blit(bold_font.render('Your Final Score:', True, (255,255,255)), (get_centered_x('Your Final Score:', bold_font, width), 210))
            screen.blit(bold_font.render(str(points), True, (255,255,0)), (get_centered_x(str(points), bold_font, width), 250))
        if elapsed_time >= 4:
            current_stratagem = stratagems.Reinforce
            screen.blit(rescale_image(current_stratagem['img'], 50, 50), (width / 2 - 100, 330))
            screen.blit(bold_font.render('Reinforce', True, (255,255,255)), (width / 2 - 40, 338))

            arrow_size, arrow_dist = 25, 10
            arrow_sequence_width = (arrow_size + arrow_dist) * len(current_stratagem['Code']) - arrow_dist
            start_x = (width - arrow_sequence_width) / 2
            for i, dir in enumerate(current_stratagem['Code']):
                x_position = start_x + i * (arrow_size + arrow_dist)
                try:
                    color = (255, 255, 255) if code[i] != current_stratagem['Code'][i] else (255, 255, 0)
                except IndexError:
                    color = (255, 255, 255)
                if wrong:
                    color = (255,0,0) if elapsed_time % 2 == 0 else (200,0,0)
                
                draw_arrow(screen, color, (x_position, 400), arrow_size, dir)

            if code == current_stratagem['Code']:
                gameover = False
                time_remaining = time_limit
                start_time = pygame.time.get_ticks()

                points = 0
                level = 1
                index = 1
                strats = strats_per_lvl(level)
                random_stratagems = [random.choice(stratagem_list) for _ in range(strats)]
                current_stratagem = random_stratagems[0]
                code = current_stratagem['Code']
                pygame.mixer.music.unpause()

    pygame.display.flip()

pygame.quit()