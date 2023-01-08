print("V0.0.1")
print("This is just a test, so dont expect anything to work well")
import time, pygame,json
pygame.init()
pygame.mixer.init()

def draw(colorNote,last):
    global indicator
    beatsPerIndicator=20
    groupwLast=0
    if indicator<beatsPerIndicator:
        ind="["+"-"*indicator+"#"+"-"*(beatsPerIndicator-indicator)+"]"
    else:
        ind="["+"-"*(beatsPerIndicator-(indicator-beatsPerIndicator))+"#"+"-"*(indicator-beatsPerIndicator)+"]"
    if colorNote["b"]-last["b"]<60/bpm/64:
        groupwLast=1
        indicator=(indicator+1)%(beatsPerIndicator*2) 
        ind+=" " + ["#-","##","-#"][last["c"]+colorNote["c"]]+" "
    else:
        ind+=" " + ["#-","-#"][colorNote["c"]]+" "
    
    print(ind,end="\r")
    return "no u"
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
pygame.mixer.music.set_volume(0.1)
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
print("Done!")
    