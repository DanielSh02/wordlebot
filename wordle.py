from pydoc import ispackage
import random

from numpy import indices, ndenumerate


default_word_list = []
with open("wordlists/valid-wordle-words.txt", "r") as words:
    for word in words:
        default_word_list.append(word.strip())


class Wordle():

    def __init__(self, words = default_word_list, guesses = 6, hardmode = True) -> None:
        self.words = words
        self.answer = random.choice(list(self.words))
        self.guesses = guesses
        self.hardmode = hardmode
        self.prev_guess = None
    
    def isCorrect(self, word: str) -> bool:
        return word == self.answer

    def validHardmodeGuess(self, guess, prev_word, partition=None):
        if not prev_word:
            return True
        if not partition:
            partition = self.result(prev_word)
        return self.result(guess, prev_word)
    
    def result(self, word: str, ans = None) -> list[int]:
        if not ans:
            ans = self.answer
        word = word.lower()
        if self.hardmode and not self.validHardmodeGuess(word, self.prev_guess):
            raise Exception("Invalid Guess")
        if not word in self.words:
            raise Exception("Invalid Guess")
        res = ""
        for i, c in enumerate(word):
            if c == ans[i]:
                res += "2"
            elif c not in ans:
                res += "0"
            else:
                word_indices = [i for i, x in enumerate(word) if x == c]
                correct_chars = len([i for i in word_indices if ans[i] == c])
                total = ans.count(c)
                if total >= len(word_indices) or i <= word_indices[total - 1 - correct_chars]:
                    res += "1"
                else:
                    res += "0"
        self.prev_guess = word
        return res 

    
    


        



