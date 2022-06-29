import random


default_word_list = []
with open("wordlists/valid-wordle-words.txt", "r") as words:
    for word in words:
        default_word_list.append(word.strip())


class Wordle():

    def __init__(self, words = default_word_list, guesses = 6) -> None:
        self.words = words
        self.answer = random.choice(list(self.words))
        print(self.answer)
        self.guesses = guesses
    
    def isCorrect(self, word: str) -> bool:
        return word == self.answer
    
    def result(self, word: str, ans) -> list[int]:
        word = word.lower()
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

    
    


        



