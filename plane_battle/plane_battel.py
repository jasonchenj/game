import pygame
import time
from pygame.locals import *
from ipdb import set_trace
import random
'''
bullet bo li chulai
'''
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
CREATE_ENEMY_EVENT = pygame.USEREVENT

ENEMY_RIGHT_MOVE = 1
ENEMY_LEFT_MOVE = 2
class BaseObject(object):

    def __init__(self, x, y, image_path):
        self.x = x # left top corner
        self.y = y
        self.image = pygame.image.load(image_path)

    def display(self, screen):
        #print(self.image.get_rect())
        screen.blit(self.image, (self.x, self.y))

    def bomb(self):
        pass


class BasePlane(BaseObject):

    def __init__(self, x, y, image_path):
        
        BaseObject.__init__(self, x, y, image_path)      
        self.bullet_list = []

    def display(self, screen):
        #print(self.image.get_rect())
        BaseObject.display(self, screen)
        
        bullet_remove=[]
        for bullet in self.bullet_list:
            bullet.display(screen)
            bullet.move()
            if bullet.move_jude()==-1:
                bullet_remove.append(bullet)
        for bullet in bullet_remove:
            self.bullet_list.remove(bullet)


class BaseBullet(BaseObject):

    def __init__(self, x, y, speed, image_path):
        
        BaseObject.__init__(self, x, y, image_path)
        self.speed = speed

    def move(self):
        self.y += self.speed

    def __del__(self):
        print('bullet is deleted')


class HeroPlane(BasePlane):

    def __init__(self):
        BasePlane.__init__(self, 210, 550, './images/me1.png')

        #super().__init__(210, 550, './images/me1.png')

    def move(self,dir_flag):
        
        if dir_flag == 'left':
            self.x -= 5
        elif dir_flag == 'right':
            self.x += 5

    def fire(self):
        self.bullet_list.append(Bullet(self.x, self.y))
    

class Bullet(BaseBullet):

    def __init__(self, plane_x, plane_y):
        
        x = plane_x + 50
        y = plane_y - 10
        speed = -5
        image_path = './images/bullet1.png'

        BaseBullet.__init__(self, x, y, speed, image_path)

    def move_jude(self):

        if self.y<=0:
            return -1
        else:
            return 0


class Enemy(BasePlane):

    def __init__(self):
        '''x,y: location,  image:pic, speed:move'''

        super().__init__(x=random.randint(0, SCREEN_RECT.width), 
                        y=0,  image_path='./images/enemy1.png')

        self.direction = random.randint(1,2)

    def move(self):

        #self.y += self.speed
        if self.direction==ENEMY_RIGHT_MOVE:
            x_speed =random.randint(1,3)
        else:
            x_speed = random.randint(-3,-1)

        self.x += x_speed

        if self.x>=SCREEN_RECT.width-45:
            self.direction = ENEMY_LEFT_MOVE
        elif self.x<=0:
            self.direction = ENEMY_RIGHT_MOVE

    def fire(self):

        radn = random.randint(1,100)
        if radn==75 or radn==90:
            self.bullet_list.append(Enemy_Bullet(self.x, self.y))


class Enemy_Bullet(BaseBullet):

    def __init__(self, plane_x, plane_y):

        x = plane_x + 25
        y = plane_y + 30
        speed = 5
        image_path = './images/bullet1.png'

        BaseBullet.__init__(self, x, y, speed, image_path)

    def move_jude(self):

        if self.y>=SCREEN_RECT.height:
            return -1
        else:
            return 0
    



def key_control(hero,enemy_list):

    for event in pygame.event.get():
        
        # key control
        if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_q):
            print('exit')
            pygame.quit()
            exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_a or event.key==pygame.K_LEFT:
                print('left')
                hero.move('left')

            elif event.key==pygame.K_d or event.key==pygame.K_RIGHT:
                print('right')
                hero.move('right')

            elif event.key==pygame.K_SPACE:
                print('generate bullet')
                hero.fire()

        # event_handle
        if event.type == CREATE_ENEMY_EVENT:
    
            print('one enemy happens')
            enemy_list.append(Enemy())


def main():

    # 1.create a screen to show something
    screen = pygame.display.set_mode(SCREEN_RECT.size)
    
    # 2.read a background pic whose size is the same as screen
    background = pygame.image.load('./images/background.png')
    #print(background.get_rect())    
    
    # 3.create a heroplane object
    hero = HeroPlane()
    enemy_list=[]

    # 4.create timer event
    pygame.time.set_timer(CREATE_ENEMY_EVENT, 3000)
        
    # 5.put the pics into screen
    while True:
        
        key_control(hero, enemy_list)

        screen.blit(background, (0,0))
        hero.display(screen)
       
        for enemy in enemy_list:
            enemy.display(screen)
            
            enemy.move()
            enemy.fire()
        pygame.display.update()

        time.sleep(0.01)

if __name__ == '__main__':

    main()
