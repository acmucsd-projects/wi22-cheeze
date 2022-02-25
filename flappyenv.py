import gym
from gym import spaces
import numpy as np
import cv2
import time
import os
from collections import deque
import random

# Creates obstacles
def create_obstacle(bottom = 100, top = 150):
    space = 0
    while space < bottom or space > top:
        obstacle = [[550, random.randrange(1,50)*10], [550, random.randrange(1,50)*10]]
        space = abs(obstacle[0][1] - obstacle[1][1])
    if obstacle[0][1] > obstacle[1][1]:
        obstacle[0][1], obstacle[1][1] = obstacle[1][1], obstacle[0][1]
    
    return obstacle

# Detects collisions
def collision(flappy_position, obstacle_position):
    for i in range(len(obstacle_position)):
        if (obstacle_position[i][0][0] - (flappy_position[0]+20))<0 and ((obstacle_position[i][0][0]+50) - flappy_position[0])>0:
            if obstacle_position[i][0][1] > flappy_position[1] or obstacle_position[i][1][1] < flappy_position[1]+20:
                return True
    if flappy_position[1] < 0 or flappy_position[1] > 500:
        return True
    return False

SPEED = 5
SPEED_CONTROL = 0 #0.0001
STROKE_STRENGTH = 15
GRAVITY = 10
DISTANCE_BW_OBS = 300
font = cv2.FONT_HERSHEY_SIMPLEX

class FlappyEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(FlappyEnv, self).__init__()

        # Define action and observation space
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
                                            shape=(4,), dtype=np.float32)

    def step(self, action):
        cv2.imshow('a',self.img)
        cv2.waitKey(1)
        self.img = np.zeros((500,500,3),dtype='uint8')
        
        # Displays flappy bird
        cv2.rectangle(self.img,(self.flappy_position[0],self.flappy_position[1]),(self.flappy_position[0]+20,self.flappy_position[1]+20),(0,0,255),3)
        
        # Displays score
        cv2.putText(self.img,'{}'.format(self.score),(350,50), font, 1,(255,255,255),2,cv2.LINE_AA)

        # Displays obstacles
        for idx, position in enumerate(self.obstacle_position):
            cv2.rectangle(self.img,(position[0][0], position[0][1]),(position[0][0]+50, 0),(0,255,0),3)
            cv2.rectangle(self.img,(position[1][0], position[1][1]),(position[1][0]+50, 500),(0,255,0),3)

            self.obstacle_position[idx][0][0] -= SPEED
            self.obstacle_position[idx][1][0] -= SPEED

        # Reduces speed of execution
        t_end = time.time() + SPEED_CONTROL
        while time.time() < t_end:
            continue

        # Processes action
        if action == 1:
            self.flappy_position[1] -= STROKE_STRENGTH
        else:
            self.flappy_position[1] += GRAVITY
        
        # Resets game upon collision
        if collision(self.flappy_position, self.obstacle_position):
            self.img = np.zeros((500,500,3),dtype='uint8')
            cv2.putText(self.img,'Your Score is {}'.format(self.score),(140,250), font, 1,(255,255,255),2,cv2.LINE_AA)
            cv2.imshow('a',self.img)
            self.done = True

        # Updates obstacle deque when obstacles are out of frame
        if self.obstacle_position[0][0][0]+50 <= 0:
            self.obstacle_position.popleft()
            self.index -= 1
        
        # Creates new obstacle and adds to deque
        if self.obstacle_position[-1][0][0] <= DISTANCE_BW_OBS:
            self.obstacle_position.append(create_obstacle())
            
        # Updates score
        if self.flappy_position[0] > self.obstacle_position[self.index][0][0] + 50:
            self.index += 1
            self.prev_score = int(self.score)
            self.score += 1
        else:
            self.prev_score = int(self.score)

        # Determines reward
        mean_clearance_pos = np.mean([self.obstacle_position[self.index][0][1], self.obstacle_position[self.index][1][1]])
        diff = abs(self.flappy_position[1] - mean_clearance_pos)
        if diff == 0:
            diff = 1
        self.reward = 1/diff
        if self.score - self.prev_score > 0:
            self.reward += 20

        # Disincentivizes collisions
        if self.done:
            self.reward = -10
        info = {}

        # Defines the observation structure
        bird_x = self.flappy_position[0]
        bird_y = self.flappy_position[1]
        top_ob_x = self.obstacle_position[self.index][0][0]
        top_ob_y = self.obstacle_position[self.index][0][1]
        bot_ob_x = self.obstacle_position[self.index][1][0]
        bot_ob_y = self.obstacle_position[self.index][1][1]

        self.observation = np.array([bird_x, bird_y, top_ob_x, np.mean([top_ob_y, bot_ob_y])])

        return self.observation, self.reward, self.done, info

    def reset(self):
        self.done = False
        self.img = np.zeros((500,500,3),dtype='uint8')
        self.flappy_position = [200, 250]
        self.obstacle_position = deque([create_obstacle()])
        self.prev_score = 0
        self.score = 0
        self.reward = 0
        self.index = 0
        self.prev_action = 0

        bird_x = self.flappy_position[0]
        bird_y = self.flappy_position[1]
        top_ob_x = self.obstacle_position[self.index][0][0]
        top_ob_y = self.obstacle_position[self.index][0][1]
        bot_ob_x = self.obstacle_position[self.index][1][0]
        bot_ob_y = self.obstacle_position[self.index][1][1]

        self.observation = np.array([bird_x, bird_y, top_ob_x, np.mean([top_ob_y, bot_ob_y])])

        return self.observation 
    def render(self, mode='human'):
        #Implementation not necessary
        ...
    def close (self):
        #Implementation not necessary
        ...