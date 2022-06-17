import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
import pyrr
from TextureLoader import load_texture,load_texture_pygame
from OBJ_LOADER import ObjLoader
import os

import pygame
from pygame.locals import *
import OpenGL

from PIL import Image
import datetime
from card import *
import asyncio
import time

flip1=-1
raised=False
checked=False
allin=False



def getFileContents(filename):
    p = os.path.join(os.getcwd(), "Shader", filename)
    return open(p, 'r').read()
vertex_src = getFileContents("shader.vertex.shader")
fragment_src = getFileContents("shader.fragment.shader")


pygame.init()
intro=pygame.mixer.Sound('Audio/Breaking_Bad_Intro_F1HNuAE9WdU_140.mp3')
folding=pygame.mixer.Sound('Audio/fold.wav')
raising=pygame.mixer.Sound('Audio/raise.wav')
checking=pygame.mixer.Sound('Audio/checked.wav')
wining=pygame.mixer.Sound('Audio/win.wav')
losing=pygame.mixer.Sound('Audio/lost.wav')
player_won=pygame.mixer.Sound('Audio/youwon.mp3')
player_lost=pygame.mixer.Sound('Audio/youlost.mp3')
tie=pygame.mixer.Sound('Audio/draw.wav')
player_tie=pygame.mixer.Sound('Audio/youtie.mp3')
display = (1400, 720)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glClearColor(.30, 0.20, 0.20, 1.0)
glViewport(0, 0, 1400,720)


#********************************************************************************
cards=CardBucket.generateRandom()
objs=[str(i)+".obj" for i in cards]


player_bucket=CardBucket([cards[0],cards[1]])
bot_bucket=CardBucket([cards[7],cards[8]])
table_bucket=CardBucket([])


total_betted_birr=100
bot_current=950
player_current=950
bot_bet=50
player_bet=50



#*******************************************************************************************************
def check():
    print("checked^^^^")
    global checked,raised,bot_current,total_betted_birr,allin
    global flip1
    if allin:
        total_betted_birr+=bot_current
        bot_current=0
    elif checked or raised:
        if raised:
            bot_current-=50
            total_betted_birr+=50
        flip1+=1
        if flip1==0:
            table_bucket.cards.extend([cards[2],cards[3],cards[4]])
            bot_bucket.cards.extend([cards[2],cards[3],cards[4]])
            player_bucket.cards.extend([cards[2],cards[3],cards[4]])
        elif flip1==1:
            table_bucket.cards.extend([cards[5]])
            bot_bucket.cards.extend([cards[5]])
            player_bucket.cards.extend([cards[5]])
        elif flip1==2:
            table_bucket.cards.extend([cards[6]])
            bot_bucket.cards.extend([cards[6]])
            player_bucket.cards.extend([cards[6]])
        checked=False
        raised=False
    checking.play()
def raise_card(is_bot):
    raising.play()
    print("rasied^^^^^")
    global total_betted_birr,player_current,bot_current
    total_betted_birr+=50
    if is_bot:
        bot_current-=50
    else:
        player_current-=50 
def fold():
    folding.play()
    time.sleep(1)
    losing.play()
    time.sleep(.5)
    player_won.play()
    global flip1
    print("folded^^^^^")
    global filp1
    flip1+=4
    print([str(i) for  i in bot_bucket.cards])
    time.sleep(2)
    pygame.quit()
    quit()
def allIn():
    global flip1,bot_current,total_betted_birr,allin
    total_betted_birr+=bot_current
    table_bucket.cards=[cards[5],cards[6],cards[2],cards[3],cards[4]]
    player_bucket.cards=table_bucket.cards+[cards[0],cards[1]]
    bot_bucket.cards=table_bucket.cards+[cards[7],cards[8]]
    bot_current=0
    flip1+=4
    allin=True
