from prettytable import PrettyTable

class TableResponse:
    def __init__(self, headers: list, data: list[list]):
        self.headers = headers
        self.data = data

    def __repr__(self):
        table = PrettyTable()
        table.field_names = self.headers
        for row in self.data:
            table.add_row(row)
        return str(table)