# bets.py
from enum import Enum, auto

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
    FIELD = auto()
    ANY_7 = auto()
    ANY_CRAPS = auto()
    CRAPS_2 = auto()
    CRAPS_3 = auto()
    CRAPS_12 = auto()
    ELEVEN = auto()
    HORN = auto()
    WHIRL = auto()
    HARDWAY = auto()
    BIG_6 = auto()
    BIG_8 = auto()

def pass_line_bet(table, roll):
    if table.point is None:
        return {
            7: 1,
            11: 1,
            2: -1,
            3: -1,
            12: -1
        }.get(roll, 0)
    else:
        if roll == table.point:
            table.point = None
            return 1
        elif roll == 7:
            table.point = None
            return -1
        return 0

def dont_pass_bet(table, roll):
    if table.point is None:
        return {
            2: 1,
            3: 1,
            7: -1,
            11: -1,
            12: 0
        }.get(roll, 0)
    else:
        if roll == 7:
            table.point = None
            return 1
        elif roll == table.point:
            table.point = None
            return -1
        return 0

def come_bet(table, roll):
    return pass_line_bet(table, roll)

def dont_come_bet(table, roll):
    return dont_pass_bet(table, roll)

def place_win_bet(table, roll):
    return {
        4: 1 if roll == 4 else -1 if roll == 7 else 0,
        5: 1 if roll == 5 else -1 if roll == 7 else 0,
        6: 1 if roll == 6 else -1 if roll == 7 else 0,
        8: 1 if roll == 8 else -1 if roll == 7 else 0,
        9: 1 if roll == 9 else -1 if roll == 7 else 0,
        10: 1 if roll == 10 else -1 if roll == 7 else 0
    }

def place_lose_bet(table, roll):
    return {
        4: -1 if roll == 4 else 1 if roll == 7 else 0,
        5: -1 if roll == 5 else 1 if roll == 7 else 0,
        6: -1 if roll == 6 else 1 if roll == 7 else 0,
        8: -1 if roll == 8 else 1 if roll == 7 else 0,
        9: -1 if roll == 9 else 1 if roll == 7 else 0,
        10: -1 if roll == 10 else 1 if roll == 7 else 0
    }

def buy_bet(table, roll):
    return place_win_bet(table, roll)

def lay_bet(table, roll):
    return place_lose_bet(table, roll)

def field_bet(table, roll):
    return {
        2: 2,
        3: 1,
        4: 1,
        9: 1,
        10: 1,
        11: 1,
        12: 2,
        5: -1,
        6: -1,
        7: -1,
        8: -1
    }.get(roll, 0)

def any_seven(table, roll):
    return 1 if roll == 7 else -1

def any_craps(table, roll):
    return 1 if roll in [2, 3, 12] else -1

def craps_bet(number):
    def bet(table, roll):
        return 1 if roll == number else -1
    return bet

def eleven_bet(table, roll):
    return 1 if roll == 11 else -1

def horn_bet(table, roll):
    return 1 if roll in [2, 3, 11, 12] else -1

def whirl_bet(table, roll):
    return 1 if roll in [2, 3, 7, 11, 12] else -1

def hardway_bet(number):
    def bet(table, roll, dice1, dice2):
        if roll == number and dice1 == dice2:
            return 1
        elif roll == number or roll == 7:
            return -1
        return 0
    return bet

def big_6_bet(table, roll):
    return 1 if roll == 6 else -1 if roll == 7 else 0

def big_8_bet(table, roll):
    return 1 if roll == 8 else -1 if roll == 7 else 0

ways_to_play = {
    BetType.PASS_LINE: pass_line_bet,
    BetType.DONT_PASS: dont_pass_bet,
    BetType.COME: come_bet,
    BetType.DONT_COME: dont_come_bet,
    BetType.PLACE_WIN: {num: place_win_bet for num in [4, 5, 6, 8, 9, 10]},
    BetType.PLACE_LOSE: {num: place_lose_bet for num in [4, 5, 6, 8, 9, 10]},
    BetType.BUY: {num: buy_bet for num in [4, 5, 6, 8, 9, 10]},
    BetType.LAY: {num: lay_bet for num in [4, 5, 6, 8, 9, 10]},
    BetType.FIELD: field_bet,
    BetType.ANY_7: any_seven,
    BetType.ANY_CRAPS: any_craps,
    BetType.CRAPS_2: craps_bet(2),
    BetType.CRAPS_3: craps_bet(3),
    BetType.CRAPS_12: craps_bet(12),
    BetType.ELEVEN: eleven_bet,
    BetType.HORN: horn_bet,
    BetType.WHIRL: whirl_bet,
    BetType.HARDWAY: {num: hardway_bet(num) for num in [4, 6, 8, 10]},
    BetType.BIG_6: big_6_bet,
    BetType.BIG_8: big_8_bet,
}

payout_odds = {
    BetType.PASS_LINE: 1,
    BetType.DONT_PASS: 1,
    BetType.COME: 1,
    BetType.DONT_COME: 1,
    BetType.PASS_LINE_ODDS: {4: 2/1, 5: 3/2, 6: 6/5, 8: 6/5, 9: 3/2, 10: 2/1},
    BetType.DONT_PASS_ODDS: {4: 1/2, 5: 2/3, 6: 5/6, 8: 5/6, 9: 2/3, 10: 1/2},
    BetType.COME_ODDS: {4: 2/1, 5: 3/2, 6: 6/5, 8: 6/5, 9: 3/2, 10: 2/1},
    BetType.DONT_COME_ODDS: {4: 1/2, 5: 2/3, 6: 5/6, 8: 5/6, 9: 2/3, 10: 1/2},
    BetType.PLACE_WIN: {4: 9/5, 5: 7/5, 6: 7/6, 8: 7/6, 9: 7/5, 10: 9/5},
    BetType.PLACE_LOSE: {4: 5/11, 5: 5/8, 6: 4/5, 8: 4/5, 9: 5/8, 10: 5/11},
    BetType.BUY: {4: 2/1, 5: 3/2, 6: 6/5, 8: 6/5, 9: 3/2, 10: 2/1},
    BetType.LAY: {4: 1/2, 5: 2/3, 6: 5/6, 8: 5/6, 9: 2/3, 10: 1/2},
    BetType.FIELD: {2: 2, 3: 1, 4: 1, 9: 1, 10: 1, 11: 1, 12: 2},
    BetType.ANY_7: 4,
    BetType.ANY_CRAPS: 7,
    BetType.CRAPS_2: 30,
    BetType.CRAPS_3: 15,
    BetType.CRAPS_12: 30,
    BetType.ELEVEN: 15,
    BetType.HORN: 27,
    BetType.WHIRL: 26,
    BetType.HARDWAY: {4: 7, 6: 9, 8: 9, 10: 7},
    BetType.BIG_6: 1,
    BetType.BIG_8: 1,
}