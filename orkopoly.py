import random
import time
import tkinter as tk
from board import Board


############
### misc ###
############

def make_invisible(widget):
   widget.pack_forget()

def make_visible(widget):
   widget.pack()

def clear_all_widgets():
    make_invisible(info_label)
    make_invisible(roll_button)
    make_invisible(question_label)
    make_invisible(yes_no_frame)
    make_invisible(finish_button)

def set_money_text():
    global player_properties
    global active_player

    money_text.set("Gold: " + str(player_properties["money"][active_player]) + " (+" + str(player_properties["income"][active_player]) + "/turn)\n" \
            + "Stone: " + str(player_properties["stone"][active_player]) + " (+" + str(player_properties["stone_income"][active_player]) + "/turn)\n" \
            + "Energy: " + str(player_properties["used_energy"][active_player]) + " of " + str(player_properties["max_energy"][active_player]) + " used\n" \
            + "Food: " + str(player_properties["used_food"][active_player]) + " of " + str(player_properties["max_food"][active_player]) + " used\n")

def set_top_text():
    global active_player
    global player_names

    top_text.set("Your turn, " + str(player_names[active_player]) + "!")

    # set the color of top_label to the player's color
    top_label["fg"] = board.player_colors[active_player]

###############
### helpers ###
###############

def do_nothing():
    return

def pass_go(player):
    global player_properties

    player_properties["money"][player] += player_properties["income"][player]
    player_properties["stone"][player] += player_properties["stone_income"][player]

    set_money_text()

def kill_player(tenant, owner):
    global player_names
    global ownership
    global player_lives

    # kill tenant
    player_lives[tenant] = 0

    # remove marker from board
    if player_positions[tenant] in [0,9,18,27]:
        board.all_positions[int(player_positions[tenant]+tenant*36)].configure(bg=board.player0_color)
    else:
        board.all_positions[int(player_positions[tenant]+tenant*36)].configure(bg=board.player0_color)

    # delete ownership
    for field in range(len(ownership)):
        if ownership[field] == tenant:
            ownership[field] = -1
            board.all_fields[field]["highlightbackground"] = board.player0_color

    # update GUI
    clear_all_widgets()
    info_text.set("You're out, " + str(player_names[owner]) + " took all your money.")
    make_visible(info_label)
    make_visible(finish_button)

def collect_problems(has_gold, needs_gold, has_stone, needs_stone, has_energy, needs_energy, has_food, needs_food):
    problems = []

    # collect all the missing ressources
    if needs_gold > has_gold:
        problems.append(str(needs_gold-has_gold) + " more Gold")
    if needs_stone > has_stone:
        problems.append(str(needs_stone-has_stone) + " more Stone")
    if needs_energy > has_energy:
        problems.append(str(needs_energy-has_energy) + " more Energy")
    if needs_food > has_food:
        problems.append(str(needs_food-has_food) + " more Food")

    # if all ressources are available, we have no problems
    if len(problems) == 0:
        return ""

    out_string = "Not enough ressources: You need "
    while len(problems) > 0:
        if len(problems) == 1:
            out_string += problems[0] + "."
        elif len(problems) == 2:
            out_string += problems[0] + " and "
        else:
            out_string += problems[0] + ", "
        del problems[0]

    return out_string


###############
### actions ###
###############

def next_player():
    global active_player
    global player_lives

    # disable all upgrade buttons
    for button in board.all_buttons:
        #button["state"] = tk.DISABLED
        button["command"] = do_nothing

    # call the next player
    active_player = (active_player+1) % len(player_lives)

    # check if we are currently skipping our turn
    if player_turns_to_skip[active_player] > 0:
        player_turns_to_skip[active_player] -=1
        next_player()
        return

    # skip dead players
    if player_lives[active_player] == 0:
        next_player()
        return

    # check if game is over
    if sum(player_lives) == 1:
        clear_all_widgets
        make_invisible(top_label)
        make_invisible(money_label)

        winner = player_names[player_lives.index(1)]

        info_text.set(winner + " has won the game!")

        finish_button["text"] = "Close"
        finish_button["command"] = window.destroy
        make_visible(finish_button)

        return

    prepare_rolling()

def prepare_rolling():
    clear_all_widgets()

    set_top_text()
    set_money_text()

    make_visible(info_label)
    info_text.set("Time to roll!")

    make_visible(roll_button)
    roll_button["text"] = "roll"

def move_player():
    global player_positions
    global player_directions
    global player_names
    global active_player
    global rent_prices
    global field_levels

    # hide roll button
    make_invisible(roll_button)

    # move player
    throw = random.randint(1,6)
    old_position = player_positions[active_player]
    new_position = old_position + throw * player_directions[active_player]

    # check if we passed GO
    if new_position >= 36:
        new_position -= 36
        pass_go(active_player)

    # update in our global list
    player_positions[active_player] = new_position

    # change the colors on the board to reflect the moved player
    if old_position in [0,9,18,27]:
        board.all_positions[int(old_position+active_player*36)].configure(bg=board.corner_color)
    else:
        board.all_positions[int(old_position+active_player*36)].configure(bg=board.back_color)
    board.all_positions[int(new_position+active_player*36)].configure(bg=board.player_colors[active_player])

    # roll again, forward
    if new_position == 9:
        make_visible(roll_button)
        roll_button.configure(text="roll again")
        return

    # skip a turn
    if new_position == 18:
        player_turns_to_skip[active_player] = 1

    # roll again, backward
    if new_position == 27:
        player_directions[active_player] = -1
        make_visible(roll_button)
        roll_button.configure(text="roll again")
        return

    make_visible(finish_button)

    # remove all the stuff that (might have) happened because of the corner fields
    player_directions[active_player] = 1
    board.all_positions[9+active_player*36].configure(bg=board.corner_color)
    board.all_positions[27+active_player*36].configure(bg=board.corner_color)

    # next step: see if we need to pay rent
    pay_rent(active_player, new_position)

def pay_rent(tenant, new_position):
    # see if field is a house in the first place
    if board.all_buttons[new_position]['bg'] == board.house_color:
        owner = ownership[new_position]
        if owner != -1 and owner != active_player:
            global player_properties

            # transfer the money; owner gets not more money than tenant has
            rent = rent_prices[field_levels[new_position]]
            player_properties["money"][owner] += min(rent, player_properties["money"][tenant])
            player_properties["money"][tenant] -= rent
            set_money_text()

            # kill the tenant if he cannot pay rent
            if player_properties["money"][tenant] < 0:
                kill_player(tenant, owner)
                return

    set_money_text()

    # next step: check if we can buy the property
    buy_property(tenant, new_position)

def buy_property(active_player, new_position):
    global player_properties
    global ownership

    # corner fields cannot be bought, go directly to updating
    if new_position in [0,9,18,27]:
        ask_for_upgrades()
        return

    # see if you can buy the property
    if ownership[new_position] == -1:
        clear_all_widgets()

        gold_cost  = 1000000000
        stone_cost = 1000000000

        if board.all_buttons[new_position]["bg"] == board.house_color:
            gold_cost = house_prices[0][0]
            stone_cost = house_prices[0][1]
            energy_cost = 1
            food_cost = 1
            income_gain = [house_gain[0], 0, 0, 0]
            question_text.set("Buy this house for " + str(gold_cost) + " Gold and " + str(stone_cost) + " Stone?\n" \
                            + "It will use " + str(energy_cost) + " Energy and " + str(food_cost) + " Food.")
        if board.all_buttons[new_position]["bg"] == board.stone_color:
            gold_cost = quarry_prices[0][0]
            stone_cost = quarry_prices[0][1]
            energy_cost = 1
            food_cost = 0
            income_gain = [0, quarry_gain[0], 0, 0]
            question_text.set("Buy this quarry for " + str(gold_cost) + " Gold and " + str(stone_cost) + " Stone?\n" \
                            + "It will use " + str(energy_cost) + " Energy and " + str(food_cost) + " Food.")
        if board.all_buttons[new_position]["bg"] == board.electr_color:
            gold_cost = powerplant_prices[0][0]
            stone_cost = powerplant_prices[0][1]
            energy_cost = 0
            food_cost = 0
            income_gain = [0, 0, 1, 0]
            question_text.set("Buy this power plant for " + str(gold_cost) + " Gold and " + str(stone_cost) + " Stone?\n" \
                            + "It will use " + str(energy_cost) + " Energy and " + str(food_cost) + " Food.")
        if board.all_buttons[new_position]["bg"] == board.food_color:
            gold_cost = farm_prices[0][0]
            stone_cost = farm_prices[0][1]
            energy_cost = 0
            food_cost = 0
            income_gain = [0, 0, 0, 1]
            question_text.set("Buy this farm for " + str(gold_cost) + " Gold and " + str(stone_cost) + " Stone?\n" \
                            + "It will use " + str(energy_cost) + " Energy and " + str(food_cost) + " Food.")

        make_visible(question_label)

        # check if we have enough ressources
        avai_energy = player_properties["max_energy"][active_player] - player_properties["used_energy"][active_player]
        avai_food = player_properties["max_food"][active_player] - player_properties["used_food"][active_player]
        problem_string = collect_problems(player_properties["money"][active_player], gold_cost, \
                                          player_properties["stone"][active_player], stone_cost, \
                                          avai_energy, energy_cost, avai_food, food_cost)
        if problem_string != "":
            question_text.set(problem_string)
            roll_button["command"] = no_money_to_buy_property
            roll_button["text"] = "OK"
            make_visible(roll_button)
        else:
            yes_button["command"] = lambda: property_bought(new_position, active_player, gold_cost, stone_cost, energy_cost, food_cost, income_gain)
            no_button["command"] = ask_for_upgrades
            make_visible(yes_no_frame)

        make_visible(finish_button)
    else:
        # go directly to upgrading if property cannot be bought
        ask_for_upgrades()

def no_money_to_buy_property():
    ask_for_upgrades()
    return

def property_bought(position, player, gold_cost, stone_cost, energy_cost, food_cost, income_gain):
    # update ressources
    player_properties["money"][active_player] -= gold_cost
    player_properties["stone"][active_player] -= stone_cost
    player_properties["used_energy"][active_player] += energy_cost
    player_properties["used_food"][active_player] += food_cost

    # update income
    player_properties["income"][active_player] += income_gain[0]
    player_properties["stone_income"][active_player] += income_gain[1]
    player_properties["max_energy"][active_player] += income_gain[2]
    player_properties["max_food"][active_player] += income_gain[3]

    # change frame color
    board.all_fields[position]["highlightbackground"] = board.player_colors[player]

    # update ownership
    ownership[position] = player

    # update money_text
    set_money_text()

    # next step: upgrade your properties
    ask_for_upgrades()

def ask_for_upgrades():
    clear_all_widgets()
    info_text.set("Click on the properties you want to upgrade.")

    for position, field in enumerate(board.all_buttons):
        if ownership[position] == active_player:
            board.all_buttons[position]["state"] = tk.NORMAL
            board.all_buttons[position]["command"] = lambda pos=position : upgrade_field(pos)

    make_visible(info_label)
    make_visible(finish_button)

def upgrade_field(position):
    clear_all_widgets()
    make_visible(info_label)

    # get current level
    field_level = field_levels[position]

    if board.all_buttons[position]["bg"] == board.house_color:
        gold_cost = house_prices[field_level+1][0]
        stone_cost = house_prices[field_level+1][1]
        energy_cost = 1
        food_cost = 1
        income_gain = [house_gain[field_level+1], 0, 0, 0]
    if board.all_buttons[position]["bg"] == board.stone_color:
        gold_cost = quarry_prices[field_level+1][0]
        stone_cost = quarry_prices[field_level+1][1]
        energy_cost = 1
        food_cost = 0
        income_gain = [0, quarry_gain[field_level+1], 0, 0]
    if board.all_buttons[position]["bg"] == board.electr_color:
        gold_cost = powerplant_prices[field_level+1][0]
        stone_cost = powerplant_prices[field_level+1][1]
        energy_cost = 0
        food_cost = 0
        income_gain = [0, 0, powerplant_gain[field_level+1], 0]
    if board.all_buttons[position]["bg"] == board.food_color:
        gold_cost = farm_prices[field_level+1][0]
        stone_cost = farm_prices[field_level+1][1]
        energy_cost = 0
        food_cost = 0
        income_gain = [0, 0, 0, food_gain[field_level+1]]

    # check if we have enough ressources
    avai_energy = player_properties["max_energy"][active_player] - player_properties["used_energy"][active_player]
    avai_food = player_properties["max_food"][active_player] - player_properties["used_food"][active_player]
    problem_string = collect_problems(player_properties["money"][active_player], gold_cost, \
                                      player_properties["stone"][active_player], stone_cost, \
                                      avai_energy, energy_cost, avai_food, food_cost)
    if problem_string != '' :
        question_text.set(problem_string)
        make_visible(question_label)
    else:
        question_text.set("Upgrade this field for " + str(gold_cost) + " Gold and " + str(stone_cost) + " Stone?\n" \
                        + "It will use " + str(energy_cost) + " Energy and " + str(food_cost) + " Food.")
        yes_button["command"] = lambda: field_upgraded(position, gold_cost, stone_cost, energy_cost, food_cost, income_gain)
        no_button["command"] = ask_for_upgrades
        make_visible(question_label)
        make_visible(yes_no_frame)

    make_visible(finish_button)

def field_upgraded(position, gold_cost, stone_cost, energy_cost, food_cost, income_gain):
    global player_properties
    global field_levels

    # update ressources
    player_properties["money"][active_player] -= gold_cost
    player_properties["stone"][active_player] -= stone_cost
    player_properties["used_energy"][active_player] += energy_cost
    player_properties["used_food"][active_player] += food_cost

    # update income
    player_properties["income"][active_player] += income_gain[0]
    player_properties["stone_income"][active_player] += income_gain[1]
    player_properties["max_energy"][active_player] += income_gain[2]
    player_properties["max_food"][active_player] += income_gain[3]

    # update level
    field_levels[position] += 1

    # change label on button
    board.all_buttons[position]["text"] = "+" + str(field_levels[position])

    # update money_text
    set_money_text()

    # done with upgrade, maybe we want more
    ask_for_upgrades()

#############################################################################
#############################################################################
#############################################################################

# initialize variables
global player_names
player_names = ["Red", "Blue", "Green", "Black"]
#player_names = ["Red"]
global number_of_players
number_of_players = len(player_names)
global player_positions
player_positions  = [0 for _ in range(number_of_players)]
global player_directions
player_directions = [1 for _ in range(number_of_players)]
global player_turns_to_skip
player_turns_to_skip  = [0 for _ in range(number_of_players)]
global player_properties
player_properties = {"money":[20,20,20,20], "income":[10,10,10,10], "stone":[20,20,20,20], "stone_income":[10,10,10,10], \
                     "used_energy":[0,0,0,0], "max_energy":[5,5,5,5], "used_food":[0,0,0,0], "max_food":[2,2,2,2], \
                     "skip_turn":[0,0,0,0], "move_direction":[1,1,1,1]}
global active_player
active_player = 0
global player_lives
player_lives = [True for _ in range(number_of_players)] # bancrupt players cannot play any more

global ownership
ownership = [-1 for _ in range(36)]
global field_levels
field_levels = [0 for _ in range(36)]

# prices
global rent_prices
rent_prices = [0,10,40,160,640,2560,10240,40960163840,655360,2621440]
global house_prices
house_prices = [[0, 8*pow(3,i)] for i in range(11)]
global quarry_prices
quarry_prices = [[4*pow(3,i), 0] for i in range(11)]
global powerplant_prices
powerplant_prices = [[4*pow(3,i), 4*pow(3,i)] for i in range(11)]
global farm_prices
farm_prices = [[2*pow(3,i), 0] for i in range(11)]

# how much upgrading a field yields
global house_gain
house_gain = [10*pow(2,i) for i in range(11)]
global quarry_gain
quarry_gain = [10*pow(2,i) for i in range(11)]
global powerplant_gain
powerplant_gain = [pow(2,i) for i in range(11)]
global food_gain
food_gain = [pow(2,i) for i in range(11)]

colors={"back_color":'#550055', "player0_color":'#FFFFFF', "player1_color":'#FF0000', "player2_color":'#0000FF', \
        "player3_color":'#008000', "player4_color":'#000000', "house_color":'#00FF00', "stone_color":'#808080', \
        "electr_color":'#FFFF00', "food_color":'#A05000', "corner_color":'#FF8000'}


# test: kill them all
# for position in [1, 5, 10, 12, 14, 16, 19, 21, 23, 25, 28, 30, 32, 34]:
#     ownership[position] = 3
#     field_levels[position] = 6


#########################
### lay out the board ###
#########################

window = tk.Tk()
window.rowconfigure(0, weight=1)
window.columnconfigure((0,1), weight=1)


# board on the right
board = Board(window, colors)
board.grid(row=0, column=1, sticky="wens")


# the control panel on the left
panel = tk.Frame(window)
panel.grid(row=0, column=0, sticky="wens")

# says who's turn it is
top_text = tk.StringVar()
top_label = tk.Label(panel, textvariable=top_text, font=("Arial", 20), pady = 20)
top_label.pack()
set_top_text()

# shows how much money etc player has
money_text = tk.StringVar()
set_money_text()
money_label = tk.Label(panel, textvariable=money_text, font=("Arial", 20), pady = 20 )
money_label.pack()

# give some info about what happens on this field
info_text = tk.StringVar()
info_text.set("Time to roll the die!")
info_label = tk.Label(panel, textvariable=info_text, font=("Arial", 20), pady = 20 )
info_label.pack()

# the single button
roll_button = tk.Button(panel, text="roll", bg=colors["corner_color"], command=move_player, font=("Arial", 20) )
roll_button.pack()

# questions
question_text = tk.StringVar()
question_text.set("Wanna see your money?")
question_label = tk.Label(panel, textvariable=question_text, font=("Arial", 20), pady = 20 )
question_label.pack()

# yes/no button
yes_no_frame = tk.Frame(panel)
yes_no_frame.pack()
yes_button = tk.Button(yes_no_frame, text="Yes", command=lambda: make_visible(money_label), font=("Arial", 20) )
yes_button.grid(row=0, column=0)
no_button = tk.Button(yes_no_frame, text="No", command=lambda: make_invisible(money_label), font=("Arial", 20) )
no_button.grid(row=0, column=1)

# the button at the bottom to finish your turn
finish_button = tk.Button(panel, text="finish turn", command=next_player, font=("Arial", 20) )
finish_button.pack()


# prepare the board for playing
prepare_rolling()
make_invisible(question_label)
make_invisible(yes_no_frame)
make_invisible(finish_button)

window.mainloop()




