import pygame
import math
import time

# pygame.mixer.quit()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
BLACK = (0,0,0)
WHITE = (255,255,255)

# Reso
size = (800,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tank Game")

#Muusika
pygame.mixer.music.set_volume(0.3)


# Clock
clock = pygame.time.Clock()

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

#Helid
background  = pygame.mixer.music.load('Waterflame-Glorious-Morning.ogg')
lask = pygame.mixer.Sound("LASK1.ogg")
plahvatus = pygame.mixer.Sound('PLAHVATUS1.ogg')
pygame.mixer.music.play(-1)
#Muutujad
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
obstacles = []
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
def OBSTACLES(obstacle):
    global obstacles
    if obstacle == "MAP1":
        obstacles = [(0, 342),(13, 354),(29, 376),(44, 351),(51, 342),
                     (159, 334),(175, 355),(197, 358),(220, 356),(3, 322),
                     (25, 345),(59, 306),(161, 310),(186, 328),(210, 329),
                     (241, 328),(262, 316),(270, 298),(274, 278),(274, 258),
                     (266, 234),(262, 198),(263, 173),(253, 148),(250, 126),
                     (249, 103),(249, 91),(245, 67),(239, 38),(234, 3),
                     (444, 214),(450, 229),(470, 228),(483, 221),(488, 202),
                     (482, 175),(446, 178),(561, 102),(547, 68),(553, 49),
                     (568, 54),(574, 65),(574, 86),(572, 107),(567, 428),
                     (558, 448),(562, 468),(573, 480),(583, 495),(578, 478),
                     (583, 452),(576, 433),(442,254),(567,441),(567,426),
                    (523, 578),(575, 578),(584, 577),(597, 577),(610, 578),(623, 578),
                    (631, 578),(645, 578),(655, 578),(669, 578),(682, 578),(695, 576),
                    (710, 578),(725, 578),(737, 578),(756, 579),(770, 579),(779, 579),
                    (786, 579),(796, 579),(577, 481),(578, 478),(583, 446),(570, 438),
                    (566, 455),(571, 472),(578, 489),(478, 225),(481, 210),(484, 192),
                    (483, 186),(469, 184),(455, 186),(449, 198),(450, 213),(452, 220),
                    (458, 218),(473, 218),(567, 85),(570, 68),(564, 54),(554, 54),
                    (551, 73),(554, 94),(795, 558),(795, 549),(795, 537),(4, 595),
                    (794, 523),(794, 514),(798, 495),(798, 482),(796, 470),(796, 458),
                    (796, 442),(794, 425),(795, 414),(798, 398),(798, 395),(798, 392),
                    (798, 390),(798, 372),(796, 356),(796, 342),(796, 329),(796, 310),
                    (794, 282),(794, 266),(794, 246),(794, 230),(794, 211),(795, 191),
                    (795, 173),(794, 152),(794, 137),(794, 125),(794, 102),(794, 86),
                    (794, 71),(793, 52),(794, 33),(794, 16),(794, 2),(779, 4),
                    (765, 6),(745, 4),(726, 3),(715, 3),(694, 3),(679, 3),
                    (666, 3),(646, 3),(512, 5),(494, 4),(468, 7),(433, 6),
                    (402, 6),(374, 6),(346, 4),(319, 4),(285, 3),(264, 3),
                    (242, 3),(218, 5),(186, 6),(162, 6),(134, 4),(120, 3),
                    (93, 2),(71, 2),(52, 4),(32, 5),(14, 6),(6, 8),
                    (6, 37),(6, 50),(4, 67),(4, 91),(4, 109),(4, 136),
                    (0, 188),(2, 214),(6, 254),(4, 279),(3, 371),(3, 398),
                    (3, 421),(6, 449),(3, 490),(3, 520),(2, 546),(2, 577),
                    (25, 591),(38, 592),(52, 593),(62, 594),(72, 594),(81, 594),
                    (97, 594),(118, 594),(134, 594),(151, 592),(175, 593),(202, 594),
                    (227, 592),(254, 592),(276, 593),(310, 590),(346, 591),(358, 591),
                    (380, 594),(406, 593),(432, 590),(462, 589),(478, 590),(502, 595),
                    (559,59),(568,432)]
#         obstacles = [(10, 310),(20, 318),(26, 326),(33, 317),(41, 308),(62,190),
#                     (177, 292),(554, 578),(185, 302),(189, 310),(199, 311),(207, 311),
#                     (220, 296),(235, 296),(240, 309),(252, 310),(258, 295),(261, 282),
#                     (263, 264),(263, 253),(254, 241),(250, 231),(251, 210),(251, 196),
#                     (252, 188),(252, 178),(246, 170),(241, 150),(240, 130),(240, 122),
#                     (238, 98),(238, 77),(234, 44),(235, 27),(236, 12),(523, 590),
#                     (523, 578),(575, 578),(584, 577),(597, 577),(610, 578),(623, 578),
#                     (631, 578),(645, 578),(655, 578),(669, 578),(682, 578),(695, 576),
#                     (710, 578),(725, 578),(737, 578),(756, 579),(770, 579),(779, 579),
#                     (786, 579),(796, 579),(577, 481),(578, 478),(583, 446),(570, 438),
#                     (566, 455),(571, 472),(578, 489),(478, 225),(481, 210),(484, 192),
#                     (483, 186),(469, 184),(455, 186),(449, 198),(450, 213),(452, 220),
#                     (458, 218),(473, 218),(567, 85),(570, 68),(564, 54),(554, 54),
#                     (551, 73),(554, 94),(795, 558),(795, 549),(795, 537),(4, 595),
#                     (794, 523),(794, 514),(798, 495),(798, 482),(796, 470),(796, 458),
#                     (796, 442),(794, 425),(795, 414),(798, 398),(798, 395),(798, 392),
#                     (798, 390),(798, 372),(796, 356),(796, 342),(796, 329),(796, 310),
#                     (794, 282),(794, 266),(794, 246),(794, 230),(794, 211),(795, 191),
#                     (795, 173),(794, 152),(794, 137),(794, 125),(794, 102),(794, 86),
#                     (794, 71),(793, 52),(794, 33),(794, 16),(794, 2),(779, 4),
#                     (765, 6),(745, 4),(726, 3),(715, 3),(694, 3),(679, 3),
#                     (666, 3),(646, 3),(512, 5),(494, 4),(468, 7),(433, 6),
#                     (402, 6),(374, 6),(346, 4),(319, 4),(285, 3),(264, 3),
#                     (242, 3),(218, 5),(186, 6),(162, 6),(134, 4),(120, 3),
#                     (93, 2),(71, 2),(52, 4),(32, 5),(14, 6),(6, 8),
#                     (6, 37),(6, 50),(4, 67),(4, 91),(4, 109),(4, 136),
#                     (0, 188),(2, 214),(6, 254),(4, 279),(3, 371),(3, 398),
#                     (3, 421),(6, 449),(3, 490),(3, 520),(2, 546),(2, 577),
#                     (25, 591),(38, 592),(52, 593),(62, 594),(72, 594),(81, 594),
#                     (97, 594),(118, 594),(134, 594),(151, 592),(175, 593),(202, 594),
#                     (227, 592),(254, 592),(276, 593),(310, 590),(346, 591),(358, 591),
#                     (380, 594),(406, 593),(432, 590),(462, 589),(478, 590),(502, 595),
#                     (54, 301),(63, 288)]
        return obstacles
    if obstacle == "MAP2":
        obstacles = [(54, 580),(51, 551),(49, 534),(53, 510),(52, 473),
                    (54, 446),(53, 414),(53, 386),(51, 354),(51, 322),
                    (52, 286),(52, 268),(34, 247),(13, 238),(119, 574),
                    (121, 543),(122, 512),(122, 486),(114, 474),(113, 448),
                    (115, 428),(115, 396),(113, 372),(113, 340),(132, 322),
                    (151, 320),(159, 324),(163, 342),(158, 363),(160, 382),
                    (158, 413),(159, 426),(159, 436),(159, 451),(159, 470),
                    (162, 490),(159, 505),(268, 432),(284, 433),(291, 433),
                    (299, 433),(314, 433),(341, 434),(364, 433),(372, 431),
                    (373, 402),(373, 382),(369, 362),(358, 360),(356, 335),
                    (354, 313),(366, 306),(371, 294),(369, 274),(349, 273),
                    (338, 263),(328, 293),(314, 322),(301, 336),(295, 350),
                    (286, 352),(286, 366),(281, 369),(273, 369),(111, 55),
                    (243, 28),(398, 151),(399, 169),(422, 178),
                    (262, 475),(284, 474),(295, 474),(347, 479),(363, 478),
                    (375, 477),(397, 226),(426, 225),(462, 218),(486, 218),
                    (502, 215),(514, 220),(515, 185),(511, 158),(504, 154),
                    (468, 150),(434, 154),(419, 153),(407, 154),(402, 168),
                    (402, 183),(434, 178),(488, 186),(608, 293),(608, 271),
                    (630, 270),(633, 282),(645, 282),(651, 296),(661, 298),
                    (661, 313),(662, 327),(647, 323),(652, 364),(673, 365),
                    (634, 350),(622, 340),(610, 334),(609, 323),(426, 582),
                    (442, 584),(462, 584),(487, 584),(501, 583),(410, 587),
                    (486, 583),(499, 583),(506, 582),(506, 569),(538, 574),
                    (550, 574),(569, 575),(571, 559),(570, 545),(579, 542),
                    (591, 547),(591, 554),(592, 573),(614, 571),(629, 570),
                    (642, 578),(656, 593)]
        return obstacles
        
explosions = []
#Mängu tsükkel
lasttype = ""
done = False
while not done:
    #Laseb mängu kinni panna
    if state == "MAPSelection":
#         pygame.mixer.music.play(-1)
        Cong1 = 0
        Cong2 = 0
        screen.fill(WHITE)
        screen.blit(MainMenuIMG,(0,0))
        mapivalik = Selectionfont.render("Mapi valik",True,(0,0,0))
        screen.blit(mapivalik,(200, 10))
        firstmap = screen.blit(MAP1,(75,250))        
        secondmap = screen.blit(MAP2,(425,250))
        QUITtext = MAPfont.render('quit',True,(0,0,0))
        MAP1text = MAPfont.render('Korbemapp',True,(0,0,0))
        MAP2text = MAPfont.render('Linnamapp', True,(0,0,0))
        Muusikatext1 = MuusikaFont.render('Muusika: ', True,(0,0,0))
        Muusikatext2 = MuusikaFont.render('Waterflame - Glorious Morning', True,(0,0,0))
        screen.blit(MAP1text,(100,475))
        screen.blit(MAP2text,(450,475))
        screen.blit(QUITtext,(350,525))
        screen.blit(Muusikatext1,(75,125))
        screen.blit(Muusikatext2,(75,150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
#                     pygame.draw.rect(screen,(255,0,0),pygame.Rect(0,0,350,350),2)
                    lasttype = pygame.K_LEFT

                if event.key == pygame.K_RIGHT:
#                     pygame.draw.rect(screen,(255,0,0),pygame.Rect(30,30,60,60),2)
                    lasttype = pygame.K_RIGHT
                if event.key == pygame.K_DOWN:
                    lasttype = pygame.K_DOWN
                if event.key == pygame.K_RETURN:
                    if lasttype == pygame.K_LEFT:
                        state = "Game"
                        backgroundImg = pygame.image.load('MAP1.png')
                        backgroundImg = pygame.transform.scale(backgroundImg, (800,600))
                        obstacle = "MAP1"
                        OBSTACLES(obstacle)
                        break
                    if lasttype == pygame.K_RIGHT:
                        state = "Game"
                        backgroundImg = pygame.image.load('MAP2.png')
                        backgroundImg = pygame.transform.scale(backgroundImg,(800,600))
                        obstacle = "MAP2"
                        OBSTACLES(obstacle)
                        break
                    if lasttype == pygame.K_DOWN:
                        done = True
        if lasttype == pygame.K_LEFT:
            pygame.draw.rect(screen,(255,0,0),pygame.Rect(75,250,300,200),3)
        if lasttype == pygame.K_RIGHT:
            pygame.draw.rect(screen,(255,0,0),pygame.Rect(425,250,300,200),3)
        if lasttype == pygame.K_DOWN:
            pygame.draw.line(screen,(255,0,0),(350,550),(425,550),width=4)
        pygame.display.flip()
        
    if state == "Game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
        player1.speed = 0
        player1.turnSpeed = 0
        player2.speed = 0
        player2.turnSpeed = 0
        keys = pygame.key.get_pressed()
#         for el in obstacles:
# #             if b.x > a[0] and b.x < a[0] + 20 and b.y > a[1] and b.y < a[1] + 20 Inspiratsiooniks
#             if player1.x >= el[0] and player1.x < el[0] + 20 and player1.y > el[1] and player1.y < el[1] + 20:
#                 player1.speed = 0
#                 player1.turnSpeed = 0
#             if player2.x >= el[0] and player2.x < el[0] + 20 and player2.y > el[1] and player2.y < el[1] + 20:
#                 player2.speed = 0
#                 player2.turnSpeed = 0
        if keys[pygame.K_w]:
            player1.speed = 1
            for obstacle in obstacles:
                if player1.x > obstacle[0] and player1.x < obstacle[0] + 20 and player1.y > obstacle[1] and player1.y < obstacle[1] + 20:
                    player1.speed = -1
        if keys[pygame.K_a]:
            player1.turnSpeed = -1
            for obstacle in obstacles:
                if player1.x > obstacle[0] and player1.x < obstacle[0] + 20 and player1.y > obstacle[1] and player1.y < obstacle[1] + 20:
                    player1.turnSpeed = 1
                
        if keys[pygame.K_d]:
            player1.turnSpeed = 1
            for obstacle in obstacles:
                if player1.x > obstacle[0] and player1.x < obstacle[0] + 20 and player1.y > obstacle[1] and player1.y < obstacle[1] + 20:
                    player1.turnSpeed = 1
        if keys[pygame.K_UP]:
            player2.speed = 1
            for obstacle in obstacles:
                if player2.x > obstacle[0] and player2.x < obstacle[0] + 20 and player2.y > obstacle[1] and player2.y < obstacle[1] + 20:
                    player2.speed = -1
            
        if keys[pygame.K_LEFT]:
            player2.turnSpeed = -1
            for obstacle in obstacles:
                if player2.x > obstacle[0] and player2.x < obstacle[0] + 20 and player2.y > obstacle[1] and player2.y < obstacle[1] + 20:
                    player2.turnSpeed = 1
        if keys[pygame.K_RIGHT]:
            player2.turnSpeed = 1
            for obstacle in obstacles:
                if player2.x > obstacle[0] and player2.x < obstacle[0] + 20 and player2.y > obstacle[1] and player2.y < obstacle[1] + 20:
                    player2.turnSpeed = 1
    
        if keys[pygame.K_s]:
            player1.speed = -1
            for obstacle in obstacles:
                if player1.x > obstacle[0] and player1.x < obstacle[0] + 20 and player1.y > obstacle[1] and player1.y < obstacle[1] + 20:
                    player1.speed = 0
        if keys[pygame.K_DOWN]:
            player2.speed = -1
            for obstacle in obstacles:
                if player2.x > obstacle[0] and player2.x < obstacle[0] + 20 and player2.y > obstacle[1] and player2.y < obstacle[1] + 20:
                    player2.speed = 0
        if keys[pygame.K_SPACE] and player1.reloadTime == 0:
            lask.play()
            player1.shoot()
        if keys[pygame.K_RETURN] and player2.reloadTime == 0:
            lask.play()
            player2.shoot()
        player1.update()
        player2.update()

        for b in player1.bullets:
            counter = 0
            for a in obstacles:
                if b.x > a[0] and b.x < a[0] + 20 and b.y > a[1] and b.y < a[1] + 20:
                #if b.x in a[0] and b.x < a[0] + 50 and b.y in a[1] and b.y < a[1] + 50:
                    counter += 1
                    plahvatus.play()
                    explosions.append(Explosion(a[0],a[1]))
                    if counter == 1:
                        player1.bullets.remove(b)
            if time.time() - b.time > 2:
                player1.bullets.remove(b)
            if b.x > player2.x and b.x < player2.x + 20 and b.y > player2.y and b.y < player2.y + 20:
                plahvatus.play()
                explosions.append(Explosion(player2.x, player2.y))
                player2.health -= 1
                player1.bullets.remove(b)
        for b in player2.bullets:
            counter = 0
            for a in obstacles:
                if b.x > a[0] and b.x < a[0] + 25 and b.y > a[1] and b.y < a[1] + 25:
                #if b.x in a[0] and b.x < a[0] + 50 and b.y in a[1] and b.y < a[1] + 50:
                    counter += 1
                    plahvatus.play()
                    explosions.append(Explosion(a[0],a[1]))
                    if counter == 1:
                        player2.bullets.remove(b)
            if time.time() - b.time > 2:
                player2.bullets.remove(b)
            if b.x > player1.x and b.x < player1.x + 50 and b.y > player1.y and b.y < player1.y + 50:
                plahvatus.play()
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
            show_congratulationsP2(GratzP2x,GratzP2y)
            Cong2 += 1
            if Cong2 >= 45:
                resetGame()
                state = "MAPSelection"
        if player2.health == 0:
            show_congratulationsP1(GratzP1x,GratzP1y)
            Cong1 += 1
            if Cong1 >= 45:
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
