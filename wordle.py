import random

from numpy import indices

default_word_list = []
with open("wordlists/valid-wordle-words.txt", "r") as words:
    for word in words:
        default_word_list.append(word.strip())

default_ans_list = []
with open("wordlists/possible_ans.txt", "r") as words:
    for word in words:
        default_ans_list.append(word.strip())


class Wordle():

    def __init__(self, words = default_word_list, guesses = 6, possible_ans = default_ans_list, hardmode = True) -> None:
        self.words = words
        self.possible_ans = possible_ans
        self.answer = random.choice(list(self.words))
        self.guesses = guesses
        self.hardmode = hardmode
        self.prev_guess = None
    
    def isCorrect(self, word: str) -> bool:
        return word == self.answer

    def validHardmodeGuess(self, guess: str, prev_word: str = None, partition: str = None) -> bool:
        if not prev_word:
            return True
        if not partition:
            partition = self.result(prev_word)
        return self.result(prev_word, guess) == partition
    
    def result(self, word: str, ans: str = None) -> str:
        if not ans:
            ans = self.answer
        word = word.lower()
        if self.hardmode and not self.validHardmodeGuess(word, self.prev_guess):
            raise Exception("Invalid Guess")
        res = ""
        for i, c in enumerate(word):
            if c == ans[i]:
                res += "2"
            elif c not in ans:
                res += "0"
            else:
                word_indices = [j for j, x in enumerate(word) if x == c]
                correct_chars = len([j for j in word_indices if ans[j] == c])
                total = ans.count(c)
                try:
                    if correct_chars >= total:
                        res += "0"
                    elif total >= len(word_indices) + correct_chars or i <= word_indices[total - correct_chars - 1]:
                        res += "1"
                    else:
                        res += "0"
                except IndexError:
                    print(word, ans,i, word_indices, total, correct_chars)
        self.prev_guess = word
        return res 
