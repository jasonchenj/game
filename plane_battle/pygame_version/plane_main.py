import pygame
from plane_sprites import *


class PlaneGame(object):
    ''' main game class'''

    def __init__(self):
        print('game initialize')
       
       # 1. create game window
        self.screen = pygame.display.set_mode(SCREEN_RECT.size) #x,y 
       # 2. create game clock
        self.clock = pygame.time.Clock()
       # 3. call the method to create sprite and sprite group
        self.__create_sprites()
       # 4. set timer event
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(CREATE_BULLET_EVENT, 500)
    
    def __create_sprites(self):
        
        bg1 = BackGround(is_alt=True)
        bg2 = BackGround(is_alt=False)
        self.bg_group = pygame.sprite.Group(bg1, bg2)
        self.enemy_group =  pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

       
    def start_game(self):
        print('game start')
        
        # 1. set frame freq
        #self.clock.tick(FRAME_PER_SEC)
        while True:
            # 1. set frame freq
            self.clock.tick(FRAME_PER_SEC)
            # 2. event watch
            self.__event_handler()
            # 3. crash detection
            self.__check_collide()
            # 4. update/draw sprite group
            self.__update_sprites()
            # 5. update show
            pygame.display.update()
            

    def __event_handler(self):
        
        for event in pygame.event.get(): # event list
        
            # whether exit the game
            if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_q):
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                print('enemy occurs')
                self.enemy_group.add(Enemy())
            elif event.type == CREATE_BULLET_EVENT:
                print('bullet shooted')
                bullet = self.hero.fire()
                self.bullet_group.add(bullet)
            '''
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                print('right')
                self.hero.dir =1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                print('left')
                self.hero.dir =2
            '''
        keys_pressed = pygame.key.get_pressed()  #return pressed tuple
        if keys_pressed[pygame.K_RIGHT]==1:
            self.hero.speed =2
        elif keys_pressed[pygame.K_LEFT]==1:
            self.hero.speed =-2
        else:
            self.hero.speed = 0
            


    def __check_collide(self):
        pygame.sprite.groupcollide(self.bullet_group, self.enemy_group,
                True, True)
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies)>0:
            self.hero.kill()
            PlaneGame.__game_over()

    def __update_sprites(self):
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.bullet_group.update()
        self.bullet_group.draw(self.screen)

    @staticmethod
    def __game_over():
        print('game stopped')
        pygame.quit()
        exit()

if __name__ == '__main__':

    game = PlaneGame()
    game.start_game()
