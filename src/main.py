import pygame
import pickle
import os
from coin import Coin

pygame.init()
pygame.mixer.init()


game_width = 750
game_height = 750
running = True

screen = pygame.display.set_mode(( game_width,game_height ))
clock = pygame.time.Clock()

#player
playerimage = pygame.image.load("images/player.png")
playerect = playerimage.get_rect(center = (game_width/2 , game_height/2))
player_speed = 10

#enemy section
enemyimage = pygame.image.load("images/enemy.png")
enemyrect = enemyimage.get_rect()
enemy_x = 0
enemy_y = game_height
enemy_speed = 1

#Text section
font = pygame.font.SysFont("arialunicode", 70, bold = True)
gameovertext = font.render("Gameover" , True , (0,0,0))
gameovertextrect = gameovertext.get_rect(center = (game_width/2 , game_height/2))

#singleplayer section
singleplayer = True
spacelock = False

#gameover section
gameover = False

#Score section
score = 0
if os.path.exists('score.dat'):
    with open ('score.dat' , 'rb') as file:
        score = pickle.load(file)
        print(score)
testcoin = Coin(37,78)


#sound/music
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.load('sounds/77 Ganondorf Battle.mp3')
pygame.mixer.music.play(loops = -1)
collision_sound = pygame.mixer.Sound("sounds/12. Palace Theme 1.mp3")
collision_sound.set_volume(0.2)

#maze section
#COPY AND PASTE PREVIOUS LINE TO CHANGE X AND Y AND USE SPECIFIC NUMBERS and can change width and Height.
border_thickness = 27
maze = [
      pygame.Rect(0,0,border_thickness,game_height)
    , pygame.Rect(0,0,game_width,border_thickness)
    , pygame.Rect(game_width - border_thickness,0,border_thickness,game_height)
    , pygame.Rect(0,game_height - border_thickness,game_width,border_thickness)
    , pygame.Rect(80+border_thickness,80+border_thickness,90,60)
    , pygame.Rect(game_width - 80 - border_thickness - 90,80+border_thickness,90,60)
    , pygame.Rect(80+border_thickness, game_height - 80 - border_thickness - 60,90,60)
    , pygame.Rect(game_width - 80 - border_thickness - 90,game_height - 80 - border_thickness - 60,90,60)
    , pygame.Rect(game_width/2 - 90,game_height/2 + 60,180,30)
    , pygame.Rect(game_width/2 - 90,game_height/2 - 60,30,150)
    , pygame.Rect(game_width/2 + 90,game_height/2 - 60,30,150)
]

#comment section
'''pac man based game with 1 enemy that can go through walls but is slow and the coins increase score.
before every move you want to save the x and y, and when collided with a wall, reset back to the previous x and y.
 Possibilities: add pellets and score counter, as well as adding extra point pellets (like cherrys).
 Eat ghosts with power pellets. save high score to computer. Maybe add the gateways at side of screen.'''

#"""""""""""""""""""""""""Menu screen for next.""""""""""""""""""""""""""""

while running:
    #event handle mouse and keyboards input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #save x and y in a variables
    save_x = playerect.x 
    save_y = playerect.y


        #player movement
    keys = pygame.key.get_pressed()
    if not gameover:
        if keys[pygame.K_d]:
            playerect.x += player_speed
        if keys[pygame.K_a]:
            playerect.x -= player_speed
        if keys[pygame.K_s]:
            playerect.y += player_speed
        if keys[pygame.K_w]:
            playerect.y -= player_speed

        #enemy movement
        if not singleplayer:
            if keys[pygame.K_RIGHT]:
               enemy_x +=enemy_speed
            if keys[pygame.K_LEFT]:
               enemy_x -=enemy_speed
            if keys[pygame.K_DOWN]:
               enemy_y +=enemy_speed
            if keys[pygame.K_UP]:
               enemy_y -=enemy_speed

        else:
            if playerect.x > enemy_x:
                #enemy moves right
                enemy_x += enemy_speed
            elif playerect.x < enemy_x:
                enemy_x -= enemy_speed
                
            if playerect.y > enemy_y:
                #enemy moves down
                enemy_y += enemy_speed
            elif playerect.y < enemy_y:
                enemy_y -= enemy_speed


    #switches between singleplayer and multiplayer
    if keys[pygame.K_SPACE] and not spacelock:
        singleplayer = not singleplayer
        spacelock = True
    elif not keys[pygame.K_SPACE] and spacelock:
        spacelock = False


   

    #moves hitbox with player
    enemyrect.x = enemy_x
    enemyrect.y = enemy_y


    #checking for colisions with the maze
    for rect in maze:
        if playerect.colliderect(rect):
            playerect.x = save_x
            playerect.y = save_y

    #checking for colisions with enemy and player and coin
    if playerect.colliderect(enemyrect):
        if not gameover:
            collision_sound.play()
        gameover = True

        

    #draw section
    if not gameover:
        for rect in maze:
            pygame.draw.rect(screen,( 0,52,0), rect )
        screen.blit(playerimage,playerect)
        #pygame.draw.rect(screen, (0,255,0), playerect)

        score += 1

        screen.blit(enemyimage,(enemy_x,enemy_y))
        testcoin.draw(screen)
    else:
        screen.fill((255,0,0))
        pygame.mixer.music.stop()
        screen.blit(gameovertext,gameovertextrect)
        if keys[pygame.K_RETURN]:
            enemy_x = 0
            enemy_y = game_height
            playerect.center = game_width/2, game_height/2
            collision_sound.stop()
            pygame.mixer.music.play(loops = -1)
            gameover = False



            
    #amount of fps being used 
    clock.tick(60)
    pygame.display.flip()
    screen.fill((0,100,120))
    






print(score)
with open ('score.dat' , 'wb') as file:
    pickle.dump(score,file)














pygame.quit()