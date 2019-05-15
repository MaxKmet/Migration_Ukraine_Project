from ukrainian_data_adt import UkrainianData


class UADataResearchCommandLine:
    """
    Class provides command line interface for the research
    Every method of the class corresponds to a method in UkrainianData
    """

    def __init__(self, ua_data):
        """
        :param ua_data: UkrainianData instance
        """
        self.data = ua_data
        self.commands = {"show_data": self.show_data, "row_names": self.row_names, "col_names": self.column_names,
                         "get_val": self.get_value, "get_row": self.get_row, "get_col": self.get_column,
                         "cor_ind": self.correlation_index, "plot": self.show_change_plot, "map": self.get_map,
                         "explain": self.explain, "exit": self.exit
                         }

    def start(self):
        while True:
            print("Enter one of the commands: ")
            for com in self.commands.keys():
                print(com)
            command = input(">>>")
            try:
                self.commands[command]()
            except KeyError:
                print(command + " is not a valid command")

    def show_data(self):
        good_input = False
        while not good_input:
            answer = input("Do you want to to display the whole dataset ?\n(y/n)")
            if answer.lower() == "y":
                good_input = True
                self.data.show_data()
            elif answer.lower() == "n":
                return
            else:
                print("Wrong input\n")

    def explain(self):
        print(self.data.explanation)

    def row_names(self):
        print("Names of rows in dataset:")
        print(self.data.row_names)

    def column_names(self):
        print("Names of columns in dataset:")
        print(self.data.column_names)

    def get_value(self):
        row = input("Enter name of row to get value from:")
        col = input("Enter name of column to get value from:")
        try:
            print(self.data.get_value(row, col))
        except KeyError as ex:
            print(ex)

    def get_row(self):
        row = input("Enter name of row to get value from:")
        try:
            print(self.data.get_row(row))
        except KeyError as ex:
            print(ex)

    def get_column(self):
        col = input("Enter name of column to get value from:")
        try:
            print(self.data.get_column(col))
        except KeyError as e:
            print(e)

    def correlation_index(self):
        param = input("Do you want to correlate rows or columns (r/c) ?")
        if param.lower() == "r":
            row1 = input("Enter name of first row to correlate:")
            row2 = input("Enter name of second row to correlate:")
            try:
                print(UkrainianData.correlation_index(list(self.data.get_row(row1).values()),
                                                      list(self.data.get_row(row2).values())))
            except ValueError as e:
                print(e)

        elif param.lower() == "c":
            col1 = input("Enter name of first column to correlate:")
            col2 = input("Enter name of second column to correlate:")
            try:
                print(UkrainianData.correlation_index(list(self.data.get_column(col1).values()),
                                                      list(self.data.get_column(col2).values())))
            except ValueError as e:
                print(e)
        else:
            print("Wrong input")

    def show_change_plot(self):
        row = input("Enter name of row to plot:")
        param = input("Enter name of parameter( part of column name, example: Число прибулих):")
        try:
            self.data.show_change_plot(row, param)
        except ValueError as e:
            print(e)

    def get_map(self):
        param = input("Enter name of parameter( part of column name, example: Число прибулих):")
        year = int(input("Enter year to plot:"))
        filename = input("Enter path to file where to save the map (.html required):")
        try:
            map_str = self.data.get_map(param, year)
            with open(filename, "w") as f:
                f.write(map_str)
        except KeyError as e:
            print(e)

    def exit(self):
        exit(0)


if __name__ == "__main__":
    migration_data = UkrainianData("338a8ccf-8b77-476b-b138-9bb5b7550584")
    print("Migration data has been uploaded")
    migration_data_ui = UADataResearchCommandLine(migration_data)
    migration_data_ui.start()
