# NeuralNetworks
Project from summer 2017. These programs are part of step, a bigger project that I am working together with @lemons2lemonade.

These neural nets all use different models to determine if given sentences are declarative "-1" or imperative "1."

In summary, each sentence is tagged by us as declarative and imperative and then fed into the neural nets to train them to recognize the type of these sentences themselves. Each sentence is transformed into a list of 10 binary values that represent the sentence so the nueral nets can operate on them. Some examples of the 10 inputs are "Is there a verb?" and "Is there a gerund?" in the sentence. It is recommended that the training set is large so the neural nets can effectively determine type. I have added "50-50-split.txt" as an example of a testing set and "ign30out.txt" as an example of a training set. Note that the given testing set only has 100 sentences with 50 being imperative and 50 being declarative. It is recommended that the training set be much larger. The testing set has 30 sentences.


"dataTagger.py" is a program that recieves a ".txt" file as input and asks you to classify whether each sentence in that file is imperative "1" or declarative "-1." The program is necessary to create the training set and testing set for the different nueral nets. See "50-50-split.txt" and "ign30out.txt" for examples of outputs from this program.

"neuralNet.py" contains code that recieves files created by "dataTagger.py" as inputs for the training set and for testing. It contains code to transform each sentence to a set of n (currently 10) inputs that the neural net actually uses to determine sentence type. This is a classic nerual net model.

"perceptron.py" contains code that recieves files created by "dataTagger.py" as inputs for the training set and for testing. It contains code to transform each sentence to a set of n (currently 10) inputs that the neural net actually uses to determine sentence type. This program uses a perceptron type model.

"multilayernet.py" contains code that recieves files created by "dataTagger.py" as inputs for the training set and for testing. It contains code to transform each sentence to a set of n (currently 10) inputs that the neural net actually uses to determine sentence type. This program uses a multi-layer back-propogation type model.
