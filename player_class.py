import pygame
import random
import time
import numpy as np
import os

from global_constants import *

class Player():

    def __init__(self, i):
        self.index = i
        #Lists to Store history
        self.action_history = []               # [Action, Time, Reward, Energy, num_offspring, [offspring ids]]


        self.playerImg = pygame.image.load('player.png')
        self.playerX = random.randint(32, SCREEN_WIDTH - 32)
        self.playerY = random.randint(32, SCREEN_HEIGHT - 32)
        self.PLAYER_WIDTH = 32
        self.PLAYER_HEIGHT = 32
        self.born_at = time.time()
        self.food_ate = 0
        self.gender = np.random.choice(['Male', 'Female'], p=[0.5, 0.5])
        self.cannot_move = False
        self.ingesting_begin_time = 0
        self.ingesting_particle_index = 0
        self.food_near = []
        self.players_near = []
        self.is_impotent = np.random.choice([True, False], p=[0.3, 0.7])
        self.mating_begin_time = 0
        self.fighting_with = -1
        self.energy = 200


    def write_data(self):
        file_name ="Players_Data/"+str(self.born_at)+"-"+str(self.index)+".txt"
        file = open(file_name, "w")
        for row in self.action_history:
            file.write(str(row))
            file.write(" \n")
        file.close()

    def update_history(self, action, time, reward, num_offspring = None, offspring_ids = None, mate_id = None, fight_with = None):
        if action<=9:
            self.action_history.append([action, time, reward, self.energy])
        elif action == 10 :
            self.action_history.append([action, time, reward, self.energy, num_offspring, offspring_ids])
        elif action == 11 :
            self.action_history.append([action, time, reward, self.energy, num_offspring, offspring_ids, mate_id])
        elif action == 12:
            self.action_history.append([action, time, reward, self.energy, fight_with])

    def change_player_xposition(self, x):
        if(not self.cannot_move):
            self.playerX += x

            if(self.playerX <= 0):
                self.playerX = 0
            elif(self.playerX >= (SCREEN_WIDTH - self.PLAYER_WIDTH)):
                self.playerX = (SCREEN_WIDTH - self.PLAYER_WIDTH)

            self.energy -= 5

    def change_player_yposition(self, y):
        if(not self.cannot_move):
            self.playerY += y

            if(self.playerY <= 0):
                self.playerY = 0
            elif(self.playerY >= (SCREEN_HEIGHT - self.PLAYER_HEIGHT)):
                self.playerY = (SCREEN_HEIGHT - self.PLAYER_HEIGHT)

            self.energy -= 5

    def asexual_reproduction(self, lenPlayers):
        offspring_players = []
        num_offspring = random.randint(2,8)
        offspring_ids = []
        for i in range(num_offspring):
            print("Born", (i+1), "/", num_offspring)
            id_offspring = lenPlayers
            offspring_ids.append(id_offspring)
            lenPlayers = lenPlayers + 1
            offspring_players.append(Player(id_offspring))
        return offspring_players, offspring_ids

    def sexual_reproduction(self, mating_begin_time, lenPlayers, gen_offspring=False):
        self.cannot_move = True
        self.mating_begin_time = mating_begin_time
        self.energy -= 30
        offspring_ids = []
        if(gen_offspring):
            INITIAL_POPULATION = random.randint(2, 8)
            offspring_players = []
            for i in range(INITIAL_POPULATION):
                print("Born", (i+1), "/", INITIAL_POPULATION)
                id_offspring = lenPlayers
                offspring_ids.append(id_offspring)
                lenPlayers = lenPlayers+1
                offspring_players.append(Player(id_offspring))
            return offspring_players, offspring_ids

    def ingesting_food(self, idx, time):
        self.cannot_move = True
        self.ingesting_begin_time = time
        self.ingesting_particle_index = idx
        self.energy += 25

    def show_player(self):
        screen.blit(self.playerImg, (self.playerX, self.playerY))

    def show_close(self):
        if(self.mating_begin_time != 0):
            screen.blit(pygame.image.load('player_mating.png'), (self.playerX, self.playerY))
        else:
            screen.blit(pygame.image.load("player_near.png"), (self.playerX, self.playerY))

    def kill_player(self):
        self.is_killed = True
