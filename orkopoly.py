import tkinter as tk
from py.board import Board
from py.game import Game

def start_game():
    player_names = [name_1.get(), name_2.get(), name_3.get(), name_4.get()]
    start_window.destroy()
    game_window = Game(player_names)



start_window = tk.Tk()
start_window.geometry('400x600')
start_window.title("ORKopoly")
start_window.columnconfigure(0, weight=1)

# get the player names
top_label = tk.Label(start_window, text="Enter your names").place(relx=0.5, rely=0.1, anchor=tk.CENTER)

name_1 = tk.StringVar()
label_1 = tk.Label(start_window, text="Player 1:").place(relx=0.35, rely=0.2, anchor=tk.CENTER)
entry_1 = tk.Entry(start_window, textvariable=name_1).place(relx=0.6, rely=0.2, anchor=tk.CENTER)

name_2 = tk.StringVar()
label_2 = tk.Label(start_window, text="Player 2:").place(relx=0.35, rely=0.3, anchor=tk.CENTER)
entry_2 = tk.Entry(start_window, textvariable=name_2).place(relx=0.6, rely=0.3, anchor=tk.CENTER)

name_3 = tk.StringVar()
label_3 = tk.Label(start_window, text="Player 3:").place(relx=0.35, rely=0.4, anchor=tk.CENTER)
entry_3 = tk.Entry(start_window, textvariable=name_3).place(relx=0.6, rely=0.4, anchor=tk.CENTER)

name_4 = tk.StringVar()
label_4 = tk.Label(start_window, text="Player 4:").place(relx=0.35, rely=0.5, anchor=tk.CENTER)
entry_4 = tk.Entry(start_window, textvariable=name_4).place(relx=0.6, rely=0.5, anchor=tk.CENTER)


# start button
start_button = tk.Button(start_window, text="start game", command=start_game).place(relx=0.5, rely=0.6, anchor=tk.CENTER)

start_window.mainloop()




