import pygame
import random
random.seed(1)

# constant of screen size
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# frame freq
FRAME_PER_SEC = 60
#timer ID constant for emeny
CREATE_ENEMY_EVENT = pygame.USEREVENT
# timer ID constant for bullet
CREATE_BULLET_EVENT = pygame.USEREVENT+1

class GameSprite(pygame.sprite.Sprite):
     
    def __init__(self, image_name='images/me1.png', speed=1):
        
        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect =  self.image.get_rect() # x,y =0
        self.speed = speed

    def update(self):
        
        self.rect.y += self.speed


class BackGround(GameSprite):

    def __init__(self, is_alt, speed=1):
        
        super().__init__(image_name='images/background.png')
        self.is_alt = is_alt
        if self.is_alt:
            self.rect.y = -self.rect.height
        else:
            self.rect.y = 0
    
    def update(self):

        super().update()

        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):

    def __init__(self):

        super().__init__(image_name='images/enemy1.png')
        self.speed = random.randint(1,3)
        self.rect.bottom = 0
        
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
        
    def __del__(self):
        print('enemy done',self.rect)
    
    def update(self):
        
        super().update()
        
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()


class Hero(GameSprite):

    def __init__(self):

        super().__init__(image_name='images/me1.png',speed=0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.height - 120

    def update(self):
        
        self.rect.x += self.speed

        if self.rect.x<=0:
            self.rect.x=0
        elif self.rect.right>=SCREEN_RECT.width:
            self.rect.right=SCREEN_RECT.width
    
    def fire(self):
        bullet_list=[]
        for i in range(3):
            bullet = Bullet(self.rect.centerx, self.rect.centery-20*i)
            bullet_list.append(bullet)
        return bullet_list

class Bullet(GameSprite):

    def __init__(self, x, y):

        super().__init__(image_name='images/bullet1.png',speed=-2)
        self.rect.y = y
        self.rect.x = x

    def update(self):
        
        super().update()
        if self.rect.bottom<=0:
            self.kill()

    def __del__(self):
        print('bullet is ended')


