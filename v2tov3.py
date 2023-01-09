import json
def convert(map):
    notes=map["_notes"]
    #sliders obstacles bombs and waypoints are not supported at this time
    newNotes=[]
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
        else:
            continue
        if "_customData" in i:
            if "_fake" in i["_customData"]:
                if i["_customData"]["_fake"]:
                    continue
        newNotes.append(note)	
    newMap={
        "version":"3.0.0",
        "bpmEvents": [],
        "rotationEvents": [],
        "colorNotes": newNotes,
        "bombNotes": [],
        "obstacles": [],
        "sliders": [],
        "burstSliders": [],
        "waypoints": [],
        "basicBeatmapEvents": [],
        "colorBoostBeatmapEvents": [],
        "lightColorEventBoxGroups": [],
        "lightRotationEventBoxGroups": [],
        "basicEventTypesWithKeywords": {},
        "useNormalEventsAsCompatibleEvents": False
    }
    return newMap

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
        json.dump(convert(map),f,indent=4)
    
print("done")