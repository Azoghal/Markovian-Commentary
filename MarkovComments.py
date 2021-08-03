import warnings

import numpy as np
import scipy.sparse
from sklearn.preprocessing import normalize

class MarkovComments:

    def __init__(self, n):
        self.data = open('scrapedSequences/outcomes.txt','r').readline()
        self.tokens = self.data.split()
        #self.tokens_distinct = list(set(self.tokens))
        self.tokens_to_id, self.id_to_tokens = MarkovComments.create_indices(self.tokens)
        self.n = n  ## consider needing to add START multiple times to the start of phrases when wanting to use ngrams
        self.ngrams, self.ngrams_distinct = self.create_ngrams()
        self.ngrams_to_id, self.id_to_ngrams = MarkovComments.create_indices(self.ngrams)
        self.transition_matrix_prob = self.create_transition_matrix_prob()


    @staticmethod
    def create_indices(values):
        ind = 0
        val_to_ind = {}
        ind_to_val = {}
        for v in values:
            if v not in val_to_ind:
                val_to_ind[v] = ind
                ind_to_val[ind] = v
                ind = ind + 1
        return val_to_ind, ind_to_val

    def create_ngrams(self):
        sequences = [self.tokens[i:] for i in range(self.n)]
        ngrams = [' '.join(ngram) for ngram in list(zip(*sequences))]
        return ngrams, list(set(ngrams))  #  ngrams a list of all 2 grams, also return one w/o duplicates

    def create_transition_matrix(self):
        row_ind, col_ind, values = [], [], []

        for i in range(len(self.tokens[:-self.n])):
            ngram = ' '.join(self.tokens[i:i + self.n])  # the seen ngram
            ngram_index = self.ngrams_to_id[ngram]  # index of the seen ngram
            next_word_index = self.tokens_to_id[self.tokens[i+self.n]]  # index of the following word

            row_ind.extend([ngram_index])
            col_ind.extend([next_word_index])
            values.extend([1])

        S = scipy.sparse.coo_matrix((values, (row_ind, col_ind)))  #  , shape=(len(self.ngrams_to_id), len(self.tokens_to_id)))
        return S  ## remember to then set counts for X->START and END->X to be 0 ???

    def create_transition_matrix_prob(self):
        transition_matrix = self.create_transition_matrix()
        return normalize(transition_matrix, norm='l1', axis=1)

    def check_prefix(self, prefix):
        p_list = prefix.split(' ')[-self.n:]  #  gets up to n from end of prefix text
        prefix = ' '.join(p_list)
        if (len(p_list) < self.n):
            warnings.warn('Prefix too short, giving random')
            return np.random.choice(self.ngrams)
        elif prefix not in self.ngrams:
            warnings.warn('Prefix not in model, giving random')
            return np.random.choice(self.ngrams)
        return prefix


    def generate_next_word(self, prefix, temperature=1):
        prefix = self.check_prefix(prefix)
        prefix_id = self.ngrams_to_id[prefix]
        weights = self.transition_matrix_prob[prefix_id].toarray()[0]
        #do temperature stuff?
        token_id = np.random.choice(range(len(weights)), p=weights)
        next_word = self.id_to_tokens[token_id]
        return next_word

    def generate_sequence(self, seed, k=10, temperature=1):
        prefix = self.check_prefix(seed)
        sequence = seed.split()
        for i in range(k):
            next_word = self.generate_next_word(prefix,temperature=temperature)
            if (next_word == 'END1') or next_word == 'END':
                break
            sequence.append(next_word)
            prefix = ' '.join(sequence[-self.n:])

        return ' '.join(sequence)

MC = MarkovComments(1)
while(input("q to quit") != 'q'):
    #print(MC.generate_sequence('START1 START2 START3', 100)[21:])
    #print(MC.generate_sequence('START2 START3', 100)[14:])
    #print(MC.generate_sequence('START3', 100)[7:])
    print(MC.generate_sequence('START', 100)[6:])

#print(MC.generate_sequence(np.random.choice(MC.ngrams), 100))q
