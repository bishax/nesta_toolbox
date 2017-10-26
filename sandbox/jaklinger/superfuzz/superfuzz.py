import math
from functools import reduce

def superfuzz(s1,s2,algs,length_norm=False):
    # Calculate the score from each algorithm
    scores = [alg(s1,s2) for alg in algs]
    # Score = Sqrt(Sum_a(score_a^2) / N_a)
    scores_sqrd = map(lambda x:x*x,scores)
    sum_scores_sqrd = reduce(lambda x,y:x+y,scores_sqrd)    
    score = math.sqrt(sum_scores_sqrd / len(scores))
    # Calculate length normalisation
    norm = 1
    if length_norm:
        norm = len(s1)/len(s2)
        if norm > 1:
            norm = 1/norm
    # Done
    return score * norm

if __name__ == "__main__":
    from fuzzywuzzy import fuzz
    s1 = "joel is a good student for a limited time"
    s2 = "a limited god studies time"
    
    print(superfuzz(s1,s2,[fuzz.ratio]))
    print(superfuzz(s1,s2,[fuzz.ratio],length_norm=True))
    print(superfuzz(s1,s2,[fuzz.ratio,fuzz.token_sort_ratio]))
    print(superfuzz(s1,s2,[fuzz.ratio,fuzz.token_sort_ratio],length_norm=True))    
                    
