import random

class Wordle():

    def __init__(self, guesses = 6) -> None:
        self.words = ["apple", "simon", "chess", "table", "glass"]
        self.answer = random.choice(self.words)
        self.guesses = guesses
    
    def isCorrect(self, word: str) -> bool:
        return word == self.answer
    
    def result(self, word: str) -> list[int]:
        word = word.lower()
        if word not in self.words:
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
    
    


        



