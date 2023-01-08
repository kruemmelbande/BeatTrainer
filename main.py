print("V0.0.1")
print("This is just a test, so dont expect anything to work well")

import time, pygame,json
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((400, 300))
board=[[0 for i in range(4)] for i in range(4)]
def printInColor(text,color):
    print("\033[38;2;"+str(color[0])+";"+str(color[1])+";"+str(color[2])+"m"+text+"\033[0m",end="")
def draw(colorNote,last):
    global indicator,board
    beatsPerIndicator=20
    if indicator<beatsPerIndicator:
        ind="["+"-"*indicator+"#"+"-"*(beatsPerIndicator-indicator)+"]"
    else:
        ind="["+"-"*(beatsPerIndicator-(indicator-beatsPerIndicator))+"#"+"-"*(indicator-beatsPerIndicator)+"]"
    if colorNote["b"]-last["b"]<60/bpm/256:
        indicator=(indicator+1)%(beatsPerIndicator*2) 
        ind+=" " + ["#-","##","-#"][last["c"]+colorNote["c"]]+" "
        board[colorNote["x"]][colorNote["y"]]=colorNote["c"]+1
    else:
        ind+=" " + ["#-","-#"][colorNote["c"]]+" "
        board=[[0 for i in range(4)] for i in range(4)]
        board[colorNote["x"]][colorNote["y"]]=colorNote["c"]+1
    
    #draw the board in the console
        
    print("\n"*10)
    for i in range(4):
        for j in range(4):
            if board[i][j]==1:
                printInColor("██",(255,0,0))
            elif board[i][j]==2:
                printInColor("██",(0,0,255))
            
            else:
                print("  ",end="")
        print()
    #print(ind,end="\r")
    #draw the board in pygame
    e=pygame.event.get()
    for i in e:
        if i.type==pygame.QUIT:
            exit()
    screen.fill((0,0,0))
    for i in range(4):
        for j in range(4):
            if board[i][j]==1:
                pygame.draw.rect(screen,(255,0,0),(i*100,j*100,100,100))
            elif board[i][j]==2:
                pygame.draw.rect(screen,(0,0,255),(i*100,j*100,100,100))
            
    pygame.display.flip()
try:
    with open("beatmap/Info.dat","r") as f:
        info = json.load(f)
    beatfile=info["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"][0]["_beatmapFilename"]
    musicfile=info["_songFilename"]
    bpm=info["_beatsPerMinute"]
    with open("beatmap/"+beatfile,"r") as f:
        beatmap = json.load(f)
except Exception as e:
    print("Error: Info.dat not found (did you add a beatmap?)")
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
    