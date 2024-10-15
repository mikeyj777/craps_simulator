from enum import Enum, auto
from typing import Optional, Tuple

class BetType(Enum):
    PASS_LINE = auto()
    DONT_PASS = auto()
    COME = auto()
    DONT_COME = auto()
    PASS_LINE_ODDS = auto()
    DONT_PASS_ODDS = auto()
    COME_ODDS = auto()
    DONT_COME_ODDS = auto()
    PLACE_WIN = auto()
    PLACE_LOSE = auto()
    BUY = auto()
    LAY = auto()
    ANY_7 = auto()
    ANY_CRAPS = auto()
    SPECIFIC_CRAPS = auto()
    HORN = auto()
    WHIRL = auto()
    HARDWAY = auto()
    FIELD = auto()
    BIG_6 = auto()
    BIG_8 = auto()
    FIRE_BET = auto()
    PUT = auto()

class Bet:
    def __init__(self, bet_type: BetType, amount: float, point: Optional[int] = None, number: Optional[int] = None):
        self.bet_type = bet_type
        self.amount = amount
        self.point = point
        self.number = number
        self.active = True

    def resolve(self, dice_sum: int, is_hardway: bool = False) -> Tuple[float, bool]:
        winnings = 0
        keep_bet = True

        if self.bet_type in [BetType.PASS_LINE, BetType.COME]:
            if not self.point:
                if dice_sum in [7, 11]:
                    winnings = self.amount
                    keep_bet = False
                elif dice_sum in [2, 3, 12]:
                    winnings = -self.amount
                    keep_bet = False
                else:
                    self.point = dice_sum
            else:
                if dice_sum == self.point:
                    winnings = self.amount
                    keep_bet = False
                elif dice_sum == 7:
                    winnings = -self.amount
                    keep_bet = False

        elif self.bet_type in [BetType.DONT_PASS, BetType.DONT_COME]:
            if not self.point:
                if dice_sum in [2, 3]:
                    winnings = self.amount
                    keep_bet = False
                elif dice_sum in [7, 11]:
                    winnings = -self.amount
                    keep_bet = False
                elif dice_sum == 12:
                    keep_bet = False  # Push
            else:
                if dice_sum == 7:
                    winnings = self.amount
                    keep_bet = False
                elif dice_sum == self.point:
                    winnings = -self.amount
                    keep_bet = False

        elif self.bet_type in [BetType.PASS_LINE_ODDS, BetType.COME_ODDS]:
            if dice_sum == self.point:
                if self.point in [4, 10]:
                    winnings = self.amount * 2
                elif self.point in [5, 9]:
                    winnings = self.amount * 1.5
                elif self.point in [6, 8]:
                    winnings = self.amount * 1.2
                keep_bet = False
            elif dice_sum == 7:
                winnings = -self.amount
                keep_bet = False

        elif self.bet_type in [BetType.DONT_PASS_ODDS, BetType.DONT_COME_ODDS]:
            if dice_sum == 7:
                if self.point in [4, 10]:
                    winnings = self.amount / 2
                elif self.point in [5, 9]:
                    winnings = self.amount * 2 / 3
                elif self.point in [6, 8]:
                    winnings = self.amount * 5 / 6
                keep_bet = False
            elif dice_sum == self.point:
                winnings = -self.amount
                keep_bet = False

        elif self.bet_type == BetType.PLACE_WIN:
            if dice_sum == self.number:
                if self.number in [4, 10]:
                    winnings = self.amount * 9 / 5
                elif self.number in [5, 9]:
                    winnings = self.amount * 7 / 5
                elif self.number in [6, 8]:
                    winnings = self.amount * 7 / 6
                keep_bet = False
            elif dice_sum == 7:
                winnings = -self.amount
                keep_bet = False

        elif self.bet_type == BetType.PLACE_LOSE:
            if dice_sum == 7:
                if self.number in [4, 10]:
                    winnings = self.amount * 5 / 11
                elif self.number in [5, 9]:
                    winnings = self.amount * 5 / 8
                elif self.number in [6, 8]:
                    winnings = self.amount * 4 / 5
                keep_bet = False
            elif dice_sum == self.number:
                winnings = -self.amount
                keep_bet = False

        # Add resolution logic for other bet types...

        return winnings, keep_bet

    def __str__(self):
        return f"{self.bet_type.name} bet of ${self.amount}" + (f" on {self.number}" if self.number else "")