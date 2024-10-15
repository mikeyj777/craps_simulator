from .bet import BetType, Bet
from typing import List, Tuple, Any

class Player:
    def __init__(self, id: int, bankroll: float):
        self.id = id
        self.bankroll = bankroll

class CrapsTable:
    def __init__(self, min_bet: float = 5, max_bet: float = 1000):
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.point = None
        self.bets: List[Tuple[Player, Bet]] = []
        self.players: List[Player] = []

    def add_player(self, bankroll: float) -> Player:
        player = Player(len(self.players), bankroll)
        self.players.append(player)
        return player

    def place_bet(self, player: Player, bet_type: BetType, amount: float, number: int = None) -> Bet:
        if amount < self.min_bet or amount > self.max_bet:
            raise ValueError(f"Bet must be between ${self.min_bet} and ${self.max_bet}")
        
        if player.bankroll < amount:
            raise ValueError(f"Player doesn't have enough funds to place this bet")
        
        bet = Bet(bet_type, amount, self.point, number)
        self.bets.append((player, bet))
        player.bankroll -= amount
        return bet

    def remove_bet(self, player: Player, bet: Bet):
        self.bets = [(p, b) for p, b in self.bets if p != player or b != bet]

    def resolve_bets(self, dice_sum: int, is_hardway: bool) -> List[Tuple[Player, Bet, float]]:
        results = []
        for player, bet in self.bets:
            winnings, keep_bet = bet.resolve(dice_sum, is_hardway)
            if winnings != 0:
                player.bankroll += (bet.amount + winnings)
                results.append((player, bet, winnings))
            if not keep_bet:
                self.remove_bet(player, bet)
        return results

    def set_point(self, point: int):
        self.point = point

    def clear_point(self):
        self.point = None

    def __str__(self):
        table_str = f"Craps Table (Point: {self.point or 'Off'})\n"
        table_str += f"Minimum bet: ${self.min_bet}, Maximum bet: ${self.max_bet}\n"
        table_str += "Current bets:\n"
        for player, bet in self.bets:
            table_str += f"  Player {player.id}: {bet}\n"
        return table_str