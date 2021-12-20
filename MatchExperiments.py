import matplotlib.pyplot as mp
import MatchSim

data = (1, 2, 3, 4, 5)

fig, sample_chart = mp.subplots()
sample_chart.plot(data)

mp.show()

Ms = MatchSim('scrapedSequences', com_n=4, outcome_n=2)  # scrapedSequences # 9-matches-punctuation-in-word
innings = Ms.simulateOneInnings()

class MatchExperimenter:

    def __init__(self):
        self.purpose = None
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

