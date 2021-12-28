import matplotlib.pyplot as mp
import MatchSim

'''
data = (1, 2, 3, 4, 5)

fig, sample_chart = mp.subplots()
sample_chart.plot(data)

mp.show()

'''

class MatchExperimenter:

    def __init__(self):
        self.match_simulator = MatchSim.MatchSim('scrapedSequences', com_n=4, outcome_n=2)
        data = self.innings_total_run_distribution()
        fig, sample_chart = mp.subplots()
        sample_chart.hist(data,bins=50)
        mp.show()
        # SINGLE INNINGS
        # TODO: plot distribution of total runs
        # TODO: plot overlay of worms
        # TODO: plot distribution of wickets taken
        # TODO: plot distribution of boundaries
        # TODO: plot distribution over different window sizes?
        # TODO: scatter of wickets, runs
        # TODO: something considering average length of innings?
        # BOTH INNINGS
        # TODO: give probability of win based on total?
        # TODO: probability of winning batting first or second
        # REAL WORLD
        # TODO: compile data (another scraper?)
        # TODO: plot graps
        # TODO: compare, fine tune model?

    def innings_total_run_distribution(self):
        scores = []
        for i in range(10000):
            if i%100==0:
                print(i)
            scores.append(self.match_simulator.simulateOneInnings().total)
        return scores

ME = MatchExperimenter()