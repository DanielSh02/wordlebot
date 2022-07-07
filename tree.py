from bot import *
from wordle import *
import json

def main():
    bot = Bot()
    init_guess = "SALET"
    partitions = bot.gen_partitions(init_guess, bot.possible_ans)
    next_guesses = {}
    count = 0
    for p in partitions:
        count += 1
        print(count, len(partitions[p]))
        next_guesses[p] = bot.solve(bot.filter(bot.words, init_guess, p), bot.filter(bot.possible_ans, init_guess, p))[1]
        print(p, next_guesses[p])

    json.dump(next_guesses, "tree.json")


if __name__ == '__main__':
    main()