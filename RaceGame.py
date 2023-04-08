import pygame
from pygame.locals import *
import random

pygame.init()

#Creating the game window
width = 600
height = 600
screen_size = (width,height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("CAR RACE GAME | Road Rash")

#Color Variables
gray = (100,100,100)
green = (76,208,56)
red = (200,0,0)
white = (255,255,255)
yellow = (255, 232, 0)

#Game Settings
gameover = False
speed = 2
score = 0

#Markers Size
marker_width = 10
marker_height = 50

#Road and edge markers
road = (100 , 0 , 400, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (495, 0, marker_width, height)

#X coordinates of Lanes
left_lane = 190
center_lane =310
right_lane = 400
lanes = [left_lane,center_lane,right_lane]

#For animating movement of the lane markers
lane_marker_move_y = 0

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        #Scaling the image to fit the lane
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image,(new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

class PlayerVehicle(Vehicle):
    def __init__(self,  x, y):
        image = pygame.image.load('car.png')
        super().__init__(image, x, y)

#Player's starting coordinates
player_x = 300
player_y = 400

#Creating the Player's car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x,player_y)
player_group.add(player)

#Loading the other vehicle images
image_files = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png','van.png']
vehicle_images = []
for image_file in image_files:
    image = pygame.image.load(image_file)
    vehicle_images.append(image)

#Sprite group for vehicles
vehicle_group = pygame.sprite.Group()

#Loading the crash image
crash = pygame.image.load('crash.png')
crash_rect = crash.get_rect()


#Game Loop
clock =pygame.time.Clock()
fps = 120
running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        #Moving the player's car using the left/right arrow keys
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 120
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 120

            #Checking if there's a side swipe collision after changing lanes
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    gameover = True

                    #Placing the player's car next to other vehicle
                    #Determinig where to position the crash image
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT :
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]

    #Drawing the Grass
    screen.fill(green)

    #Drawing the Road
    pygame.draw.rect(screen, gray, road)

    #Drwaing the Edge Markers
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    #Drawing the lane markers
    lane_marker_move_y += speed*2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0

    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width,marker_height))
        pygame.draw.rect(screen,white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

    #Drawing the player's car
    player_group.draw(screen)

    #Adding up to two Vehicles
    if len(vehicle_group) < 2:
        #Ensuring there is enough gap between vehicles
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:
            #Selecting a random Lane
            lane = random.choice(lanes)
            #Selecting a random vehicle image
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height/-2)
            vehicle_group.add(vehicle)

    #Making the vehicles move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        #Removing the vehicle once it goes off screen
        if vehicle.rect.top >= height:
            vehicle.kill()

            #Adding to score
            score += 1

            #Speeding up the game after passing 5 vehicles
            if score >0 and score % 5 == 0:
                speed+=1

    #Drwaing the vehicles
    vehicle_group.draw(screen)

    #Displaying the Score
    font = pygame.font.Font(pygame.font.get_default_font(),16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 450)
    screen.blit(text, text_rect)

    #Checking if there is a Head on Collision
    if pygame.sprite.spritecollide(player , vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    #Dispalying Game Over
    if gameover:
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, red, (0, 50, width, 200))
        font = pygame.font.Font(pygame.font.get_default_font(), 32)
        text = font.render('Game Over. Play Again? (y/n)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2 , 175)
        screen.blit(text, text_rect)

    pygame.display.update()

    #Checking if player wants to play Again
    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running  = False

            #Get the player's input (y or n)
            if event.type == KEYDOWN:
                if event.key == K_y:
                    #Reset the Game
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n :
                    #Exit Game Loop
                    gameover = False
                    running = False
            
pygame.quit()