import json,os
from PIL import Image, ImageTk
currentBeatmap={}
beemaps=[]
song=None
cover=None
def makeCopy(list):
    newList={}
    for i in list:
        newList[i]=list[i]
    return newList

def get_current_file_path():
    global path
    return path

def getThumbnail():
    global thumnail
    try:
        im = thumbnail.copy()
        im = im.resize((100,100), Image.ANTIALIAS)
        #im.show() <- shows the image correctly
        return ImageTk.PhotoImage(im)
    except:
        return None
def getBeatmapName():
    global info
    try:
        return str(info["_songName"])
    except:
        return "No beatmap loaded"
def loadbeatmap(filepath):
    try:
        global beemaps,info,song,cover, thumbnail, path
        beemaps={}
        path=filepath
        with open(filepath+"/Info.dat","r") as f:
            info=json.load(f)
        #print(json.dumps(info,indent=4))
        for i in info["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"]:
            with open(filepath+"/"+i["_beatmapFilename"],"r") as f:
                beemaps[str(i["_difficulty"])]=json.load(f)
        thumbnail=Image.open(filepath+"/"+info["_coverImageFilename"])
        song=open(filepath+"/"+info["_songFilename"],"rb")
        cover=open(filepath+"/"+info["_coverImageFilename"],"rb")
        return 0
    except:
        return 1
def getLoadedDifficulties():
    return [i for i in beemaps]

def clearLoaded():
    global currentBeatmap,beemaps,song,cover
    currentBeatmap={}
    beemaps=[]
    song=None
    cover=None

def convertLoaded(difficulty,saveLocation):
    try:
        global beemaps,currentBeatmap,info
        currentBeatmap=beemaps[difficulty]
        try:
            v=currentBeatmap["version"]
        except:
            try:
                v=currentBeatmap["_version"]
            except:
                print("Couldnt determine version of map (trying to continue anyway)")
                v="3.0.0"
        if v.startswith("2."):
            from v2tov3 import convert
            currentBeatmap=convert(currentBeatmap)
        lefts=[]
        rights=[]
        easy={}
        normal={}
        #print(str(json.dumps(currentBeatmap,indent=4)[:1000]))
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
        for i in info["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"]:
            if i["_difficulty"] == difficulty:
                ogInfo=i
                break
        easyLevel=makeCopy(ogInfo)
        easyLevel["_difficulty"]="Easy"
        easyLevel["_difficultyRank"]=1
        easyLevel["_beatmapFilename"]="StandartEasy.dat"
        normalLevel=makeCopy(ogInfo)
        normalLevel["_difficulty"]="Normal"
        normalLevel["_difficultyRank"]=3
        normalLevel["_beatmapFilename"]="StandartNormal.dat"
        newInfo["_difficultyBeatmapSets"]=[{}]
        newInfo["_difficultyBeatmapSets"][0]["_beatmapCharacteristicName"]="Standard"
        newInfo["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"]=[easyLevel,normalLevel]
        newInfo["_songSubName"]="(training edition)"
        try:
            #delete all existing files
            os.remove(saveLocation+"/Info.dat")
            os.remove(saveLocation+"/StandartEasy.dat")
            os.remove(saveLocation+"/StandartNormal.dat")
            os.remove(saveLocation+"/"+newInfo["_songFilename"])
            os.remove(saveLocation+"/"+newInfo["_coverImageFilename"])
        except:
            pass
        try:
            os.mkdir(saveLocation)
        except:
            pass
        with open(saveLocation+"/Info.dat","w") as f:
            json.dump(newInfo,f,indent=2)
        with open(saveLocation+"/StandartEasy.dat","w") as f:
            json.dump(easy,f)
        with open(saveLocation+"/StandartNormal.dat","w") as f:
            json.dump(normal,f)
        with open(saveLocation+"/"+newInfo["_songFilename"], "wb") as f:
            f.write(song.read())
        with open(saveLocation+"/"+newInfo["_coverImageFilename"], "wb") as f:
            f.write(cover.read())
        print("Done!")
        return 0
    except:
        return 1
if __name__ == "__main__":
    print("This is a library, not a program. Run beatTrainer.py instead.")