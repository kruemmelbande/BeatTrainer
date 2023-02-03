use std::process::exit;
use serde_json;
fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2{
        println!("no map specified");
        exit(1);
    }else if args.len() <3{
        println!("Invalid arguments");
        exit(1);
    }
    let folder_location = &args[1];
    //check if folder exists
    if !std::path::Path::new(folder_location).exists() {
        println!("The folder {} does not exist", folder_location);
        exit(1);
    }
    let folder = std::fs::read_dir(folder_location).unwrap();
    let mut info_path = String::new();
//    println!("The folder {} the following files:", folder_location);
    let mut is_valid_map = false;
    for file in folder{
        let file_name = file.unwrap().path().display().to_string();
        //print!("{}", file_name);
        if file_name.ends_with("Info.dat") {
            is_valid_map = true;
            info_path = file_name.to_string();
            //println!("info_path: {}", info_path);
            //print!("\t\t<- map info")
        }
        //println!();

    }


    if !is_valid_map {
        println!("The folder {} does not contain a valid map", folder_location);
        exit(1);
    }

    let info= std::fs::read_to_string(info_path).unwrap();
    //println!("{}", info);
    //load info as json
    let info_json: serde_json::Value = serde_json::from_str(&info).unwrap();
    //println!("{}", info_json["_songName"]);
    if args[2] == "info" {
        get_info(info_json);
    }
    else if args[2] == "verbinfo"{
        println!("info: {}", serde_json::to_string_pretty(&info_json).unwrap());
    }
}
fn get_info(info_json: serde_json::Value) {
    //print the song name, subname and author as a json
    let c = info_json.as_object().unwrap();
    //create json
    let mut json = serde_json::Map::new();
    //song author name
    json.insert(String::from("_songAuthorName"), c.get("_songAuthorName").unwrap().clone());
    //level author name
    json.insert(String::from("_levelAuthorName"), c.get("_levelAuthorName").unwrap().clone());
    //song name
    json.insert(String::from("_songName"), c.get("_songName").unwrap().clone());
    //song subname
    json.insert(String::from("_songSubName"), c.get("_songSubName").unwrap().clone());
    //version
    json.insert(String::from("_version"), c.get("_version").unwrap().clone());
    let mut json = serde_json::Value::Object(json);
    //get the difficulties
    let difficulties = c.get("_difficultyBeatmapSets").unwrap().as_array().unwrap();
    //get the difficulties from the first set
    //println!("difficulties: {}", serde_json::to_string_pretty(&difficulties).unwrap());
    let mut category = serde_json::Value::Null;
    for cat in difficulties.iter() {
        //search for the "Standart" beatmap category
        //println!("difficulty: {}", serde_json::to_string_pretty(&cat).unwrap());
        if  cat.as_object().unwrap().get("_beatmapCharacteristicName").unwrap().as_str().unwrap() == "Standard" {
            //get the category 
            category = cat.clone();
            break;
        }
    }
    if category == serde_json::Value::Null {
        println!("No standard difficulty found");
        exit(1);
    }
    //difficulty now sotres the standard category. We now need to get all the difficulties from the category, and also the file name
    let mut difficulties = Vec::new();
    for d in category.as_object().unwrap().get("_difficultyBeatmaps").unwrap().as_array().unwrap() {
        let mut dif= serde_json::Map::new();
        dif.insert(String::from("difficulty"), d.as_object().unwrap().get("_difficulty").unwrap().clone());
        dif.insert(String::from("file"), d.as_object().unwrap().get("_beatmapFilename").unwrap().clone());
        difficulties.push(serde_json::Value::Object(dif));

    }
    json.as_object_mut().unwrap().insert(String::from("difficulties"), serde_json::Value::Array(difficulties));
    //format json
    let json = serde_json::to_string_pretty(&json).unwrap();
    println!("{}", json);

}
