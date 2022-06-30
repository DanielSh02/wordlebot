from turtle import pos
from wordle import *


class Bot(Wordle):
    def __init__(self, words=["table", "tabbe", "fable", "juzzy", "simon", "tabby"], guesses=6) -> None:
        super().__init__(words, guesses)
        
    
    def solve(self):
        def minoverwords(guessable, possible_ans, guesses, beta = float("inf")):
            def heuristic_sort():
                letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
                freq = {letter: 0 for letter in letters}
                for w in possible_ans:
                    for c in w:
                        freq[c] += 1
                guessable.sort(key=lambda w: sum([freq[c] for c in w]), reverse = True)
            if guesses == 0: return float("inf"), None
            if len(possible_ans) == 1:
                return 1, possible_ans[0]
            heuristic_sort()
            if len(possible_ans) == 6:
                print(guessable)
            best_word = None
            for word in guessable:
                temp = beta
                beta = sumoverpartitions(guessable, possible_ans, guesses - 1, word, beta)
                if beta < temp:
                    best_word = word
            return beta, best_word

        def sumoverpartitions(guessable, possible_ans, guesses, word, beta):
            partitions = {}
            for ans in possible_ans:
                p = self.result(word, ans)
                if partitions.get(p):
                    partitions[p].append(ans)
                else:
                    partitions[p] = [ans]
            t = 0
            for p in partitions:
                t += minoverwords(filter(guessable, word, p), partitions[p], guesses, beta)[0]
                if t >= beta:
                    return beta
            return t

        def filter(possible_ans, word, partition):
            return possible_ans

    
        return minoverwords(self.words[0:], self.words[0:], self.guesses)