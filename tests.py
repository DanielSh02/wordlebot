import unittest
from bot import *
from wordle import *
import time
from main import gen_first_guesses

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

def count_guesses(guessable = list[str], possible_ans = list[str]) -> int:
    bot = Bot(words = guessable, possible_ans = possible_ans, guesses = 6)
    res = 0
    for i, ans in enumerate(possible_ans):
        bot.words = guessable
        bot.possible_ans = possible_ans
        p = None
        guesses = 0
        while p != "22222":
            guess = bot.solve(depth = 6 - guesses)[1]
            guesses += 1
            p = bot.result(guess, ans)
            bot.words = bot.filter(bot.words, guess, p)
            bot.possible_ans = bot.filter(bot.possible_ans, guess, p)
        res += guesses
    return res
            


def test_avg_guesses_with_lookup():
    bot = Bot()
    tot = 0 
    first_guesses = gen_first_guesses()
    for i, w in enumerate(default_ans_list):
        if not i % 100:
            print(f"Completed {i} words of {len(default_ans_list)}. Total guesses so far: {tot}")
        bot.words = default_word_list
        bot.possible_ans = default_ans_list
        guess = "SALET"
        p = bot.result(guess, w)
        g = 0
        while p != "22222":
            bot.words = bot.filter(bot.words, guess, p)
            bot.possible_ans = bot.filter(bot.possible_ans, guess, p)
            g += 1
            if guess == "SALET":
                guess = first_guesses[p]
            else:
                guess = bot.solve(depth = 6 - g)[1]
            p = bot.result(guess, w)
        tot += g + 1
    print(f'Average guesses: {tot / len(default_ans_list)}')
    return tot / len(default_ans_list)

wordle = Wordle(hardmode = False)
# bot = Bot()

class WordleTests(unittest.TestCase):
    
    def test_result(self):
        self.assertEqual(wordle.result("crane", "place"), "10202")
        self.assertEqual(wordle.result("crane", "jazzy"), "00100")
        self.assertEqual(wordle.result("tests", "jazzy"), "00000", "all 0s")
        self.assertEqual(wordle.result("radar", "alarm"), "11010", "double letters")
        self.assertEqual(wordle.result("geese", "elite"), "01002", "triple letters")
        self.assertEqual(wordle.result('gamba', 'maxim'), "02100", "double letters false")
        self.assertEqual(wordle.result("apart", "quart"), "00222", "apart quart")
        self.assertEqual(wordle.result("quart", "apart"), "00222", "quart apart")

    def test_hardmode(self):
        self.assertTrue(wordle.validHardmodeGuess("place", "crane", "10202"), msg = 'hardmode crane place')
        self.assertFalse(wordle.validHardmodeGuess('maxim', 'gamba', '02101'), msg = 'hardmode gamba maxim')


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

    def test_solve_simple(self):
        rhymes = ['fight', 'light', 'tight', 'right']
        rhyme_bot = Bot(words = rhymes, possible_ans=rhymes, guesses = 5)
        self.assertEqual(rhyme_bot.solve()[0], 10.0, msg = "rhyme bot")
        rhyme_bot.guesses = 3
        self.assertEqual(rhyme_bot.solve()[0], float("inf"), "not solvable")
        one_word_bot = Bot(words = ["arise"], possible_ans = ["arise"])
        self.assertEqual(one_word_bot.solve(), (1.0, "arise"), msg="one word bot")
        clear_answer_bot = Bot(words = ["plant", "jazzy", "print", "mouse"], 
                               possible_ans = ["plant", "jazzy", "print", "mouse"],
                               guesses = 6)
        self.assertEqual(clear_answer_bot.solve(), (7.0, "plant"), msg = "first guess partitions")

    def test_bot_night(self):
        self.maxDiff = None
        bot = Bot()
        bot.answer = "night"
        bot.words = bot.filter(bot.words, "salet", "00002")
        bot.possible_ans = bot.filter(bot.possible_ans, "salet", "00002")
        remaining = [
            "CRYPT", "DIGIT", "DRIFT", "FIGHT", "RIGHT", "TIGHT", "TWIXT", "WIGHT",
            "BIGOT", "DROIT", "IDIOT", "ORBIT", "PIVOT",
            "GROUT", "OUGHT", "TROUT",
            "INPUT", "UNCUT", "UNFIT",
            "BRUNT", "GRUNT",
            "COURT", "DOUBT",
            "JOINT",
            "POINT",
            "BURNT",
            "COUNT",
            "DONUT",
            "FRONT",
            "FRUIT",
            "INGOT",
            "MIGHT",
            "MOUNT",
            "NIGHT",
            "PRINT",
            "ROBOT",
            "VOMIT"]
        remaining = list(map(lambda w: w.lower(), remaining))
        self.assertCountEqual(remaining, bot.possible_ans)
        total, next_guess = bot.solve()
        word_list = bot.words[0:]
        def count_guesses(init_guess):
            tot = 0 
            for ans in remaining:
                guess = init_guess
                p = bot.result(guess, ans)
                guesses = 1
                while p != "22222":
                    bot.words = bot.filter(bot.words, guess, p)
                    bot.possible_ans = bot.filter(bot.possible_ans, guess, p)
                    guess = bot.solve()[1]
                    p = bot.result(guess, ans)
                    guesses += 1
                tot += guesses
                bot.words = word_list[0:]
                bot.possible_ans = remaining[0:]
            return tot
        tot = count_guesses(next_guess)
        d = {}
        self.assertEqual(total, tot, "expected[solve] = actual expected")
        self.assertEqual(total, 92, "expected value correct")


if __name__ == '__main__':
    unittest.main()
    # test_avg_guesses_with_lookup()


