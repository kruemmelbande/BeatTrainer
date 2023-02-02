use std::process::exit;
fn main() {
    let args: Vec<String> = std::env::args().collect();
    let folder_location = &args[1];
    let folder = std::fs::read_dir(folder_location).unwrap();
    let mut info_path = String::new();
    println!("The folder {} the following files:", 
    folder_location);
    let mut is_valid_map = false;
    for file in folder{
        let file_name = file.unwrap().path().display().to_string();
        print!("{}", file_name);
        if file_name.ends_with("Info.dat") {
            is_valid_map = true;
            info_path = file_name.to_string();
            //println!("info_path: {}", info_path);
            print!("\t\t<- map info")
        }
        println!();

    }


    if !is_valid_map {
        println!("The folder {} does not contain a valid map", folder_location);
        exit(1);
    }

    let info= std::fs::read_to_string(info_path).unwrap();
    println!("{}", info);
    //load info as json
    let info_json: serde_json::Value = serde_json::from_str(&info).unwrap();
    println!("{}", info_json["name"]);
}
