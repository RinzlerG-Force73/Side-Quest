import pygame
import pickle
import os
from coin import Coin

pygame.init()
pygame.mixer.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

#For controller purposes
#LEFT = 1024

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



#Score section
score = 0
highscore = 0
pog = []
def resetpog():
    global pog
    pog = [
    Coin(37,78)
    ,Coin(37,94)
    ,Coin(37,108)
    ]
resetpog()

if os.path.exists('highscore.dat'):
    with open ('highscore.dat' , 'rb') as file:
        highscore = pickle.load(file)

#Text section
font = pygame.font.SysFont("arialunicode", 70, bold = True)
font2 = pygame.font.SysFont("arialunicode", 24, italic = True)
gameovertext = font.render("Gameover" , True , (0,0,0))
gameovertextrect = gameovertext.get_rect(center = (game_width/2 , game_height/2))
scoretext = font2.render(f"Score: {score}" , True , (0,0,0))
highscoretext = font2.render(f"Highscore: {highscore}" , True , (0,0,0))
highscoretextrect = highscoretext.get_rect()


#singleplayer section
singleplayer = True
spacelock = False

#gameover section
gameover = False



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
'''Possibilities: add pellets and score counter, as well as adding extra point pellets (like cherrys).
 Eat ghosts with power pellets. save high score to computer. Maybe add the gateways at side of screen. Laser system'''

while running:
    #event handle mouse and keyboards input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.JOYBUTTONDOWN:
            pass #print(event)

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

    #checking for colisions with enemy and player
    if playerect.colliderect(enemyrect):
        if not gameover:
            collision_sound.play()
        gameover = True


    #Add Score
    for coin in pog:
        if playerect.colliderect(coin.rect):
            score += 10
            scoretext = font2.render(f"Score: {score}" , True , (0,0,0))
            pog.remove(coin)
            highscore = max(score,highscore)
            highscoretext = font2.render(f"Highscore: {highscore}" , True , (0,0,0))
            highscoretextrect = highscoretext.get_rect()

    #draw section
    if not gameover:
        for rect in maze:
            pygame.draw.rect(screen,( 0,52,0), rect )
        screen.blit(playerimage,playerect)
        screen.blit(scoretext,(12,0))
        screen.blit(highscoretext, (game_width - highscoretextrect.width,0))
        #pygame.draw.rect(screen, (0,255,0), playerect)

    
        screen.blit(enemyimage,(enemy_x,enemy_y))
        for coin in pog:
            coin.draw(screen)

    else:
        screen.fill((255,0,0))
        pygame.mixer.music.stop()
        screen.blit(gameovertext,gameovertextrect)
        screen.blit(scoretext,(gameovertextrect.x,gameovertextrect.bottom))
        screen.blit(highscoretext, (gameovertextrect.x,gameovertextrect.bottom + 30))
        if keys[pygame.K_RETURN]:
            enemy_x = 0
            enemy_y = game_height
            playerect.center = game_width/2, game_height/2
            collision_sound.stop()
            pygame.mixer.music.play(loops = -1)
            gameover = False
            score = 0
            scoretext = font2.render(f"Score: {score}" , True , (0,0,0))
            resetpog()



            
    #amount of fps being used 
    clock.tick(60)
    pygame.display.flip()
    screen.fill((0,100,120))
    






with open ('highscore.dat' , 'wb') as file:
    pickle.dump(highscore,file)














pygame.quit()