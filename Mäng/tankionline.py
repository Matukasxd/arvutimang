import pygame
import math
import time

pygame.init()
pygame.mixer.init()
BLACK = (0,0,0)
WHITE = (255,255,255)

# Reso
size = (800,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tank Game")

# Clock
clock = pygame.time.Clock()

#Muusika
pygame.mixer.music.load('Waterflame-Glorious-Morning.ogg')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
#state
state = "MAPSelection"

#Map
MAP1 = pygame.image.load('MAP1.png')
MAP1 = pygame.transform.scale(MAP1, (300,200))
MAP2 = pygame.image.load('MAP2.png')
MAP2 = pygame.transform.scale(MAP2, (300,200))
#Pildid
tankImg = pygame.image.load('dank.png')
tankImg = pygame.transform.scale(tankImg, (50,70))
bulletImg = pygame.image.load('cannon ball.png')
bulletImg = pygame.transform.scale(bulletImg, (10,10))
explosionImg = pygame.image.load('explosion.png')
explosionImg = pygame.transform.scale(explosionImg, (50,50))
CongratulationsP1 = pygame.image.load('CongratulationsP1.png')
CongratulationsP1 = pygame.transform.scale(CongratulationsP1,(400,125))
CongratulationsP2 = pygame.image.load('CongratulationsP2.png')
CongratulationsP2 = pygame.transform.scale(CongratulationsP2,(400,125))
MainMenuIMG = pygame.image.load('MainMenuBackground.png')
MainMenuIMG = pygame.transform.scale(MainMenuIMG,(800,600))
Cong1 = 0
Cong2 = 0
#Fontid teksti jaoks
Selectionfont = pygame.font.Font('SuperMario256.ttf',64)
MAPfont = pygame.font.Font('SuperMario256.ttf', 30)
HPfont = pygame.font.Font('SuperMario256.ttf', 20)
MuusikaFont = pygame.font.Font('SuperMario256.ttf',15)
#HP asukohad(x,y)
P1HPx = 10
P1HPy = 10
P2HPx = 600
P2HPy = 10
#Õnnitluspildi asukohad(x,y)
GratzP1x = 180
GratzP1y = 250
GratzP2x = 180
GratzP2y = 250

#Klassid
class Tank():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.turnSpeed = 0
        self.bullets = []
        self.reloadTime = 0
        self.health = 2
    def rotate(self):
        self.angle += self.turnSpeed * 0.02
        if self.angle >= 360:
            self.angle -= 360
    def move(self):
        if 0 < self.x + math.sin(self.angle) * self.speed < 800 and 0 < self.y - math.cos(self.angle) * self.speed < 600:
            self.x += math.sin(self.angle) * self.speed
            self.y -= math.cos(self.angle) * self.speed
    def draw(self):
        rotated = pygame.transform.rotate(tankImg, -self.angle)
        screen.blit(rotated, (self.x, self.y))
        pygame.draw.line(screen, WHITE, (self.x + 25, self.y + 25), (self.x + 25 + math.sin(self.angle) * 50, self.y + 25 - math.cos(self.angle) * 50), 5) 
    def shoot(self):
        if self.reloadTime == 0:
            bullet = Bullet(self.x, self.y, self.angle)
            bullet.time = time.time()
            self.bullets.append(bullet)
            self.reloadTime = 0.7
    def update(self):
        self.rotate()
        self.move()
        for b in self.bullets:
            b.update()
        if self.reloadTime > 0:
            self.reloadTime -= 1/60
            if self.reloadTime < 0:
                self.reloadTime = 0
class Bullet():
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
    def update(self):
        if 0 < self.x + math.sin(self.angle) * self.speed < 800 and 0 < self.y - math.cos(self.angle) * self.speed < 600:
            self.x += math.sin(self.angle) * self.speed
            self.y -= math.cos(self.angle) * self.speed
    def draw(self):
        screen.blit(bulletImg, (self.x, self.y))
class Explosion():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = time.time()
    def draw(self):
        screen.blit(explosionImg, (self.x, self.y))
    def update(self):
        if time.time() - self.time > 0.7:
            explosions.remove(self)

def show_congratulationsP1(x,y):
    screen.blit(CongratulationsP1,(GratzP1x,GratzP1y))
def show_congratulationsP2(x,y):
    screen.blit(CongratulationsP2,(GratzP2x,GratzP2y))
#Mängijad ja asukohad
player1 = Tank(100, 100)
player2 = Tank(700, 500)
def update_P1HP(P1HPx,P1HPy):
    P1HP = HPfont.render("1.mangija elud:" + str(player1.health), True,(0,0,0))
    screen.blit(P1HP,(P1HPx,P1HPy))
def update_P2HP(P2HPx,P2HPy):
    P2HP = HPfont.render("2.mangija elud:" + str(player2.health), True, (0,0,0))
    screen.blit(P2HP,(P2HPx,P2HPy))
def resetGame():
    # Reset player 1
    player1.x = 100
    player1.y = 100
    player1.angle = 0
    player1.speed = 0
    player1.turnSpeed = 0
    player1.bullets = []
    player1.reloadTime = 0
    player1.health = 2
    
    # Reset player 2
    player2.x = 700
    player2.y = 500
    player2.angle = 0
    player2.speed = 0
    player2.turnSpeed = 0
    player2.bullets = []
    player2.reloadTime = 0
    player2.health = 2

explosions = []
#Mängu tsükkel
lasttype = ""
done = False
while not done:
#     print(state)
    #Laseb mängu kinni panna
    if state == "MAPSelection":
        Cong1 = 0
        Cong2 = 0
        screen.fill(WHITE)
        screen.blit(MainMenuIMG,(0,0))
        mapivalik = Selectionfont.render("Mapi valik",True,(0,0,0))
        screen.blit(mapivalik,(200, 10))
        firstmap = screen.blit(MAP1,(75,200))        
        secondmap = screen.blit(MAP2,(425,200))
        QUITtext = MAPfont.render('quit',True,(0,0,0))
        MAP1text = MAPfont.render('Korbemapp',True,(0,0,0))
        MAP2text = MAPfont.render('Paintiga tehtud', True,(0,0,0))
        Muusikatext1 = MuusikaFont.render('Muusika: ', True,(0,0,0))
        Muusikatext2 = MuusikaFont.render('Waterflame - Glorious Morning', True,(0,0,0))
        screen.blit(MAP1text,(100,425))
        screen.blit(MAP2text,(450,425))
        screen.blit(QUITtext,(350,500))
        screen.blit(Muusikatext1,(75,125))
        screen.blit(Muusikatext2,(75,150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lasttype = pygame.K_LEFT
                if event.key == pygame.K_RIGHT:
                    lasttype = pygame.K_RIGHT
                if event.key == pygame.K_DOWN:
                    lasttype = pygame.K_DOWN
                if event.key == pygame.K_RETURN:
                    if lasttype == pygame.K_LEFT:
                        state = "Game"
                        backgroundImg = pygame.image.load('MAP1.png')
                        backgroundImg = pygame.transform.scale(backgroundImg, (800,600))
                        break
                    if lasttype == pygame.K_RIGHT:
                        state = "Game"
                        backgroundImg = pygame.image.load('MAP2.png')
                        backgroundImg = pygame.transform.scale(backgroundImg,(800,600))          
                        break
                    if lasttype == pygame.K_DOWN:
                        done = True
        if lasttype == pygame.K_LEFT:
            pygame.draw.rect(screen,(255,0,0),pygame.Rect(75,200,300,200),4)
        if lasttype == pygame.K_RIGHT:
            pygame.draw.rect(screen,(255,0,0),pygame.Rect(425,200,300,200),4)
        if lasttype == pygame.K_DOWN:
            pygame.draw.line(screen,(255,0,0),(350,525),(425,525),width=4)
        pygame.display.flip()
        
    if state == "Game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        player1.speed = 0
        player1.turnSpeed = 0
        player2.speed = 0
        player2.turnSpeed = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1.speed = 1
        if keys[pygame.K_a]:
            player1.turnSpeed = -1
        if keys[pygame.K_d]:
            player1.turnSpeed = 1
        if keys[pygame.K_UP]:
            player2.speed = 1
        if keys[pygame.K_LEFT]:
            player2.turnSpeed = -1
        if keys[pygame.K_RIGHT]:
            player2.turnSpeed = 1
        if keys[pygame.K_SPACE] and player1.reloadTime == 0:
            player1.shoot()
        if keys[pygame.K_RETURN] and player2.reloadTime == 0:
            player2.shoot()
        player1.update()
        player2.update()

        for b in player1.bullets:
            if time.time() - b.time > 2:
                player1.bullets.remove(b)
            if b.x > player2.x and b.x < player2.x + 50 and b.y > player2.y and b.y < player2.y + 50:
                explosions.append(Explosion(player2.x, player2.y))
                player2.health -= 1
                player1.bullets.remove(b)
        for b in player2.bullets:
            if time.time() - b.time > 2:
                player2.bullets.remove(b)
            if b.x > player1.x and b.x < player1.x + 50 and b.y > player1.y and b.y < player1.y + 50:
                explosions.append(Explosion(player1.x, player1.y))
                player1.health -= 1
                player2.bullets.remove(b)
        #Joonistab asjad ekraanile
        screen.fill(BLACK)
        screen.blit(backgroundImg, (0,0))
        rotated1 = pygame.transform.rotate(tankImg, -player1.angle * 57)
        screen.blit(rotated1, (player1.x, player1.y))
        rotated2 = pygame.transform.rotate(tankImg, -player2.angle * 57)
        screen.blit(rotated2, (player2.x, player2.y))
        if player1.health == 0:
    #         if clock.get_time() < 60:
            show_congratulationsP2(GratzP2x,GratzP2y)
    #         print("Congratulations Player 2!")
            Cong2 += 1
            if Cong2 >= 30:
                resetGame()
                state = "MAPSelection"
        if player2.health == 0:
    #         if clock.get_time() < 60:
            show_congratulationsP1(GratzP1x,GratzP1y)
    #         print("Congratulations Player 1!")
            Cong1 += 1
            if Cong1 >= 30:
                resetGame()
                state = "MAPSelection"
        #Sihtimisjooned
        #pygame.draw.line(screen, WHITE, (player1.x + 25, player1.y + 25), (player1.x + 25 + math.sin(player1.angle) * 50, player1.y + 25 - math.cos(player1.angle) * 50), 5) 
        #pygame.draw.line(screen, WHITE, (player2.x + 25, player2.y + 25), (player2.x + 25 + math.sin(player2.angle) * 50, player2.y + 25 - math.cos(player2.angle) * 50), 5) 
        for b in player1.bullets:
            b.draw()
        for b in player2.bullets:
            b.draw()
        for e in explosions:
            e.draw()
            e.update()
        update_P1HP(P1HPx,P1HPy)
        update_P2HP(P2HPx,P2HPy)
        #Mängu tickrate
        pygame.display.flip()
        clock.tick(60)
pygame.mixer.quit()
pygame.quit()
