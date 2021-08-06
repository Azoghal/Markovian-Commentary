import os

from MarkovComments import MarkovComments


class outcome:
    def __init__(self, name, runs, extras=0, overIncrement=1, wicket=0):
        self.name = name
        self.runs = runs
        self.extras = extras
        self.overIncrementsBy = overIncrement
        self.wicket = wicket

class inningsState:
    def __init__(self):
        self.runs = 0
        self.extras = 0
        self.wickets = 0
        self.totalBalls = 0
        self.legalBalls = 0

    def updateState(self, ball):
        self.runs = self.runs + ball.runs
        self.extras = self.extras + ball.extras
        self.wickets = self.wickets + ball.wicket
        self.totalBalls = self.totalBalls + 1
        self.legalBalls = self.legalBalls + ball.overIncrementsBy

    def printState(self):
        overs = self.legalBalls // 6
        balls = self.legalBalls % 6
        print(str(self.runs) + '-' + str(self.wickets) + '  ' + str(overs) + '.' + str(balls) + ' Overs')

class MatchSim:

    def __init__(self, fileDirectory):
        self.fileDirectory = fileDirectory
        inState = inningsState()
        self.models = self.createDictOfModels()
        self.outcomeMarkov = self.models['outcomes.txt']
        print('madeMatchSim')
        prefix = ['START0', 'START1']
        self.batterRuns = 0
        self.extraRuns = 0
        self.validBalls = 0
        self.totalBalls = 0
        self.wickets = 0
        outcomeDict = self.initialiseOutcomes()
        while inState.legalBalls < 300 and inState.wickets < 10:
            word = 'END'
            while word == 'END':
                word = self.outcomeMarkov.generate_next_word(' '.join(prefix)) # do not allow match to end early
            prefix[0] = prefix[1]
            prefix[1] = word
            thisModel = self.models[word+'.txt']
            inState.updateState(outcomeDict[word])
            print(word)                                                         # risk of infinite loop if destined for END
            print(thisModel.generate_sequence(thisModel.startPrefix,30))
            inState.printState()
            # if inState.legalBalls % 6 == 0 or inState.wickets == 10:
            #   inState.printState()
            #print('\n')
        # print(self.outcomeMarkov.generate_sequence('START', 5)[6:])    #  for outcomes.txt n = 1

    def createDictOfModels(self):
        models = {}
        address = os.getcwd() + '/' + self.fileDirectory
        for filename in os.listdir(address):
            models[filename] = MarkovComments(2,self.fileDirectory + '/' + filename)
        return models



    def initialiseOutcomes(self):                                           #       rebowl
        outcomeDict = {}                                                    #   R  E  v  W
        outcomeDict['(no_ball)'] =                  outcome('(no_ball)',        0, 1, 0, 0)
        outcomeDict['(no_ball)_1_run'] =            outcome('(no_ball)_1_run',  1, 1, 0, 0)
        outcomeDict['(no_ball)_2_runs'] =           outcome('(no_ball)_2_runs', 2, 1, 0, 0)
        outcomeDict['(no_ball)_4_byes'] =           outcome('(no_ball)_4_byes', 0, 5, 0, 0)
        outcomeDict['(no_ball)_4_runs'] =           outcome('(no_ball)_4_runs', 4, 1, 0, 0)
        outcomeDict['1_bye'] =                      outcome('1_bye',            0, 1, 1, 0)
        outcomeDict['1_leg_bye'] =                  outcome('1_leg_bye',        0, 1, 1, 0)
        outcomeDict['1_run,_OUT'] =                 outcome('1_run,_OUT',       1, 0, 1, 1)
        outcomeDict['1_run'] =                      outcome('1_run',            1, 0, 1, 0)
        outcomeDict['1_wide'] =                     outcome('1_wide',           0, 1, 0, 0)
        outcomeDict['2_leg_byes'] =                 outcome('2_leg_byes',       0, 2, 1, 0)
        outcomeDict['2_runs'] =                     outcome('2_runs',           2, 0, 1, 0)
        outcomeDict['2_wide'] =                     outcome('2_wide',           0, 2, 0, 0)
        outcomeDict['3_runs'] =                     outcome('3_runs',           3, 0, 1, 0)
        outcomeDict['3_wide'] =                     outcome('3_wide',           0, 3, 0, 0)
        outcomeDict['4_runs'] =                     outcome('4_runs',           4, 0, 1, 0)
        outcomeDict['4_leg_byes'] =                 outcome('4_leg_byes',       0, 4, 1, 0)
        outcomeDict['5_wide'] =                     outcome('5_wide',           0, 5, 0, 0)
        outcomeDict['6_runs'] =                     outcome('6_runs',           6, 0, 1, 0)
        outcomeDict['no_run'] =                     outcome('no_run',           0, 0, 1, 0)
        outcomeDict['OUT'] =                        outcome('OUT',              0, 0, 1, 1)
        return outcomeDict

Ms = MatchSim('scrapedSequences')  # scrapedSequences # 9-matches-punctuation-in-word
