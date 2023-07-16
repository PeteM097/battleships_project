from random import *
class Battleships:
    def is_sunk(self, ship):
        if len(ship[4]) == ship[3]:
            return True
        else:
            return False

    def ship_type(self, ship):
        ship_list = list(ship)
        length = ship_list[3]
        if length < 1 or length > 4:
            return "Invalid ship type!"
        elif length == 1:
            return "Submarine"
        elif length == 2:
            return "Destroyer"
        elif length == 3:
            return "Cruiser"
        else:
            return "Battleship"

    def is_open_sea(self, row, column, fleet):
        fleet_cells = set()
        for ship in fleet:
            fleet_cells.add((ship[0], ship[1]))
            if ship[2]:
                for a in range(1, ship[3]):
                    fleet_cells.add((ship[0], ship[1] + a))
            else:
                for b in range(1, ship[3]):
                    fleet_cells.add((ship[0] + b, ship[1]))

        illegal_cells = ["*" for cell in fleet_cells if
                         cell[0] in range(row - 1, row + 2) and cell[1] in range(column - 1,
                                                                                 column + 2)]
        if illegal_cells:
            return False
        else:
            return True

    def ok_to_place_ship_at(self, row, column, horizontal, length, fleet):
        ship_cells = {(row, column)}
        if horizontal:
            for a in range(1, length):
                ship_cells.add((row, column + a))
        else:
            for b in range(1, length):
                ship_cells.add((row + b, column))

        illegal_cells = ["*" for cell in ship_cells if not self.is_open_sea(cell[0], cell[1], fleet)]
        same_length = len(["*" for ship in fleet if ship[3] == length])

        out_of_bounds = row + (length - 1) > 9 or column + (length - 1) > 9

        if not illegal_cells and same_length <= 4 - length and not out_of_bounds:
            return True
        else:
            return False

    def place_ship_at(self, row, column, horizontal, length, fleet):
        ship = (row, column, horizontal, length, set())
        fleet.append(ship)
        return fleet

    def randomly_place_all_ships(self):
        fleet = []
        while len(fleet) < 10:
            ship = [randint(0, 9), randint(0, 9), choice([True, False]), randint(1, 5)]
            if self.ok_to_place_ship_at(ship[0], ship[1], ship[2], ship[3], fleet):
                self.place_ship_at(ship[0], ship[1], ship[2], ship[3], fleet)
        return fleet

    def check_if_hits(self, row, column, fleet):
        fleet_cells, shot = set(), (row, column)
        for ship in fleet:
            for a in range(0, ship[3]):
                if shot not in ship[4]:
                    if ship[2]:
                        fleet_cells.add((ship[0], ship[1] + a))
                    else:
                        fleet_cells.add((ship[0] + a, ship[1]))
        return shot in fleet_cells

    def hit(self, row, column, fleet):
        hit_tuple = tuple()

        for ship in fleet:
            if ship[2] and row == ship[0] and column in range(ship[1], ship[1] + ship[3]) or not ship[2] and row in \
                    range(ship[0], ship[0] + ship[3]) and column == ship[1]:
                ship[4].add((row, column))
                hit_tuple = (fleet, ship)

        return hit_tuple

    def are_unsunk_ships_left(self, fleet):
        ship_checks = []
        for ship in fleet:
            if self.is_sunk(ship):
                ship_checks.append("*")

        return len(ship_checks) != len(fleet)

    def stats(self, fleet):
        stat_string = "\nSHIPS SUNK\n"
        for length in range(1, 5):
            same_length = len(["*" for ship in fleet if self.is_sunk(ship) and ship[3] == length])
            stat_string += "%ss: %d/%d    " % (self.ship_type((0, 0, True, length, set())), same_length, 5 - length)
        stat_string += "Total: %d/10" % len(["*" for ship in fleet if len(ship[4]) == ship[3]])
        return stat_string
