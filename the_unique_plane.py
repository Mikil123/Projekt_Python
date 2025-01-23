import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_move_1 = pygame.image.load('graphics/player_move1.png').convert_alpha()
        player_move_2 = pygame.image.load('graphics/player_move2.png').convert_alpha()
        self.player_move = [player_move_1, player_move_2]
        self.player_index = 0
        self.player_jumping = pygame.image.load('graphics/player_jumping.png').convert_alpha()
        self.image = self.player_move[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        if keys[pygame.K_w] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom>=300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jumping
        else:
            self.player_index +=0.1
            if self.player_index >= len(self.player_move):
                self.player_index = 0
            self.image = self.player_move[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'airship':
            airship_frame_1 = pygame.image.load('graphics/airship1.png').convert_alpha()
            airship_frame_2 = pygame.image.load('graphics/airship2.png').convert_alpha()
            self.frames = [airship_frame_1,airship_frame_2]
            y_pos = 200
        else:
            plane_frame_1 = pygame.image.load('graphics/plane1.png').convert_alpha()
            plane_frame_2 = pygame.image.load('graphics/plane2.png').convert_alpha()
            self.frames = [plane_frame_1,plane_frame_2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"{current_time}",False,('Black'))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True



pygame.init()

screen =  pygame.display.set_mode((800,400))
pygame.display.set_caption('The Unique Plane')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Goudament.ttf', 50)
test_font2 = pygame.font.Font('font/Goudament.ttf', 30)
game_active = False
start_time = 0
score = 0
bg_Music = pygame.mixer.Sound('audio/music.wav')
bg_Music.play(loops=-1)

player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()


background_surface = pygame.image.load('graphics/background.png').convert()
frontground_surface = pygame.image.load('graphics/frontground.png')


plane_frame_1 = pygame.image.load('graphics/plane1.png').convert_alpha()
plane_frame_2 = pygame.image.load('graphics/plane2.png').convert_alpha()
plane_frames = [plane_frame_1, plane_frame_2]
plane_frame_index = 0
plane_surf = plane_frames[plane_frame_index]

airship_frame_1 = pygame.image.load('graphics/airship1.png').convert_alpha()
airship_frame_2 = pygame.image.load('graphics/airship2.png').convert_alpha()
airship_frames = [airship_frame_1, airship_frame_2]
airship_frame_index = 0
airship_surf = airship_frames[airship_frame_index]




obstacle_rect_list = []


player_move_1 = pygame.image.load('graphics/player_move1.png').convert_alpha()
player_move_2 = pygame.image.load('graphics/player_move2.png').convert_alpha()
player_move = [player_move_1, player_move_2]
player_index = 0
player_jumping = pygame.image.load('graphics/player_jumping.png').convert_alpha()
player_surf = player_move[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

player_stand = pygame.image.load('graphics/player_stand.png').convert_alpha()
player_stand_scaled = pygame.transform.scale(player_stand,(200, 400))
player_stand_rect = player_stand.get_rect(center = (400,200))

name_surf = test_font.render('The Unique Plane', False, 'Black')
name_rect = name_surf.get_rect(center = (400,50))

message_surf = test_font2.render('Kliknij SPACJE/W a wyruszysz w poszukiwanie unikalnego samolotu...', False, (3,0,150))
message_rect = message_surf.get_rect(center = (400, 320))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

plane_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(plane_animation_timer,500)

airship_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(airship_animation_timer,200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos)  and player_rect.bottom >= 300: 
                    player_gravity = -20   
        
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or pygame.K_w:
            
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
                    
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['airship','plane','plane','plane'])))   
            
            if event.type == plane_animation_timer:
                if plane_frame_index == 0:
                    plane_frame_index = 1
                else:
                    plane_frame_index=0
                plane_surf = plane_frames[plane_frame_index]
            
            if event.type == airship_animation_timer:
                if airship_frame_index == 0:
                    airship_frame_index = 1
                else:
                    airship_frame_index=0
                airship_surf = airship_frames[airship_frame_index]



         
    if game_active:   
        screen.blit(background_surface,(0,0))
        screen.blit(frontground_surface,(0,300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((77,190,240))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0
        score_message = test_font.render(f"Wynik poszukiwania: {score}",False, (3,0,150))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(name_surf,name_rect)

        if score == 0:
            screen.blit(message_surf,message_rect)
        else:
            screen.blit(score_message,score_message_rect)
        bg_Music.stop

   
    pygame.display.update()
    clock.tick(60)











































































































































































































































