import pgzrun
import pygame
import pgzero
from random import randint
from pgzero.builtins import Actor
import time


WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False
finalized = False
garden_happy = True
fangflower_collision = False
raining = False

time_elapsed = 0
start_time = time.time()

cow = Actor("cow")
cow.pos = 100, 500

flower_list = []
wilted_list = []
fangflower_list = []

fangflower_vy_list = [] # fangflower vertical velocity.
fangflower_vx_list = [] # fangflower horizontal velocity

def draw():
    global game_over, time_elapsed, finalized, raining      #add rain
    if not game_over:
        raining = True 
        screen.clear()
        screen.blit("garden-raining", (0, 0))
        cow.draw()
        for flower in flower_list:
            flower.draw()
        for fangflower in fangflower_list:
            fangflower.draw()
        time_elapsed = int(time.time() - start_time)
        screen.draw.text(
            "Garden happy for: " +
            str(time_elapsed) + " seconds",
            topleft=(10, 10), color="black"
        )
    else:
        if not finalized:
            cow.draw()
            screen.draw.text(
                "Garden happy for: " +                  #garden happy message
                str(time_elapsed) + " seconds",
                topleft=(10, 10), color="black"
            )
        if (not garden_happy):
            screen.draw.text(
                "GARDEN UNHAPPY... GAME OVER!", color="black",  #game over message
                topleft=(10, 50)
            )
            finalized = True
        else:                   #happy garden but zapped cow
            screen.draw.text(
                "FANGFLOWER ATTACK... GAME OVER!", color="black",   #fangflower game over message
                topleft=(10, 50)
            )
            finalized = True
    return

def new_flower():
    global flower_list, wilted_list 
    flower_new = Actor("flower") 
    flower_new.pos = randint(50, WIDTH - 50), randint(150, HEIGHT - 100)    #new flower position
    flower_list.append(flower_new)      #add new flower to array
    wilted_list.append("happy")         #status of flower
    return

def add_flowers():
    global game_over
    if not game_over:
        new_flower() 
        clock.schedule(add_flowers, 3)      #flower added every 3s (originally 4s)
    return

def check_wilt_times():
    global wilted_list, game_over, garden_happy
    if wilted_list: 
        for wilted_since in wilted_list: 
            if (not wilted_since == "happy"):                   #check wilted flower status
                time_wilted = int(time.time() - wilted_since)
                if (time_wilted) > 15.0:                        #Game over if wilted flower for >15s (originally 10s)
                    garden_happy = False
                    game_over = True
                    break
    return

def wilt_flower():
    global flower_list, wilted_list, game_over
    if not game_over:
        if flower_list:
            rand_flower = randint(0, len(flower_list) - 1) 
        if (flower_list[rand_flower].image == "flower"): 
            flower_list[rand_flower].image = "flower-wilt" #changes to wilted flower image
            wilted_list[rand_flower] = time.time()
        clock.schedule(wilt_flower, 3)
    return

def check_flower_collision():
    global cow, flower_list, wilted_list
    index = 0
    for flower in flower_list:
        if(flower.colliderect(cow) and flower.image == "flower-wilt"):
            flower.image = "flower"     #changes back to flower image if cow is close
            wilted_list[index] = "happy"
            break
        index = index + 1
    return

def check_fangflower_collision():
    # Global Variables
    global cow, fangflower_list, fangflower_collision
    global game_over
    for fangflower in fangflower_list:
        if fangflower.colliderect(cow):
            cow.image = "zap"   #zapped cow image if contact with fangflower
            game_over = True    #Game Over
            break
    return

def velocity():
     random_dir = randint(0, 1)         #fangflower direction
     random_velocity = randint(2, 3)    #fangflower speed
     if random_dir == 0:
         return -random_velocity
     else:
         return random_velocity

def mutate():
      global flower_list, fangflower_list, fangflower_vy_list
      global fangflower_vx_list, game_over
      if not game_over and flower_list:
          rand_flower = randint(0, len(flower_list) - 1)    #mutate random flower
          fangflower_pos_x = flower_list[rand_flower].x
          fangflower_pos_y = flower_list[rand_flower].y
          del flower_list[rand_flower]
          fangflower = Actor("fangflower")
          fangflower.pos = fangflower_pos_x, fangflower_pos_y   #replace flower image
          fangflower_vx = velocity()                            #vertical fangflower speed
          fangflower_vy = velocity()                            #horizontal fangflower speed
          fangflower = fangflower_list.append(fangflower)
          fangflower_vx_list.append(fangflower_vx)
          fangflower_vy_list.append(fangflower_vy)
          clock.schedule(mutate, 5)                 #mutates flower every 15s (originally 20s)
          return

def update_fangflowers():
    # Global Variables
    global fangflower_list, game_over
    if not game_over:
        index = 0
        for fangflower in fangflower_list:
            fangflower_vx = fangflower_vx_list[index]
            fangflower_vy = fangflower_vy_list[index]
            fangflower.x = fangflower.x + fangflower_vx
            fangflower.y = fangflower.y + fangflower_vy
            if fangflower.left < 0:                             #ensure fangflower doesn't exit screen
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.right > WIDTH:
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.top < 150:
                fangflower_vy_list[index] = -fangflower_vy
            if fangflower.bottom > HEIGHT:
                fangflower_vy_list[index] = -fangflower_vy
            index = index + 1
            return


def reset_cow():
    global game_over
    if not game_over: 
        cow.image = "cow"
    return

add_flowers()
wilt_flower()

def update():
    global score, game_over, fangflower_collision
    global flower_list, fangflower_list, time_elapsed
    fangflower_collision = check_fangflower_collision()
    check_wilt_times()
    if not game_over:
        if keyboard.space:
            cow.image = "cow-water"     #watering cow image on spacebar press
            clock.schedule(reset_cow, 0.5)
            check_flower_collision()
        if keyboard.left and cow.x > 0:
            cow.x -= 5
        elif keyboard.right and cow.x < WIDTH:
            cow.x += 5
        elif keyboard.up and cow.y > 150:
            cow.y -= 5
        elif keyboard.down and cow.y < HEIGHT:
            cow.y += 5
        if time_elapsed > 15 and not fangflower_list:
            mutate()
        update_fangflowers()

pgzrun.go()
