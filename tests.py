from email.policy import default
import unittest
from bot import *
from wordle import *
import time

words = random.sample(default_word_list, 500)
bot = Bot(words=words, guesses=5)
# print(words)

wordlist = words[0:]

def test_avg_guesses():
    start = time.time()
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
            bot.words = bot.filter(bot.words, guess, partition)
            guess = bot.solve()[1]
            depth += 1
        total_guessses += depth
    print(f'Predicted: {predicted_avg}, actual: {total_guessses / len(wordlist)}')
    end = time.time()
    print(end - start)

wordle = Wordle(hardmode = False)
# bot = Bot()

class WordleTests(unittest.TestCase):
    
    def test_result(self):
        self.assertEqual(wordle.result("crane", "place"), "10202")
        self.assertEqual(wordle.result("crane", "jazzy"), "00100")
        self.assertEqual(wordle.result("tests", "jazzy"), "00000", "all 0s")
        self.assertEqual(wordle.result("radar", "alarm"), "11010", "double letters")
        self.assertEqual(wordle.result("geese", "elite"), "01002", "triple letters")
        with self.assertRaises(Exception, msg="invalid guess exception"):
            wordle.result("xxxxx", "crane")

    def test_hardmode(self):
        self.assertTrue(wordle.validHardmodeGuess("place", "crane", "10202"))

    def test_gen_partitions(self):
        possible_ans = ["crane",
                        "train",
                        "jazzy",
                        "simon",
                        "plane",
                        "flout",
                        "clout",
                        "arise"]
        self.assertDictEqual(bot.gen_partitions("arise", possible_ans), 
                             {"12002": ["crane"], 
                              "12100": ["train"],
                              "10000": ["jazzy"],
                              "00110": ["simon"],
                              "10002": ["plane"],
                              "00000": ["flout", "clout"],
                              "22222": ["arise"]},
                             msg = "gen_partitions med")


# if __name__ == '__main__':
#     unittest.main()
test_avg_guesses()  

