import os

from MarkovComments import MarkovComments


class MatchSim:

    def __init__(self, fileDirectory):
        self.fileDirectory = fileDirectory
        self.models = self.createDictOfModels()
        self.outcomeMarkov = self.models['outcomes.txt']
        print('madeMatchSim')
        prefix = ['START0','START1']
        while input('q to quit') != 'q':
            word = self.outcomeMarkov.generate_next_word(' '.join(prefix))
            print(word)
            prefix[0] = prefix[1]
            prefix[1] = word
            thisModel = self.models[word+'.txt']
            print(thisModel.generate_sequence(thisModel.startPrefix,30))
        # print(self.outcomeMarkov.generate_sequence('START', 5)[6:])    #  for outcomes.txt n = 1

    def createDictOfModels(self):
        models = {}
        address = os.getcwd() + '/' + self.fileDirectory
        for filename in os.listdir(address):
            models[filename] = MarkovComments(2,self.fileDirectory + '/' + filename)
        return models

Ms = MatchSim('9-matches-punctuation-in-word')  # scrapedSequences # 9-matches-punctuation-in-word
