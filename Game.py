import pygame
from random import choice, randint
from os import path,listdir,remove
from math import floor
from pygame.locals import * 
quits=[False,False] 
pygame.init()
size=  width, height = 1000,800
screen=pygame.display.set_mode(size)
pygame.display.set_caption('Blob EXTERMINATOR')
font = pygame.font.Font("Ubuntu-B.ttf", 20)
screen.fill((0,0,0))
pygame.display.flip()
clock=pygame.time.Clock()
frame=6
tiles={}
pics={}
maps=[]
options2=["music","attack","up","down","left","right","blobs"]
options={"music":50,"attack":K_SPACE,"up":K_w,"down":K_s,"left":K_a,"right":K_d,"blobs":20}
file=open("options.txt","r")

for option in options2:
    options[option]=int(file.readline())
file.close()
listing = listdir('pics/tiles')
for file in listing:
    filename=file.split(".")
    tiles[filename[0]]=pygame.image.load('pics/tiles/'+str(file))
listing = listdir('pics')
for file in listing:
    filename=file.split(".")
    if len(filename)==2 and filename[1]=="png":
        pics[filename[0]]=pygame.image.load('pics/'+str(file))

def loadmaps():
    maps=[""]
    listing = listdir("maps")
    for file in listing:
        filename=file.split(".")
        if len(filename)==2 and filename[1]=="txt":
            maps.append(filename[0])
    maps.sort()
    maps[0]=1
    return maps
    
def button(screen,text,font,tcol,bcol,x,y,sx,sy):
    brect=pygame.Rect(x,y, sx, sy)
    txt=font.render(text, True, tcol)
    txtrect=txt.get_rect()
    txtrect.center=brect.center
    screen.fill(bcol,brect)
    screen.blit(txt,(txtrect.x,txtrect.y))
    return brect
    
def overwrite(screen,name,quits):
    if path.exists("maps/"+name+".txt"):
        box=pygame.Rect(295,295,410,75)
        screen.fill((90,30,0),box)
        button(screen,"Overwrite?",font,(0,0,0),(255,255,255),300,300, 400, 30)
        buttons={"yes":button(screen,"Yes",font,(0,0,0),(255,255,255),300,335, 195, 30),
        "no":button(screen,"No",font,(0,0,0),(255,255,255),505,335, 195, 30)}
        pygame.display.flip()
        while quits[0]==False and quits[1]==False:
            for event in pygame.event.get():
                if event.type ==QUIT:
                    pygame.quit()
                    quits[0]=True
                    quits[1]=True
                if event.type == MOUSEBUTTONUP:
                    if event.button==1:
                        for but in buttons:
                            if buttons[but].collidepoint(event.pos):
                                if but=="yes":
                                    return True
                                if but=="no":
                                    return False
    return True
    
def setName(screen,font,question,quits,keyinput=[]):
    if len(keyinput)>0 and type(keyinput)==str:
        letters=[]
        for let in keyinput:
            letters.append(let)
        keyinput=letters
    buttons={}
    rshift=False
    lshift=False
    box=pygame.Rect(295,295,410,75)
    screen.fill((90,30,0),box)
    buttons["!!_BACK_!!"]=button(screen,"Back",font,(0,0,0),(255,255,255),300,335, 195, 30)
    buttons["!!_SAVE_!!"]=button(screen,"Save",font,(0,0,0),(255,255,255),505,335, 195, 30)
    while quits[1]==False and quits[0]==False:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_LSHIFT:
                    lshift=False
                if event.key == K_RSHIFT:
                    rshift=False
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    keyinput = keyinput[0:-1]
                elif event.key == K_RETURN:
                    quits[1]=True
                elif event.key == K_LSHIFT:
                    lshift=True
                elif event.key == K_RSHIFT:
                    rshift=True
                elif event.key <= 127:
                    if lshift or rshift:
                        keyinput.append(chr(event.key).upper())
                    else:
                        keyinput.append(chr(event.key))
            button(screen, question + "".join(keyinput),font,(0,0,0),(255,255,255),300,300,400,30)
            pygame.display.flip()
            if event.type == MOUSEBUTTONUP:
                if event.button==1:
                    for but in buttons:
                        if buttons[but].collidepoint(event.pos):
                            if but=="!!_BACK_!!":
                                return
                            if but=="!!_SAVE_!!":
                                quits[1]=True
    return "".join(keyinput)
    
def MainMenu(screen,quits):
    screen.blit(pics["Main"],(0,0)) 
    buttons={
    "!!_PLAY_!!":button(screen,"Play",font,(0,0,0),(255,255,255),300,200, 400, 30),
    "!!_EDIT_!!":button(screen,"Load Map",font,(0,0,0),(255,255,255),300,275, 195, 30),
    "!!_OPTIONS_!!":button(screen,"Options",font,(0,0,0),(255,255,255),300,315, 400, 30),
    "!!_NEW_!!":button(screen,"New Map",font,(0,0,0),(255,255,255),505,275, 195, 30),
    "!!_QUIT_!!":button(screen,"Quit",font,(0,0,0),(255,255,255),300,740, 400, 30)}
    button(screen,"Map Editor",font,(0,0,0),(255,255,255),300,240, 400, 30),
    pygame.display.flip()
    while quits[0]==False and quits[1]==False:
        for event in pygame.event.get():
            if event.type ==QUIT:
                pygame.quit()
                quits[0]=True
                quits[1]=True
            if event.type == MOUSEBUTTONUP:
                if event.button==1:
                    for but in buttons:
                        if buttons[but].collidepoint(event.pos):
                            if but=="!!_QUIT_!!":
                                pygame.quit()
                                quits[0]=True
                            else:
                                quits[1]=True
                                return but 
                            break
        if quits[1]==True:
            break
        clock.tick(frame)
        
def createMapMen(screen,maps,mes,buttons,delete):
    screen.blit(pics["Main"],(0,0))
    if not delete:
        button(screen,mes,font,(0,0,0),(255,255,255),300,80, 300, 30)
        buttons["!!_DELETE_!!"]=button(screen,"Delete",font,(0,0,0),(255,255,255),610,80, 90, 30)
    else: button(screen,mes,font,(0,0,0),(255,255,255),300,80, 400, 30)
    y=90
    if len(maps)<19:
        for ma in maps:
            if type(ma)==str:
                y+=35
                buttons[ma]=button(screen,ma,font,(0,0,0),(255,255,255),300,y, 400, 30)
    else:
        for mapnr in range(maps[0],maps[0]+17):
            if type(maps[mapnr])==str:
                y+=35
                buttons[maps[mapnr]]=button(screen,maps[mapnr],font,(0,0,0),(255,255,255),300,y, 400, 30)
        buttons["!!_UP_!!"]=button(screen,"^",font,(0,0,0),(255,255,255),710,125, 20, 290)
        buttons["!!_DOWN_!!"]=button(screen,"V",font,(0,0,0),(255,255,255),710,425, 20, 290)
    buttons["!!_BACK_!!"]=button(screen,"Back",font,(0,0,0),(255,255,255),300,740, 400, 30)
    return screen
    
def chooseMap(screen,quits,mes="Maps:",delete=False):
    maps=loadmaps()
    buttons={}
    createMapMen(screen,maps,mes,buttons,delete)
    pygame.display.flip()
    while quits[0]==False and quits[1]==False:
        for event in pygame.event.get():
            if event.type ==QUIT:
                pygame.quit()
                quits[0]=True
                quits[1]=True
            if event.type == MOUSEBUTTONUP:
                if event.button==1:
                    for but in buttons:
                        if buttons[but].collidepoint(event.pos):
                            if but=="!!_UP_!!":
                                if maps[0]>1:
                                    maps[0]-=1
                                    createMapMen(screen,maps,mes,buttons,delete)
                                    pygame.display.flip()
                            elif but=="!!_DOWN_!!":
                                if maps[0]<len(maps)-17:
                                    maps[0]+=1
                                    createMapMen(screen,maps,mes,buttons,delete)
                                    pygame.display.flip()
                            elif but=="!!_DELETE_!!":
                                deleteMap(screen,quits)
                                maps=loadmaps()
                                createMapMen(screen,maps,mes,buttons,delete)
                                pygame.display.flip()
                            else:
                                quits[1]=True
                                return but
                            break
        if quits[1]==True:
            break
        clock.tick(frame)
        
def getKey(screen):
    button(screen,"Press Any Key",font,(0,0,0),(255,255,255),300,300, 400, 50)
    pygame.display.flip()
    while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
            
def loadopt(screen,buttons):
    screen.blit(pics["Main"],(0,0))
    buttons["!!_BACK_!!"]=button(screen,"Back",font,(0,0,0),(255,255,255),300,740, 400, 30)
    button(screen,"Options",font,(0,0,0),(255,255,255),300,80, 400, 30)
    x=300
    y=120
    for option in options2:
        if x>700:
            x-=410
            y+=40
        if option=="blobs":
            buttons[option]=button(screen,str(option)+": "+str(options[option]),font,(0,0,0),(255,255,255),x,y, 195, 30)
        elif option=="music":
            buttons[option]=button(screen,str(option)+": "+str(options[option]),font,(0,0,0),(255,255,255),x,y, 195, 30)
        else:
            buttons[option]=button(screen,str(option)+": "+pygame.key.name(options[option]),font,(0,0,0),(255,255,255),x,y, 195, 30)
        x+=205
    pygame.display.flip()
    
def SetOptions(screen,quits):
    buttons={}
    loadopt(screen,buttons)
    while quits[0]==False and quits[1]==False:
        for event in pygame.event.get():
            if event.type ==QUIT:
                pygame.quit()
                quits[0]=True
                quits[1]=True
            if event.type == MOUSEBUTTONUP:
                if event.button==1:
                    for but in buttons:
                        if buttons[but].collidepoint(event.pos):
                            if but=="!!_BACK_!!":
                                quits[1]=True
                            elif but=="blobs":
                                vol=setName(screen,font,"Number of Blolbs: ",quits,str(options["blobs"]))
                                quits[1]=False
                                try: vol=int(vol)
                                except: loadopt(screen,buttons)
                                else:
                                    if vol>100: vol=100
                                    elif vol<0:vol=0
                                    options["blobs"]=vol
                            elif but=="music":
                                vol=setName(screen,font,"Volume %: ",quits,str(options["music"]))
                                quits[1]=False
                                try: vol=int(vol)
                                except: loadopt(screen,buttons)
                                else:
                                    if vol>100: vol=100
                                    elif vol<0:vol=0
                                    options["music"]=vol
                                    pygame.mixer.music.set_volume(vol/100)
                            else:
                                options[but]=getKey(screen)
                            loadopt(screen,buttons)
                            break
        clock.tick(frame)
    file=open("options.txt","w+")
    for opt in options2:
        file.write(str(options[opt])+"\n")
    file.close()
    
def deleteMap(screen,quits):
    remov=chooseMap(screen,quits,"Delete:",True)
    quits[1]=False
    if remov!="!!_BACK_!!":
        remove("maps/"+remov+".txt")
        
def MapGen(name,buttons,cordinatemap):
    land=pygame.Surface(size)
    tilemap=open("maps/"+name+".txt","r").read().split("\n")
    y=0
    for line in tilemap:
        if len(line)<50: continue
        x=0
        cordinatemap.append([])
        line=line.strip().split(" ")
        if y>49: continue
        for tile in line:
            if x>49: continue
            land.blit(tiles[tile],(x*16,y*16))
            cordinatemap[y].append(tile)
            x+=1
        y+=1
    land.blit(pics["leftbar"],(801,0))
    buttons["!!_QUIT_!!"]=button(land,"Quit",font,(255,0,0),(90,30,0),830,740, 144, 30)
    buttons["!!_MAIN_!!"]=button(land,"Main menu",font,(255,0,0),(90,30,0),830,700, 144, 30)
    return land
    
def Cordstoland(cords,buttons):
    land=pygame.Surface(size)
    y=0
    for line in cords:
        x=0
        for tile in line:
            land.blit(tiles[tile],(x*16,y*16))
            x+=1
        y+=1
    land.blit(pics["leftbar"],(801,0))
    buttons["!!_QUIT_!!"]=button(land,"Quit",font,(255,0,0),(90,30,0),830,740, 144, 30)
    buttons["!!_MAIN_!!"]=button(land,"Main menu",font,(255,0,0),(90,30,0),830,700, 144, 30)
    return land
    
class thingy(object):
    kills=0
    def __init__(self,x,y,pic,name):
        self.x=x
        self.y=y
        self.pic=pic
        self.name=name
    def move(self,where,gameobjects,cordinatemap):
        if where==0:
            if checktile(self.x,self.y-1,gameobjects,cordinatemap):
                self.y-=1
        elif where==1:
            if checktile(self.x+1,self.y,gameobjects,cordinatemap):
                self.x+=1
        elif where==2:
            if checktile(self.x-1,self.y,gameobjects,cordinatemap):
                self.x-=1
        elif where==3:
            if checktile(self.x,self.y+1,gameobjects,cordinatemap):
                self.y+=1
    def attack(self,gameobjects):
        for ob in gameobjects:
            self.pic=pics[self.name+"2"]
            if(ob.x==self.x+1 and ob.y==self.y)or(ob.y==self.y+1 and ob.x==self.x)or(ob.x==self.x-1 and ob.y==self.y)or(ob.y==self.y-1 and ob.x==self.x):
                gameobjects.remove(ob)
                self.kills+=1
                
def checktile(tilex,tiley,objects,cordinatemap):
    if tilex>49 or tiley>49 or tilex<0 or tiley<0:
        return False
    if cordinatemap[tiley][tilex][:4]!="walk":
        return False
    for ob in objects:
        if [tilex,tiley]==[ob.x,ob.y]:
            return False
    return True
    
def addblob(name,gameobjects,cordinatemap,walkables):
    x,y=choice(walkables)
    if checktile(x,y,gameobjects,cordinatemap):
        blob=thingy(x,y,pics[name],name)
        gameobjects.append(blob)
        
def updatedata(screen,kills):
    font = pygame.font.Font("Ubuntu-B.ttf", 20)
    if len(kills)<3:
        screen.blit(font.render('Blobs killed: '+kills, True, (255,0,0)),(830,120))
    else:
        screen.blit(font.render('Blobs killed: ', True, (255,0,0)),(830,120))
        screen.blit(font.render(kills, True, (255,0,0)),(830,140))
        
def createMap(name):
    Map=open("maps/"+name+".txt","w")
    data="empty "*50
    for i in range(49):
        data+="\n"+"empty "*50
    Map.write(data)
    Map.close()
    
def Draw(screen,cords,brush,pos,selected):
    xor=floor(pos[0]/16)
    yor=floor(pos[1]/16)
    size=floor(brush/2)
    x=xor-size
    for ix in range(brush):
        y=yor-size
        for iy in range(brush):
            if not(y<0 or x<0 or y>49 or x>49):
                screen.blit(tiles[selected],(x*16,y*16))
                cords[y][x]=selected
            y+=1
        x+=1
        
def EditMapMenu(name,buttons,cords,brushes,tiles2,fromcords=False):
    screen=pygame.Surface(size)
    if fromcords:
        land=Cordstoland(cords,buttons)
    else:
        land=MapGen(name,buttons,cords)
    for tile in tiles:
        tiles2.append(tile)
    tiles2.sort()
    tilenr=len(tiles2)
    buttons["!!_SCREEN_!!"]=button(screen,"",font,(255,0,0),(90,30,0),0,0,800,800)
    buttons["!!_SAVE_!!"]=button(land,"Save",font,(255,0,0),(90,30,0),830,620, 144, 30)
    buttons["!!_LOAD_!!"]=button(land,"Load",font,(255,0,0),(90,30,0),830,660, 144, 30)
    buttons["!!_NEW_!!"]=button(land,"New",font,(255,0,0),(90,30,0),830,580, 144, 30)
    land.blit(font.render("Selected: ", True, (255,0,0)),(830,130))
    y=170
    x=830
    screen.blit(land,(0,0))
    while tilenr>0:
        tilenr+=-1
        if x>970:
            y+=18
            x=830
        buttons[tiles2[tilenr]]=screen.blit(tiles[tiles2[tilenr]],(x,y))
        x+=18
    y+=20
    x=830
    screen.blit(font.render("Brushes: ", True, (255,0,0)),(x,y))
    y+=30
    for bru in brushes:
        buttons[bru]=button(screen,str(bru),font,(255,0,0),(90,30,0),x,y, 24,24)
        x+=30
    return screen
    
def EditMap(screen,name):
    brushes=[1,3,5,7,9]
    brush=1
    buttons={}
    cords=[]
    selected="empty"
    tiles2=[]
    land=EditMapMenu(name,buttons,cords,brushes,tiles2)
    screen.blit(land,(0,0))
    screen.blit(tiles[selected],(930,134))
    pygame.display.flip()
    drawing=False
    while quits[0]==False and quits[1]==False:
        for event in pygame.event.get():
            if event.type ==QUIT:
                pygame.quit()
                quits[0]=True
                quits[1]=True
            if event.type == MOUSEMOTION and drawing:
                Draw(screen,cords,brush,event.pos,selected)
            if event.type == MOUSEBUTTONDOWN:
                if event.button==1:
                    for but in buttons:
                        if buttons[but].collidepoint(event.pos):
                            if but=="!!_SCREEN_!!":
                                Draw(screen,cords,brush,event.pos,selected)
                                drawing=True
            if event.type == MOUSEBUTTONUP:
                if event.button==1:
                    drawing=False
                    for but in buttons:
                        if buttons[but].collidepoint(event.pos):
                            if but=="!!_QUIT_!!":
                                pygame.quit()
                                quits[0]=True
                            elif but=="!!_MAIN_!!":
                                quits[1]=True
                            elif but=="!!_LOAD_!!":
                                brush=1
                                buttons={}
                                selected="empty"
                                tiles2=[]
                                name2=chooseMap(screen,quits)
                                if name2!="!!_BACK_!!":
                                    cords=[]
                                    name=name2
                                    land=EditMapMenu(name,buttons,cords,brushes,tiles2)
                                else:
                                    land=EditMapMenu(name,buttons,cords,brushes,tiles2,True)
                                quits[1]=False
                                screen.blit(land,(0,0))
                            elif but=="!!_SAVE_!!":
                                name2=setName(screen,font,"Save as: ",quits,name)
                                quits[1]=False
                                if name2!=None and overwrite(screen,name2,quits):
                                    name=name2
                                    MAP=open("maps/"+name+".txt","w+")
                                    for line in cords:
                                        for tile in line:
                                            MAP.write(tile+str(" "))
                                        MAP.write("\n")
                                    MAP.close()
                                    brush=1
                                    buttons={}
                                    selected="empty"
                                    tiles2=[]
                                    land=EditMapMenu(name,buttons,cords,brushes,tiles2)
                                else:
                                    brush=1
                                    buttons={}
                                    selected="empty"
                                    tiles2=[]
                                    land=EditMapMenu(name,buttons,cords,brushes,tiles2,True)
                                quits[1]=False
                                screen.blit(land,(0,0))
                            elif but=="!!_NEW_!!":
                                name2=setName(screen,font,"Name: ",quits)
                                brush=1
                                buttons={}
                                selected="empty"
                                tiles2=[]
                                quits[1]=False
                                if name2!=None and overwrite(screen,name2,quits):
                                    name=name2
                                    createMap(name)
                                    cords=[]
                                    land=EditMapMenu(name,buttons,cords,brushes,tiles2)
                                else:
                                    land=EditMapMenu(name,buttons,cords,brushes,tiles2,True)
                                quits[1]=False
                                screen.blit(land,(0,0))
                            elif but in tiles2:
                                selected=but
                            elif but in brushes:
                                brush=but
                            elif but=="!!_SCREEN_!!":
                                Draw(screen,cords,brush,event.pos,selected)
        if quits[1] or quits[0]:
            break
        screen.blit(tiles[selected],(930,134))
        button(screen,str(brush),font,(255,0,0),(90,30,0),950,130, 20,20)
        pygame.display.flip()
        clock.tick(frame)
        
def Game(screen,mapname):
    walkables=[]
    up,right=0,0
    gameobjects=[]
    buttons={}
    cordinatemap=[]
    land=MapGen(mapname,buttons,cordinatemap)
    land.blit(font.render("WASD to move", True, (255,0,0)),(830,180))
    land.blit(font.render("Space to attack", True, (255,0,0)),(830,210))
    for x in range(50):
        for y in range(50):
            if checktile(x,y,[],cordinatemap):
                walkables.append((x,y))
    if len(walkables)<5:
        return False
    x,y=choice(walkables)
    player=thingy(x,y,pics["player1"],"player")
    gameobjects.append(player)
    while quits[0]==False and quits[1]==False:
        player.pic=pics["player1"]
        for event in pygame.event.get():
            if event.type ==QUIT:
                pygame.quit()
                quits[0]=True
            if event.type == KEYDOWN:
                if event.key == options["up"]:
                    up+=1
                if event.key == options["left"]:
                    right-=1
                if event.key == options["down"]:
                    up-=1
                if event.key == options["right"]:
                    right+=1
                if event.key == options["attack"]:
                    player.attack(gameobjects)
            if event.type == KEYUP:
                if event.key == options["up"]:
                    up-=1
                if event.key == options["left"]:
                    right+=1
                if event.key == options["down"]:
                    up+=1
                if event.key == options["right"]:
                    right-=1
            if event.type == MOUSEBUTTONUP:
                if event.button==1:
                    for but in buttons:
                        if buttons[but].collidepoint(event.pos):
                            if but=="!!_MAIN_!!":
                                quits[1]=True
                            elif but=="!!_QUIT_!!":
                                pygame.quit()
                                quits[0]=True
        if quits[0]==True or quits[1]==True:
            break
        if up <0:
            player.move(3,gameobjects,cordinatemap)
        if up >0:
            player.move(0,gameobjects,cordinatemap)
        if right <0:
            player.move(2,gameobjects,cordinatemap)
        if right >0:
            player.move(1,gameobjects,cordinatemap)
        screen.blit(land,(0,0))
        if len(gameobjects)<options["blobs"]+1:
            addblob("blob",gameobjects,cordinatemap,walkables)
        for ob in gameobjects:
            if ob.name[:4]=="blob":
                ob.move(randint(0,3),gameobjects,cordinatemap)
            screen.blit(ob.pic,(ob.x*16,ob.y*16))
        updatedata(screen,str(player.kills))
        pygame.display.flip()
        clock.tick(frame)

pygame.mixer.music.load("Intro.ogg")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(options["music"]/100)
while quits[0]==False:
    achoice=MainMenu(screen,quits)
    
    quits[1]=False
    if achoice=="!!_PLAY_!!":
        mapname=chooseMap(screen,quits)
        quits[1]=False
        if mapname!="!!_BACK_!!" and mapname!=None:
            frame=6
            Game(screen,mapname)
            quits[1]=False
    elif achoice=="!!_EDIT_!!":
        mapname=chooseMap(screen,quits)
        quits[1]=False
        if mapname!="!!_BACK_!!" and mapname!=None:
            frame=30
            EditMap(screen,mapname)
            quits[1]=False
    elif achoice=="!!_NEW_!!":
        mapname=setName(screen,font,"Name: ",quits)
        quits[1]=False
        if mapname!="!!_BACK_!!" and mapname!=None and overwrite(screen,mapname,quits):
            quits[1]=False
            createMap(mapname)
            frame=30
            EditMap(screen,mapname)
            quits[1]=False
    elif achoice=="!!_OPTIONS_!!":
        SetOptions(screen,quits)
        quits[1]=False
