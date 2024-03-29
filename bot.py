from math import log2
from wordle import *

class Bot(Wordle):
    def __init__(self, words=default_word_list, possible_ans = default_ans_list, guesses=6) -> None:
        super().__init__(words, guesses, possible_ans)

    def result(self, word: str, ans: str = None) -> list[int]:
        self.prev_guess = None
        return super().result(word, ans)

    def gen_partitions(self, word: str, possible_ans: list[str]) -> list[str]:
            partitions = {}
            for ans in possible_ans:
                p = self.result(word, ans)
                if partitions.get(p):
                    partitions[p].append(ans)
                else:
                    partitions[p] = [ans]
            return partitions

    def filter(self, lst: list[str], word: str, partition: str) -> list[str]:
            if not self.hardmode:
                return lst
            return [g for g in lst if self.validHardmodeGuess(g, word, partition)]

    def solve(self, guessable: list[str] = None, possible_ans: list[str] = None, depth = 6) -> tuple[float, str]:
        if guessable is None:
            guessable = self.words

        if possible_ans is None:
            possible_ans = self.possible_ans

        cache = {}

        def entropy(word: str, possible_ans: list[str]) -> float:
            p = self.gen_partitions(word, possible_ans)
            n = len(possible_ans)
            res = 0
            for x in p:
                px = len(p[x]) / n
                res -= px * log2(px)
            return res
        
        def heuristic_sort(guessable: list[str], possible_ans: list[str]):
                letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
                freq = {letter: 0 for letter in letters}
                for w in possible_ans:
                    for c in w:
                        freq[c] += 1
                guessable.sort(key=lambda w: sum([freq[c] for c in w]), reverse = True)

        def minoverwords(guessable: list[str], possible_ans: list[str], guesses: int, beta: float = float("inf")):
            # for x in cache:
                # print(f"{x}: {cache[x]}")

            # Defines a tuple to place m(G, P, g) in the cache.
            def cache_hash():
                if not self.hardmode:
                    return tuple(sorted(possible_ans)), guesses
                return tuple(sorted(guessable)), tuple(sorted(possible_ans)), guesses
           
            if guesses == 0: return float("inf"), None
            if len(possible_ans) == 1:
                return 1, possible_ans[0]
            # Lookup m(G, P, g) in the cache
            hash = cache_hash()
            if cache.get(hash):
                # print("cache used!")
                return cache[hash]
            guessable.sort(key = lambda w: entropy(w, possible_ans), reverse = True)
            # heuristic_sort(guessable, possible_ans)
            best_word = None
            for word in guessable:
                temp = beta
                beta = sumoverpartitions(guessable, possible_ans, guesses - 1, word, beta)
                if beta < temp:
                    best_word = word
            beta += len(possible_ans)
            # Adds m(G, P, g) to the cache
            cache[hash] = beta, best_word
            return beta, best_word

        def sumoverpartitions(guessable: list[str], possible_ans: list[str], guesses: int, word: str, beta: float) -> float:
            partitions = self.gen_partitions(word, possible_ans)
            partitions = dict(sorted(partitions.items(), key=lambda item: item[1]))
            t = 0 
            # If t in possible_ans, we should not count the partition "22222"
            if word in possible_ans:
                t -= 1
            for p in partitions:
                t += minoverwords(self.filter(guessable, word, p), partitions[p], guesses, beta)[0]
                if t >= beta:
                    return beta
            return t

    
        return minoverwords(guessable, possible_ans, depth)
