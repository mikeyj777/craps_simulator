# agent.py
from craps.bets import BetType, payout_odds

class Agent:
    def __init__(self, bankroll: float):
        self.bankroll = bankroll
        self.bets = {bet_type: 0 for bet_type in BetType}
        self.current_amount_wagered = 0

    def place_bet(self, bet_type: BetType, amount: float, number: int = None):
        available_funds = self.bankroll - self.current_amount_wagered
        if amount > available_funds:
            amount = available_funds  # Cap the bet at available funds

        if amount > 0:
            if number:
                if self.bets[bet_type] == 0:
                    self.bets[bet_type] = {}
                self.bets[bet_type][number] = amount
            else:
                self.bets[bet_type] = amount
            self.current_amount_wagered += amount
        else:
            raise ValueError("Insufficient funds to place bet")

    def remove_bet(self, bet_type: BetType, number: int = None):
        if number:
            if isinstance(self.bets[bet_type], dict) and number in self.bets[bet_type]:
                amount = self.bets[bet_type][number]
                del self.bets[bet_type][number]
                if not self.bets[bet_type]:  # If no more bets for this type
                    self.bets[bet_type] = 0
            else:
                raise ValueError("Bet not found")
        else:
            amount = self.bets[bet_type]
            self.bets[bet_type] = 0

        self.current_amount_wagered -= amount

    def calculate_payouts(self, table_winnings):
        total_payout = 0
        for bet_type, bet_amount in self.bets.items():
            if isinstance(bet_amount, dict):
                # For bets on specific numbers
                for number, amount in bet_amount.items():
                    result = table_winnings[bet_type][number]
                    odds = payout_odds[bet_type][number] if isinstance(payout_odds[bet_type], dict) else payout_odds[bet_type]
                    payout = amount * result * odds if result > 0 else amount * result
                    total_payout += payout
            else:
                # For single bets
                result = table_winnings[bet_type]
                odds = payout_odds[bet_type]
                payout = bet_amount * result * odds if result > 0 else bet_amount * result
                total_payout += payout
        
        return total_payout

    def receive_payouts(self, payout: float):
        self.bankroll += payout
        self.bets = {bet_type: 0 for bet_type in BetType}
        self.current_amount_wagered = 0

    def make_betting_decision(self, table):
        if self.bankroll > table.min_bet:
            self.place_bet(BetType.PASS_LINE, table.min_bet)

    def __str__(self):
        bet_str = ', '.join([f'{bet.name}: ${amount}' for bet, amount in self.bets.items() if amount > 0])
        return f"Agent Bankroll: ${self.bankroll:.2f}\n" \
               f"Current Amount Wagered: ${self.current_amount_wagered:.2f}\n" \
               f"Current Bets: {bet_str}"