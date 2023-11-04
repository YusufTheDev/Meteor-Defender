import pygame
import random
import math

#button class

class Meteorite():
    def __init__(self, x, y, filename, factor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.clicked = False
        self.speedX = math.sqrt(factor) * (random.uniform(2,5))
        self.speedY = math.sqrt(factor) * (random.uniform(-1, 1))
        self.health = math.sqrt(factor) * (random.uniform(50,150))
        self.damage = math.sqrt(factor) * (random.uniform(20,50))
        self.points = math.sqrt(factor) * (random.randrange(50,100))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def click(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                 self.clicked = True
                 action = True
            if pygame.mouse.get_pressed()[0] == 0:
                 self.clicked = False
        return action
    
    def move (self, screenY):
        offScreen = False
        self.rect.x -= self.speedX
        self.rect.y -= self.speedY

        if (self.rect.x + self.width) <= 0:
            offScreen = True
        elif (self.rect.y +self.height) <= 0:
            offScreen = True
        elif (self.rect.y) >= screenY:
            offScreen = True

        return offScreen
