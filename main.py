from wordle import *
from bot import *

def main():
    wordle = Wordle()
    guesses = 0
    while guesses <= wordle.guesses:
        try:
            guesses += 1
            guess = input("Enter your guess: ")
            if wordle.isCorrect(guess):
                print(f"Congrats! You won in {guesses} guesses!")
                break
            else:
                print(wordle.result(guess, wordle.answer))
        except:
            print("Not a valid word")

            
bot = Bot(guesses=100)
print(bot.result("table", "fable"))
print(bot.solve())