# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
from adafruit_circuitplayground import cp
import random

cp.pixels.brightness = 0.1
cp.pixels.fill((0, 0, 0))

def win_tune():
    cp.play_tone(280, 0.1)
    cp.play_tone(180, 0.1)
    cp.play_tone(280, 0.1)
    cp.play_tone(180, 0.1)
    cp.play_tone(280, 0.1)
    cp.play_tone(180, 0.1)
    cp.play_tone(280, 0.1)
    cp.play_tone(180, 0.1)
    cp.play_tone(280, 0.1)

def reset_tune():
    cp.play_tone(180, 1)

def start_tune():
    cp.play_tone(294, 1)

def lose_tune():
    cp.play_tone(280, 0.5)
    cp.play_tone(180, 0.5)
    cp.play_tone(280, 0.5)

def move_tune():
    cp.play_tone(100, 0.1)

class PlayState:

    def __init__(self):
        self.running = False
        self.player_pixels = [5,6,7,8,9]
        self.enemy_pixels = 2
        self.score = 0
    
    def reset_state(self):
        self.running = False
        self.player_pixels = [5,6,7,8,9]
        self.enemy_pixels = 2
        self.score = 0

    def light_board(self):
        cp.pixels.fill((0, 0, 0))
        for pp in self.player_pixels:
            cp.pixels[pp] = (0, 255, 0)
        cp.pixels[self.enemy_pixels] = (255, 0, 0)

    def toggle_running(self):
        self.running = not self.running

    def is_running(self):
        return self.running

    def is_game_over(self):
        print("Score : {0}".format(self.score))
        return self.enemy_pixels in self.player_pixels

    def is_winner(self):
        return self.is_game_over() and self.enemy_pixels == 7

    def move_left(self):
        self.player_pixels.pop(-1)
        val = (self.player_pixels[0] -1)%10
        self.player_pixels.insert(0, val)
        self.score += 1
        
    def move_right(self):
        self.player_pixels.pop(0)
        val = (self.player_pixels[-1] +1)%10
        self.player_pixels.append(val)
        self.score += 1
        
    def move_enemy(self):
        self.enemy_pixels = (self.enemy_pixels + random.randint(-1, 1)) % 10


ps = PlayState()
ps.light_board()

while True:
    time.sleep(1.0)
        
    if cp.button_a:
        reset_tune()
        ps.reset_state()
        ps.light_board()
        continue

    if cp.button_b:
        start_tune()
        ps.toggle_running()
        continue

    if not ps.is_running():
        continue

    ps.move_enemy()

    if cp.touch_A1:
        ps.move_left()

    if cp.touch_A3:
        ps.move_right()

    ps.light_board()
    
    if ps.is_game_over():
        if ps.is_winner():
            win_tune()
        else:
            lose_tune()
        ps.toggle_running()
    else:
        move_tune()
    