from battleships import Battleships
class Visualisation(Battleships):
    def get_grid(self, shots, fleet):
        grid = "   0  1  2  3  4  5  6  7  8  9  "
        hits, sunk_types = set(), [set(), set(), set(), set()]
        for ship in fleet:
            for hit in ship[4]:
                if self.is_sunk(ship):
                    sunk_types[ship[3] - 1].add(hit)
                hits.add(hit)
        sunk_cells = [cell for inner_set in sunk_types for cell in inner_set]
        for row in range(10):
            grid += "\n%s " % chr(row + 65)
            for column in range(10):
                if (row, column) in shots:
                    if (row, column) in hits:
                        if (row, column) in sunk_cells:
                            if (row, column) in sunk_types[0]:
                                i = " S "
                            elif (row, column) in sunk_types[1]:
                                i = " D "
                            elif (row, column) in sunk_types[2]:
                                i = " C "
                            else:
                                i = " B "
                        else:
                            i = " * "
                    else:
                        i = " - "
                else:
                    i = " . "
                grid += i
        grid += "\n\n\t- miss\t* hit\to sunk"
        return grid

def main():
    game = Battleships()
    grid = Visualisation()
    current_fleet,  game_over, num_shots, shots_rec = game.randomly_place_all_ships(), False, 0, set()
    print("WELCOME TO BATTLESHIPS!\n\nYou can type \"x\" to quit the game at any time.\n\n%s\n" %
          grid.get_grid(shots_rec, current_fleet))
    while not game_over:
        print("Enter a row (A-J), followed by a column (0-9).")
        kbd_input = str(input())
        input_edit = kbd_input.replace(" ", "")
        if input_edit != "x" and input_edit != "X":
            try:
                if len(input_edit) == 2 and (ord(input_edit[0]) in range(65, 75) or ord(input_edit[0]) in
                                             range(97, 107)) and ord(input_edit[1]) in range(48, 58):
                    current_row, current_column = int(chr(ord(input_edit[0].upper()) - 17)), int(input_edit[1])
                    if (current_row, current_column) in shots_rec:
                        print("YOU'VE ALREADY SHOT AT THIS CELL!\n")
                    else:
                        num_shots += 1
                        shots_rec.add((current_row, current_column))
                        if game.check_if_hits(current_row, current_column, current_fleet):
                            (current_fleet, ship_hit) = game.hit(current_row, current_column, current_fleet)
                            if game.is_sunk(ship_hit):
                                print("YOU SANK A %s!\t\tShots: %d\n" % (game.ship_type(ship_hit).upper(), num_shots))
                            else:
                                print("HIT\t\tShots: %d\n" % num_shots)
                        else:
                            print("MISS\t\tShots: %d\n" % num_shots)
                        print(grid.get_grid(shots_rec, current_fleet))
                        print(game.stats(current_fleet) + "\n\n")
                else:
                    raise ValueError

            except ValueError:
                print("INVALID INPUT; PLEASE TRY AGAIN\n")
        else:
            game_over = True
            print("YOU'VE LEFT THE GAME")
            break
        if not game.are_unsunk_ships_left(current_fleet):
            game_over = True
            print("YOU SANK THE FLEET!\n Total Shots Used: %d" % num_shots)
            break

if __name__ == '__main__':
    main()
