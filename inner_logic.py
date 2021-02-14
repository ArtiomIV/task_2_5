from random import randint


class BoardException(Exception):
    pass

class BoardWrongSize(BoardException):
    def __str__(self):
        return "Wrong board size"

class BoardWrongTargetException(BoardException):
    def __str__(self):
        return "Target out of board range"

class BoardTagetUsedException(BoardException):
    def __str__(self):
        return "Target has been already used"

class BoardWrongShipPositionException(BoardException):
    def __str__(self):
        return "Wrong ship position"

class Dot:
    def __init__(self, x, y):
        self.x = x 
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Dot(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Dot is ({self.x} {self.y})"

class Ship:
    def __init__(self, len_, dot, direction):
        self.len_ = len_
        self.dot = dot
        self.direction = direction
        self.hp = len_

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.len_):
            cor_x, cor_y = self.dot.x, self.dot.y
            
            if self.direction == 0:
                cor_y += i
            
            elif self.direction == 1:
                cor_x += i

            ship_dots.append(Dot(cor_x, cor_y))
        return ship_dots
    
    def shooted(self, cor):
        return cor in self.dots
    
class GameBoard:
    def __init__(self, size = 6, hid = False):
        self.size = size
        self.hid = hid
        self.ships = []
        self.count = 0
        self.busy = []
        self.field = [["0"] * self.size for _ in range(self.size)]

    def addShip(self, ship):
        for cor in ship.dots:
            if self.out(cor) or cor in self.busy:
                raise BoardWrongShipPositionException(BoardException)
            else:
                self.field[cor.x][cor.y] = "◆"
                self.busy.append(cor)
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, stait = False):
        contour_cords = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0), (0, 0), (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ]
        for dot in ship.dots:
            for corx, cory in contour_cords:
                cor = dot  + Dot(corx, cory)
                if not(self.out(cor)) and cor not in self.busy:
                    if stait: 
                        self.field[cor.x][cor.y] = "."
                    self.busy.append(cor)

    def shot(self, shot):
        if self.out(shot):
            raise BoardWrongTargetException(BoardException)
        
        elif shot in self.busy:
            raise BoardTagetUsedException(BoardException)
        
        self.busy.append(shot)
        
        for ship in self.ships:
            if shot in ship.dots:
                ship.hp -= 1
                self.field[shot.x][shot.y] = "X"
                print( "Enemy ship has beenn hit" )
                if ship.hp == 0:
                    self.count += 1
                    self.contour(ship, True)
                    print( "Enemy ship has been destroy" )
                return True
                
        self.field[shot.x][shot.y] = "M"
        print( "Miss" )
        return False
        

    def __str__(self):
        res = "   "
        for i in range(len(self.field)):
            if i > 8:
                res += f"|{i + 1} "
            else:
                res += f"| {i + 1} "
        for j, row in enumerate(self.field):
            if j > 8:
                res += f"\n{j + 1} | " + " | ".join(row)
            else:
                res += f"\n{j + 1}  | " + " | ".join(row)
        if self.hid:
            res = res.replace("◆", "0")
        return res

    def out(self, cor):
        return not (( 0 <= cor.x < self.size ) and ( 0 <= cor.y < self.size ))

    def begin(self):
        self.busy = []

class Player:
    def __init__(self, board, enemy_board, size = 0, name = ""):
        self.board = board
        self.enemy_board = enemy_board
        self.size = size
        self.name = name

    def ask(self):
        pass

    def move(self):
        position = self.ask()
        try:
            shot = self.enemy_board.shot(position)
            return shot
        except BoardException as e:
            print(e)

class AI(Player):
    def ask(self):
        x, y = randint(0, self.size), randint(0, self.size)
        cor = Dot(x, y)
        print( "AI turn" )
        return cor

class User(Player):
    def ask(self):
        while True:
            cor = input( f"Yor turn {self.name}, enter target to shot(x, y): " ).split()
            if len(cor) != 2:
                print( "Two values required" )
                continue

            x, y = cor

            if not x.isdigit() or not y.isdigit():
                print( "Number required" )
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)