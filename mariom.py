import pygame as pg
import random

pg.init()

WIDTH = 800
HEIGHT = 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Falling Debris and Hazards")
clock = pg.time.Clock()
font = pg.font.Font(None, 30)

BLACK = (0, 0, 0)


player_size = 40
player_x = WIDTH // 2
player_y = HEIGHT - player_size
player_speed = 5
player_jump = False
player_vel_y = 0
jump_strength = 12
gravity = 0.5
lives = 3
score = 0
small_timer = 0
is_small = False


debris = []
debris_speed = 5
debris_size = 40

spikes = []
spike_size = 40
spike_speed = 5


blue_mushrooms = []
blue_mushroom_size = 40
blue_mushroom_speed = 5


red_mushrooms = []
red_mushroom_size = 40
red_mushroom_speed = 5


hammer_img = pg.image.load("C:\MyFiles\pyproj\pygame_env\TNS\hammer.png")
hammer_img = pg.transform.scale(hammer_img, (100, 100))
hammer_active = False
hammer_pos = [0, HEIGHT * 3 // 4]  
hammer_swing_speed = 3  
hammer_side = "left"
hammer_timer = 0
hammer_warning = False


player_img = pg.image.load("C:/MyFiles/pyproj/pygame_env/TNS/mario.png")
player_img = pg.transform.scale(player_img, (player_size, player_size))

debris_img = pg.image.load("C:/MyFiles/pyproj/pygame_env/TNS/e1.png")
debris_img = pg.transform.scale(debris_img, (debris_size, debris_size))

spike_img = pg.image.load("C:/MyFiles/pyproj/pygame_env/TNS/spike.png")
spike_img = pg.transform.scale(spike_img, (spike_size, spike_size))

blue_mushroom_img = pg.image.load("C:/MyFiles/pyproj/pygame_env/TNS/blue_mushroom.png")
blue_mushroom_img = pg.transform.scale(blue_mushroom_img, (blue_mushroom_size, blue_mushroom_size))

red_mushroom_img = pg.image.load("C:/MyFiles/pyproj/pygame_env/TNS/red_mushroom.png")
red_mushroom_img = pg.transform.scale(red_mushroom_img, (red_mushroom_size, red_mushroom_size))

bg_img = pg.image.load("C:/MyFiles/pyproj/pygame_env/TNS/background.png")
bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))


def restart_game():
    global player_x, player_y, player_jump, player_vel_y, lives, score, debris, spikes, blue_mushrooms, red_mushrooms, is_small
    player_x = WIDTH // 2
    player_y = HEIGHT - player_size
    player_jump = False
    player_vel_y = 0
    lives = 3
    score = 0
    debris = []
    spikes = []
    blue_mushrooms = []
    red_mushrooms = []
    is_small = False

def main():
    global player_x, player_y, player_vel_y, player_jump
    global player_size, player_img, is_small
    global debris, spikes, blue_mushrooms, red_mushrooms
    global hammer_img, hammer_timer, hammer_warning, hammer_side, hammer_active, hammer_pos
    global lives, score

    running = True
    while running:
        clock.tick(60)
        screen.blit(bg_img, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            player_x -= player_speed
        if keys[pg.K_RIGHT]:
            player_x += player_speed
        if keys[pg.K_UP] and not player_jump:
            player_jump = True
            player_vel_y = -jump_strength

        if player_jump:
            player_vel_y += gravity
            player_y += player_vel_y
            if player_y >= HEIGHT - player_size:
                player_y = HEIGHT - player_size
                player_jump = False
                player_vel_y = 0

        if is_small and pg.time.get_ticks() - small_timer > 3000:
            player_size = 40
            player_img = pg.transform.scale(pg.image.load("mario.png"), (player_size, player_size))
            is_small = False

        if random.random() < 0.02:
            x = random.randint(0, WIDTH - debris_size)
            debris.append([x, 0])

        if random.random() < 0.01:
            x = random.randint(0, WIDTH - spike_size)
            spikes.append([x, HEIGHT])

        if random.random() < 0.002:
            x = random.randint(0, WIDTH - blue_mushroom_size)
            blue_mushrooms.append([x, 0])

        if random.random() < 0.002:
            x = random.randint(0, WIDTH - red_mushroom_size)
            red_mushrooms.append([x, 0])

        if not hammer_active and not hammer_warning and random.random() < 0.002:
            hammer_warning = True
            hammer_timer = pg.time.get_ticks()
            hammer_side = random.choice(["left", "right"])

        if hammer_warning:
            warning_text = font.render("WARNING: Hammer coming!", True, (255, 0, 0))
            screen.blit(warning_text, (WIDTH // 2 - warning_text.get_width() // 2, 20))
            if pg.time.get_ticks() - hammer_timer > 1000:
                hammer_active = True
                hammer_warning = False
                hammer_angle = 0
                if hammer_side == "left":
                    hammer_pos = [0, HEIGHT * 3 // 4]  
                else:
                    hammer_pos = [WIDTH - 100, HEIGHT * 3 // 4]

        if hammer_active:
            hammer_pos[1] += hammer_swing_speed
            if hammer_pos[1] >= HEIGHT - 100:  
                hammer_active = False
                hammer_pos[1] = HEIGHT - 100  

                
                if hammer_side == "left":
                    hammer_img = pg.transform.rotate(hammer_img, 90)
                else:
                    hammer_img = pg.transform.rotate(hammer_img, -90)
            else:
                screen.blit(hammer_img, hammer_pos)
                player_rect = pg.Rect(player_x, player_y, player_size, player_size)
                hammer_rect = pg.Rect(hammer_pos[0], hammer_pos[1], 100, 100)
                if hammer_rect.colliderect(player_rect):
                    lives -= 2
                    hammer_active = False

        for d in debris[:]:
            d[1] += debris_speed + score // 5
            screen.blit(debris_img, (d[0], d[1]))
            if pg.Rect(player_x, player_y, player_size, player_size).colliderect(pg.Rect(d[0], d[1], debris_size, debris_size)):
                lives -= 1
                debris.remove(d)
            elif d[1] > HEIGHT:
                debris.remove(d)
                score += 1

        for s in spikes[:]:
            s[1] -= spike_speed + score // 10
            screen.blit(spike_img, (s[0], s[1]))
            if pg.Rect(player_x, player_y, player_size, player_size).colliderect(pg.Rect(s[0], s[1], spike_size, spike_size)):
                lives -= 1
                spikes.remove(s)
            elif s[1] < -spike_size:
                spikes.remove(s)

        for b in blue_mushrooms[:]:
            b[1] += blue_mushroom_speed + score // 10
            screen.blit(blue_mushroom_img, (b[0], b[1]))
            if pg.Rect(player_x, player_y, player_size, player_size).colliderect(pg.Rect(b[0], b[1], blue_mushroom_size, blue_mushroom_size)):
                player_size = 25
                player_img = pg.transform.scale(pg.image.load("mario.png"), (player_size, player_size))
                is_small = True
                small_timer = pg.time.get_ticks()
                blue_mushrooms.remove(b)
            elif b[1] > HEIGHT:
                blue_mushrooms.remove(b)

        for r in red_mushrooms[:]:
            r[1] += red_mushroom_speed + score // 10
            screen.blit(red_mushroom_img, (r[0], r[1]))
            if pg.Rect(player_x, player_y, player_size, player_size).colliderect(pg.Rect(r[0], r[1], red_mushroom_size, red_mushroom_size)):
                lives += 1
                red_mushrooms.remove(r)
            elif r[1] > HEIGHT:
                red_mushrooms.remove(r)

        screen.blit(player_img, (player_x, player_y))

        info = font.render(f"Score: {score}  Lives: {lives}", True, BLACK)
        screen.blit(info, (WIDTH - 200, HEIGHT - 40))

        if lives <= 0:
            game_over_text = font.render(f"Game Over! Score: {score}", True, BLACK)
            restart_text = font.render("Press R to Restart", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
            pg.display.update()
            waiting = True
            while waiting:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        waiting = False
                        running = False
                    if event.type == pg.KEYDOWN and event.key == pg.K_r:
                        restart_game()
                        waiting = False

        pg.display.update()

    pg.quit()

main()