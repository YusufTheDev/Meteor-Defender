import pygame
import math
import button
import meteorite
import random

#functions
def drawText(text, font, textColor, screen, x, y):
    img = font.render(text, True, textColor)
    screen.blit(img,(x,y))

#upgradables
health = 100
resistance = 1
damage = 50
reloadSpeed = 30


#classes
class Player():
    def __init__(self, filename, x, y, width, height):
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.health = health
        self.dead = False
        #damage taken = damage / resistance
        self.resistance = resistance
        self.damage = damage
        #since 60 fps, 60 would mean 1 second reload speed
        self.rSpeed = reloadSpeed
        self.counter = 0
        self.clicked = False
        self.totalPoints = 0
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def checkAlive(self):
        self.dead = False
        if self.health <=0:
            self.dead = True
        return self.dead
    def checkHit(self, enemy, damage):
        global playerHit 
        playerHit = False
        if self.rect.colliderect(enemy):
            playerHit = True
            self.health -= damage
            print("hit", self.health)
    def attackReload(self):
        self.counter -=1
        print(self.counter)
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.counter <=0:
            self.clicked = True
            self.counter = self.rSpeed
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
    def resetPlayer(self):
        self.health = health
        self.dead = False
        self.resistance = resistance
        self.damage = damage
        self.rSpeed = reloadSpeed

    
        
#constants and variables
pygame.init()
SCREEN = (1600,900)
WHITE = (255, 255, 255)
RED = (255, 5, 5)
GREEN = (50,205,50)
GRAY = (66, 66, 66)
screen_1 = pygame.display.set_mode(SCREEN)
tempLoop = True
menuLoop = True
gamemodeLoop = False
gameLoop = False
instructionLoop = False
deathLoop = False
shopLoop = False
levelCompleteLoop = False
gamePause = False
meteoriteReset = True
dontClick = False
endless = False
stages = False

background = pygame.image.load('images/background.png').convert_alpha()
background = pygame.transform.scale(background, SCREEN)

deathScreen = pygame.image.load("images/deathscreen.jpg").convert_alpha()
deathScreen = pygame.transform.scale(deathScreen, (1000, 600))

shopUI = pygame.image.load('images/shop.jpg').convert_alpha()
shopUI = pygame.transform.scale(shopUI, (1100,700))

target = pygame.image.load('images/target.png').convert_alpha()
target = pygame.transform.scale(target, (100, 100))

title = pygame.image.load('images/title.png').convert_alpha()
title = pygame.transform.scale(title, (1000, 150))

spawnTime = 300
stageTime = 1800
endlessFactor = 1
endlessCounter = 0
stageCounter = stageTime
stagePoints = 0
currentStage = 1
spawnCounter = spawnTime 

#player
player1 = Player("images/base.png", 0, 50, 200, 800)

meteoriteSprites = ["meteorites/meteorite1.png", "meteorites/meteorite2.png", "meteorites/meteorite3.png", "meteorites/meteorite4.png", "meteorites/meteorite5.png"]
meteoriteArray = []

#upgrades
healthCost = 400
healthIncrease = 50
healthLevel = 0

damageCost = 500
damageIncrease = 20
damageLevel = 0

armorCost = 700
armorIncrease = 0.2
armorLevel = 0

attackSpeedCost = 500
attackSpeedIncrease = 1.1 #multiply by 1.1
ASLevel = 0

#instantiate buttons
playButton = button.Button((1600/2 - 300/2), 300, 'buttons/play.jpg', 300, 100)
instructionButton = button.Button((1600/2 - 300/2), 450, 'buttons/instruction.jpg', 300, 100)
backButton = button.Button(50, 50, 'buttons/back.jpg', 225, 75)
resumeButton = button.Button((1600/2 - 300/2), 200, 'buttons/resume.jpg', 300, 100)
menuButton = button.Button((1600/2 - 300/2), 400, 'buttons/menu.jpg', 300, 100)
exitButton = button.Button((1600/2 - 300/2), 600, 'buttons/exit.jpg', 300, 100)
retryButton = button.Button((1600/2 - 300/2 - 200), 375, 'buttons/retry.jpg', 300, 100)
shopButton = button.Button((1600/2 - 300/2), 600, 'buttons/shop.jpg', 300, 100)
nextStageButton = button.Button((1600/2 - 300/2 - 200), 375, 'buttons/nextstage.jpg', 300, 100)

campaignButton = button.Button((1600/2 - 300/2 -200), 200, 'buttons/campaign.jpg', 300, 100)
endlessButton = button.Button((1600/2 - 300/2 + 200), 200, 'buttons/endless.jpg', 300, 100)

healthButton = button.Button(400, 275, 'buttons/health.jpg', 350, 175)
damageButton = button.Button(850, 275, 'buttons/damage.jpg', 350, 175)
armorButton = button.Button(400, 525, 'buttons/armor.jpg', 350, 175)
attackSpeedButton = button.Button(850, 525, 'buttons/attackspeed.jpg', 350, 175)


#fonts
font1 = pygame.font.SysFont("arialblack", 40)
font2 = pygame.font.SysFont("arialblack", 20)
font3 = pygame.font.SysFont("arialblack", 50)
font4 = pygame.font.SysFont("Verdana", 40, True)
statFont = pygame.font.SysFont("Verdana", 25, True)
costFont = pygame.font.SysFont("Verdana", 20, True)
pointsFont = pygame.font.SysFont("Verdana", 35, True)


#refresh speed
clock = pygame.time.Clock()

#project loop
while tempLoop == True:

    #creates and/or resets meteorites for display
    if (menuLoop == True or shopLoop == True) and meteoriteReset == True:
        print('reset')
        meteoriteArray.clear()
        for i in range (5):
            meteoriteArray.append(meteorite.Meteorite((SCREEN[0] + random.randrange(0, 250)), random.randrange(150, (SCREEN[1] - 150)), meteoriteSprites[random.randrange(0,4)], 1))

    #menu loop
    while menuLoop == True:
        #prevents clicking immediatly upon entering
        if pygame.mouse.get_pressed()[0] == 0:
            dontClick = False
        screen_1.blit(background, (0,0))
        print("health" + str(player1.health))
        player1.resetPlayer()

        for meteorites in meteoriteArray:
            meteorites.draw(screen_1)
            if meteorites.move(SCREEN[1]):
                meteoriteArray.pop(meteoriteArray.index(meteorites))
                meteoriteArray.append(meteorite.Meteorite((SCREEN[0] + random.randrange(0, 250)), random.randrange(150, (SCREEN[1] - 150)), meteoriteSprites[random.randrange(0,4)], 1))

        playButton.draw(screen_1)
        if playButton.click() and dontClick == False:
            print("play")
            menuLoop = False
            gamemodeLoop = True
            player1.counter = 0
            
        instructionButton.draw(screen_1)
        if instructionButton.click() and dontClick == False:
            instructionLoop = True
            menuLoop = False
            print("instruction")

        shopButton.rect.y = 600
        shopButton.rect.x = 650
        shopButton.draw(screen_1)
        if shopButton.click() and dontClick == False:
            menuLoop = False
            shopLoop = True
            dontClick = True
        
        screen_1.blit(title, (300, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.update()
        clock.tick(60)
        
    
    #instruction loop
    while instructionLoop == True:
        screen_1.blit(background, (0,0))

        for meteorites in meteoriteArray:
            meteorites.draw(screen_1)
            if meteorites.move(SCREEN[1]):
                meteoriteArray.pop(meteoriteArray.index(meteorites))
                meteoriteArray.append(meteorite.Meteorite((SCREEN[0] + random.randrange(0, 250)), random.randrange(150, (SCREEN[1] - 150)), meteoriteSprites[random.randrange(0,4)], 1))

        backButton.draw(screen_1)
        drawText("The goal of this game is to defend your base against the onslaught of meteorites.", font2, (255,255,255), screen_1, 350, 200)
        drawText("You can choose either campaign or endless gamemode for mission based or endless gameplay!", font2, (255,255,255), screen_1, 300, 300)
        drawText("You use your mouse to aim and destroy the meteorites and you are able to upgrade your abilities in the shop!", font2, (255,255,255), screen_1, 250, 400)
        if backButton.click():
            instructionLoop = False
            menuLoop = True
            #prevents meteorites from being reset
            meteoriteReset = False
            print("back")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pygame.display.update()
        clock.tick(60)

    while shopLoop == True:
        #prevents clicking immediatly upon entering
        if pygame.mouse.get_pressed()[0] == 0:
            dontClick = False
        

        print(player1.rSpeed)
        player1.resetPlayer()
        screen_1.blit(background, (0,0))
        
        screen_1.blit(shopUI, (250, 100))

        healthButton.draw(screen_1)
        if healthButton.click() and player1.totalPoints >= healthCost and dontClick == False:
            health += healthIncrease
            player1.totalPoints -= healthCost
            healthLevel +=1
            healthCost +=(125 * healthLevel)

        damageButton.draw(screen_1)
        if damageButton.click() and player1.totalPoints >= damageCost and dontClick == False:
            damage += damageIncrease
            player1.totalPoints -= damageCost
            damageLevel +=1
            damageCost +=(125 * damageLevel)

        armorButton.draw(screen_1)
        if armorButton.click() and player1.totalPoints >= armorCost and dontClick == False:
            resistance += armorIncrease
            player1.totalPoints -= armorCost
            armorLevel +=1
            armorCost +=(150 * armorLevel)

        attackSpeedButton.draw(screen_1)
        if attackSpeedButton.click() and player1.totalPoints >= attackSpeedCost and dontClick == False:
            reloadSpeed /= attackSpeedIncrease
            player1.totalPoints -= attackSpeedCost
            ASLevel +=1
            attackSpeedCost +=(100 * ASLevel)

        menuButton.image = pygame.transform.scale(menuButton.image, (210,70))
        menuButton.rect.width = 210
        menuButton.rect.height = 70
        menuButton.rect.y = 50
        menuButton.rect.x = 20
        menuButton.draw(screen_1)
        if menuButton.click():
            menuLoop = True
            shopLoop = False

        exitButton.image = pygame.transform.scale(exitButton.image, (210, 70))
        exitButton.rect.width = 210
        exitButton.rect.height = 70
        exitButton.rect.y = 50
        exitButton.rect.x = 1370
        exitButton.draw(screen_1)
        if exitButton.click():
            exit()

        drawText(("Current points: " + str(int(player1.totalPoints))), pointsFont, WHITE, screen_1, 650, 725)

        drawText((str(player1.health) + " -> " + str(player1.health + healthIncrease)), statFont, WHITE, screen_1, 500, 350)
        drawText(("Cost: " + str(healthCost)), costFont, WHITE, screen_1, 525, 400)

        drawText((str(player1.damage) + " -> " + str(player1.damage + damageIncrease)), statFont, WHITE, screen_1, 960, 350)
        drawText(("Cost: " + str(damageCost)), costFont, WHITE, screen_1, 975, 400)

        drawText((str(round(player1.resistance, 1)) + " -> " + str(round((player1.resistance + armorIncrease), 1))), statFont, WHITE, screen_1, 515, 600)
        drawText(("Cost: " + str(armorCost)), costFont, WHITE, screen_1, 520, 650)

        drawText((str(round(60/player1.rSpeed, 1)) + " -> " + str(round((60/(player1.rSpeed /attackSpeedIncrease)),1))), statFont, WHITE, screen_1, 950, 600)
        drawText(("Cost: " + str(attackSpeedCost)), costFont, WHITE, screen_1, 965, 650)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pygame.display.update()
        clock.tick(60)

    while gamemodeLoop == True:
        screen_1.blit(background, (0,0))

        for meteorites in meteoriteArray:
            meteorites.draw(screen_1)
            if meteorites.move(SCREEN[1]):
                meteoriteArray.pop(meteoriteArray.index(meteorites))
                meteoriteArray.append(meteorite.Meteorite((SCREEN[0] + random.randrange(0, 250)), random.randrange(150, (SCREEN[1] - 150)), meteoriteSprites[random.randrange(0,4)], math.sqrt(currentStage)))
        
        drawText("Please Select a Gamemode", font4, (255,255,255), screen_1, 500, 50)

        backButton.draw(screen_1)
        if backButton.click():
            gamemodeLoop = False
            menuLoop = True
            #prevents meteorites from being reset
            meteoriteReset = False

        campaignButton.draw(screen_1)
        if campaignButton.click():
            endless = False
            stages = True
            gamemodeLoop = False
            gameLoop = True

        endlessButton.draw(screen_1)
        if endlessButton.click():
            stages = False
            endless = True
            gamemodeLoop = False
            gameLoop = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.update()
        clock.tick(60)
        

    #resets meteorites for gameloop
    if gameLoop == True:
        if stages == True:
            stageTime = 600 * math.sqrt(currentStage)
            stageCounter = stageTime
            spawnCounter = (spawnTime / (math.sqrt(currentStage)))

        if endless == True:
            endlessFactor = 1
            stageCounter = 0
            endlessCounter = 0

        meteoriteArray.clear()
        
        for i in range (2):
            meteoriteArray.append(meteorite.Meteorite((SCREEN[0] + random.randrange(0, 250)), random.randrange(150, (SCREEN[1] - 150)), meteoriteSprites[random.randrange(0,4)], math.sqrt(currentStage)))
    #game loop
    while gameLoop == True:
        screen_1.blit(background, (0,0))

        if gamePause == True:

            for meteorites in meteoriteArray:
                meteorites.draw(screen_1)

            resumeButton.draw(screen_1)
            if resumeButton.click():
                gamePause = False

            exitButton.image = pygame.transform.scale(exitButton.image, (300, 100))
            exitButton.rect.width = 300
            exitButton.rect.height = 100
            exitButton.rect.y = 600
            exitButton.rect.x = 650
            exitButton.draw(screen_1)
            if exitButton.click():
                exit()
            
            menuButton.image = pygame.transform.scale(menuButton.image, (300, 100))
            menuButton.rect.width = 300
            menuButton.rect.height = 100
            menuButton.rect.y = 400
            menuButton.rect.x = 650
            menuButton.draw(screen_1)
            if menuButton.click():
                gameLoop = False
                gamePause = False
                menuLoop = True
                meteoriteReset = True
                player1.totalPoints += stagePoints
                stagePoints = 0
                dontClick = True

            player1.draw(screen_1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            pygame.display.update()
            clock.tick(60)
        else:
            spawnCounter-=1
            x, y = pygame.mouse.get_pos()

            if stages == True:
                stageCounter -=1
                drawText(("Current Stage: " + str(currentStage)), font4, (255,255,255), screen_1, 650, 10)
                drawText(("Time Remainging : " + str(round(stageCounter/60))), font4, (255,255,255), screen_1, 600, 50)

                if spawnCounter <= 0:
                    meteoriteArray.append(meteorite.Meteorite((SCREEN[0] + random.randrange(0, 250)), random.randrange(150, (SCREEN[1] - 150)), meteoriteSprites[random.randrange(0,4)], math.sqrt(currentStage)))
                    spawnCounter = spawnTime
                    print("spawn")

                if stageCounter <=0 and player1.health >=0:
                    print("level won")
                    levelCompleteLoop = True
                    gameLoop = False
                    player1.totalPoints += stagePoints

                for meteorites in meteoriteArray:
                    meteorites.draw(screen_1)
                    if meteorites.move(SCREEN[1]):
                        meteoriteArray.pop(meteoriteArray.index(meteorites))
                        meteoriteArray.append(meteorite.Meteorite((SCREEN[0] + random.randrange(0, 250)), random.randrange(150, (SCREEN[1] - 150)), meteoriteSprites[random.randrange(0,4)], math.sqrt(currentStage)))
                    
                    if meteorites.click() and player1.counter <=0:
                        print("attacked")
                        meteorites.health -= player1.damage 
                        if meteorites.health <= 0:
                            stagePoints += meteorites.points
                            meteoriteArray.pop(meteoriteArray.index(meteorites))
                            
                    player1.checkHit(meteorites, (meteorites.damage / player1.resistance))

                    if playerHit == True:
                        meteoriteArray.pop(meteoriteArray.index(meteorites))

            if endless == True:
                stageCounter += 1
                endlessCounter += 1
                drawText(("Time Alive : " + str(round(stageCounter/60))), font4, (255,255,255), screen_1, 650, 50)

                if endlessCounter >= 300:
                    endlessFactor +=1
                    endlessCounter = 0

                if spawnCounter <= 0:
                    meteoriteArray.append(meteorite.Meteorite((SCREEN[0] + random.randrange(0, 250)), random.randrange(150, (SCREEN[1] - 150)), meteoriteSprites[random.randrange(0,4)], math.sqrt(endlessFactor)))
                    spawnCounter = spawnTime / math.sqrt(endlessFactor)
                    print("spawn")

                for meteorites in meteoriteArray:
                    meteorites.draw(screen_1)
                    if meteorites.move(SCREEN[1]):
                        meteoriteArray.pop(meteoriteArray.index(meteorites))
                        meteoriteArray.append(meteorite.Meteorite((SCREEN[0] + random.randrange(0, 250)), random.randrange(150, (SCREEN[1] - 150)), meteoriteSprites[random.randrange(0,4)], math.sqrt(endlessFactor)))
                    
                    if meteorites.click() and player1.counter <=0:
                        print("attacked")
                        meteorites.health -= player1.damage 
                        if meteorites.health <= 0:
                            stagePoints += meteorites.points
                            meteoriteArray.pop(meteoriteArray.index(meteorites))
                            
                    player1.checkHit(meteorites, (meteorites.damage / player1.resistance))

                    if playerHit == True:
                        meteoriteArray.pop(meteoriteArray.index(meteorites))
            
            drawText(("Score: " + str(int(stagePoints))), font2, WHITE, screen_1, 1400, 800)

            pygame.draw.rect(screen_1, RED, pygame.Rect((SCREEN[0]/2 - 250), (SCREEN[1] - 100), 500, 50))
            pygame.draw.rect(screen_1, GREEN, pygame.Rect((SCREEN[0]/2 - 250), (SCREEN[1] - 100), (player1.health / health * 500), 50))
            pygame.draw.rect(screen_1, GRAY, pygame.Rect(x - 50, y + 75, (player1.counter / player1.rSpeed * 100), 30))
            screen_1.blit(target, (x - 50, y - 50))

            player1.attackReload()
            player1.draw(screen_1)

            if player1.checkAlive():
                print("dead")
                deathLoop = True
                gameLoop = False
                player1.totalPoints += stagePoints

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamePause = True
                        print('pause')
            pygame.display.update()
            clock.tick(60)

    while levelCompleteLoop == True:
        screen_1.blit(background, (0,0))

        print("totalpoints" + str(player1.totalPoints))

        for meteorites in meteoriteArray:
                meteorites.draw(screen_1)

        player1.draw(screen_1)

        screen_1.blit(deathScreen, (300, 150))

        menuButton.image = pygame.transform.scale(menuButton.image, (300,100))
        menuButton.rect.width = 300
        menuButton.rect.height = 100
        menuButton.rect.y = 550
        menuButton.rect.x = 450
        menuButton.draw(screen_1)
        if menuButton.click():
            stagePoints = 0
            currentStage +=1
            menuLoop = True
            meteoriteReset = True
            levelCompleteLoop = False
            dontClick = True

        exitButton.image = pygame.transform.scale(exitButton.image, (300,100))
        exitButton.rect.width = 300
        exitButton.rect.height = 100
        exitButton.rect.y = 550
        exitButton.rect.x = 850
        exitButton.draw(screen_1)
        if exitButton.click():
            exit()
        
        shopButton.rect.y = 375
        shopButton.rect.x = 850
        shopButton.draw(screen_1)
        if shopButton.click():
            stagePoints = 0
            currentStage +=1
            levelCompleteLoop = False
            shopLoop = True
            dontClick = True
        
        nextStageButton.draw(screen_1)
        if nextStageButton.click():
            stagePoints = 0
            currentStage +=1
            player1.resetPlayer()
            meteoriteReset = True
            levelCompleteLoop = False
            gameLoop = True

        drawText("Stage Completed!", font3, WHITE, screen_1, 575, 175)
        drawText(("Total Score: " + str(int(stagePoints))), font3, WHITE, screen_1, 575, 225)
        drawText(("Next Stage: " + str(currentStage + 1)), font3, WHITE, screen_1, 615, 275)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pygame.display.update()
        clock.tick(60)

    while deathLoop == True:
        screen_1.blit(background, (0,0))

        print("totalpoints" + str(player1.totalPoints))

        for meteorites in meteoriteArray:
                meteorites.draw(screen_1)

        player1.draw(screen_1)

        screen_1.blit(deathScreen, (300, 150))

        menuButton.image = pygame.transform.scale(menuButton.image, (300,100))
        menuButton.rect.width = 300
        menuButton.rect.height = 100
        menuButton.rect.y = 550
        menuButton.rect.x = 450
        menuButton.draw(screen_1)
        if menuButton.click():
            stagePoints = 0
            menuLoop = True
            meteoriteReset = True
            deathLoop = False
            dontClick = True

        retryButton.draw(screen_1)
        if retryButton.click():
            stagePoints = 0
            player1.resetPlayer()
            meteoriteReset = True
            deathLoop = False
            gameLoop = True
        
        exitButton.image = pygame.transform.scale(exitButton.image, (300,100))
        exitButton.rect.width = 300
        exitButton.rect.height = 100
        exitButton.rect.y = 550
        exitButton.rect.x = 850
        exitButton.draw(screen_1)
        if exitButton.click():
            exit()
        
        shopButton.rect.y = 375
        shopButton.rect.x = 850
        shopButton.draw(screen_1)
        if shopButton.click():
            stagePoints = 0
            deathLoop = False
            shopLoop = True
            dontClick = True

        drawText(("Total Score: " + str(int(stagePoints))), font3, WHITE, screen_1, 600, 200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pygame.display.update()
        clock.tick(60)
        



    
