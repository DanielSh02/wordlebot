from bot import *
from wordle import *

words = random.sample(default_word_list, 1000)
bot = Bot(words=words, guesses=5)
print(words)

wordlist = words[0:]

def test_avg_guesses():
    beta, best_word = bot.solve()

    predicted_avg = beta / len(wordlist)
    print(best_word, predicted_avg)
    total_guessses = 0
    for i, ans in enumerate(wordlist):
        if not i % 10 and i > 0:
            print(f'Completed batch {i}: avg_guesses = {total_guessses / i}')
        depth = 1
        bot.words = wordlist[0:]
        bot.answer = ans
        guess = best_word
        while not bot.isCorrect(guess):
            partition = bot.result(guess)
            bot.words = [g for g in bot.words if bot.validHardmodeGuess(g, [guess], partitions=[partition])]
            guess = bot.solve()[1]
            depth += 1
        total_guessses += depth
    print(f'Predicted: {predicted_avg}, actual: {total_guessses / len(wordlist)}')

test_avg_guesses()