import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
import pyrr
from TextureLoader import load_texture
from OBJECT_IMPORTER import ObjLoader
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
cards[7]=Card('8','h',8)
cards[8]=Card('8','f',8)
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
    time.sleep(2.5)
    player_won.play()
    global flip1

    global filp1
    flip1+=4

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




async def bot_reponse(table_bucket,bot_bucket):
    global raised
    # time.sleep(1)
    if len(table_bucket.cards)==0:
        value=bot_bucket.hasPair()
        if value==None:
            check()
        else:
            value=2
            raise_card(True)

    else:
        value=bot_bucket.checkAll()[0]
        if value>=7:
            allIn()
        elif value>=3:
            raise_card(True)
            
        elif value==2:
            check()
        else:
            if raised:
                fold()
            else:
                check()
    if raised and value!=None and value <3:
        raised=False

    
            
    

# objects
object_0, object_buffer = ObjLoader.load_model("Objects/simple_table.obj")
object_01, object_buffer1 = ObjLoader.load_model("New cards/"+objs[0])
object_02, object_buffer2 = ObjLoader.load_model("New cards/"+objs[1])
object_03, object_buffer3 = ObjLoader.load_model("New cards/"+objs[2])
object_04, object_buffer4 = ObjLoader.load_model("New cards/"+objs[3])
object_05, object_buffer5 = ObjLoader.load_model("New cards/"+objs[4])
object_06, object_buffer6 = ObjLoader.load_model("New cards/"+objs[5])
object_07, object_buffer7 = ObjLoader.load_model("New cards/"+objs[6])
object_08, object_buffer8 = ObjLoader.load_model("Objects/robot head.obj")
object_08_1, object_buffer8_1 = ObjLoader.load_model("Objects/robot body.obj")
object_09, object_buffer9 = ObjLoader.load_model("New cards/"+objs[7])
object_10, object_buffer10 = ObjLoader.load_model("New cards/"+objs[8])
object_11, object_buffer11 = ObjLoader.load_model("Objects/floor.obj")
object_12, object_buffer12 = ObjLoader.load_model("Objects/control carved.obj")



shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# VAO and VBO
VAO = glGenVertexArrays(14)
VBO = glGenBuffers(14)

# 
glBindVertexArray(VAO[0])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, object_buffer.nbytes, object_buffer, GL_STATIC_DRAW)



# 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer.itemsize * 8, ctypes.c_void_p(12))
# 
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

#**********************************************
glBindVertexArray(VAO[1])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, object_buffer1.nbytes, object_buffer1, GL_STATIC_DRAW)



# 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer1.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer1.itemsize * 8, ctypes.c_void_p(12))
# 
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer1.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)
#*******************************************************

#**********************************************
glBindVertexArray(VAO[2])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, object_buffer2.nbytes, object_buffer2, GL_STATIC_DRAW)



# 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer2.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer2.itemsize * 8, ctypes.c_void_p(12))
# 
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer2.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)
#*******************************************************
#**********************************************
glBindVertexArray(VAO[3])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[3])
glBufferData(GL_ARRAY_BUFFER, object_buffer3.nbytes, object_buffer3, GL_STATIC_DRAW)



# 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer3.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer3.itemsize * 8, ctypes.c_void_p(12))
# 
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer3.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)
#*******************************************************
#**********************************************
glBindVertexArray(VAO[4])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[4])
glBufferData(GL_ARRAY_BUFFER, object_buffer4.nbytes, object_buffer4, GL_STATIC_DRAW)



# 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer4.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer4.itemsize * 8, ctypes.c_void_p(12))
# 
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer4.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)
#*******************************************************

#**********************************************
glBindVertexArray(VAO[5])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[5])
glBufferData(GL_ARRAY_BUFFER, object_buffer5.nbytes, object_buffer5, GL_STATIC_DRAW)



# 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer5.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer5.itemsize * 8, ctypes.c_void_p(12))
# 
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer5.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)
#*******************************************************
#**********************************************
glBindVertexArray(VAO[6])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[6])
glBufferData(GL_ARRAY_BUFFER, object_buffer6.nbytes, object_buffer6, GL_STATIC_DRAW)



# 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer6.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer6.itemsize * 8, ctypes.c_void_p(12))
# 
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer6.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)
#*******************************************************

#**********************************************
glBindVertexArray(VAO[7])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[7])
glBufferData(GL_ARRAY_BUFFER, object_buffer7.nbytes, object_buffer7, GL_STATIC_DRAW)



# 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer7.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer7.itemsize * 8, ctypes.c_void_p(12))
# 
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer7.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)
#*******************************************************


#**********************************************
glBindVertexArray(VAO[8])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[8])
glBufferData(GL_ARRAY_BUFFER, object_buffer8.nbytes, object_buffer8, GL_STATIC_DRAW)



# 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer8.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer8.itemsize * 8, ctypes.c_void_p(12))
# 
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer8.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)
#*******************************************************


glBindVertexArray(VAO[9])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[9])
glBufferData(GL_ARRAY_BUFFER, object_buffer9.nbytes, object_buffer9, GL_STATIC_DRAW)



# 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer9.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer9.itemsize * 8, ctypes.c_void_p(12))
# 
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer9.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)
#*******************************************************

glBindVertexArray(VAO[10])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[10])
glBufferData(GL_ARRAY_BUFFER, object_buffer10.nbytes, object_buffer10, GL_STATIC_DRAW)



# 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer10.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer10.itemsize * 8, ctypes.c_void_p(12))
# 
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer10.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)
#*******************************************************
glBindVertexArray(VAO[11])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[11])
glBufferData(GL_ARRAY_BUFFER, object_buffer8_1.nbytes, object_buffer8_1, GL_STATIC_DRAW)



# 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer8_1.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer8_1.itemsize * 8, ctypes.c_void_p(12))
# 
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer8_1.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)
#*******************************************************
glBindVertexArray(VAO[12])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[12])
glBufferData(GL_ARRAY_BUFFER, object_buffer11.nbytes, object_buffer11, GL_STATIC_DRAW)



# 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer11.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer11.itemsize * 8, ctypes.c_void_p(12))
# 
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer11.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)
#*******************************************


glBindVertexArray(VAO[13])
# 
glBindBuffer(GL_ARRAY_BUFFER, VBO[13])
glBufferData(GL_ARRAY_BUFFER, object_buffer12.nbytes, object_buffer12, GL_STATIC_DRAW)




glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, object_buffer12.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, object_buffer12.itemsize * 8, ctypes.c_void_p(12))

glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, object_buffer12.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)






textures = glGenTextures(14)
load_texture("Textures/a.jpg", textures[0])
load_texture("Textures/jj.jpg", textures[1])
load_texture("Textures/jj.jpg", textures[2])
load_texture("Textures/jj.jpg", textures[3])
load_texture("Textures/jj.jpg", textures[4])
load_texture("Textures/jj.jpg", textures[5])
load_texture("Textures/jj.jpg", textures[6])
load_texture("Textures/jj.jpg", textures[7])
load_texture("Textures/iron.jpg", textures[8])
load_texture("Textures/jj.jpg", textures[9])
load_texture("Textures/jj.jpg", textures[10])
load_texture("Textures/iron.jpg", textures[11])
load_texture("Textures/floor.jpg", textures[12])
load_texture("Textures/iron.jpg", textures[13])


glUseProgram(shader)
glClearColor(0, 0.05, 0.05, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 800 / 720, 0.1, 100)
obj_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,0 , 1]))
obj_pos1 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-.3,2.7 , 4.2]))
obj_pos2 = pyrr.matrix44.create_from_translation(pyrr.Vector3([.3,2.7 , 4.2]))
obj_pos3 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-1.2,2.7 , 2.6]))
obj_pos4 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-.6,2.7 , 2.6]))
obj_pos5 = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,2.7 , 2.6]))
obj_pos6 = pyrr.matrix44.create_from_translation(pyrr.Vector3([.6,2.7 , 2.6]))
obj_pos7 = pyrr.matrix44.create_from_translation(pyrr.Vector3([1.2,2.7 , 2.6]))
obj_pos8 = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,3.8 , -2]))
obj_pos8_1 = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,2.5 , -2]))
obj_pos9 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-.3,3 , -1]))
obj_pos10 = pyrr.matrix44.create_from_translation(pyrr.Vector3([.3,3 , -1]))
obj_pos11 = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,-.2 , 0]))
obj_pos12 = pyrr.matrix44.create_from_translation(pyrr.Vector3([2.1,4.6 , 0]))


# eye, target, up
view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 5, 0]), pyrr.Vector3([0, -1, -1]), pyrr.Vector3([0, -1, 2]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

# the main application loop

rot=-16
rot_first=3.1
rot_second=3.1
rot_third=3.1
pick2=3.14
pick=0
j=0
left=True
intro.play()
while True:
    if len(table_bucket.cards)>=5 and rot_third >0:
        pick=-1.2
    elif len(table_bucket.cards)>=5 and rot_third <0:
        time.sleep(2)

        winner=CardBucket.compare(player_bucket,bot_bucket)
        if winner==1:
            wining.play()
            time.sleep(2.8)
            player_lost.play()
        elif winner==-1:
            losing.play()
            time.sleep(2.5)
            player_won.play()
        else:
            tie.play()
            time.sleep(2.5)
            player_tie.play()
        time.sleep(2)
        pygame.quit()
        quit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if  event.key == pygame.K_c:
                if allin:

                    total_betted_birr+=bot_current
                    bot_current=0
                elif checked or raised:
                    if raised:
                        player_current-=50
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
                else:
                    checked=True

                asyncio.run(bot_reponse(table_bucket,bot_bucket))




            elif event.key == pygame.K_r :
                player_current-=50
                total_betted_birr+=50
                raised=True
                asyncio.run(bot_reponse(table_bucket,bot_bucket))
            elif event.key == pygame.K_f :
                flip1+=4
                wining.play()
                time.sleep(2.5)
                player_lost.play()
                time.sleep(2)
                pygame.quit()
                quit()

            elif event.key == pygame.K_a  :
                table_bucket.cards=[cards[5],cards[6],cards[2],cards[3],cards[4]]
                player_bucket.cards=table_bucket.cards+[cards[0],cards[1]]
                bot_bucket.cards=table_bucket.cards+[cards[7],cards[8]]
                total_betted_birr+=player_current
                player_current=0
                flip1+=4
                allin=True
                asyncio.run(bot_reponse(table_bucket,bot_bucket))

                
    rot+=0.05
    if rot>7.5:
        rot=7.5

    view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 5, rot]), pyrr.Vector3([0, 3, 0]), pyrr.Vector3([0, 1, 2]))
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_y = pyrr.Matrix44.from_y_rotation(0)
    scale=[[1.3,0,0,0],[0,1.3,0,0],[0,0,1.3,0],[0,0,0,1]]
    mod = pyrr.matrix44.multiply(rot_y, obj_pos)

    model = pyrr.matrix44.multiply(scale,mod)
    
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_0))

    #**********************************************
    
    if left and (datetime.datetime.now().second//5)%2==0:
        j+=0.0045
        if j>.35:
            j=.35
            left=False
    elif not left and (datetime.datetime.now().second//5)%2!=0:
        j-=0.0045
        if j<-.35 :
            j=-.35
            left=True


#**********************************************************************

    rot_y = pyrr.Matrix44.from_y_rotation(j)
    rot_x = pyrr.Matrix44.from_x_rotation(-.35)
    scale=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    mod = pyrr.matrix44.multiply(rot_y, obj_pos8)
    mod = pyrr.matrix44.multiply(rot_x, mod)

    model = pyrr.matrix44.multiply(scale,mod)
    
    glBindVertexArray(VAO[8])
    glBindTexture(GL_TEXTURE_2D, textures[8])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_08))



#**************************************************************
#**********************************************************************

    rot_y = pyrr.Matrix44.from_y_rotation(0)
    mod = pyrr.matrix44.multiply(rot_y, obj_pos8_1)

    model = pyrr.matrix44.multiply(scale,mod)
    glBindVertexArray(VAO[11])
    glBindTexture(GL_TEXTURE_2D, textures[11])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_08_1))



#**************************************************************
    scale=[[.2,0,0,0],[0,2.2,0,0],[0,0,.2,0],[0,0,0,1]]
    rot_x = pyrr.Matrix44.from_x_rotation(36.5)
    # rot_y = pyrr.Matrix44.from_x_rotation(180)
    mod = pyrr.matrix44.multiply(rot_x, obj_pos1)
    # mod = pyrr.matrix44.multiply(rot_y, obj_pos1)
    model = pyrr.matrix44.multiply(scale,mod)

 

    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_01))

#*************************************************************  


#**********************************************************************
    
    rot_x = pyrr.Matrix44.from_x_rotation(36.5)
    mod = pyrr.matrix44.multiply(rot_x, obj_pos2)
    model = pyrr.matrix44.multiply(scale,mod)

 

    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_01))

#************************************************************* 
#**********************************************************************
    scale=[[.3,0,0,0],[0,1,0,0],[0,0,.3,0],[0,0,0,1]]
    
    rot_x = pyrr.Matrix44.from_z_rotation(rot_first)
    mod = pyrr.matrix44.multiply(rot_x, obj_pos3)
    model = pyrr.matrix44.multiply(scale,mod)

 

    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_01))

#************************************************************* 
#**********************************************************************
    if rot==7.5 and rot_first>0 and flip1>-1:
        rot_first-=0.1
    if flip1>=1 and rot_second>0:
        rot_second-=0.1
    if flip1>=2 and rot_third>0:
        rot_third-=0.1
    
    rot_x = pyrr.Matrix44.from_z_rotation(rot_first)
    mod = pyrr.matrix44.multiply(rot_x, obj_pos4)
    model = pyrr.matrix44.multiply(scale,mod)

 

    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, textures[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_01))

#*************************************************************

#**********************************************************************
    
    rot_x = pyrr.Matrix44.from_z_rotation(rot_first)
    mod = pyrr.matrix44.multiply(rot_x, obj_pos5)
    model = pyrr.matrix44.multiply(scale,mod)

 

    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, textures[5])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_01))

#************************************************************* 

#**********************************************************************
    
    rot_x = pyrr.Matrix44.from_z_rotation(rot_second)
    mod = pyrr.matrix44.multiply(rot_x, obj_pos6)
    model = pyrr.matrix44.multiply(scale,mod)

 

    glBindVertexArray(VAO[6])
    glBindTexture(GL_TEXTURE_2D, textures[6])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_01))

#*************************************************************  

#**********************************************************************
    
    rot_x = pyrr.Matrix44.from_z_rotation(rot_third)
    mod = pyrr.matrix44.multiply(rot_x, obj_pos7)
    model = pyrr.matrix44.multiply(scale,mod)

 

    glBindVertexArray(VAO[7])
    glBindTexture(GL_TEXTURE_2D, textures[7])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_01))

#*************************************************************

    if rot==7.5:
        pick2=0
        pick+=0.1
    if pick>1:
        pick=1
    scale=[[.2,0,0,0],[0,1.4,0,0],[0,0,.2,0],[0,0,0,1]]
    
    
    rot_x = pyrr.Matrix44.from_x_rotation(pick)
    rot_z = pyrr.Matrix44.from_z_rotation(pick2)
    mod = pyrr.matrix44.multiply(rot_x, obj_pos9)
    mod = pyrr.matrix44.multiply(rot_z, mod)
    model = pyrr.matrix44.multiply(scale,mod)

 

    glBindVertexArray(VAO[9])
    glBindTexture(GL_TEXTURE_2D, textures[9])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_09))

#************************************************************* 

#**********************************************************************
    
    rot_x = pyrr.Matrix44.from_x_rotation(pick)
    rot_z = pyrr.Matrix44.from_z_rotation(pick2)
    mod = pyrr.matrix44.multiply(rot_x, obj_pos10)
    mod = pyrr.matrix44.multiply(rot_z, mod)
    model = pyrr.matrix44.multiply(scale,mod)

 

    glBindVertexArray(VAO[10])
    glBindTexture(GL_TEXTURE_2D, textures[10])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_10))

#************************************************************* 

#**********************************************************************
    scale=[[.2,0,0,0],[0,.2,0,0],[0,0,1.9,0],[0,0,0,1]]
    rot_x = pyrr.Matrix44.from_x_rotation(1.57)
    mod = pyrr.matrix44.multiply(rot_x, obj_pos11)
    model = pyrr.matrix44.multiply(scale,mod)

 

    glBindVertexArray(VAO[12])
    glBindTexture(GL_TEXTURE_2D, textures[12])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_11))

#*************************************************************  
#**********************************************************************
    scale=[[.1,0,0,0],[0,.03,0,0],[0,0,.2,0],[0,0,0,1]]
    rot_x = pyrr.Matrix44.from_x_rotation(-1.57)
    rot_y = pyrr.Matrix44.from_y_rotation(.02)
    mod = pyrr.matrix44.multiply(rot_x, obj_pos12)
    mod = pyrr.matrix44.multiply(rot_y, mod)
    model = pyrr.matrix44.multiply(scale,mod)

 

    glBindVertexArray(VAO[13])
    glBindTexture(GL_TEXTURE_2D, textures[13])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(object_12))

#************************************************************* 


    pygame.display.flip()
    pygame.time.wait(10)
