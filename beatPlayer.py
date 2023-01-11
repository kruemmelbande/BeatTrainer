#print("V0.0.2")
#print("This is just a test, so dont expect anything to work well")
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from v2tov3 import convert
import time, pygame,json, sys

size = width, height = 400, 300
board=[[0 for i in range(4)] for i in range(4)]
dirs=[[0 for i in range(4)] for i in range(4)]
volume=0.1

def pyUpdate():
    e=pygame.event.get()
    for f in e:
        if f.type==pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            return 1
    return 0
def printInColor(text,color):
    print("\033[38;2;"+str(color[0])+";"+str(color[1])+";"+str(color[2])+"m"+text+"\033[0m",end="")

def moveCursor(lines):
   sys.stdout.write(f"\x1b[{lines}A")

def draw(colorNote,last, consoleversion=False):
    global indicator,board, bpm
    beatsPerIndicator=20
    
    dirs[colorNote["x"]][colorNote["y"]]=colorNote["d"]
    if colorNote["b"]-last["b"]<60/bpm/256:
        indicator=(indicator+1)%(beatsPerIndicator*2) 

        board[colorNote["x"]][colorNote["y"]]=colorNote["c"]+1
    else:

        board=[[0 for i in range(4)] for i in range(4)]
        board[colorNote["x"]][colorNote["y"]]=colorNote["c"]+1
    
    if consoleversion:
        #draw the board in the console
        
        moveCursor(5)
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
    
def play(path, consoleversion=False, difficulty=0):
    try:
        global beatfile, musicfile, bpm, indicator, screen
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        try:
            with open(path+"/Info.dat","r") as f:
                info = json.load(f)
            for i in info["_difficultyBeatmapSets"]:
                if i["_beatmapCharacteristicName"]=="Standard":
                    info["_difficultyBeatmapSets"]=[i]
                    break
            if difficulty==0:
                beatfile=info["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"][0]["_beatmapFilename"]
            else:
                for i in info["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"]:
                    if i["_difficulty"]==difficulty:
                        beatfile=i["_beatmapFilename"]
                        break
            musicfile=info["_songFilename"]
            bpm=info["_beatsPerMinute"]
            #set the captiom
            pygame.display.set_caption(info["_songName"]+" - "+info["_songAuthorName"])
            with open(path+"/"+beatfile,"r") as f:
                beatmap = json.load(f)
            #just for development purposes, we are gonna store the beatmap
            #in a temporary file, which will be indented correctly, so its
            #understandable and can be developed with, cuz im not reading the docs.
            devmode=False
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
                    
            #print(beatmap)
        except Exception as e:
            print("Error: Info.dat not found (did you add a beatmap?)")
            print(path+"/"+beatfile)
            return
        try:
            v=beatmap["version"]
        except:
            v=beatmap["_version"]
        if v.startswith("2."):
            beatmap=convert(beatmap)
            print("Updated beatmap to version 3.0.0")
            print(len(beatmap["colorNotes"]),"notes found")

        indicator=0

    
        #load the music
        try:
            
            pygame.mixer.init()
            pygame.mixer.music.load(path+"/"+musicfile)
            #set the volume
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()
        except:
            print("Audio disabled due to error.", end="\r")
            time.sleep(2)
            print("                            ", end="")
        #start the map
        starttime=time.time()
        last=beatmap["colorNotes"][0]

        for i in beatmap["colorNotes"]:
            t=i["b"]
            seconds=t*60/bpm
            pygame.mixer.music.set_volume(volume)
            while starttime+seconds-1>time.time():
                time.sleep(0.1)
                if pyUpdate():
                    return
            if starttime+seconds>time.time():
                time.sleep(starttime+seconds-time.time())
            draw(i,last)
            last=i
            if pyUpdate():
                return
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.stop()
        pygame.quit()
        return
    except:
        pygame.mixer.music.stop()
        pygame.quit()
        return
        
if __name__ == "__main__":
    play("beatmap")