from turtle import pos
from wordle import *


class Bot(Wordle):
    def __init__(self, words=["salet", "slate", "spunk", "jazzy"], guesses=6) -> None:
        super().__init__(words, guesses)
        
    
    def solve(self):

        cache = {}

        def minoverwords(guessable, possible_ans, guesses, beta = float("inf")):
            # for x in cache:
                # print(f"{x}: {cache[x]}")
            def heuristic_sort():
                letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
                freq = {letter: 0 for letter in letters}
                for w in possible_ans:
                    for c in w:
                        freq[c] += 1
                guessable.sort(key=lambda w: sum([freq[c] for c in w]), reverse = True)

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
                print("cache used!")
                return cache[hash]
            heuristic_sort()
            best_word = None
            for word in guessable:
                temp = beta
                beta = sumoverpartitions(guessable, possible_ans, guesses - 1, word, beta)
                if beta < temp:
                    best_word = word
            # Adds m(G, P, g) to the cache
            cache[hash] = beta, best_word
            return beta, best_word

        def sumoverpartitions(guessable, possible_ans, guesses, word, beta):
            partitions = {}
            for ans in possible_ans:
                p = self.result(word, ans)
                if partitions.get(p):
                    partitions[p].append(ans)
                else:
                    partitions[p] = [ans]
            partitions = dict(sorted(partitions.items(), key=lambda item: item[1]))
            t = 0
            for p in partitions:
                t += minoverwords(filter(guessable, word, p), partitions[p], guesses, beta)[0]
                if t >= beta:
                    return beta
            return t

        def filter(guessable, word, partition):
            if not self.hardmode:
                return guessable
            return [g for g in guessable if self.validHardmodeGuess(g, [word], partitions=[partition])]


    
        return minoverwords(self.words[0:], self.words[0:], self.guesses)