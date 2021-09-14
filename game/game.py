
#bz6cx bilun zhang
'''
Space Invaders game
Features:
Optional Feature 1:6 enemies
Optional Feature 2:3 lives
Optional Feature 3:collectibles
Optional Feature 4:count up timer
The rules of game:
The player (flight) can shoot the bullets to hit the enemies(UFO) to remove them on the screen. Once they shoot all
the UFO and UFO does not touch the flight , the player will earn 5 points for each touch.
If player get of all the UFO with three lives in 60 seconds,they win.
Once the UFO touch the player, the lives will lose one until three lives gone.
If the bullets touch the luck key the time will -1.
The hard point of the project:
how to let flight shoot the bullet
how to remove the UFO when the bullet touch it   ==>is there any remove function
how to let the UFO move from top to the bottom   ==>import random?
'''

import pygame
import gamebox
screenx = 800
screeny = 600
camera = gamebox.Camera(screenx, screeny)
background=gamebox.from_image(800, 600,'background.jpg')
background.scale_by(4)
ship=gamebox.from_image(400,500,'player.png')
bullet=gamebox.from_color(400,400,'white',10,10)
bullet_list = []
lucky=gamebox.from_image(20,80,'bullet.png')

#enemy
enemy1 = gamebox.from_image(300, 300, 'enemy.png')
enemy1.speedx -= 5
enemy2= gamebox.from_image(30, 200, 'enemy.png')
enemy2.speedx -= 5
enemy3=gamebox.from_image(550, 127, 'enemy.png')
enemy3.speedx -= 5
enemy4=gamebox.from_image(600, 240, 'enemy.png')
enemy4.speedx -= 5
enemy5=gamebox.from_image(100, 320, 'enemy.png')
enemy5.speedx -= 5
enemy6=gamebox.from_image(200, 189, 'enemy.png')
enemy6.speedx -= 5
enemy_list=[enemy1,enemy2,enemy3,enemy4,enemy5,enemy6]
score=0
lives = 3
time=0
game_on=False

def front_page():
    game=gamebox.from_text(400,200,"Space War",57,'white')
    name = gamebox.from_text(400, 300, "bz6cx Bilun Zhang", 36, 'white')
    instructions= gamebox.from_text(400,400,"Press the UP to start!",36,'white')
    how=gamebox.from_text(400,500,"Shoot all the UFO in 60 seconds then you win",36,'white')
    camera.draw(name)
    camera.draw(game)
    camera.draw(instructions)
    camera.draw(how)

def draw_stats():
  """draws the gameplay information (lives, score)"""
  scorebox = gamebox.from_text(350, 25, "score: " + str(score), 36, 'red')
  camera.draw(scorebox)
  timebox=gamebox.from_text(150, 25, "Time: " + str(time) + " seconds", 36, 'gray')
  camera.draw(timebox)
  for i in range(lives):
      heart = gamebox.from_circle(775, 25, 'yellow', 10)
      heart.x -= 50 * i
      heart.scale_by(0.5)
      camera.draw(heart)

def game_start(keys): #hit the space key to start the game
    global game_on
    if pygame.K_UP in keys:
       game_on=True

def draw_enemy():
    global enemy_list
    for each in enemy_list:

        if each.right>=camera.right:
            each.y += 80
            each.speedx *= -1
        if each.left<=camera.left:
            each.y += 80
            each.speedx*=-1
        each.move_speed()
        camera.draw(each)

def move_ship(keys):
    if pygame.K_RIGHT in keys:
        ship.x += 15
    if pygame.K_LEFT in keys:
        ship.x -= 15
    if ship.left<camera.left:
        ship.left=camera.left
    if ship.right>camera.right:
       ship.right=camera.right

def draw_bullet():
    global bullet,bullet_list
    x=ship.x
    y=ship.top
    for i in range (5):
        bullet = gamebox.from_color(x, y, 'white', 5, 5)
        bullet_list.append(bullet)
draw_bullet()

def move_bullet(keys):             #bug: after press the space, even bullet does not exit it still touch UFO
    if pygame.K_SPACE in keys:
        for bullet in bullet_list:
            bullet.speedy -= 10
            bullet.move_speed()
            camera.draw(bullet)

def scored():
    global score,enemy_list
    for i in enemy_list:
        for fire in bullet_list:
            if fire.touches(i):
                score+=5
                i.move(1000, 1000)

def lucky_key():
    global score,time
    lucky.move(10,9)
    lucky.move_speed()
    for fire in bullet_list:
        if fire.touches(lucky):
            time-=1
    camera.draw(lucky)

def lives_lose():
    global lives
    for i in enemy_list:
        if i.touches(ship):
            i.move(900, 1000)
            lives-=1

def game_over():
    global game_on,game_end,score
    if lives == 0:
       camera.draw(gamebox.from_text(400, 300, 'Game Over', 42, 'white', True))
       camera.display()
       game_on = False
       return True
    return False

def win():
    global time,score
    if  lives==3 and time<=60 and score==30:
        camera.draw(gamebox.from_text(400, 300, 'You Win', 42, 'white', True))
        time=0
    if ((lives<3 and lives>0)or lives==3) and time>60 and score==30:
        camera.draw(gamebox.from_text(400, 300, 'Sorry', 42, 'white', True))
        time =100
    if (lives<3 and lives>0) and time>60 and score!=30:
        camera.draw(gamebox.from_text(400, 300, 'Sorry', 42, 'white', True))
        time =100
    camera.display()

def tick(keys):
    global score,time
    camera.clear('black')
    camera.draw(background)
    if game_over():
        return
    if game_on==False:
        front_page()
    if game_on==True:
        move_ship(keys)
        scored()
        draw_enemy()
        draw_bullet()
        move_bullet(keys)
        draw_stats()
        lucky_key()
        time+=1
        win()
        lives_lose()
        camera.draw(ship)

    game_start(keys)
    camera.display()

gamebox.timer_loop(30, tick)