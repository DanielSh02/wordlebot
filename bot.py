from turtle import pos
from wordle import *


class Bot(Wordle):
    def __init__(self, words=["table", "tabbe", "fable", "juzzy"], guesses=6) -> None:
        super().__init__(words, guesses)
        
    
    def solve(self):
        print(self.words)
        def minoverwords(guessable, possible_ans, guesses, beta = float("inf")):
            if guesses == 0: return float("inf"), None
            if len(possible_ans) == 1:
                return 1, possible_ans[0]
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
            print("got to t!")
            return t

        def filter(possible_ans, word, partition):
            return possible_ans

        return minoverwords(self.words, self.words, self.guesses)

            
        
        # def minoverwords(T,H,g,β=infinity):
            # if g==0: return infinity
            # for w in T:
            #     β=sumoverpartitions(T,H,g-1,w,β)
            # return β

            # def sumoverpartitions(T,H,g,w,β):
            # Let s_1,...,s_k denote the possible colour scores (GBYBG etc) of H with the trial word w,
            #     and H_1,...,H_k denote the corresponding subsets of H
            # t=0
            # for i in {1,...,k}:
            #     t=t+minoverwords(filter(T,w,s_i), H_i, g, β)
            #     if t>=β: return β
            # return t

            # def filter(T,w,s):
            # If easy mode: return T
            # If hard mode: return {t in T | t is an allowable test word in hard mode given that word w has scored s}