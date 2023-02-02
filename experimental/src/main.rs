fn main() {
    let args: Vec<String> = std::env::args().collect();
    let folder_location = &args[1];
    let folder = std::fs::read_dir(folder_location).unwrap();
    println!("The folder {} the following files:", folder_location);
    for file in folder {
        println!("{}", file.unwrap().path().display());
    }
}
