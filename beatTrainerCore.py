import json,os
from PIL import Image, ImageTk
from v2tov3 import convert

currentBeatmap={}
beemaps=[]
song=None
cover=None
updated=0
def makeCopy(list):
    newList={}
    for i in list:
        newList[i]=list[i]
    return newList

def get_current_file_path():
    global path
    return path

def has_bpm_events():
    global currentBeatmap
    if "bpmEvents" in currentBeatmap:
        if len(currentBeatmap["bpmEvents"])>0:
            return True
    return False

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
        return str(info["_songName"]+"\n"+info["_songSubName"]+"\n"+info["_songAuthorName"]+"\n"+info["_levelAuthorName"])
    except:
        return "No beatmap loaded"

def getBeatmapNames():
    global info
    for i in info["_difficultyBeatmapSets"]:
        if i["_beatmapCharacteristicName"]=="Standard":
            info["_difficultyBeatmapSets"]=[i]
            break
    return [i["_beatmapFilename"] for i in info["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"]]

def loadbeatmap(filepath):
    try:
        global beemaps,info,song,cover, thumbnail, path,v, updated
        beemaps={}
        path=filepath
        with open(filepath+"/Info.dat","r") as f:
            info=json.load(f)
        #print(json.dumps(info,indent=4))
        for i in info["_difficultyBeatmapSets"]:
            if i["_beatmapCharacteristicName"]=="Standard":
                info["_difficultyBeatmapSets"]=[i]
                break
        for i in info["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"]:
            with open(filepath+"/"+i["_beatmapFilename"],"r") as f:
                beemaps[str(i["_difficulty"])]=json.load(f)
        thumbnail=Image.open(filepath+"/"+info["_coverImageFilename"])
        song=open(filepath+"/"+info["_songFilename"],"rb")
        cover=open(filepath+"/"+info["_coverImageFilename"],"rb")
        currentBeatmap=beemaps[[i for i in beemaps][0]]
        try:
            v=currentBeatmap["version"]
        except:
            try:
                v=currentBeatmap["_version"]
            except:
                print("Couldnt determine version of map (trying to continue anyway)")
                v="3.0.0"
        if v.startswith("2."):
            
            currentBeatmap=convert(currentBeatmap)
            updated=1
        else:
            updated=0
        return 0
    except Exception as e:
        print(e)
        return 1
    
def getLoadedDifficulties():
    return [i for i in beemaps]

def getInfo():
    global info
    return info

def clearLoaded():
    global currentBeatmap,beemaps,song,cover
    currentBeatmap={}
    beemaps=[]
    song=None
    cover=None

def isUpdated():
    global updated
    return updated

def saveUpdated(filepath):
    try:
        oldfiles=get_current_file_path()
        #copy files from old to new
        for i in os.listdir(oldfiles):
            if i not in os.listdir(filepath):
                with open(os.path.join(filepath,i),'wb') as f:
                    with open(os.path.join(oldfiles,i),'rb') as g:
                        f.write(g.read())
        beatmapnames=getBeatmapNames()
        for beatmap in beatmapnames:
            oldbeatmap=json.load(open(os.path.join(oldfiles,beatmap),'r'))
            newbeatmap=convert(oldbeatmap)
            with open(os.path.join(filepath,beatmap),'w') as f:
                f.write(json.dumps(newbeatmap,separators=(',', ':')))
    except Exception as e:
        print("Failed to update beatmap. Either the beatmap is already updated or the beatmap is corrupted.")
        print(e)
        print("line:",e.__traceback__.tb_lineno)

def convertLoaded(difficulty,saveLocation):
    try:
        global beemaps,currentBeatmap,info,updated,v
        updated=0 
        
        print(updated)
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
            json.dump(easy,f,separators=(',', ':'))
        with open(saveLocation+"/StandartNormal.dat","w") as f:
            json.dump(normal,f,separators=(',', ':'))
        with open(saveLocation+"/"+newInfo["_songFilename"], "wb") as f:
            f.write(song.read())
        with open(saveLocation+"/"+newInfo["_coverImageFilename"], "wb") as f:
            f.write(cover.read())

        return 0
    except:
        return 1
if __name__ == "__main__":
    print("This is the backend, and cannot be run directly.")