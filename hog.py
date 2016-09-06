"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    total = 0
    ones = 0
    while num_rolls:
        result = dice()
        num_rolls = num_rolls - 1

        if result > 1:
            total = result + total
            
        elif result == 1:
            ones = result + ones
                       
    if ones:
        return ones
    else:
        return total
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    num1 = opponent_score % 10
    num2 = opponent_score // 10
    high= max(num1, num2)
    return high + 1
    # END PROBLEM 2


# Write your prime functions here!
def is_prime(x):
    """Checks whether x is a prime number
    >>>is_prime(3)
    True
    >>>is_prime(23)
    True
    >>>is_prime(5)
    True 
    """
    
    b = x-1
    n = 1
    if x == 1:
        return False
    while n < b:
        n = n + 1
        rem = x % n
        if rem == 0:
            return False
    return True

def next_prime(x):

    """ Returns the next prime number after x.
    >>>next_prime(13)
    17
    >>> next_prime(23)
    29
    """
    if is_prime(x):
        x=x+1
        while not is_prime(x):
            x = x+1
        return x

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime and When Pigs Fly rules.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    points = 0
    if num_rolls == 0:
        points = free_bacon(opponent_score)
        if is_prime(points):
            return next_prime(points)
        else:
            return points

    else:
        points = roll_dice(num_rolls, dice)
        if is_prime(points):
            points = next_prime(points)
        return min(points, 25-num_rolls)

    # END PROBLEM 2


def reroll(dice):
    """Return dice that return even outcomes and re-roll odd outcomes of DICE."""
    def rerolled():
        # BEGIN PROBLEM 3
        result = roll_dice(1, dice)
        if result % 2 != 0:
            result = roll_dice(1, dice)
            return result
        else:
            return result

        # END PROBLEM 3
    return rerolled


def select_dice(score, opponent_score, dice_swapped):
    """Return the dice used for a turn, which may be re-rolled (Hog Wild) and/or
    swapped for four-sided dice (Pork Chop).

    DICE_SWAPPED is True if and only if four-sided dice are being used.
    """
    # BEGIN PROBLEM 4
    if dice_swapped == True:
        dice = four_sided  # Replace this statement
    if dice_swapped == False:
        dice = six_sided
    if (score + opponent_score) % 7 == 0:
        dice = reroll(dice)
    return dice   
    # END PROBLEM 4
    


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    dice_swapped = False  # Whether 4-sided dice have been swapped for 6-sided
    # BEGIN PROBLEM 5
    
    while (score0 < goal and score1 < goal):
        if player == 0:
            if strategy0(score0, score1) == -1:
                score0 += 1
                dice_swapped = not dice_swapped
                if score0 == (score1*2):
                    score0, score1 = score1, score0
                elif score1 == (score0*2):
                    score0, score1 = score1, score0

                if score0 >= goal or score1 >= goal:
                    break
                
                player = other(player)

            else:
                dice = select_dice(score0, score1, dice_swapped)
                score0 += take_turn(strategy0(score0, score1), score1, dice)
                if score0 == (score1*2):
                    score0, score1 = score1, score0
                elif score1 == (score0*2):
                   score0, score1 = score1, score0

                if score0 >= goal or score1 >= goal:
                    break
                
                player = other(player)

        elif player == 1:
            if strategy1(score1, score0) == -1:
                score1 += 1
                dice_swapped = not dice_swapped
                if score0 == (score1*2):
                    score0, score1 = score1, score0
                elif score1 == (score0*2):
                    score0, score1 = score1, score0  

                if score0 >= goal or score1 >= goal:
                    break
                
                player = other(player)

            else:
                dice = select_dice(score1, score0, dice_swapped)
                score1 += take_turn(strategy1(score1, score0), score0, dice)
                if score0 == (score1*2):
                    score0, score1 = score1, score0
                elif score1 == (score0*2):
                    score0, score1 = score1, score0
                if score0 >= goal or score1 >= goal:
                    break
                
                player = other(player)


        


        



    # END PROBLEM 5
    return score0, score1
    
    score0 = 0
    score1 = 0
    while score0 < goal and score1 < goal:
        check_strategy_roll(score0, score1, strategy(score0, score1))
        score0 += 1
        if score0 == goal:
              score0 = 0
              score1 += 1

    return None
    
    def average_value(*args):
        n = 0
        total = 0
        while n < num_samples:
            n += 1
            total += fn(*args)
        return total / num_samples


    return average_value
