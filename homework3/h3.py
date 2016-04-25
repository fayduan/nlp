#!/usr/bin/python
#coding:utf-8

import sys, codecs

from model import Counter
from model import IBM1
from model import IBM2

#Open eng and chn corpus files, splits each line into lists
def read_corpus(eng_corpus, chn_corpus):
    en_f = codecs.open(eng_corpus,'r','utf-8')
    cn_f = codecs.open(chn_corpus,'r','utf-8')#open(chn_filename,'r')
    en = en_f.readlines()
    cn = cn_f.readlines()
    eng = [esentence.split() for esentence in en]
    chn = [csentence.split() for csentence in cn]
    en_f.close()
    cn_f.close()
    return eng, chn

#Main code for EM algorithm
def EM(counter, model, iterations):
    print "Calculate params..."
    for i in range(iterations):
        #Calls the Counter class to re-estimate the parameters for the model
        counts = counter.estimate_counts(model)
        #Updates the model with the new parameters
        model.recalculate(counts)
    print "Model Implement"
    return model

def implIBM1(eng, chn):
    #Initializes counter for model
    counter = Counter(eng, chn)
    #Calculates initial parameters for model
    counts = counter.initialize_counts()
    #Creates model using counts
    model = IBM1(counts)
    #Runs EM algorithm 5 times
    model = EM(counter, model, 5)
    return model

def implIBM2(model1, eng, chn):
    counter = Counter(eng, chn)
    #Initializes model using IBM Model 1
    model = IBM2(model1)
    #Removes model1 from memory
    del model1
    #Runs EM algorithm 5 times
    model = EM(counter, model, 5)
    return model

#Calculates alignments for the first k sentences of eng_corpus and chn_corpus in a given model
def align_sentences(output_filename,model, k, eng, chn):
    #output = codecs.open(output_filename, 'w','utf-8')
    output = codecs.open(output_filename,'wb','utf-8')
    #For each pair of sentences, find the alignment using the model
    for i in range(k):
        alignment = model.align(eng[i], chn[i])
        output.write(" ".join(eng[i]).encode('utf-8') + "\n")
        output.write(" ".join(chn[i]).encode('utf-8') + "\n")
        output.write(str(alignment) + "\n\n")

        #outstr =  " ".join(eng[i]) + "\n" + " ".join(chn[i]).encode('utf-8') + "\n" + str(alignment) + "\n"
        #output.write(outstr)

    output.close()
    print "Output close..."

#Function main 
if __name__ == '__main__':
    print "Read file..."
    eng_filename = sys.argv[1]
    chn_filename = sys.argv[2]
    eng,chn = read_corpus(eng_filename,chn_filename)

    print "IBM Model1"
    model1 = implIBM1(eng, chn)
    align_sentences('model1.result',model1,10000,eng,chn)

    print "IBM Model2"
    model2 = implIBM2(model1,eng,chn)
    align_sentences('model2.result',model2,10000,eng,chn)


    '''
    cn_f = codecs.open(chn_filename,'r','utf-8')#open(chn_filename,'r')#
    cn = cn_f.readlines()

    print cn
    print '-'*72
    for csentence in cn:
        print csentence
    print '-'*72 
    chn = [csentence.split() + ['NULL'] for csentence in cn]

    cn_f.close()

    print chn
    '''


#End