use std::process::exit;
use serde_json;
fn main() {
    let args: Vec<String> = std::env::args().collect();
    let folder_location = &args[1];
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
    let json = serde_json::Value::Object(json);

    //format json
    let json = serde_json::to_string_pretty(&json).unwrap();
    println!("{}", json);

}
