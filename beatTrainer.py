import tkinter as tk
from tkinter import filedialog
from beatTrainerCore import loadbeatmap, convertLoaded, getLoadedDifficulties, clearLoaded, getBeatmapName, getThumbnail, get_current_file_path, isUpdated, saveUpdated
from beatPlayer import play

def playBeatmap():
    play(get_current_file_path(), difficulty=difficulty_var.get())

def on_load_button_click():
    global img_label
    filepath = filedialog.askdirectory()
    load_result = loadbeatmap(filepath)
    
    if load_result == 0:
        name = getBeatmapName()
        beatmap_label.config(text=name)
        difficulties = getLoadedDifficulties()
        difficulty_var.set(difficulties[0])
        difficulty_menu['menu'].delete(0, 'end')
        for difficulty in difficulties:
            difficulty_menu['menu'].add_command(label=difficulty, command=tk._setit(difficulty_var, difficulty))

        convert_button['state'] = 'normal'
        clear_button['state'] = 'normal'
        play_button['state'] = 'normal'
        img = getThumbnail()
        #show the image
        img_label = tk.Label(root, image=img)
        img_label.image = img
        img_label.grid(row=0, column=1, sticky='W')
        if isUpdated():
            update_button['state'] = 'normal'
        else:
            update_button['state'] = 'disable'



def on_convert_button_click():
    beatmap_label.config(text="Converting...")
    root.update()
    difficulty = difficulty_var.get()
    save_location = filedialog.askdirectory()
    conversion_result = convertLoaded(difficulty, save_location)
    if conversion_result == 0:
        beatmap_label.config(text="Conversion Successful!")
    else:
        beatmap_label.config(text="Conversion Failed!")

def on_clear_button_click():
    clearLoaded()
    difficulty_var.set('')
    difficulty_menu['menu'].delete(0, 'end')
    convert_button['state'] = 'disable'
    clear_button['state'] = 'disable'
    play_button['state'] = 'disable'
    update_button['state'] = 'disable'
    beatmap_label.config(text="No beatmap loaded")
    img_label.image = None

def on_update_button_click():
    #get file path for update
    filepath=filedialog.askdirectory()
    saveUpdated(filepath)
    

root = tk.Tk()
root.title("BeatTrainer")
root.geometry("300x300")
root.resizable(False, False)
root.columnconfigure(0, minsize=50, pad=10)
root.rowconfigure(0, minsize=50, pad=10)
load_button = tk.Button(root, text="Load Beatmap", command=on_load_button_click)
load_button.grid(row=0, column=0, sticky='W')

beatmap_label = tk.Label(root, text="No beatmap loaded")
beatmap_label.grid(row=1, column=1, sticky='W')

difficulty_var = tk.StringVar(value='')
difficulty_menu = tk.OptionMenu(root, difficulty_var, [])
difficulty_menu.grid(row=1, column=0, sticky='W')

convert_button = tk.Button(root, text="Convert", command=on_convert_button_click)
convert_button.grid(row=3, column=0, sticky='W')
convert_button['state'] = 'disable'

clear_button = tk.Button(root, text="Clear", command=on_clear_button_click)
clear_button.grid(row=4, column=0,sticky='W')
clear_button['state'] = 'disable'

play_button = tk.Button(root, text="Preview Beatmap", command=playBeatmap)
play_button.grid(row=5, column=0,sticky='W')
play_button['state'] = 'disable'

update_button = tk.Button(root, text="Update", command=on_update_button_click)
update_button.grid(row=6, column=0,sticky='W')
update_button['state'] = 'disable'

root.mainloop()
