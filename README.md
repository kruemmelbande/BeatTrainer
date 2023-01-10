# BeatTrainer
A a visualizer for beatsaber maps, that can also convert a beatmap to train one hand individually.  
Please note that the exe uses pyinstaller which can at times cause false positives in av engines.

Noodle and chroma maps might load, but no chroma or noodle features are supported.
## Installation

If you are cloning this repository, install the dependencies with `pip install -r requirements.txt`
The executable from the releases tab should in theory include all dependencies.
## Usage

Either clone this repository and run `python main.py` or download the latest release from the releases tab and run the executable (it might not be up to date).

Then just load a beatmap through the gui, choose your difficulty and either export it to a new beatmap for training, or preview the current map.

## Building an exe

Clone this repository, and download the dependencies.  
Additionally you will need to download pyinstaller with `pip install pyinstaller`
Afterwards you can build the exe with `pyinstaller --windowed --onefile beatTrainer.py`