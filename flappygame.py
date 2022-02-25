import numpy as np
import random
import cv2
import copy
from collections import deque
import time
import os

SPEED = 5
STROKE_STRENGTH = 15
GRAVITY = 10
font = cv2.FONT_HERSHEY_SIMPLEX

def create_obstacle(bottom = 100, top = 150):
    space = 0
    while space < bottom or space > top:
        obstacle = [[550, random.randrange(1,50)*10], [550, random.randrange(1,50)*10]]
        space = abs(obstacle[0][1] - obstacle[1][1])
    if obstacle[0][1] > obstacle[1][1]:
        obstacle[0][1], obstacle[1][1] = obstacle[1][1], obstacle[0][1]
    
    return obstacle

def collision(flappy_position, obstacle_position):
    for i in range(len(obstacle_position)):
        if (obstacle_position[i][0][0] - (flappy_position[0]+20))<0 and ((obstacle_position[i][0][0]+50) - flappy_position[0])>0:
            if obstacle_position[i][0][1] > flappy_position[1] or obstacle_position[i][1][1] < flappy_position[1]+20:
                return True
    if flappy_position[1] < 0 or flappy_position[1] > 500:
        return True
    return False


index = 0
flappy_position = [200, 250]
obstacle_position = deque([create_obstacle()])
img = np.zeros((500,500,3),dtype='uint8')
score = 0

while True:
    cv2.imshow('a',img)
    cv2.waitKey(1)
    img = np.zeros((500,500,3),dtype='uint8')
    cv2.rectangle(img,(flappy_position[0],flappy_position[1]),(flappy_position[0]+20,flappy_position[1]+20),(0,0,255),3)
    cv2.putText(img,'{}'.format(score),(350,50), font, 1,(255,255,255),2,cv2.LINE_AA)
    for idx, position in enumerate(obstacle_position):
        cv2.rectangle(img,(position[0][0], position[0][1]),(position[0][0]+50, 0),(0,255,0),3)
        cv2.rectangle(img,(position[1][0], position[1][1]),(position[1][0]+50, 500),(0,255,0),3)

        obstacle_position[idx][0][0] -= SPEED
        obstacle_position[idx][1][0] -= SPEED

    t_end = time.time() + 0.001
    k = -1
    while time.time() < t_end:
        if k == -1:
            k = cv2.waitKey(125)
        else:
            continue

    if k == ord('w'):
        button_direction = 3
    elif k == ord('q'):
        break
    else:
        button_direction = -1

    if button_direction == 3:
        flappy_position[1] -= STROKE_STRENGTH
    else:
        flappy_position[1] += GRAVITY
    
    if collision(flappy_position, obstacle_position):
        print("Your score was: {}".format(score))
        if os.path.exists("log.txt"):
            with open("log.txt", "r") as f:
                high_score = f.read()
            if high_score == "":
                high_score = 0
            else:
                high_score = int(high_score)
        else:
            high_score = 0
        if score > high_score:
            with open("log.txt", "w") as f:
                f.write(str(score))
            print("NEW HIGH SCORE!!!")
            high_score = score
        print("High score: {}".format(high_score))
        break

    if obstacle_position[0][0][0]+50 <= 0:
        obstacle_position.popleft()
        index -= 1
    
    if obstacle_position[-1][0][0] <= 300:
        obstacle_position.append(create_obstacle())
        

    if flappy_position[0] > obstacle_position[index][0][0] + 50:
        index += 1
        score += 1

cv2.destroyAllWindows()