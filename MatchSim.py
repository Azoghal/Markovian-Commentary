from MarkovComments import MarkovComments


class MatchSim:

    def __init__(self, fileDirectory):
        print('madeMatchSim')
        self.fileDirectory = fileDirectory
        self.outcomeMarkov = MarkovComments(1, fileDirectory+'/outcomes.txt')
        print(self.outcomeMarkov.generate_sequence('START', 5)[6:])    #  for outcomes.txt n = 1


Ms = MatchSim('scrapedSequences')
