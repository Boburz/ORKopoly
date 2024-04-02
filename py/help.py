import tkinter as tk

class Help:
    def __init__(self):
        root = tk.Tk()
        #root.title("Help")
        v = tk.Scrollbar(root)
        v.pack(side = tk.RIGHT, fill = tk.Y)

        help_text = tk.Text(root, width = 72, height = 15, wrap = tk.NONE, yscrollcommand = v.set)
        help_text.insert(tk.END,
          "\n How to play\n\n"
        + " You can think of this game as a combination between Monopoly and a\n"
        + " simple economy simulator: All players take turns rolling dice and\n"
        + " move their playing pieces accordingly. Apart from the self-explaining\n"
        + " corner fields, you can land on one of four different kinds of fields:\n"
        + " Houses (green) produce Gold, Quarries (grey) produce Stone, Power\n"
        + " Plants (yellow) produce Electricity, and Farms (brown) produce Food.\n"
        + " While Gold and Stone are disbursed each time you pass GO, Electricity\n"
        + " and Food are a requirement to buy and upgrade your buildings.\n\n\n"
        + " How do I progress?\n\n"
        + " Try to buy as many fields as possible to boost your production. But\n"
        + " be careful: Houses and Quarries comsume Electricity and Houses\n"
        + " additionally consume Food. So don't forget to upgrade your Power\n"
        + " Plants and Farms! The price for upgrading any of the four different\n"
        + " fields triples with every level, while the production boost only\n"
        + " doubles.\n\n\n"
        + " How do I win?\n\n"
        + " To win, you need to eliminate all the other players. This is done by\n"
        + " upgrading your Houses, as landing on a different player's House\n"
        + " warrants rent. Without any improvements, the rent is free; landing\n"
        + " on a house of level \"+1\" costs 10 Gold. From there, the rent\n"
        + " quadruples with every level.\n\n\n"
        + " Got any tips?\n\n"
        + " You cannot sell any of the fields or improvements you made in the\n"
        + " past, so it is strongly advised to always carry enough Gold with you\n"
        + " on your journeys. Try to upgrade your Quarries in the last turn\n"
        + " before passing GO. This way, you are less vulnerable against your\n"
        + " rivals' exorbitant rent prices, while still getting a boost in Stone\n"
        + " production when you pass GO in the next turn.")
        help_text.pack(side=tk.TOP, fill=tk.X)

        v.config(command=help_text.yview)

        root.title("Help")
        root.resizable(False,False)
        root.mainloop()

# for testing
#test = Help()
