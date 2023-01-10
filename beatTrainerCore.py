import json,os
currentBeatmap={}
beemaps=[]
song=None
cover=None
def makeCopy(list):
    newList={}
    for i in list:
        newList[i]=list[i]
    return newList
def loadbeatmap(filepath):
    global beemaps,info,song,cover
    beemaps={}
    with open(filepath+"\Info.dat","r") as f:
        info=json.load(f)
    for i in info["_difficultyBeatmapsSets"]:
        with open(i["_beatmapFilename"],"r") as f:
            beemaps[str(i["_difficulty"])]=json.load(f)
    song=open(filepath+info["_songFilename"],"rb")
    cover=open(filepath+info["_coverImageFilename"],"rb")

def getLoadedDifficulties():
    return beemaps.keys()

def clearLoaded():
    global currentBeatmap,beemaps,song,cover
    currentBeatmap={}
    beemaps=[]
    song=None
    cover=None

def convertLoaded(difficulty,saveLocation):
    global beemaps,currentBeatmap,info
    currentBeatmap=beemaps[difficulty]
    lefts=[]
    rights=[]
    easy={}
    normal={}
    for i in currentBeatmap["colorNotes"]:
        if i["c"] == 0:
            lefts.append(i)
        else:
            rights.append(i)
    
    easy=makeCopy(currentBeatmap)
    normal=makeCopy(currentBeatmap)
    easy["colorNotes"]=lefts
    normal["colorNotes"]=rights
    newInfo=makeCopy(info)
    ogInfo={}
    for i in info["_difficultyBeatmapsSets"]:
        if i["_difficulty"] == difficulty:
            ogInfo=i
            break
    easyLevel=makeCopy(ogInfo)
    easyLevel["_difficulty"]="Easy"
    easyLevel["_difficultyRank"]=1
    easyLevel["_beatmapFilename"]="Easy.dat"
    normalLevel=makeCopy(ogInfo)
    normalLevel["_difficulty"]="Normal"
    normalLevel["_difficultyRank"]=3
    newInfo["_difficultyBeatmapSets"]={}
    newInfo["_difficultyBeatmapSets"]["_beatmapCharacteristicName"]="Standard"
    newInfo["_difficultyBeatmapSets"]["_difficultyBeatmaps"]=[easyLevel,normalLevel]
    try:
        os.rmdir(saveLocation)
    except:
        pass
    os.mkdir(saveLocation)
    with open(saveLocation+"\Info.dat","w") as f:
        json.dump(newInfo,f)
    with open(saveLocation+"\Easy.dat","w") as f:
        json.dump(easy,f)
    with open(saveLocation+"\Normal.dat","w") as f:
        json.dump(normal,f)
    with open(saveLocation+newInfo["_songFilename"]) as f:
        f.write(song.read())
    with open(saveLocation+newInfo["_coverImageFilename"]) as f:
        f.write(cover.read())