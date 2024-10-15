# table.py
from craps.bets import BetType, ways_to_play

class CrapsTable:
    def __init__(self, min_bet: float = 5, max_bet: float = 1000):
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.point = None
        self.winnings = {bet_type: 0 for bet_type in BetType}
        self.roll_history = []
        self.points_in_a_row = []
        self.valid_points = [4, 5, 6, 8, 9, 10]

    def add_roll(self, roll: int):
        self.roll_history.append(roll)
        if len(self.roll_history) > 1000:
            self.roll_history.pop(0)
        
        if roll in self.valid_points:
            self.points_in_a_row.append(roll)
            self.set_point()
        elif roll == 7:
            self.points_in_a_row.clear()
            self.clear_point()

    def set_point(self, point: int):
        self.point = point

    def clear_point(self):
        self.point = None

    def update_winnings(self, roll: int):
        for bet_type, bet_function in ways_to_play.items():
            if isinstance(bet_function, dict):
                # For bets like PLACE_WIN that have multiple numbers
                self.winnings[bet_type] = {num: func(self, roll) for num, func in bet_function.items()}
            else:
                self.winnings[bet_type] = bet_function(self, roll)

    def __str__(self):
        return f"Craps Table (Point: {self.point or 'Off'})\n" \
               f"Minimum bet: ${self.min_bet}, Maximum bet: ${self.max_bet}"