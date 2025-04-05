from pygame import *
mixer.init()

window = display.set_mode((700,500))
display.set_caption('')
bg = transform.scale(image.load('background.jpg'), (700,500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self))

class Player (GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 500 - 80:
            self.rect.y += self.speed
    
class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= 700 - 85:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3,  wall_x, wall_y, wall_width, wall_height ):
        super().__init__()
        self.image = Surface((wall_width, wall_height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption('Maze')

background = transform.scale(image.load('background.jpg'), (win_width, win_height))


player = Player('hero.png', 5, 420, 4)
monster = Enemy('cyborg.png', 620,280,2)
final = GameSprite('treasure.png', 580, 420, 0)

w1 = Wall(154, 205, 50, 100, 20, 450, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w3 = Wall(154, 205, 50, 100, 20, 10, 380)
w4 = Wall(154, 205, 50, 550, 20, 10, 380)
    
game = True
clock = time.Clock()

mixer.music.load('jungles.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

font.init()
font = font.SysFont('Arial',70)
win = font.render("YOU WIN", True, (0,255,0))
lose = font.render("YOU LOSE", True, (255,0,0))

walls = [w1, w2, w3, w4]
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        window.blit(bg, (0,0))
        player.reset()
        monster.reset()
        final.reset()
        player.update()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        if sprite.collide_rect(player, final):
            finish = True
            money.play()
            window.blit(win, (200, 200))
        if sprite.collide_rect(player, monster):
            finish = True
            kick.play()
            window.blit(win, (200, 200))
        for i in walls:   
            if sprite.collide_rect(player, i):
                finish = True
                kick.play()
                window.blit(lose, (200, 200))




    display.update()
    time.delay(10)