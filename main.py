from wordle import *
from bot import *

def main():
    bot = Bot()
    guesses = 0
    guess = "SALET"
    first_guesses = gen_first_guesses()
    print("Welcome to the Wordle Solver!")
    print(f"The first recommended guess is '{guess}'.")
    partition = ""
    while partition != "22222":
        partition = input(f"Type in the result from guessing {guess.upper()}: ")
        if validPartition(partition):
            bot.possible_ans = bot.filter(bot.possible_ans, guess, partition)
            bot.words = bot.filter(bot.words, guess, partition)
            if guess == "SALET":
                guess = first_guesses[partition]
            else:
                if len(bot.words) > 200:
                    print("This may take a while. Please be patient.")
                guess = bot.solve()[1]
            if partition != "22222":
                print(f"Your next recommended guess is '{guess.upper()}'")
        else:
            print("That is not a valid string. Please try again.")
    print("Thank you for using Wordle Solver!")


def validPartition(s: str) -> bool:
    if not len(s) == 5:
        return False
    for c in s:
        if c not in ['0', '1', '2']:
            return False
    return True

def gen_first_guesses():
    guesses = {}
    with open ('firstguess.txt', 'r') as f:
        for line in f:
            line = line.strip()
            partition, guess = line.split(" ")[0], line.split(" ")[1]
            guesses[partition] = guess
    return guesses

if __name__ == '__main__':
    main()