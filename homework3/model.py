#!/usr/bin/python
#coding:utf-8

import collections, math, itertools

#Creates a counts class to keep track of all count and alignment parameters
class Counts:
    def __init__(self):
        #Stores c(e) values
        self.word = collections.defaultdict(int)
        #Stores c(e,f) values
        self.words = collections.defaultdict(int)
        #Stores c(i,l,m) values
        self.alignment = collections.defaultdict(int)
        #Stores c(j,i,l,m) values
        self.alignments = collections.defaultdict(int)

#Creates a model class to store parameters for a given model
class Model:
    #Sets new parameters
    def recalculate(self, counts):
        self.counts = counts
        self.initialize_step = False
        self.initialize_step_2 = False
    #Probability of an alignment -- different for IBM 1 and 2, so won't specify here
    def p(self, e, f, j, i, l, m):
        pass
    #Calculates t parameter
    def t(self, f, e):
        #If it is our first time running IBM 1, set t values to 1/n(e)
        if self.initialize_step:
            return 1.0 / self.counts.word[e]
        #Otherwise, calculate t normally
        else:
            if self.counts.word[e] > 0:
                return self.counts.words[(e, f)] / self.counts.word[e]
            else:return 0
    #Given an eng sentence and a chn sentence, produces a list containing alignment values
    def align(self, esent, fsent):
        l = len(esent)
        m = len(fsent)
        alignment = []
        #For each word in the chn sentence, find the alignment with the highest probability
        for i, f_i in enumerate(fsent):
            j, p = amax([(j, self.p(e_j, f_i, j, i, l, m)) for j, e_j in enumerate(esent)])
            alignment.append(j)
        return alignment

#Creates a special class for IBM Model 1
class IBM1(Model):
    def __init__(self, counts):
        #Tells Model class to calculate t parameters as 1/n(e) for this iteration
        self.initialize_step = True
        self.initialize_step_2 = False
        self.counts = counts
    #In IBM Model 1, p only depends on t parameters
    def p(self, e, f, j, i, l, m):
        return self.t(f, e)

#Creates a special class for IBM Model 2
class IBM2(Model):
    #Initiates using IBM Model 1
    def __init__(self, model1):
        self.initialize_step = False
        #Indicates that this is our first time running IBM Model 2, important for setting q parameters
        self.initialize_step_2 = True
        self.counts = model1.counts
    #Sets q parameters
    def q(self, j, i, l, m):
        if self.initialize_step_2:
            return 1.0 / (l + 1.0)
        else:
            if self.counts.alignment[(i,l,m)] > 0.0:
                return self.counts.alignments[(j, i, l, m)] / self.counts.alignment[(i, l, m)]
            else:
                return 0.0
    #Defines p parameters for model 2, where p depends on t and q parameters
    def p(self, e, f, j, i, l, m):
        return self.t(f,e) * self.q(j, i, l, m)

#Creates a counter class to calculate initial counts from the corpus and update them using the EM algorithm
class Counter:
    def __init__(self, eng_corpus, chn_corpus):
        #Matches each sentence in the eng corpus with the corresponding sentence in the chn corpus
        self.both = zip(eng_corpus, chn_corpus)
    #Runs through the corpus and populates the Counts class dictionaries 
    def initialize_counts(self):
        #Creates new instance of Counts class
        self.initial_counts = Counts()
        #For each pair of sentences in the corpus
        for e, f in self.both:
            #For each eng word in the sentence
            for e_j in e:
                #For each chn word in the sentence
                for f_i in f:
                    key = (e_j, f_i)
                    #Checks if word pair is in words dictionary; if not, adds it
                    if key not in self.initial_counts.words:
                        self.initial_counts.words[key] = 1.0
                        #Checks if eng word is in word dictionary; if not, adds it
                        if e_j not in self.initial_counts.word:
                            self.initial_counts.word[e_j] = 1.0
                        #If so, increments it
                        else:
                            self.initial_counts.word[e_j] += 1.0
                    #If so, increments it
                    else:
                        self.initial_counts.words[key] += 1.0
        return self.initial_counts
    #Updates parameters according to the IBM Model 1
    def estimate_counts(self, model):
        #Creates new instance of Counts class
        counts = Counts()
        #For each pair of sentences
        for k, (e, f) in enumerate(self.both):
            #Sets l and m length variables
            l = len(e)
            m = len(f)
            #For each word in the chn sentence
            for i, f_i in enumerate(f):
                #Calculates denominator of delta value
                denominator = sum((model.p(e_j, f_i, j, i, l, m) for (j, e_j) in enumerate(e)))
                #For each word in the eng sentence, increment each count by delta
                for j, e_j in enumerate(e):
                    if denominator > 0.0:
                        delta = model.p(e_j, f_i, j, i, l, m) / denominator
                    else:
                        delta = 0
                    counts.words[(e_j, f_i)] += delta
                    counts.word[e_j] += delta
                    counts.alignments[(j, i, l, m)] += delta
                    counts.alignment[(i, l, m)] += delta
        return counts

def amax(l):
    if not l:
        return None, 0
    else:
        return max(l, key = lambda x: x[1])