# tester.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from craps.bets import BetType, ways_to_play
from craps.table import CrapsTable
from craps.agent import Agent

pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Craps Simulation Tester")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def test_table():
    table = CrapsTable()
    
    # Test 1: Pass Line Bet (winning scenario)
    screen.fill(WHITE)
    draw_text("Table Test 1: Pass Line Bet (Win)", BLACK, 10, 10)
    table.add_roll(7)
    table.update_winnings(7)
    draw_text(f"Pass Line Result: {table.winnings[BetType.PASS_LINE]}", GREEN, 10, 50)
    draw_text(f"Expected: 1", BLACK, 10, 90)
    pygame.display.flip()
    wait_for_key()

    # Test 2: Pass Line Bet (losing scenario)
    screen.fill(WHITE)
    draw_text("Table Test 2: Pass Line Bet (Loss)", BLACK, 10, 10)
    table.add_roll(2)
    table.update_winnings(2)
    draw_text(f"Pass Line Result: {table.winnings[BetType.PASS_LINE]}", RED, 10, 50)
    draw_text(f"Expected: -1", BLACK, 10, 90)
    pygame.display.flip()
    wait_for_key()

    # Test 3: Place Win Bet
    screen.fill(WHITE)
    draw_text("Table Test 3: Place Win Bet", BLACK, 10, 10)
    table.add_roll(6)
    table.update_winnings(6)
    draw_text(f"Place Win 6 Result: {table.winnings[BetType.PLACE_WIN][6]}", GREEN, 10, 50)
    draw_text(f"Expected: 1", BLACK, 10, 90)
    pygame.display.flip()
    wait_for_key()

def test_agent():
    agent = Agent(100)
    table = CrapsTable()

    # Test 1: Place bet and win
    screen.fill(WHITE)
    draw_text("Agent Test 1: Place Bet and Win", BLACK, 10, 10)
    agent.place_bet(BetType.PASS_LINE, 10)
    table.add_roll(7)
    table.update_winnings(7)
    initial_bankroll = agent.bankroll
    payout = agent.calculate_payouts(table.winnings)
    agent.receive_payouts(payout)
    draw_text(f"Initial Bankroll: ${initial_bankroll:.2f}", BLACK, 10, 50)
    draw_text(f"Payout: ${payout:.2f}", GREEN, 10, 90)
    draw_text(f"Final Bankroll: ${agent.bankroll:.2f}", BLUE, 10, 130)
    draw_text(f"Expected: ${initial_bankroll + 10:.2f}", BLACK, 10, 170)
    pygame.display.flip()
    wait_for_key()

    # Test 2: Place bet and lose
    screen.fill(WHITE)
    draw_text("Agent Test 2: Place Bet and Lose", BLACK, 10, 10)
    agent.place_bet(BetType.PASS_LINE, 10)
    table.add_roll(2)
    table.update_winnings(2)
    initial_bankroll = agent.bankroll
    payout = agent.calculate_payouts(table.winnings)
    agent.receive_payouts(payout)
    draw_text(f"Initial Bankroll: ${initial_bankroll:.2f}", BLACK, 10, 50)
    draw_text(f"Payout: ${payout:.2f}", RED, 10, 90)
    draw_text(f"Final Bankroll: ${agent.bankroll:.2f}", BLUE, 10, 130)
    draw_text(f"Expected: ${initial_bankroll - 10:.2f}", BLACK, 10, 170)
    pygame.display.flip()
    wait_for_key()

    # Test 3: Place multiple bets
    screen.fill(WHITE)
    draw_text("Agent Test 3: Multiple Bets", BLACK, 10, 10)
    agent.place_bet(BetType.PASS_LINE, 10)
    agent.place_bet(BetType.PLACE_WIN, 10, 6)
    table.add_roll(6)
    table.update_winnings(6)
    initial_bankroll = agent.bankroll
    payout = agent.calculate_payouts(table.winnings)
    agent.receive_payouts(payout)
    draw_text(f"Initial Bankroll: ${initial_bankroll:.2f}", BLACK, 10, 50)
    draw_text(f"Payout: ${payout:.2f}", GREEN, 10, 90)
    draw_text(f"Final Bankroll: ${agent.bankroll:.2f}", BLUE, 10, 130)
    expected_payout = 10 * (7/6)  # Place Win on 6 pays 7:6
    draw_text(f"Expected Payout: ${expected_payout:.2f}", BLACK, 10, 170)
    pygame.display.flip()
    wait_for_key()

def test_agent_wagering():
    screen.fill(WHITE)
    draw_text("Agent Wagering Test", BLACK, 10, 10)

    agent = Agent(100)
    
    # Test 1: Place bet within limits
    agent.place_bet(BetType.PASS_LINE, 50)
    draw_text(f"Bet 1: Pass Line $50", BLACK, 10, 50)
    draw_text(f"Current Wagered: ${agent.current_amount_wagered}", BLUE, 10, 90)
    draw_text(f"Expected: $50", BLACK, 10, 130)

    # Test 2: Try to place bet exceeding bankroll
    agent.place_bet(BetType.COME, 60)
    draw_text(f"Bet 2: Come $60 (should be capped at $50)", BLACK, 10, 170)
    draw_text(f"Current Wagered: ${agent.current_amount_wagered}", BLUE, 10, 210)
    draw_text(f"Expected: $100", BLACK, 10, 250)

    # Test 3: Remove a bet
    agent.remove_bet(BetType.PASS_LINE)
    draw_text(f"Remove Pass Line bet", BLACK, 10, 290)
    draw_text(f"Current Wagered: ${agent.current_amount_wagered}", BLUE, 10, 330)
    draw_text(f"Expected: $50", BLACK, 10, 370)

    pygame.display.flip()
    wait_for_key()

# Add this to your main() function
def main():
    test_table()
    test_agent()
    test_agent_wagering()

if __name__ == "__main__":
    main()