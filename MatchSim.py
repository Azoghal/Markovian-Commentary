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
        self.total = 0
        self.wickets = 0
        self.totalBalls = 0
        self.legalBalls = 0
        # extra stats
        self.fallOfWickets = {}
        self.fours = 0
        self.sixes = 0
        self.history = []
        self.maidens = 0

    def updateState(self, ball):
        self.runs = self.runs + ball.runs
        self.extras = self.extras + ball.extras
        self.total = self.runs + self.extras
        self.wickets = self.wickets + ball.wicket
        self.totalBalls = self.totalBalls + 1
        self.legalBalls = self.legalBalls + ball.overIncrementsBy
        self.history.append(ball)
        self.updateStatistics(ball)
        if self.legalBalls % 6 == 0: # at end of over (and not at first ball of )
            if len(self.history) == 6:
                sixDots = True
                for b in self.history:
                    if b.runs >0 or b.overIncrementsBy == 0: # not a dot if runs scored or a wide or a no ball
                        sixDots = False
                if sixDots:
                    self.maidens = self.maidens + 1
            if ball.overIncrementsBy == 1:  # don't empty if a bowler extra (at start of over)
                self.history = []   # empty history for next over


    def updateStatistics(self, ball):
        if ball.wicket:
            self.fallOfWickets[self.wickets] = self.total   # make sure to be aware if running before or after updatestate
        if ball.runs == 4:
            self.fours = self.fours + 1
        if ball.runs == 6:
            self.sixes = self.sixes + 1

    def printStatistics(self):
        print('Fours:'.rjust(10), str(self.fours).ljust(5))
        print('Sixes:'.rjust(10), str(self.sixes).ljust(5))
        print('Maidens:'.rjust(10), str(self.maidens).ljust(5))
        print('Wicket:'.rjust(10), ' '.join(str(key).ljust(5) for key in self.fallOfWickets))
        print('Runs:'.rjust(10), ' '.join(str(self.fallOfWickets[key]).ljust(5) for key in self.fallOfWickets))

    def printState(self):
        overs = self.legalBalls // 6
        balls = self.legalBalls % 6
        print(str(self.total) + '-' + str(self.wickets) + '  ' + str(overs) + '.' + str(balls) + ' Overs')

class MatchSim:

    def __init__(self, fileDirectory, com_n, outcome_n):
        self.fileDirectory = fileDirectory
        self.com_n = com_n
        self.outcome_n = outcome_n
        self.models = self.createDictOfModels()
        self.outcomeMarkov = self.models['outcomes.txt']
        self.outcomeDict = self.initialiseOutcomes()
        print('madeMatchSim')

    def simulateMatch(self, comm):
        inningsA = self.simulateOneInnings(commentary=comm)
        inningsB = self.simulateOneInnings(commentary=comm, target=inningsA.total)
        inningsA.printStatistics()
        print()
        inningsB.printStatistics()
        self.compareInnings(inningsA, inningsB)

    def simulateOneInnings(self, target=10000, showOutput=True, scoreEveryBall=False, commentary=False):
        inState = inningsState()
        prefix = [('START' + str(i)) for i in range(self.outcome_n, self.com_n)]
        while inState.legalBalls < 300 and inState.wickets < 10 and inState.total <= target:
            word = 'END'
            while word == 'END':
                word = self.outcomeMarkov.generate_next_word(' '.join(prefix))  # do not allow match to end early
            for ind in range(self.outcome_n-1):
                prefix[ind] = prefix[ind+1]
            prefix[self.outcome_n-1] = word
            thisModel = self.models[word + '.txt']
            inState.updateState(self.outcomeDict[word])
            if showOutput:
                if commentary:  # risk of infinite loop if destined for END
                    print(word.ljust(15), ':', thisModel.generate_sequence(thisModel.startPrefix, 30)[7*self.com_n-1:])
                if scoreEveryBall:
                    inState.printState()
                else:
                    if inState.legalBalls % 6 == 0 or inState.wickets == 10:
                        inState.printState()
                        print()
        # print(self.outcomeMarkov.generate_sequence('START', 5)[6:])    #  for outcomes.txt n = 1
        return inState

    def compareInnings(self, first, second):
        print()
        print('First Innings: ')
        first.printState()
        print('Second Innings: ')
        second.printState()
        firstTotal = first.runs + first.extras
        secondTotal = second.runs + second.extras
        if firstTotal > secondTotal:
            print('Team A wins by', firstTotal - secondTotal, 'runs!')
        elif firstTotal == secondTotal:
            print('It\'s a tie!')
        else:
            print('Team B wins by', 10-second.wickets, 'wickets!')

    def createDictOfModels(self):
        models = {}
        address = os.getcwd() + '/' + self.fileDirectory
        for filename in os.listdir(address):
            if filename == 'outcomes.txt':
                models[filename] = MarkovComments(self.outcome_n, self.fileDirectory + '/' + filename)
            else:
                models[filename] = MarkovComments(self.com_n, self.fileDirectory + '/' + filename)
        return models

    def initialiseOutcomes(self):                                           #       rebowl
        outcomeDict = {}                                                    #   R  E  v  W
        outcomeDict['(no_ball)'] =                  outcome('(no_ball)',        0, 1, 0, 0)
        outcomeDict['(no_ball)_1_run'] =            outcome('(no_ball)_1_run',  1, 1, 0, 0)
        outcomeDict['(no_ball)_2_runs'] =           outcome('(no_ball)_2_runs', 2, 1, 0, 0)
        outcomeDict['(no_ball)_4_byes'] =           outcome('(no_ball)_4_byes', 0, 5, 0, 0)
        outcomeDict['(no_ball)_4_runs'] =           outcome('(no_ball)_4_runs', 4, 1, 0, 0)
        outcomeDict['(no_ball)_6_runs'] =           outcome('(no_ball)_6_runs', 6, 1, 0, 0)
        outcomeDict['1_bye'] =                      outcome('1_bye',            0, 1, 1, 0)
        outcomeDict['1_leg_bye'] =                  outcome('1_leg_bye',        0, 1, 1, 0)
        outcomeDict['1_run,_OUT'] =                 outcome('1_run,_OUT',       1, 0, 1, 1)
        outcomeDict['1_run'] =                      outcome('1_run',            1, 0, 1, 0)
        outcomeDict['1_wide'] =                     outcome('1_wide',           0, 1, 0, 0)
        outcomeDict['2_byes'] =                     outcome('2_byes',           0, 2, 1, 0)
        outcomeDict['2_leg_byes'] =                 outcome('2_leg_byes',       0, 2, 1, 0)
        outcomeDict['2_runs'] =                     outcome('2_runs',           2, 0, 1, 0)
        outcomeDict['2_wide'] =                     outcome('2_wide',           0, 2, 0, 0)
        outcomeDict['3_runs'] =                     outcome('3_runs',           3, 0, 1, 0)
        outcomeDict['3_wide'] =                     outcome('3_wide',           0, 3, 0, 0)
        outcomeDict['3_leg_byes'] =                 outcome('3_leg_byes',       0, 3, 1, 0)
        outcomeDict['4_runs'] =                     outcome('4_runs',           4, 0, 1, 0)
        outcomeDict['4_byes'] =                     outcome('4_byes',           0, 4, 1, 0)
        outcomeDict['4_leg_byes'] =                 outcome('4_leg_byes',       0, 4, 1, 0)
        outcomeDict['5_wide'] =                     outcome('5_wide',           0, 5, 0, 0)
        outcomeDict['6_runs'] =                     outcome('6_runs',           6, 0, 1, 0)
        outcomeDict['no_run'] =                     outcome('no_run',           0, 0, 1, 0)
        outcomeDict['OUT'] =                        outcome('OUT',              0, 0, 1, 1)
        return outcomeDict

#Ms = MatchSim('scrapedSequences', com_n=4, outcome_n=2)  # scrapedSequences # 9-matches-punctuation-in-word
#Ms.simulateMatch(comm=True)


'''         # find an innings with at least 400 runs
iterations = 0
inState = inningsState()
highest = 0
while inState.total < 400:
    inState = Ms.simulateOneInnings(showOutput=False)
    iterations = iterations + 1
    if inState.total > highest:
        highest = inState.total
    if iterations%512 == 0:
        print(iterations, 'iterations. Highest: ', highest)

print(iterations,'iterations')

inState.printStatistics()
inState.printState()
'''

'''inState = inningsState()     # test the maiden detection
dot = outcome('no_run', 0, 0, 1, 0)
notDot = outcome('not_dot', 2, 0, 1, 0)
wide = outcome('wide',0,1,0,0)
bye = outcome('bye',0,1,1,0)
wicket = outcome('wicket',0,0,1,1)

inState.updateState(notDot)
inState.updateState(notDot)
inState.updateState(notDot)
inState.updateState(wicket)
inState.updateState(notDot)
inState.updateState(notDot)
inState.updateState(wide)
inState.updateState(dot)
inState.updateState(dot)
inState.updateState(dot)
inState.updateState(dot)
inState.updateState(dot)
inState.updateState(dot)
inState.updateState(dot)
inState.updateState(dot)
inState.updateState(wicket)
inState.updateState(dot)
inState.updateState(dot)
inState.updateState(dot)
inState.printState()
inState.printStatistics()
'''
