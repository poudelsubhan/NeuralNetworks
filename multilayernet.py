#Written by Matt Wallace and Subhan Poudel on 7/28/17
#This is a neural network that decides whether a sentence is imperative or declarative through a multi-layer back-propogation neural net model.
#The program will stop once the number of iterations that you give it is over.
#The code is similar to neuralNet.py but uses a multi-layer back-propogation model

import sys
import nltk
from nltk.tokenize import sent_tokenize
from numpy import exp, array, random, dot



#Getting the data ready
def syntax_classifier(sentence):
    #Reads through a sentece, add a classification to each element and add the element and classification to a tuple.
    #Returns a list of tuples.
    tokens = nltk.word_tokenize(sentence)
    return nltk.pos_tag(tokens)

def bool_verb(sentText):
    #First input dendrite
    #Gets a list of tuples. Each tuple is style: (word, POS)
    #Returns bool for if there is a verb
    sentinel = 0
    for item in sentText:
        if 'V' in item[1]:
            sentinel = 1
    return sentinel

def bool_verbPos(senti):
    #Second input dendrite
    #Gets a list of tuples. Each tuple is style: (word, POS)
    #Returns bool if verb is at beginning and not gerund
    sent = 0
    if 'V' in senti[0][1]:
        sent = 1
    return sent

def bool_VBZ(sento):
    #Third input dendrite
    #Checks for the presence of a VBZ (verb singular third person) instance in the entire sentence
    senti = 0
    for item in sento:
        if item[1] == "VBZ":
            senti = 1
    return senti

def gerund_bool(sentence):
    #Fourth input dendrite
    #Checks for the presence of a gerund in a given sentence.
    for item in sentence:
        if item[1] == "VBG":
            return 1
        else:
            return 0

def gerund_first(sentence):
    #Fifth input dendrite
    #Checks for the presence of a gerund at the beginning of a sentence.
    if 'VBG' in sentence[0][1]:
        return 1
    else:
        return 0

def question_bool(sentence):
    c = len(sentence) -1 
    #Sixth input dendrite
    #Checks for the presence of a question mark in a given sentence
    if '?' in sentence[c][1] or '?' in sentence[c-1][1]:
        return 1
    else:
        return 0

def exclamation_bool(sentence):
    c = len(sentence) -1 
    #Seventh input dendrite
    #Checks for the presence of an exclamation point in a given sentence
    if '!' in sentence[c][1] or '!' in sentence[c-1][1]:
        return 1
    else:
        return 0

def colon_bool(sentence):
    #Eighth input dendrite
    #Checks for the presence of a colon instance in the entire sentence
    
    for item in sentence:
        if item[0] == ":":
            return 1
    return 0

def semi_colon_bool(sentence):
    #Ninth input dendrite
    #Checks for the presence of a semi-colon instance in the entire sentence
    
    for item in sentence:
        if item[0] == ";":
            return 1
    return 0

def proper_noun_bool(sentence):
    #Tenth input dendrite
    #Checks for the presence of a proper noun instance in the entire sentence
    
    for item in sentence:
        if item[1] == "NNP" or item[1] == "NNPS":
            return 1
    return 0
    
def input_builder(dataFile):
    #Reads in the data file.
    #outputs a list of lists that contains boolean values.
    listSent = []
    with open(dataFile, 'r') as op:
        for line in op:
            results = []
            i = line.split(' ~')
            tokenTag = syntax_classifier(i[0])

            #first input dendrite
            verBool = bool_verb(tokenTag)
            results.append(verBool)

            #second input dendrite
            posVerb = 0
            if verBool == 1:
                posVerb = bool_verbPos(tokenTag)
            results.append(posVerb)
            
            #third input dendrite
            verbVBZ = 0
            if verBool == 1:
                verbVBZ = bool_VBZ(tokenTag)
            results.append(verbVBZ)

            #Fourth input dendrite
            verbGerund = 0
            if verBool == 1:
                verbGerund = gerund_bool(tokenTag)
            results.append(verbGerund)

            #Fifth input dendrite
            gerundFirst = 0
            if verbGerund == 1:
                gerundFirst = gerund_first(tokenTag)
            results.append(gerundFirst)

            #Sixth input dendrite
            questionMark = question_bool(tokenTag)
            results.append(questionMark)

            #Seventh input dendrite
            exclamationMark = exclamation_bool(tokenTag)
            results.append(exclamationMark)

            #Eighth input dendrite
            colonMark = colon_bool(tokenTag)
            results.append(colonMark)

            #Ninth input dendrite
            semiColonMark = semi_colon_bool(tokenTag)
            results.append(semiColonMark)

            #Tenth input dendrite
            properNoun = proper_noun_bool(tokenTag)
            results.append(properNoun)

            #add results to the overall list
            listSent.append(results)  
    return listSent

def output_builder(dataFile):
    #Reads in the data file
    #outputs a list of lists of answers. [[0, 1, 1, 0]]
    ansList = []
    with open(dataFile, 'r') as fp:
        anotherList = []
        for line in fp:
            i = line.split(' ~')
            i[1] = i[1].replace('\n', '')
            anotherList.append(int(i[1]))
    ansList.append(anotherList)
    return ansList

class DeepNet():
    def __init__(self):
        self.learn_rate = 1.0
        self.bias_j = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        self.bias_k = 1.0
        #These are the hidden Z values:
        self.z_values = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        self.k_values = 0.0
        
        #Creates a random array of 10 length arrays
        random.seed(1)
        self.weights_j = random.rand(10,10)
        #Creates a random array of 10 length arrays
        random.seed(2)
        self.weights_k = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


    
    def train(self,train_inputs,train_outputs,iterations):
        for num in xrange(iterations):
            index = 0
            for item in train_inputs:
                #Currently in a single sentence,
                #we are calc'ing vals for hidden z unit
                z_int = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                for j in xrange(10):
                    z_int[j] = self.bias_j[j]
                    for i in xrange(10):
                        z_int[j] += item[i]*self.weights_j[i][j]
                for l in xrange(10):
                    self.z_values[l] = bi_sigmoid(z_int[l])
                    
                #Calc'ing vals for output k unit
                y_int = self.bias_k
                for k in xrange(10):
                    for j in xrange(10):
                        y_int += self.z_values[j]*self.weights_k[k]
                self.k_values = bi_sigmoid(y_int)

                #Backpropogation of Error
                error_k = (train_outputs[0][index] - self.k_values) * derivative(y_int)
                weight_corr_Y = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                for i in xrange(10):
                    weight_corr_Y[i] = self.learn_rate * error_k * self.z_values[i]
                bias_k_change = self.learn_rate * error_k

                error_In_Z = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                for k in xrange(10):
                    error_In_Z[k] = error_k * self.weights_k[0][k]
                error_Z = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                for i in xrange(10):
                    error_Z[i] = error_In_Z[i] * derivative(z_int[i])
                weight_corr_Z = random.rand(10,10)
                for i in xrange(10):
                    for j in xrange(10):
                        weight_corr_Z[i][j] = self.learn_rate * error_Z[j] * item[i]
                bias_j_change = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                for i in xrange(10):
                    bias_j_change[i] = self.learn_rate * error_Z[i] 

                #Updates weights and biases
                for x in xrange(10):
                    self.weights_k[x] += weight_corr_Y[x]
                self.bias_k += bias_k_change

                for i in xrange(10):
                    for j in xrange(10):
                        self.weights_j[i][j] += weight_corr_Z[i][j]
                for i in xrange(10):
                    self.bias_j[i] += bias_j_change[i]
                
                index += 1
                
    
    def bi_sigmoid(value):
        return (2.0/(1+exp(-value))) - 1 

    def derivative(value):
        return (0.5)*(1+bi_sigmoid(value))*(1-bi_sigmoid(value))

    
def main():
    test = DeepNet()
    print test.weights_j
    print "HEYYY"
    print test.weights_k


main()
