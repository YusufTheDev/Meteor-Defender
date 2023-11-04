import pygame

#button class

class Button():
    def __init__(self, x, y, filename, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.clicked = False

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
