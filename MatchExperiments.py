import math

import matplotlib.pyplot as mp
import MatchSim
import json
import numpy as np
import pandas

'''
data = (1, 2, 3, 4, 5)

fig, sample_chart = mp.subplots()
sample_chart.plot(data)

mp.show()

'''

class MatchExperimenter:

    def __init__(self):
        self.innings_dicts = self.load_innings_to_dict()
        self.innings_df = self.undictify_innings(self.innings_dicts)
        self.limits = self.get_limits()
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

    def create_match_sim(self):
        self.match_simulator = MatchSim.MatchSim('scrapedSequences', com_n=4, outcome_n=2)

    def run_and_save_n(self,n):
        self.save_innings(self.dictify_innings(self.run_n_innings(n)))

    def run_n_innings(self, n=10000):
        innings = []
        for i in range(n):
            if i % 100 == 0:
                print(i)
            innings.append(self.match_simulator.simulateOneInnings())
        return innings

    def dictify_innings(self, all_innings):
        all_dicts = {}
        for i,innings in enumerate(all_innings):
            in_dict = {'runs': innings.runs,
                       'extras': innings.extras,
                       'total': innings.total,
                       'wickets': innings.wickets,
                       'totalBalls': innings.totalBalls,
                       'legalBalls': innings.legalBalls,
                       'fallOfWickets': innings.fallOfWickets,
                       'fours': innings.fours,
                       'sixes': innings.sixes,
                       'maidens': innings.maidens}
            all_dicts[i] = in_dict
        return all_dicts

    def undictify_innings(self,all_innings):    # convert to pandas dataframe
        innings_df = pandas.DataFrame.from_dict(all_innings,orient='index')
        return innings_df

    def get_limits(self):
        limits = {'runs': (self.innings_df['runs'].min(), self.innings_df['runs'].max(),len(pandas.unique(self.innings_df['runs']))),
                  'extras': (self.innings_df['extras'].min(), self.innings_df['extras'].max(),len(pandas.unique(self.innings_df['extras']))),
                  'total': (self.innings_df['total'].min(), self.innings_df['total'].max(),len(pandas.unique(self.innings_df['total']))),
                  'wickets': (self.innings_df['wickets'].min(), self.innings_df['wickets'].max(),len(pandas.unique(self.innings_df['wickets']))),
                  'totalBalls': (self.innings_df['totalBalls'].min(), self.innings_df['totalBalls'].max(),len(pandas.unique(self.innings_df['totalBalls']))),
                  'legalBalls': (self.innings_df['legalBalls'].min(), self.innings_df['legalBalls'].max(),len(pandas.unique(self.innings_df['legalBalls']))),
                  'fours': (self.innings_df['fours'].min(), self.innings_df['fours'].max(),len(pandas.unique(self.innings_df['fours']))),
                  'sixes': (self.innings_df['sixes'].min(), self.innings_df['sixes'].max(),len(pandas.unique(self.innings_df['sixes']))),
                  'maidens': (self.innings_df['maidens'].min(), self.innings_df['maidens'].max(),len(pandas.unique(self.innings_df['maidens'])))}
                    # no need for entry for fall of wickets
        for key, value in limits.items():
            print(key, value)
        return limits

    def save_innings(self, innings_dicts):
        print('saving')
        with open('data.txt', 'w') as outfile:
            json.dump(innings_dicts, outfile)

    def load_innings_to_dict(self):
        print('loading')
        with open('data.txt', 'r') as readfile:
            return json.load(readfile)

    def calculate_bin_limits(self, key):
        min, max, unique = self.limits[key]
        dif = max - min  # min: 2, max:4, values = 2,3,4 then we need > 2 unique values to have 3 equal bins
        if unique > dif:  # pigeon hole, with bin size 1 we can have at least one value per bin.
            bin_size = 1
        else:  # min 0, max 10, unique values = 0,3,6,10. ceil(10/4) = 3 so we get bins for 0 1 2|3 4 5|6 7 8|9 10 11
            bin_size = 2*int(math.ceil(float(dif + 1) / float(unique)))  # plus one to centre on integers?
        print('chosen bin size:', bin_size)
        bin_start, bin_end = min - 0.5, max + 0.5
        bins = np.arange(bin_start, bin_end, bin_size)
        return bins

    def innings_histogram_from_key(self, key, bins=50):
        print('getting', key, 'distribution')
        values = self.innings_df[key]
        bins = self.calculate_bin_limits(key)
        print(bins)
        fig, sample_chart = mp.subplots()
        sample_chart.hist(values, bins=bins)
        mp.xlabel(key)
        mp.show()

    def scatter_plot_histograms_from_keys(self,x_key,y_key):
        print('getting', x_key, 'against',y_key, 'distribution')
        x_values = self.innings_df[x_key]
        y_values = self.innings_df[y_key]
        left, width = 0.1, 0.65
        bottom, height = 0.1, 0.65
        spacing = 0.005
        rect_scatter = [left, bottom, width, height]
        rect_histx = [left, bottom + height + spacing, width, 0.2]
        rect_histy = [left + width + spacing, bottom, 0.2, height]
        fig = mp.figure(figsize=(8,8))
        ax = fig.add_axes(rect_scatter)
        ax.scatter(x_values, y_values,alpha=0.05)
        #ax.imshow(np.array([x_values, y_values]))
        ax_histx = fig.add_axes(rect_histx, sharex=ax)
        ax_histy = fig.add_axes(rect_histy, sharey=ax)
        ax_histx.hist(x_values, bins=self.calculate_bin_limits(x_key))
        ax_histy.hist(y_values, bins=self.calculate_bin_limits(y_key), orientation='horizontal')
        mp.xlabel(x_key)
        mp.ylabel(y_key)
        mp.show()

ME = MatchExperimenter()
ME.innings_histogram_from_key('total')
ME.scatter_plot_histograms_from_keys('fours', 'sixes')
'''
ME.innings_histogram_from_key('total', bins=50)
ME.innings_histogram_from_key('wickets', bins=10)
ME.innings_histogram_from_key('fours', bins=40)
ME.innings_histogram_from_key('sixes', bins=20)
ME.innings_histogram_from_key('extras', bins=35)
ME.innings_histogram_from_key('runs', bins=40)
ME.innings_histogram_from_key('maidens', bins=10)
'''
