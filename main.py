import pygame
import os
pygame.font.init()
WIDTH = 900
HEIGHT=500
xe = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

WHITE = (255, 255, 255)
BLACK= (0,0,0)

FPS = 60
BULLET_SPEED=7
max_bullet=4
spaceship_width, spaceship_height= 70, 100

RED_HIT= pygame.USEREVENT+1
BLUE_HIT= pygame.USEREVENT+2
SCORE_FONT=pygame.font.SysFont("ubuntu", 40)

spaceship_red=pygame.image.load(os.path.join('media', 'spaceship_yellow.png'))
red_space=pygame.transform.rotate(pygame.transform.scale(spaceship_red, (spaceship_width, spaceship_height)), 270)
spaceship_blue=pygame.image.load(os.path.join('media', 'spaceship_red.png'))
blue_space=pygame.transform.rotate(pygame.transform.scale(spaceship_blue, (spaceship_width, spaceship_height)), 90)


space=pygame.image.load(os.path.join('media', 'space.png'))

def draw_game(red, blue, red_bullet, blue_bullet, red_point, blue_point):
    xe.blit(space, (0,0))

    red_score_text=SCORE_FONT.render("RED: " + str(red_point), 1, WHITE)
    xe.blit(red_score_text, [0,0])
    blue_score_text=SCORE_FONT.render("BLUE: "+ str(blue_point),1, WHITE)
    xe.blit(blue_score_text,[700,0])
    xe.blit(red_space, (red.x, red.y))
    xe.blit(blue_space, (blue.x, blue.y))


    for bullet in red_bullet:
        pygame.draw.rect(xe, WHITE, bullet)
    for bullet in blue_bullet:
        pygame.draw.rect(xe, WHITE, bullet)
#movements
def blue_movements(key_pressed, blue):
    if key_pressed[pygame.K_LEFT] and blue.x+ blue.width>540:
        blue.x -= 2
    if key_pressed[pygame.K_RIGHT] and blue.x<800:
        blue.x += 2
    if key_pressed[pygame.K_UP] and blue.y>0:
        blue.y -= 2
    if key_pressed[pygame.K_DOWN] and blue.y < 425:
        blue.y += 2
def red_movements(key_pressed, red):
    if key_pressed[pygame.K_a] and red.x>0:
        red.x -= 2
    if key_pressed[pygame.K_d] and red.x+ red.width< 415:
        red.x += 2
    if key_pressed[pygame.K_w] and red.y>0 :
        red.y -= 2
    if key_pressed[pygame.K_s] and red.y<425:
        red.y += 2

def shoot_bullet(red_bullet, blue_bullet, red, blue):
    for bullet in red_bullet:
        bullet.x+=BULLET_SPEED
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullet.remove(bullet)
        if bullet.x>WIDTH:
           red_bullet.remove(bullet)

    for bullet in blue_bullet:
        bullet.x-=BULLET_SPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullet.remove(bullet)
        if bullet.x<0:
            blue_bullet.remove(bullet)


def main():
    red = pygame.Rect(200, 100, spaceship_width, spaceship_height)
    blue = pygame.Rect(700, 200, spaceship_width, spaceship_height)
    red_bullet=[]
    blue_bullet=[]
    red_point=100
    blue_point=100

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullet)< max_bullet:
                    bullet=pygame.Rect(red.x+red.width+20, red.y+red.height//3, 10,5)
                    red_bullet.append(bullet)
                if event.key == pygame.K_RCTRL and len(blue_bullet)< max_bullet:
                    bullet=pygame.Rect(blue.x, blue.y+blue.height//3, 10, 5)
                    blue_bullet.append(bullet)

            if event.type==RED_HIT:
                red_point-=10
            if event.type==BLUE_HIT:
                blue_point-=10

            winner_text=""

            if red_point<=0:
                winner_text= "BLUE SHIP WINS!"
            if blue_point<=0:
                winner_text= "RED SHIP WINS!"
            if winner_text!= "":
                draw_winner= SCORE_FONT.render(winner_text, 1, WHITE)
                xe.blit(draw_winner, [WIDTH/3, HEIGHT/3])
                pygame.display.update()
                pygame.time.delay(1500)
                pygame.quit()


        key_pressed = pygame.key.get_pressed()
        red_movements(key_pressed, red)
        blue_movements(key_pressed,blue)
        shoot_bullet(red_bullet,blue_bullet,red,blue)





        draw_game(red, blue, red_bullet, blue_bullet, red_point, blue_point)
        pygame.display.update()




    pygame.quit()


if __name__ == "__main__":
    main()