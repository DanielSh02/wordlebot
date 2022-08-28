from bot import *
from wordle import *
import json

def main():
    bot = Bot(guesses=5)
    init_guess = "SALET"
    partitions = bot.gen_partitions(init_guess, bot.possible_ans)
    next_guesses = {}
    count = 0
    for p in partitions:
        count += 1
        print(f'Partition: {count}/{len(partitions)}; words:{len(partitions[p])}')
        next_guesses[p] = bot.solve(bot.filter(bot.words, init_guess, p), bot.filter(bot.possible_ans, init_guess, p), 5)[1]
        print(p, next_guesses[p])

    with open('firstguess.txt', 'w') as f:
        for p in next_guesses:
            f.write(f'{p} {next_guesses[p]}\n')


if __name__ == '__main__':
    main()