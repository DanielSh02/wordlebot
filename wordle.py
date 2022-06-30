import enum
import random

from numpy import ndenumerate


default_word_list = []
with open("wordlists/valid-wordle-words.txt", "r") as words:
    for word in words:
        default_word_list.append(word.strip())


class Wordle():

    def __init__(self, words = default_word_list, guesses = 6, hardmode = True) -> None:
        self.words = words
        self.answer = random.choice(list(self.words))
        print(self.answer)
        self.guesses = guesses
        self.hardmode = hardmode
    
    def isCorrect(self, word: str) -> bool:
        return word == self.answer

    def validHardmodeGuess(self, guess, prev_words, partitions=None):
        if not partitions:
            partitions = [self.result(w) for w in prev_words]
        for depth, w in enumerate(prev_words):
            for i, c in enumerate(partitions[depth]):
                if c == '2' and guess[i] != w[i]:
                    return False
                if c == '1' and (guess[i] == w[i] or w[i] not in guess):
                    return False
                if c == '0' and (w[i] in guess):
                    return False
        return True 
    
    def result(self, word: str, ans = None) -> list[int]:
        if not ans:
            ans = self.answer
        word = word.lower()
        # TODO: Implement checking for valid guesses in hardmode.
        if not word in self.words:
            raise Exception("Invalid Guess")
        res = ""
        for i, c in enumerate(word):
            if c == ans[i]:
                res += "2"
            elif c in ans:
                res += "1"
            else:
                res += "0"
        return res 

    
    


        



