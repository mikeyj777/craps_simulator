import pygame
import sys
from ..game.dice import DicePair
from ..game.bet import BetType, Bet
from ..game.craps_table import CrapsTable, Player

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

def test_dice():
    dice_pair = DicePair()
    rolls = [0] * 13
    num_rolls = 1000

    for _ in range(num_rolls):
        result = dice_pair.sum()
        rolls[result] += 1

    # Visual representation
    screen.fill(WHITE)
    draw_text("Dice Test", BLACK, 10, 10)
    
    for i in range(2, 13):
        height = rolls[i] * 2
        pygame.draw.rect(screen, BLUE, (50 + (i-2)*60, 550 - height, 50, height))
        draw_text(str(i), BLACK, 65 + (i-2)*60, 560)

    # Verification method 1: Check if all numbers are rolled
    all_rolled = all(rolls[i] > 0 for i in range(2, 13))
    draw_text(f"All numbers rolled: {'Yes' if all_rolled else 'No'}", GREEN if all_rolled else RED, 10, 50)

    # Verification method 2: Check if 7 is the most common roll
    most_common = max(range(2, 13), key=lambda x: rolls[x])
    draw_text(f"Most common roll is 7: {'Yes' if most_common == 7 else 'No'}", GREEN if most_common == 7 else RED, 10, 90)

    pygame.display.flip()
    wait_for_key()

def test_bet():
    bet = Bet(BetType.PASS_LINE, 10)
    results = []

    for _ in range(10):
        dice_sum = DicePair().sum()
        winnings, keep_bet = bet.resolve(dice_sum)
        results.append((dice_sum, winnings, keep_bet))

    # Visual representation
    screen.fill(WHITE)
    draw_text("Bet Test (Pass Line)", BLACK, 10, 10)

    for i, (dice_sum, winnings, keep_bet) in enumerate(results):
        color = GREEN if winnings > 0 else RED if winnings < 0 else BLUE
        draw_text(f"Roll: {dice_sum}, Winnings: ${winnings}, Keep: {keep_bet}", color, 10, 50 + i*40)

    # Verification method 1: Check if there's at least one win and one loss
    has_win = any(winnings > 0 for _, winnings, _ in results)
    has_loss = any(winnings < 0 for _, winnings, _ in results)
    draw_text(f"Has wins and losses: {'Yes' if has_win and has_loss else 'No'}", GREEN if has_win and has_loss else RED, 10, 460)

    # Verification method 2: Check if keep_bet is False when there's a win or loss
    correct_keep = all((winnings == 0) == keep_bet for _, winnings, keep_bet in results)
    draw_text(f"Correct keep_bet behavior: {'Yes' if correct_keep else 'No'}", GREEN if correct_keep else RED, 10, 500)

    pygame.display.flip()
    wait_for_key()

def test_craps_table():
    table = CrapsTable(min_bet=5, max_bet=100)
    player = table.add_player(1000)
    
    bets = [
        (BetType.PASS_LINE, 10),
        (BetType.PLACE_WIN, 20, 6),
        (BetType.FIELD, 15),
    ]

    for bet_type, amount, *args in bets:
        table.place_bet(player, bet_type, amount, *args)

    # Visual representation
    screen.fill(WHITE)
    draw_text("Craps Table Test", BLACK, 10, 10)

    draw_text(f"Player Bankroll: ${player.bankroll}", BLUE, 10, 50)
    for i, (_, bet) in enumerate(table.bets):
        draw_text(f"Bet {i+1}: {bet}", BLACK, 10, 90 + i*40)

    # Verification method 1: Check if all bets are placed
    all_bets_placed = len(table.bets) == len(bets)
    draw_text(f"All bets placed: {'Yes' if all_bets_placed else 'No'}", GREEN if all_bets_placed else RED, 10, 250)

    # Verification method 2: Check if player's bankroll is correctly updated
    expected_bankroll = 1000 - sum(bet[1] for bet in bets)
    correct_bankroll = player.bankroll == expected_bankroll
    draw_text(f"Correct bankroll: {'Yes' if correct_bankroll else 'No'}", GREEN if correct_bankroll else RED, 10, 290)

    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def main():
    test_dice()
    test_bet()
    test_craps_table()

if __name__ == "__main__":
    main()