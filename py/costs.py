import tkinter as tk

class Costs:
    def __init__(self, house_prices, quarry_prices, powerplant_prices, farm_prices, house_gain, quarry_gain, powerplant_gain, food_gain, rent_prices):
        #super().__init__()

        # set variables
        self.house_prices = house_prices
        self.quarry_prices = quarry_prices
        self.powerplant_prices = powerplant_prices
        self.farm_prices = farm_prices
        self.house_gain = house_gain
        self.quarry_gain = quarry_gain
        self.powerplant_gain = powerplant_gain
        self.food_gain = food_gain
        self.rent_prices = rent_prices

        ####################
        # build the window #
        ####################

        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.title("Cost Overview")

        self.building_number = 0

        # top frame to switch between the different buildings
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack()

        self.left_button = tk.Button(self.top_frame, text="<", command=self.switch_left)
        self.left_button.grid(row=0, column=0)

        self.building_label = tk.Label(self.top_frame, text="house")
        self.building_label.grid(row=0, column=1)

        self.right_button = tk.Button(self.top_frame, text=">", command=self.switch_right)
        self.right_button.grid(row=0, column=2)

        # main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()


        # build the table
        self.update_table()

        self.root.mainloop()

    def switch_left(self):
        self.building_number = (self.building_number - 1) % 4
        self.update_table()
        return

    def switch_right(self):
        self.building_number = (self.building_number + 1) % 4
        self.update_table()
        return

    def update_table(self):
        total_gain_number = 0

        # remove the old numbers
        for widgets in self.main_frame.winfo_children():
            widgets.destroy()

        # captions
        self.level        = tk.Label(self.main_frame, text="level").grid(row=0, column=0)
        self.gold         = tk.Label(self.main_frame, text="Gold").grid(row=0, column=1)
        self.stone        = tk.Label(self.main_frame, text="Stone").grid(row=0, column=2)
        self.empty        = tk.Label(self.main_frame, text="  ").grid(row=0, column=3)
        self.income_gain  = tk.Label(self.main_frame, text="income gain").grid(row=0, column=4)
        self.total_income = tk.Label(self.main_frame, text="total income").grid(row=0, column=5)
        self.rent_label   = tk.Label(self.main_frame, text="rent").grid(row=0, column=6)


        if self.building_number == 0:
            # update building name
            self.building_label.grid_remove()
            self.building_label = tk.Label(self.top_frame, text="house")
            self.building_label.grid(row=0, column=1)

            for i in range(len(self.house_prices)):
                tk.Label(self.main_frame, text=str(i)).grid(row=i+1, column=0)
                tk.Label(self.main_frame, text=str(self.house_prices[i][0])).grid(row=i+1, column=1)
                tk.Label(self.main_frame, text=str(self.house_prices[i][1])).grid(row=i+1, column=2)
                tk.Label(self.main_frame, text=str(self.house_gain[i])).grid(row=i+1, column=4)
                total_gain_number += self.house_gain[i]
                tk.Label(self.main_frame, text=str(total_gain_number)).grid(row=i+1, column=5)
                tk.Label(self.main_frame, text=str(self.rent_prices[i])).grid(row=i+1, column=6)

        elif self.building_number == 1:
            # update building name
            self.building_label.grid_remove()
            self.building_label = tk.Label(self.top_frame, text="quarry")
            self.building_label.grid(row=0, column=1)

            for i in range(len(self.quarry_prices)):
                tk.Label(self.main_frame, text=str(i)).grid(row=i+1, column=0)
                tk.Label(self.main_frame, text=str(self.quarry_prices[i][0])).grid(row=i+1, column=1)
                tk.Label(self.main_frame, text=str(self.quarry_prices[i][1])).grid(row=i+1, column=2)
                tk.Label(self.main_frame, text=str(self.quarry_gain[i])).grid(row=i+1, column=4)
                total_gain_number += self.quarry_gain[i]
                tk.Label(self.main_frame, text=str(total_gain_number)).grid(row=i+1, column=5)
                tk.Label(self.main_frame, text="-").grid(row=i+1, column=6)
        elif self.building_number == 2:
            # update building name
            self.building_label.grid_remove()
            self.building_label = tk.Label(self.top_frame, text="power plant")
            self.building_label.grid(row=0, column=1)

            for i in range(len(self.powerplant_prices)):
                tk.Label(self.main_frame, text=str(i)).grid(row=i+1, column=0)
                tk.Label(self.main_frame, text=str(self.powerplant_prices[i][0])).grid(row=i+1, column=1)
                tk.Label(self.main_frame, text=str(self.powerplant_prices[i][1])).grid(row=i+1, column=2)
                tk.Label(self.main_frame, text=str(self.powerplant_gain[i])).grid(row=i+1, column=4)
                total_gain_number += self.powerplant_gain[i]
                tk.Label(self.main_frame, text=str(total_gain_number)).grid(row=i+1, column=5)
                tk.Label(self.main_frame, text="-").grid(row=i+1, column=6)
        else:
            # update building name
            self.building_label.grid_remove()
            self.building_label = tk.Label(self.top_frame, text="farm")
            self.building_label.grid(row=0, column=1)

            for i in range(len(self.farm_prices)):
                tk.Label(self.main_frame, text=str(i)).grid(row=i+1, column=0)
                tk.Label(self.main_frame, text=str(self.farm_prices[i][0])).grid(row=i+1, column=1)
                tk.Label(self.main_frame, text=str(self.farm_prices[i][1])).grid(row=i+1, column=2)
                tk.Label(self.main_frame, text=str(self.food_gain[i])).grid(row=i+1, column=4)
                total_gain_number += self.food_gain[i]
                tk.Label(self.main_frame, text=str(total_gain_number)).grid(row=i+1, column=5)
                tk.Label(self.main_frame, text="-").grid(row=i+1, column=6)

        return

# for testing

# house_prices = [[0, 8*pow(3,i)] for i in range(11)]
# quarry_prices = [[4*pow(3,i), 0] for i in range(11)]
# powerplant_prices = [[4*pow(3,i), 4*pow(3,i)] for i in range(11)]
# farm_prices = [[2*pow(3,i), 0] for i in range(11)]

# house_gain = [10*pow(2,i) for i in range(11)]
# quarry_gain = [10*pow(2,i) for i in range(11)]
# powerplant_gain = [pow(2,i) for i in range(11)]
# food_gain = [pow(2,i) for i in range(11)]

# rent_prices = [0,10,40,160,640,2560,10240,40960,163840,655360,2621440]

# test = Costs(house_prices, quarry_prices, powerplant_prices, farm_prices, house_gain, quarry_gain, powerplant_gain, food_gain, rent_prices)
