from inner_logic import *
from random import randint

class Game:
    def __init__(self, size = 0, name = ""):
        self.name = self.askName()
        self.size = self.boardSize()
        ai_board = self.randomBoard()
        user_board = self.randomBoard()
        ai_board.hid = True

        self.ai = AI(ai_board, user_board, size = self.size)
        self.user = User(user_board, ai_board, name = self.name)

    def askName(self):
        self.name = input ( "Enter your name: " )
        return self.name

    def askBoard(self):
            self.size = input( "Enter board size what you prefer: " )
            if not self.size.isdigit():
                print( "Must be a number" )
                raise BoardWrongSize(BoardException)
            
            size = int(self.size)

            if not (6 < size < 20):
                print( "Value must ve inside a range 6 < size < 20" )
                raise BoardWrongSize(BoardException)
            
            return size

    def boardSize(self):
        while True:
            try:
                size = self.askBoard()
                return size
            except BoardException as e:
                print(e)

    def randomBoard(self):
        board = None
        while board is None:
            board = self.tryBoard()
        return board

    def tryBoard(self):
        ships_len = [3, 2, 2, 1, 1, 1, 1]
        board = GameBoard(size = self.size)
        attemps = 0
        for i in ships_len:
            while True:
                attemps += 1
                if attemps > 2000:
                    return None
                ship = Ship(i, Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1))
                try:
                    board.addShip(ship)
                    break
                except BoardException:
                    pass
        board.begin()
        return board

    #@staticmethod
    def greet(self):
        print("-----------".center(30))
        print(f"We welcom you {self.name}".center(30))
        print("In the game".center(30))
        print("'Battle ship'".center(30))
        print("-----------".center(30))
        print("Input format is: x, y".center(30))
        print("x = number of row".center(30))
        print("y = number of column".center(30))
        print("-----------".center(30))

    def loop(self):
        cycle_num = 0
        while True:
            print("-"*20)
            print(f"Board of user {self.name}")
            print(self.user.board)
            print("-"*20)
            print(f"AI bord")
            print(self.ai.board)
            print("-"*20)
            if cycle_num % 2 == 0:
                print(f"Your turn {self.name}")
                shot = self.user.move()
                if shot:
                    cycle_num -= 1
            else:
                print("AI turn keep calm dude :)")
                shot = self.ai.move()
                if shot:
                    cycle_num -= 1

            if self.ai.board.count == 7:
                print("-"*20)
                print(self.user.board)
                print("-"*20)
                print(self.ai.board)
                print("-"*20)
                print( "Congratulation you WIN! :)" )
                break

            if self.user.board.count == 7:
                print("-"*20)
                print(self.user.board)
                print("-"*20)
                print(self.ai.board)
                print("-"*20)
                print( "You loos! :(" )

            cycle_num += 1

    def start(self):
        self.greet()
        self.loop()

game = Game()
game.start()