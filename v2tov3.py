import json


def convert(map):
    notes=map["_notes"]
    #sliders obstacles bombs and waypoints are not supported at this time
    newNotes=[]
    bombs=[]
    for i in notes:
        note={
            "b": i["_time"],
            "x": i["_lineIndex"],
            "y": i["_lineLayer"],
            "c": 0,
            "a": 0,
            "d": i["_cutDirection"]
        }
        if i["_type"]==0:
            note["c"]=0
        elif i["_type"]==1:
            note["c"]=1
        elif i["_type"]==3:
            bombs.append({
                "b":i["_time"],
                "x": i["_lineIndex"],
                "y": i["_lineLayer"]        
            })
        else:
            continue
        if "_customData" in i:
            if "_fake" in i["_customData"]:
                if i["_customData"]["_fake"]:
                    continue
        newNotes.append(note)
    oldObstacles=map["_obstacles"]
    obstacles=[]
    for i in oldObstacles:
        ob={
            "b": i["_time"],
            "x": i["_lineIndex"],
            "y": 0 if["_type"]==0 else 2,
            "d": i["_duration"],
            "w": i["_width"],
            "h": 5 - (0 if["_type"]==0 else 2)
        }
        obstacles.append(ob)
    lights=[]
    for i in map["_events"]:
        
        li={
            "b": i["_time"],
            "et": i["_type"],
            "i": i["_value"],
            "f": 1
        }
        try:
            li["f"]= i["_floatValue"]
        except:
            pass
        lights.append(li)
    newMap={
        "version":"3.0.0",
        "bpmEvents": [],
        "rotationEvents": [],
        "colorNotes": newNotes,
        "bombNotes": bombs,
        "obstacles": obstacles,
        "sliders": [],
        "burstSliders": [],
        "waypoints": [],
        "basicBeatmapEvents": lights,
        "colorBoostBeatmapEvents": [],
        "lightColorEventBoxGroups": [],
        "lightRotationEventBoxGroups": [],
        "basicEventTypesWithKeywords": {},
        "useNormalEventsAsCompatibleEvents": False
    }
    return newMap

if __name__=="__main__":
    with open("beatmap/Info.dat","r") as f:
        info = json.load(f)
    beatmaps=info["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"]
    for i in beatmaps:
        print(i["_beatmapFilename"])
        with open("beatmap/"+i["_beatmapFilename"],"r") as f:
            print("beatmap/"+i["_beatmapFilename"])
            try:
                map=json.load(f)
            except:
                continue
        with open("beatmap/"+i["_beatmapFilename"],"w") as f:
            #print(convert(map))
            json.dump(convert(map),f,separators=(',', ':'))
        
    print("done")