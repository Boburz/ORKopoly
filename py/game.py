import random
import tkinter as tk
from py.board import Board
from py.help import Help
from py.costs import Costs


############
### misc ###
############

class Game():
    def __init__(self, names):
        # initialize variables
        self.player_names = [name for name in names]
        self.number_of_players = len(self.player_names)
        self.player_positions  = [0 for _ in range(self.number_of_players)]
        self.player_directions = [1 for _ in range(self.number_of_players)]
        self.player_turns_to_skip  = [0 for _ in range(self.number_of_players)]
        self.player_properties = {"money":[20,20,20,20], "income":[10,10,10,10], "stone":[20,20,20,20], "stone_income":[10,10,10,10], \
                                  "used_energy":[0,0,0,0], "max_energy":[5,5,5,5], "used_food":[0,0,0,0], "max_food":[2,2,2,2], \
                                  "skip_turn":[0,0,0,0], "move_direction":[1,1,1,1]}
        self.active_player = 0
        self.player_lives = [True for _ in range(self.number_of_players)] # bancrupt players cannot play any more

        self.ownership = [-1 for _ in range(36)]
        self.field_levels = [0 for _ in range(36)]

        # prices
        self.rent_prices = [0,10,40,160,640,2560,10240,40960,163840,655360,2621440]
        self.house_prices = [[0, 8*pow(3,i)] for i in range(11)]
        self.quarry_prices = [[4*pow(3,i), 0] for i in range(11)]
        self.powerplant_prices = [[4*pow(3,i), 4*pow(3,i)] for i in range(11)]
        self.farm_prices = [[2*pow(3,i), 0] for i in range(11)]

        # how much upgrading a field yields
        self.house_gain = [10*pow(2,i) for i in range(11)]
        self.quarry_gain = [10*pow(2,i) for i in range(11)]
        self.powerplant_gain = [pow(2,i) for i in range(11)]
        self.food_gain = [pow(2,i) for i in range(11)]

        self.colors={"back_color":'#DDBB99', "player0_color":'#FFFFFF', "player1_color":'#FF0000', "player2_color":'#0000FF', \
                     "player3_color":'#008000', "player4_color":'#000000', "house_color":'#00FF00', "stone_color":'#808080', \
                     "electr_color":'#FFFF00', "food_color":'#A05000', "corner_color":'#FF8000'}


        # build the window
        self.window = tk.Tk()
        self.window.geometry('850x600')
        self.window.title("ORKopoly")
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure((0,1), weight=1)

        # board on the right
        self.board = Board(self.window, self.colors)
        self.board.grid(row=0, column=1, sticky="wens")

        # the control panel on the left
        self.panel = tk.Frame(self.window, bg=self.colors["back_color"])
        self.panel.grid(row=0, column=0, sticky="wens")

        # the buttons to get help
        self.help_frame = tk.Frame(self.panel)
        self.help_frame.pack(pady=20)
        self.rules_button = tk.Button(self.help_frame, text="help", command=self.open_help, font=("Arial", 20), bg=self.colors["corner_color"])
        self.rules_button.grid(row=0, column=0)
        self.numbers_button = tk.Button(self.help_frame, text="numbers", command=self.open_numbers, font=("Arial", 20), bg=self.colors["corner_color"])
        self.numbers_button.grid(row=0, column=1)

        # says who's turn it is
        self.top_text = tk.StringVar()
        self.top_label = tk.Label(self.panel, textvariable=self.top_text, font=("Arial", 20), pady = 20, bg=self.colors["back_color"])
        self.top_label.pack()
        self.set_top_text()

        # shows how much money etc player has
        self.money_text = tk.StringVar()
        self.set_money_text()
        self.money_label = tk.Label(self.panel, textvariable=self.money_text, font=("Arial", 20), pady = 20, bg=self.colors["back_color"])
        self.money_label.pack()

        # give some info about what happens on this field
        self.info_text = tk.StringVar()
        self.info_text.set("Time to roll the die!")
        self.info_label = tk.Label(self.panel, textvariable=self.info_text, font=("Arial", 20), pady = 20, bg=self.colors["back_color"])
        self.info_label.pack()

        # the single button
        self.roll_button = tk.Button(self.panel, text="roll", command=self.move_player, font=("Arial", 20), bg=self.colors["corner_color"])
        self.roll_button.pack()

        # questions
        self.question_text = tk.StringVar()
        self.question_label = tk.Label(self.panel, textvariable=self.question_text, font=("Arial", 20), pady = 20, bg=self.colors["back_color"])
        self.question_label.pack()

        # yes/no button
        self.yes_no_frame = tk.Frame(self.panel)
        self.yes_no_frame.pack()
        self.yes_button = tk.Button(self.yes_no_frame, text="Yes", command=lambda: self.make_visible(self.money_label), font=("Arial", 20), bg=self.colors["corner_color"])
        self.yes_button.grid(row=0, column=0)
        self.no_button = tk.Button(self.yes_no_frame, text="No", command=lambda: self.make_invisible(self.money_label), font=("Arial", 20), bg=self.colors["corner_color"])
        self.no_button.grid(row=0, column=1)

        # finish button
        self.finish_frame = tk.Frame(self.panel, bg=self.colors["back_color"])
        self.finish_frame.pack(pady=20)
        self.finish_button = tk.Button(self.finish_frame, text="finish turn", command=self.next_player, font=("Arial", 20), bg=self.colors["corner_color"])
        self.finish_button.pack()


        # test: kill them all
#         for field in [1,5,10,12,14,16,19,21,23,25,28,30,32,34]:
#             self.ownership[field] = 3
#             self.field_levels[field] = 4
#             self.board.all_fields[field]["highlightbackground"] = self.colors["player4_color"]
#             self.field_upgraded(field, 0, 0, 0, 0, [self.house_gain[5],0,0,0])

        # remove all players without a name
        for index, name in enumerate(self.player_names):
            if name == "":
                self.kill_player(index, index)


        # prepare the board for playing
        self.prepare_rolling()
        self.make_invisible(self.question_label)
        self.make_invisible(self.yes_no_frame)
        self.make_invisible(self.finish_frame)


        self.window.mainloop()


    ###############
    ### helpers ###
    ###############

    def open_help(self):
        help_window = Help()

    def open_numbers(self):
        costs_window = Costs(self.house_prices, self.quarry_prices, self.powerplant_prices, self.farm_prices, self.house_gain, self.quarry_gain, self.powerplant_gain, self.food_gain, self.rent_prices)

    def make_invisible(self, widget):
        widget.pack_forget()
        return

    def make_visible(self, widget):
        if widget == self.finish_frame:
            widget.pack(pady=20)
        else:
            widget.pack()
        return

    def clear_all_widgets(self):
        self.make_invisible(self.info_label)
        self.make_invisible(self.roll_button)
        self.make_invisible(self.question_label)
        self.make_invisible(self.yes_no_frame)
        self.make_invisible(self.finish_frame)
        return

    def set_money_text(self):
        self.money_text.set("Gold: " + str(self.player_properties["money"][self.active_player]) \
                          + " (+" + str(self.player_properties["income"][self.active_player]) + "/turn)\n" \
                          + "Stone: " + str(self.player_properties["stone"][self.active_player]) + " (+" \
                          + str(self.player_properties["stone_income"][self.active_player]) + "/turn)\n" \
                          + "Energy: " + str(self.player_properties["used_energy"][self.active_player]) + " of " \
                          + str(self.player_properties["max_energy"][self.active_player]) + " used\n" \
                          + "Food: " + str(self.player_properties["used_food"][self.active_player]) + " of " \
                          + str(self.player_properties["max_food"][self.active_player]) + " used\n")
        return

    def set_top_text(self):
        self.top_text.set("Your turn, " + str(self.player_names[self.active_player]) + "!")

        # set the color of top_label to the player's color
        self.top_label["fg"] = self.board.player_colors[self.active_player]

        return

    def do_nothing(self):
        return

    def pass_go(self, player):
        self.player_properties["money"][player] += self.player_properties["income"][player]
        self.player_properties["stone"][player] += self.player_properties["stone_income"][player]

        self.set_money_text()

        return

    def kill_player(self, tenant, owner):
        # kill tenant
        self.player_lives[tenant] = 0

        # remove marker from board
        if self.player_positions[tenant] in [0,9,18,27]:
            self.board.all_positions[int(self.player_positions[tenant]+tenant*36)].configure(bg=self.board.corner_color)
        else:
            self.board.all_positions[int(self.player_positions[tenant]+tenant*36)].configure(bg=self.board.player0_color)

        # delete ownership
        for field in range(len(self.ownership)):
            if self.ownership[field] == tenant:
                self.ownership[field] = -1
                self.board.all_fields[field]["highlightbackground"] = self.board.player0_color
                self.field_levels[field] = 0
                self.board.all_buttons[field]["text"] = ""

        # update GUI
        self.clear_all_widgets()
        self.info_text.set("You're out, " + str(self.player_names[owner]) + " took all your money.")
        self.make_visible(self.info_label)
        self.make_visible(self.finish_frame)

        return

    def collect_problems(self, has_gold, needs_gold, has_stone, needs_stone, has_energy, needs_energy, has_food, needs_food):
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

        out_string = "Not enough ressources: You need\n"
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

    def next_player(self):
        # disable all upgrade buttons
        for button in self.board.all_buttons:
            button["command"] = self.do_nothing

        # call the next player
        self.active_player = (self.active_player+1) % len(self.player_lives)

        # test
        print("Now giving dice to player " + self.player_names[self.active_player])

        # check if we are currently skipping our turn
        if self.player_turns_to_skip[self.active_player] > 0:

            # test
            print(self.player_names[self.active_player] + "needs to skip a turn")

            self.player_turns_to_skip[self.active_player] -=1
            self.next_player()
            return

        # skip dead players
        if self.player_lives[self.active_player] == 0:
            self.next_player()
            return

        # check if game is over
        if sum(self.player_lives) == 1:
            self.clear_all_widgets()
            self.make_invisible(self.top_label)
            self.make_invisible(self.money_label)

            winner = self.player_names[self.player_lives.index(1)]

            self.info_text.set(winner + " has won the game!")

            self.finish_frame["text"] = "Close"
            self.finish_frame["command"] = self.window.destroy
            self.make_visible(self.finish_frame)

            return

        self.prepare_rolling()
        return

    def prepare_rolling(self):
        self.clear_all_widgets()
        self.set_top_text()
        self.set_money_text()

        self.make_visible(self.info_label)
        self.info_text.set("Time to roll!")

        self.make_visible(self.roll_button)
        self.roll_button["text"] = "roll"
        self.roll_button["command"] = self.move_player

        return

    def move_player(self):
        # hide roll button
        self.make_invisible(self.roll_button)

        # move player
        throw = random.randint(1,6)
        old_position = self.player_positions[self.active_player]
        new_position = old_position + throw * self.player_directions[self.active_player]

        # check if we passed GO
        if new_position >= 36:
            new_position -= 36
            self.pass_go(self.active_player)

        # update in our global list
        self.player_positions[self.active_player] = new_position

        # change the colors on the board to reflect the moved player
        if old_position in [0,9,18,27]:
            self.board.all_positions[int(old_position+self.active_player*36)].configure(bg=self.board.corner_color)
        else:
            self.board.all_positions[int(old_position+self.active_player*36)].configure(bg=self.board.back_color)
        self.board.all_positions[int(new_position+self.active_player*36)].configure(bg=self.board.player_colors[self.active_player])

        # roll again, forward
        if new_position == 9:
            self.make_visible(self.roll_button)
            self.roll_button.configure(text="roll again")
            return

        # skip a turn
        if new_position == 18:
            self.player_turns_to_skip[self.active_player] = 1

        # roll again, backward
        if new_position == 27:
            self.player_directions[self.active_player] = -1
            self.make_visible(self.roll_button)
            self.roll_button.configure(text="roll again")
            return

        self.make_visible(self.finish_frame)

        # remove all the stuff that (might have) happened because of the corner fields
        self.player_directions[self.active_player] = 1
        self.board.all_positions[ 9+self.active_player*36].configure(bg=self.board.corner_color)
        self.board.all_positions[27+self.active_player*36].configure(bg=self.board.corner_color)

        # next step: see if we need to pay rent
        self.pay_rent(new_position)
        return

    def pay_rent(self, new_position):
        tenant = self.active_player

        # see if field is a house in the first place
        if self.board.all_buttons[new_position]['bg'] == self.board.house_color:
            owner = self.ownership[new_position]
            if owner != -1 and owner != tenant:
                # transfer the money; owner gets not more money than tenant has
                rent = self.rent_prices[self.field_levels[new_position]]
                self.player_properties["money"][owner] += min(rent, self.player_properties["money"][tenant])
                self.player_properties["money"][tenant] -= rent
                self.set_money_text()

                # kill the tenant if he cannot pay rent
                if self.player_properties["money"][tenant] < 0:
                    self.kill_player(tenant, owner)
                    return

        self.set_money_text()

        # next step: check if we can buy the property
        self.buy_property(new_position)
        return

    def buy_property(self, new_position):
        # corner fields cannot be bought, go directly to updating
        if new_position in [0,9,18,27]:
            self.ask_for_upgrades()
            return

        # see if you can buy the property
        if self.ownership[new_position] == -1:
            self.clear_all_widgets()

            gold_cost  = 1000000000
            stone_cost = 1000000000

            if self.board.all_buttons[new_position]["bg"] == self.board.house_color:
                gold_cost = self.house_prices[0][0]
                stone_cost = self.house_prices[0][1]
                energy_cost = 1
                food_cost = 1
                income_gain = [self.house_gain[0], 0, 0, 0]
                self.question_text.set("Buy this house for " + str(gold_cost) + " Gold and " + str(stone_cost) + " Stone?\n" \
                            + "It will use " + str(energy_cost) + " Energy and " + str(food_cost) + " Food.")
            if self.board.all_buttons[new_position]["bg"] == self.board.stone_color:
                gold_cost = self.quarry_prices[0][0]
                stone_cost = self.quarry_prices[0][1]
                energy_cost = 1
                food_cost = 0
                income_gain = [0, self.quarry_gain[0], 0, 0]
                self.question_text.set("Buy this quarry for " + str(gold_cost) + " Gold and " + str(stone_cost) + " Stone?\n" \
                            + "It will use " + str(energy_cost) + " Energy and " + str(food_cost) + " Food.")
            if self.board.all_buttons[new_position]["bg"] == self.board.electr_color:
                gold_cost = self.powerplant_prices[0][0]
                stone_cost = self.powerplant_prices[0][1]
                energy_cost = 0
                food_cost = 0
                income_gain = [0, 0, self.powerplant_gain[0], 0]
                self.question_text.set("Buy this power plant for " + str(gold_cost) + " Gold and " + str(stone_cost) + " Stone?\n" \
                            + "It will use " + str(energy_cost) + " Energy and " + str(food_cost) + " Food.")
            if self.board.all_buttons[new_position]["bg"] == self.board.food_color:
                gold_cost = self.farm_prices[0][0]
                stone_cost = self.farm_prices[0][1]
                energy_cost = 0
                food_cost = 0
                income_gain = [0, 0, 0, self.food_gain[0]]
                self.question_text.set("Buy this farm for " + str(gold_cost) + " Gold and " + str(stone_cost) + " Stone?\n" \
                            + "It will use " + str(energy_cost) + " Energy and " + str(food_cost) + " Food.")

            self.make_visible(self.question_label)

            # check if we have enough ressources
            avai_energy = self.player_properties["max_energy"][self.active_player] - self.player_properties["used_energy"][self.active_player]
            avai_food = self.player_properties["max_food"][self.active_player] - self.player_properties["used_food"][self.active_player]
            problem_string = self.collect_problems(self.player_properties["money"][self.active_player], gold_cost, \
                                                   self.player_properties["stone"][self.active_player], stone_cost, \
                                                   avai_energy, energy_cost, avai_food, food_cost)
            if problem_string != "":
                self.question_text.set(problem_string)
                self.roll_button["command"] = self.no_money_to_buy_property
                self.roll_button["text"] = "OK"
                self.make_visible(self.roll_button)
            else:
                self.yes_button["command"] = lambda: self.property_bought(new_position, self.active_player, gold_cost, stone_cost, energy_cost, food_cost, income_gain)
                self.no_button["command"] = self.ask_for_upgrades
                self.make_visible(self.yes_no_frame)

            self.make_visible(self.finish_frame)
        else:
            # go directly to upgrading if property cannot be bought
            self.ask_for_upgrades()

        return

    def no_money_to_buy_property(self):
        self.ask_for_upgrades()
        return

    def property_bought(self, position, player, gold_cost, stone_cost, energy_cost, food_cost, income_gain):
        # update ressources
        self.player_properties["money"][self.active_player] -= gold_cost
        self.player_properties["stone"][self.active_player] -= stone_cost
        self.player_properties["used_energy"][self.active_player] += energy_cost
        self.player_properties["used_food"][self.active_player] += food_cost

        # update income
        self.player_properties["income"][self.active_player] += income_gain[0]
        self.player_properties["stone_income"][self.active_player] += income_gain[1]
        self.player_properties["max_energy"][self.active_player] += income_gain[2]
        self.player_properties["max_food"][self.active_player] += income_gain[3]

        # change frame color
        self.board.all_fields[position]["highlightbackground"] = self.board.player_colors[player]

        # update ownership
        self.ownership[position] = player

        # update money_text
        self.set_money_text()

        # next step: upgrade your properties
        self.ask_for_upgrades()

        return

    def ask_for_upgrades(self):
        self.clear_all_widgets()
        self.info_text.set("Click on the properties you want to upgrade.")

        for position, field in enumerate(self.board.all_buttons):
            if self.ownership[position] == self.active_player:
                self.board.all_buttons[position]["state"] = tk.NORMAL
                self.board.all_buttons[position]["command"] = lambda pos=position : self.upgrade_field(pos)

        self.make_visible(self.info_label)
        self.make_visible(self.finish_frame)

    def upgrade_field(self, position):
        self.clear_all_widgets()
        self.make_visible(self.info_label)

        # get current level
        field_level = self.field_levels[position]

        if self.board.all_buttons[position]["bg"] == self.board.house_color:
            gold_cost = self.house_prices[field_level+1][0]
            stone_cost = self.house_prices[field_level+1][1]
            energy_cost = 1
            food_cost = 1
            income_gain = [self.house_gain[field_level+1], 0, 0, 0]
        if self.board.all_buttons[position]["bg"] == self.board.stone_color:
            gold_cost = self.quarry_prices[field_level+1][0]
            stone_cost = self.quarry_prices[field_level+1][1]
            energy_cost = 1
            food_cost = 0
            income_gain = [0, self.quarry_gain[field_level+1], 0, 0]
        if self.board.all_buttons[position]["bg"] == self.board.electr_color:
            gold_cost = self.powerplant_prices[field_level+1][0]
            stone_cost = self.powerplant_prices[field_level+1][1]
            energy_cost = 0
            food_cost = 0
            income_gain = [0, 0, self.powerplant_gain[field_level+1], 0]
        if self.board.all_buttons[position]["bg"] == self.board.food_color:
            gold_cost = self.farm_prices[field_level+1][0]
            stone_cost = self.farm_prices[field_level+1][1]
            energy_cost = 0
            food_cost = 0
            income_gain = [0, 0, 0, self.food_gain[field_level+1]]

        # check if we have enough ressources
        avai_energy = self.player_properties["max_energy"][self.active_player] - self.player_properties["used_energy"][self.active_player]
        avai_food = self.player_properties["max_food"][self.active_player] - self.player_properties["used_food"][self.active_player]
        problem_string = self.collect_problems(self.player_properties["money"][self.active_player], gold_cost, \
                                               self.player_properties["stone"][self.active_player], stone_cost, \
                                               avai_energy, energy_cost, avai_food, food_cost)
        if problem_string != '' :
            self.question_text.set(problem_string)
            self.make_visible(self.question_label)
        else:
            self.question_text.set("Upgrade this field for " + str(gold_cost) + " Gold and " + str(stone_cost) + " Stone?\n" \
                                 + "It will use " + str(energy_cost) + " Energy and " + str(food_cost) + " Food.")
            self.yes_button["command"] = lambda: self.field_upgraded(position, gold_cost, stone_cost, energy_cost, food_cost, income_gain)
            self.no_button["command"] = self.ask_for_upgrades
            self.make_visible(self.question_label)
            self.make_visible(self.yes_no_frame)

        self.make_visible(self.finish_frame)

        return

    def field_upgraded(self, position, gold_cost, stone_cost, energy_cost, food_cost, income_gain):
        # update ressources
        self.player_properties["money"][self.active_player] -= gold_cost
        self.player_properties["stone"][self.active_player] -= stone_cost
        self.player_properties["used_energy"][self.active_player] += energy_cost
        self.player_properties["used_food"][self.active_player] += food_cost

        # update income
        self.player_properties["income"][self.active_player] += income_gain[0]
        self.player_properties["stone_income"][self.active_player] += income_gain[1]
        self.player_properties["max_energy"][self.active_player] += income_gain[2]
        self.player_properties["max_food"][self.active_player] += income_gain[3]

        # update level
        self.field_levels[position] += 1

        # change label on button
        self.board.all_buttons[position]["text"] = "+" + str(self.field_levels[position])

        # update money_text
        self.set_money_text()

        # done with upgrade, maybe we want more
        self.ask_for_upgrades()

        return




