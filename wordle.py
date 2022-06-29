from email.policy import default
import random


default_word_list = set()
with open("wordlists/valid-wordle-words.txt", "r") as words:
    for word in words:
        default_word_list.add(word.strip())


class Wordle():

    def __init__(self, words = default_word_list, guesses = 6) -> None:
        self.words = words
        self.answer = random.choice(list(self.words))
        print(self.answer)
        self.guesses = guesses
    
    def isCorrect(self, word: str) -> bool:
        return word == self.answer
    
    def result(self, word: str) -> list[int]:
        word = word.lower()
        print(self.words)
        print(word in self.words)
        if not word in self.words:
            raise Exception("Invalid Guess")
        res = []
        for i, c in enumerate(word):
            if c == self.answer[i]:
                res.append(2)
            elif c in self.answer:
                res.append(1)
            else:
                res.append(0)
        return res


    
    


        



