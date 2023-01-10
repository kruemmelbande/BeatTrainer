import tkinter as tk
from tkinter import filedialog
from beatTrainerCore import loadbeatmap, convertLoaded, getLoadedDifficulties, clearLoaded

def on_load_button_click():
    filepath = filedialog.askdirectory()
    loadbeatmap(filepath)
    difficulties = getLoadedDifficulties()
    difficulty_var.set(difficulties[0])
    difficulty_menu['menu'].delete(0, 'end')
    for difficulty in difficulties:
        difficulty_menu['menu'].add_command(label=difficulty, command=lambda val=difficulty: difficulty_var.set(val))

        convert_button['state'] = 'normal'
        clear_button['state'] = 'normal'

def on_convert_button_click():
    difficulty = difficulty_var.get()
    save_location = filedialog.askdirectory()
    convertLoaded(difficulty, save_location)

def on_clear_button_click():
    clearLoaded()
    difficulty_var.set('')
    difficulty_menu['values'] = []
    convert_button['state'] = 'disable'
    clear_button['state'] = 'disable'

root = tk.Tk()
root.title("Beat3 Training Map Converter")
root.geometry("800x600")

load_button = tk.Button(root, text="Load Beatmap", command=on_load_button_click)
load_button.pack()

difficulty_var = tk.StringVar(value='')
difficulty_menu = tk.OptionMenu(root, difficulty_var, [])
difficulty_menu.pack()

convert_button = tk.Button(root, text="Convert", command=on_convert_button_click)
convert_button.pack()
convert_button['state'] = 'disable'

clear_button = tk.Button(root, text="Clear", command=on_clear_button_click)
clear_button.pack()
clear_button['state'] = 'disable'

root.mainloop()
