from prettytable import PrettyTable
from colorama import Fore, Style, init

init(autoreset=True)

class TableResponse:
    def __init__(self, headers: list, data: list[list]):
        self.headers = headers
        self.data = data

    def __repr__(self):
        colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA]
        table = PrettyTable()
        table.field_names = self.headers
        # for row in self.data:
        #     table.add_row(row)
        for index, row in enumerate(self.data):
            color = colors[index % len(colors)]  # Cycle through colors
            colored_row = [f"{color}{cell}{Style.RESET_ALL}" for cell in row]
            table.add_row(colored_row)
        return str(table)