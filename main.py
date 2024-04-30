import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800,600))


# Background
background = pygame.image.load('i.png')
over_font = pygame.font.Font('t.otf', 64)
p_font = pygame.font.Font('freesansbold.ttf', 72)
i = pygame.font.Font('freesansbold.ttf', 32)
k = pygame.font.Font('freesansbold.ttf', 52)
w = pygame.font.Font('h.otf',72)
#w = pygame.font.Font('c.ttf', 72)
def p_text():
        over_text = p_font.render("Paused", True, (100, 0, 0))
        screen.blit(over_text, (240, 200))
def im():
        over_text = w.render("             space invaders", True, (0,255,255))
        screen.blit(over_text, (0, 100))
def imy():
        over_text = i.render("-created by adi", True, (0,255,0))
        screen.blit(over_text, (500, 160))

def pkm():
        over_text =k.render("press space to begin...", True, (255,255,0))
        screen.blit(over_text, (100, 300))


# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

            
            
def welcome():
    bg = pygame.image.load('i.png')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Game()
        screen.blit(bg,(0,0))
        im()
        imy()
        pkm()
        pygame.display.update()
def Game():
    shield_active = False
    shield_duration = 30   # seconds
    time_since_shield_activation = 0
    deflect_attack = False
    running = True
    p_v = False
    mixer.music.load("background.wav")
    mixer.music.play(-1)
    clock = pygame.time.Clock()
    game_over = False
    # Player
    playerImg = pygame.image.load('player.png')
    playerX = 370
    playerY = 480
    playerX_change = 0
    p_m = pygame.mask.from_surface(playerImg)
    # Enemy
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6
    h    = 5
    e_bs =[]
    e_b_r = False
    l = pygame.time.get_ticks()
    g = 500
    hp = []
    mhp =[]
    r = []
    p_hp = 100
    p_mhp = 100
    a = []
    timea =[]
    time =[]

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('enemy.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)
        hp.append(100)
        mhp.append(100)
        
    # Bullet

    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving
    p = pygame.image.load("bullet.png")
    bulletImg = pygame.image.load('b.png')

    b_m = pygame.mask.from_surface(p)          
    e_b_m = pygame.mask.from_surface(bulletImg)
    bulletX = [] 
    bulletY = []
    bullet_ready = False
    bul = []
    rect = pygame.Rect(playerX,playerY,50,50)       

    # Score

    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)

    textX = 10
    testY = 10

    # Game Over
    

    e_bt = random.randint(2,5)

    def show_score(x, y):
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))
    def c(x, y):
        score = font.render("shield : " + str(time_since_shield_activation*3//1000)+"%", True, (255, 255, 255))
        screen.blit(score, (x, y))


    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(over_text, (200, 200))


    def player(x, y):
        screen.blit(playerImg, (x, y))


    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))




    def isCollision(x,y, a, b):
        distance = math.sqrt(math.pow(x - a, 2) + (math.pow(y - b, 2)))
        if distance < 27:
            return True
        else:
            return False
    def e_isCollision(x,y, a, b):
        distance = math.sqrt(math.pow(x + a, 2) + (math.pow(y + b, 2)))
        if distance < 27:
            return True
        else:
            return False

    class Explosion(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            for num in range(1, 6):
                img = pygame.image.load(f"img/exp{num}.png")
                img = pygame.transform.scale(img, (100, 100))
                self.images.append(img)
            self.index = 0
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.counter = 0

        def update(self):
            explosion_speed = 3
            #update explosion animation
            self.counter += 1

            if self.counter >= explosion_speed and self.index < len(self.images) - 1:
                self.counter = 0
                self.index += 1
                self.image = self.images[self.index]

            #if the animation is complete, reset animation index
            if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
                self.kill()


    explosion_group = pygame.sprite.Group()

    # Game Loop
    while running:
        
        if game_over:
            r_b = pygame.image.load("R.png")
            r_b = pygame.transform.scale(r_b,(115,65))
            
            e_b = pygame.image.load("R (1).png")
            e_b = pygame.transform.scale(e_b,(145,130))
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))
            screen.blit(e_b, (320+10+10+100,350))
            screen.blit(r_b, (210+10-10,360+10))
            r_b_r = pygame.Rect(210,370,r_b.get_height(),r_b.get_width())
            e_b_r = pygame.Rect(440,350,e_b.get_height(),e_b.get_width())
            game_over_text()
            

            pos = pygame.mouse.get_pos()
            mixer.music.stop()
            if r_b_r.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]==1:
                    Game()
                    

            if e_b_r.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]==1:
                    running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            pygame.display.update()
            
        else:
            
            if p_v == True:
                
                r_b = pygame.image.load("d.png")
                r_b = pygame.transform.scale(r_b,(150,65))
                
                e_b = pygame.image.load("R (1).png")
                e_b = pygame.transform.scale(e_b,(170,130))
                
                r_b_r = pygame.Rect(210,370,r_b.get_height(),r_b.get_width())
                e_b_r = pygame.Rect(440,350,e_b.get_height(),e_b.get_width())
                
                mixer.music.stop()
                
                
                    
                pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False


                if r_b_r.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0]==1:
                        p_v = False
                        mixer.music.load("background.wav")
                        mixer.music.play(-1)

                if e_b_r.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0]==1:
                        running = False
                
                screen.fill((0, 0, 0))
                screen.blit(background, (0, 0))
                screen.blit(e_b, (320+10+10+100,350))
                screen.blit(r_b, (210+10-10,360+10))
                p_text()
                pygame.display.update()
        # RGB = Red, Green, Blue
            else:
                screen.fill((0, 0, 0))
                screen.blit(background, (0, 0))

                # Background Image
                screen.blit(background, (0, 0))
                explosion_group.draw(screen)
                explosion_group.update()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                            # if keystroke is pressed check whether its right or left
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            playerX_change = -7
                        if event.key == pygame.K_RIGHT:
                            playerX_change = 7
                        if event.key == pygame.K_SPACE and len(bul) <=5:
                            bullet_ready = True
                            #b_s = mixer.Sound('laser.wav')
                            #b_s.play()
                        if event.key == pygame.K_ESCAPE:
                            
                            p_v = True
                        if event.key == pygame.K_RETURN:
                # Activate shield if enough time has passed since the last activation
                            if time_since_shield_activation >= shield_duration * 1000:
                                shield_active = True
                                deflect_attack = True
                                  # Reset the timer

                    if event.type == pygame.KEYUP :
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            playerX_change = 0
                    

                time_since_shield_activation += clock.get_time()
                # 5 = 5 + -0.1 -> 5 = 5 - 0.1
                # 5 = 5 + 0.1
                t = pygame.time.get_ticks()
                if t -l >g:
                    e_b_x = random.choice(enemyX)
                    e_b_y = random.choice(enemyY)
                    e_b_r = True
                    l = t
                playerX += playerX_change
                if playerX <= 0:
                    playerX = 0
                elif playerX >= 736:
                    playerX = 736

                if e_b_r and len(e_bs) < 5:
                    e_bs.append(pygame.Rect(e_b_x-10,e_b_y+25,50,50) )
                    e_b_r = False
                for b in e_bs:
                    
                    b.y +=10
                    screen.blit(bulletImg,b)
                for r,b in enumerate(e_bs):
                    if b.y > 500:
                        del(e_bs[r]) 
                    if shield_active:
                        pygame.draw.rect(screen, "blue", (playerX, playerY, 75, 15))
                    else:
                        p_r = p_hp/p_mhp

                        pygame.draw.rect(screen, "red", (playerX, playerY, 75, 15))  
                        pygame.draw.rect(screen, "green", (playerX, playerY, 75 * p_r, 15))

                    
                    if p_m.overlap(b_m,(playerX-b.x,playerY-b.y)) and deflect_attack:
                            b.y = 10000
                            deflect_attack = False
                            time_since_shield_activation = 0
                            
                    elif p_m.overlap(b_m,(playerX-b.x,playerY-b.y)):
                            pygame.draw.rect(screen, "red", (playerX, playerY, 75, 15))  
                            pygame.draw.rect(screen, "green", (playerX, playerY, 75 * p_r, 15))
                            
                            shield_active = False
                            p_hp = p_hp- 40
                            p_hp = p_hp
                            explosionSound = mixer.Sound("explosion.wav")
                            explosionSound.play()
                            explosion = Explosion(playerX, playerY)
                            explosion_group.add(explosion)
                            shield_active = False
                            for r,b in enumerate(e_bs):
                                    del(e_bs[r]) 

                            if p_hp <= 0:
                                game_over = True
                
                if bullet_ready:
                    bul.append(pygame.Rect(playerX-10,playerY+15,50,50) )
                    bullet_ready = False

                for bulle in bul:
                    
                    bulle.y -=10
                    screen.blit(p,bulle)

                for rs,bd in enumerate(bul):
                    if bd.y < 100:
                        del(bul[rs])
                for bulle in bul:
                    for b in e_bs:
                        if e_b_m.overlap(b_m,(bulle.x-b.x,bulle.y-b.y)):
                            
                            for r,b in enumerate(e_bs):
                            
                                del(e_bs[r]) 
                            for rs,bd in enumerate(bul):
                                
                                    del(bul[rs])

                            explosion = Explosion(bulle.x,bulle.y)
                            explosion_group.add(explosion)
                # Enemy Movement
                for i in range(num_of_enemies): 

                    a=pygame.time.get_ticks()
                    time = str(a)[0]
                    
                    # Game Over
                    if enemyY[i] > 440:
                        game_over = True

                    enemyX[i] += enemyX_change[i]
                    if enemyX[i] <= 0:
                        enemyX_change[i] = 5
                        enemyY[i] += enemyY_change[i]
                    elif enemyX[i] >= 736:
                        enemyX_change[i] = -5      
                        enemyY[i] += enemyY_change[i]
                    
                                
                    for bulle in bul:
                        collision = isCollision(enemyX[i], enemyY[i], bulle.x, bulle.y)
                        if collision:
                                explosionSound = mixer.Sound("explosion.wav")
                                explosionSound.play()
                                for rs,bd in enumerate(bul):
                    
                                    del(bul[rs]) 
                                score_value += 1
                                hp[i] -= random.randint(10,50)
                                
                                explosion = Explosion(enemyX[i], enemyY[i])
                                explosion_group.add(explosion)
                                
            # If the shield is active, decrease its strength
            
                                if hp[i] <= 0:
                                    enemyX[i] = random.randint(0, 736)
                                    enemyY[i] = random.randint(50, 150)
                                    hp[i] = 100

                    enemy(enemyX[i], enemyY[i], i)
                    r=hp[i]/mhp[i]
                    
                    pygame.draw.rect(screen,"red",(enemyX[i],enemyY[i],75,15))
                    pygame.draw.rect(screen,"green",(enemyX[i],enemyY[i],75*r,15))
                        
                # Bullet Movemeant
            c(500,50)    
            clock.tick(60)
            player(playerX, playerY)
            show_score(textX, testY)
            
            pygame.display.update()
            
welcome()