from collections import Counter
import nltk
import numpy as np
import pandas as pd
import re 

class AutoCompounder:
    '''Extracts commonly associated words by extracting recursively smaller common n-grams,
    where the "commoness" of an n-gram is defined by it's frequency with respect to the mean
    number of occurences, and the standard deviation of occurences. The threshold parameter
    (which controls the minimum number of standard deviations required for an n-gram to pass the
    selection) is automatically determined according to when the change in word frequency
    becomes 'stable' with threshold change. 'Stable' is defined as a threshold range of <alpha>
    standard deviation in which the change in word frequency is less than <beta>. The maximum 
    size of n-grams, from which the algorithm starts, is given by the <max_context> parameter.
    '''

    def __init__(self,max_context=10,alpha=5,beta=0.05,
                 extra_stops=[],max_threshold=20.25,
                 threshold_increments=0.25,
                 default_stops=nltk.corpus.stopwords.words('english')):

        # Parameters from constructor
        self.max_context = max_context
        self.alpha = alpha
        self.beta = beta        
        self.max_threshold = max_threshold
        self.threshold_increments = threshold_increments
        self.stops = default_stops + extra_stops        

        # Data to be filled
        self.data = []
        self.thresholds = {}
        self.compounds = []
        self.drop = {}
        
    def _extract_subsentences(self,sentences):
        '''Split up sentences sub-sentences, based on any non-alphanum'''
        _sentences = []
        for _sentence in sentences:
            # Ignore dodgy inputs
            if pd.isnull(_sentence):
                continue
            # Tokenise on any non-alphanum
            _sub_sentences = [x.rstrip(" ").lstrip(" ").lower() 
                              for x in re.split('[^a-zA-Z\d\s]',_sentence)]
            # Ignore empty sentences
            if _sub_sentences != []:
                _sentences += _sub_sentences
        return _sentences

    def process_sentences(self,sentences):
        '''Iteratively extract compounds from sentences'''
        # Extract nested sentences, e.g. from paragraphs
        print("Extracting nested sentences...")
        _sentences = self._extract_subsentences(sentences)
        print("Extracted a total of",len(_sentences),"sentences")
        # Iterate over context range
        the_range = np.arange(self.max_context,1,-1)
        for _context in the_range:
            # Remove any previous compounds from the sentence
            for _c in self.compounds:
                _sentences = [_s.replace(" ".join(_c),"") for _s in _sentences
                              if not pd.isnull(_s)]
            # Get compounds for this context
            self.compounds += self._process_sentences(_sentences,_context)
        # Select the compound words within the required context
        self.compounds = [_c for _c in self.compounds
                          if not self.drop[len(_c)]]

    def _process_sentences(self,sentences,context):
        '''Extract compounds from sentences with a given context'''
        compounds = []
        for words in self._preprocess(sentences):
            # Get all compounds in this sentence
            for _compound in nltk.ngrams(words,context):
                # Ignore words starting or ending in stops
                first_word = _compound[0]
                last_word = _compound[-1]
                if ((first_word in self.stops or first_word.isdigit()) or
                    (last_word in self.stops or last_word.isdigit())):
                    continue
                # Append compound
                compounds.append(_compound)
        
        # Count compounds
        counts = Counter(compounds)
        count_values = [x for x in counts.values()]
        # Calculate the mean and std
        mean = np.mean(count_values)
        std = np.std(count_values)
        
        # Calculate the threshold data for this context
        first = sum(1 for _compound,_count in counts.items()
                    if _count > mean)
        last_frac = 0
        best_threshold = 0
        found_any = False        
        for i in np.arange(0,self.max_threshold,self.threshold_increments):
            total = sum(1 for _compound,_count in counts.items()
                        if _count > mean + i*std)
            # Calculate the total fraction removed due to this threshold
            frac_removed = (first - total)/first
            
            # The calculate the change in the fraction removed
            if last_frac > 0:
                delta = (frac_removed - last_frac)/last_frac
            # Defined as 1 until a non-zero fraction is removed
            else:
                delta = 1
            # If the change is greater than beta, and not in a region
            # of continuity (defined by alpha)            
            if (best_threshold + self.alpha >= i) or not found_any:
                if delta > self.beta:
                    found_any = True
                    #print('\t',i,total,delta)
                    best_threshold = i
            last_frac = frac_removed
            
            # Append results for analysis
            self.data.append(dict(threshold=i,context=context,total=total))
        # If no threshold found
        if best_threshold == (self.max_threshold - self.threshold_increments):
            best_threshold = 0
        self.thresholds[context] = best_threshold
        
        # Filter out the compounds passing the threshold condition
        for _compound,_count in counts.items():            
            if _count <= mean + best_threshold*std:
                compounds = list(filter((_compound).__ne__, compounds))
        # Return unique compounds
        compounds = set(compounds)        
        self.drop[context] = (len(compounds) == first) 
        return compounds

    def _preprocess(self,sentences):
        _sentences = []
        for _sentence in sentences:
            # Split sentences into words
            words = nltk.word_tokenize(_sentence)
            words = list(filter(lambda w: not w.isdigit(),words))
            _sentences.append(words)
        return _sentences

    def print_sorted_compounds(self):
        '''Method for printing compounds'''
        c = [(" ".join(c)) for c in self.compounds]
        for _c in sorted(c):
            print(_c)

#___________________
# Example of how to run
if __name__ == "__main__":

    from nltk.corpus import brown
    text = brown.words(categories='news')
    sentences = " ".join(text).split(".")    

    # Instantiate autocompounder, considerering a maximum of 8-grams
    # and not forming n-grams containing additional stop words
    autocomp = AutoCompounder(max_context=8,
                              extra_stops=['said','one','two','three'])
    # Build the compounds
    autocomp.process_sentences(sentences)
    # Print out results
    autocomp.print_sorted_compounds()

    # Note: compounds can be accessed from autocomp.compounds
    # if you want to filter these from your original words, you
    # should start with large n-grams, and recurse to small n-grams
