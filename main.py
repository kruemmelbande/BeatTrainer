print("V0.0.1")
print("This is just a test, so dont expect anything to work well")

import time, pygame,json
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((400, 300))
size = width, height = 400, 300
board=[[0 for i in range(4)] for i in range(4)]
dirs=[[0 for i in range(4)] for i in range(4)]
def printInColor(text,color):
    print("\033[38;2;"+str(color[0])+";"+str(color[1])+";"+str(color[2])+"m"+text+"\033[0m",end="")

def draw(colorNote,last):
    global indicator,board
    beatsPerIndicator=20
    
    dirs[colorNote["x"]][colorNote["y"]]=colorNote["d"]
    if colorNote["b"]-last["b"]<60/bpm/256:
        indicator=(indicator+1)%(beatsPerIndicator*2) 

        board[colorNote["x"]][colorNote["y"]]=colorNote["c"]+1
    else:

        board=[[0 for i in range(4)] for i in range(4)]
        board[colorNote["x"]][colorNote["y"]]=colorNote["c"]+1
    
    #draw the board in the console
        
    print("\n"*10)
    print("##########")
    for j in range(2,-1,-1):
        print("#",end="")
        for i in range(4):
            if board[i][j]==1:
                printInColor("██",(255,0,0))
            elif board[i][j]==2:
                printInColor("██",(0,0,255))
            
            else:
                print("[]",end="")
        print("#")
    print("##########")
    #print(ind,end="\r")
    #draw the board in pygame
    e=pygame.event.get()
    for i in e:
        if i.type==pygame.QUIT:
            exit()
    screen.fill((0,0,0))
    grid=1
    if grid:
        #draw grid
        for i in range(5):
            screen.fill((255,255,255),(100*i,0,1,height))
        for i in range(4):
            screen.fill((255,255,255),(0,100*i,width,1))
    for i in range(4):
        for j in range(4):
            if not board[i][j]==0:
                x,y=100*i,height-j*100-100
                if board[i][j]==1:
                    pygame.draw.rect(screen,(255,0,0),(x,y,100,100))
                elif board[i][j]==2:
                    pygame.draw.rect(screen,(0,0,255),(x,y,100,100))
                dir=dirs[i][j]
                #draw the triangles for all directions except center
                if dir==0:
                    #up
                    pygame.draw.polygon(screen,(255,255,255),((x+50,y+50),(x+100,y+100),(x,y+100)))
                elif dir==1:
                    #down
                    pygame.draw.polygon(screen,(255,255,255),((x+50,y+50),(x+100,y),(x,y)))
                elif dir==2:
                    #left
                    pygame.draw.polygon(screen,(255,255,255),((x+50,y+50),(x+100,y),(x+100,y+100)))
                elif dir==3:
                    #right
                    pygame.draw.polygon(screen,(255,255,255),((x+50,y+50),(x,y),(x,y+100)))
                elif dir==4:
                    #upleft
                    pygame.draw.polygon(screen,(255,255,255),((x+25,y+25),(x+25,y+100),(x+100,y+25)))
                elif dir==5:
                    #upright
                    pygame.draw.polygon(screen,(255,255,255),((x+75,y+25),(x+75,y+100),(x,y+25)))
                elif dir==6:
                    #downleft
                    pygame.draw.polygon(screen,(255,255,255),((x+25,y+75),(x+25,y),(x+100,y+75)))
                elif dir==7:
                    #downright
                    pygame.draw.polygon(screen,(255,255,255),((x+75,y+75),(x+75,y),(x,y+75)))
                elif dir==8:
                    #center
                    pygame.draw.circle(screen,(255,255,255),(x+50,y+50),20)
    pygame.display.flip()
    
    
if __name__ == "__main__":
    try:
        with open("beatmap/Info.dat","r") as f:
            info = json.load(f)
        beatfile=info["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"][0]["_beatmapFilename"]
        musicfile=info["_songFilename"]
        bpm=info["_beatsPerMinute"]
        with open("beatmap/"+beatfile,"r") as f:
            beatmap = json.load(f)
        #print(beatmap)
    except Exception as e:
        print("Error: Info.dat not found (did you add a beatmap?)")
        
    if beatmap["version"].startswith("2."):
        print("To use v2 beatmaps, please use the v2tov3 coverter included.")
    #just for development purposes, we are gonna store the beatmap
    #in a temporary file, which will be indented correctly, so its
    #understandable and can be developed with, cuz im not reading the docs.
    devmode=False
    indicator=0
    try:
        with open("devmode.txt","r") as f:
            devmode = f.read()
        if devmode.strip().lower() == "true":
            devmode = True
        else:
            devmode=False
    except:
        pass
    if devmode:
        print("Devmode enabled")
        with open("temp.txt","w") as f:
            json.dump(beatmap,f,indent=4)
            
    #load the music
    pygame.mixer.music.load("beatmap/"+musicfile)
    #set the volume
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play()
    #start the map
    starttime=time.time()
    last=beatmap["colorNotes"][0]

    for i in beatmap["colorNotes"]:
        t=i["b"]
        seconds=t*60/bpm
        if starttime+seconds>time.time():
            time.sleep(starttime+seconds-time.time())
        draw(i,last)
        last=i
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    print("\nDone!")
        