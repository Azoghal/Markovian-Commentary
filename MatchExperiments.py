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
        self.match_simulator = None
        self.innings_dicts = None
        self.innings_df = None
        self.limits = None
        # SINGLE INNINGS
        # DONE: plot distribution of total runs
        # DONE: plot overlay of worms
        # DONE: plot distribution of wickets taken
        # DONE: plot distribution of boundaries
        # TODO: plot distribution over different window sizes?
        # DONE: scatter of wickets, runs
        # DONE:?something considering average length of innings?

        # BOTH  INNINGS
        # DONE: give probability of win based on total? - from cumfreq
        # NO:   probability of winning batting first or second - same

        # REAL  WORLD
        # TODO: compile data (another scraper?)
        # TODO: plot graphs
        # TODO: compare, fine tune model?

    def run_and_load_in(self, n=10000):
        self.create_match_sim()
        self.run_and_save_n(n)
        self.load_in()

    def load_in(self):
        self.innings_dicts = self.__class__.load_innings_to_dict()
        self.innings_df = self.__class__.undictify_innings(self.innings_dicts)
        self.limits = self.get_limits(self.innings_df)

    def create_match_sim(self):
        self.match_simulator = MatchSim.MatchSim('scrapedSequences', com_n=4, outcome_n=2)

    def run_and_save_n(self, n):
        self.save_innings(self.dictify_innings(self.run_n_innings(n)))

    def run_n_innings(self, n=10000):
        innings = []
        for i in range(n):
            if i % 100 == 0:
                print(i)
            innings.append(self.match_simulator.simulateOneInnings())
        return innings

    @staticmethod
    def dictify_innings(all_innings):
        all_dicts = {}
        for i, innings in enumerate(all_innings):
            in_dict = {'runs': innings.runs,
                       'extras': innings.extras,
                       'total': innings.total,
                       'wickets': innings.wickets,
                       'totalBalls': innings.totalBalls,
                       'legalBalls': innings.legalBalls,
                       'fallOfWickets': innings.fallOfWickets,
                       'total_and_wickets_each_over': innings.total_and_wickets_each_over,
                       'fours': innings.fours,
                       'sixes': innings.sixes,
                       'maidens': innings.maidens}
            all_dicts[i] = in_dict
        return all_dicts

    @staticmethod
    def undictify_innings(all_innings):    # convert to pandas dataframe
        innings_df = pandas.DataFrame.from_dict(all_innings, orient='index')
        return innings_df

    def get_limits(self, df):
        limits = {'runs': (df['runs'].min(),
                           df['runs'].max(),
                           len(pandas.unique(df['runs']))),
                  'extras': (df['extras'].min(),
                             df['extras'].max(),
                             len(pandas.unique(df['extras']))),
                  'total': (df['total'].min(),
                            df['total'].max(),
                            len(pandas.unique(df['total']))),
                  'wickets': (df['wickets'].min(),
                              df['wickets'].max(),
                              len(pandas.unique(df['wickets']))),
                  'totalBalls': (df['totalBalls'].min(),
                                 df['totalBalls'].max(),
                                 len(pandas.unique(df['totalBalls']))),
                  'legalBalls': (df['legalBalls'].min(),
                                 df['legalBalls'].max(),
                                 len(pandas.unique(df['legalBalls']))),
                  'fours': (df['fours'].min(),
                            df['fours'].max(),
                            len(pandas.unique(df['fours']))),
                  'sixes': (df['sixes'].min(),
                            df['sixes'].max(),
                            len(pandas.unique(df['sixes']))),
                  'maidens': (df['maidens'].min(),
                              df['maidens'].max(),
                              len(pandas.unique(df['maidens'])))}
        # no need for entry for fall of wickets
        for key, value in limits.items():
            print(key, value)
        return limits

    @staticmethod
    def save_innings(innings_dicts, name='data.txt'):
        print('saving')
        with open(name, 'w') as outfile:
            json.dump(innings_dicts, outfile)

    @staticmethod
    def load_innings_to_dict(name='data.txt'):
        print('loading')
        with open(name, 'r') as readfile:
            return json.load(readfile)

    def calculate_bin_limits(self, key, mmu=None, df=None):
        if mmu is None:
            if df is None:
                min, max, unique = self.limits[key]
            else:
                min, max, unique = self.get_limits(df=df)[key]
        else:
            min, max, unique = mmu

        dif = max - min  # min: 2, max:4, values = 2,3,4 then we need > 2 unique values to have 3 equal bins
        if unique > dif:  # pigeon hole, with bin size 1 we can have at least one value per bin.
            bin_size = 1
        elif unique > dif*0.9:  # for the cases where thin tails have gaps, but 1-bins are still sensible
            bin_size = 1
        else:  # min 0, max 10, unique values = 0,3,6,10. ceil(10/4) = 3 so we get bins for 0 1 2|3 4 5|6 7 8|9 10 11
            bin_size = 4*int(math.ceil(float(dif + 1) / float(unique)))  # plus one to centre on integers?
        print('chosen bin size:', bin_size)
        bin_start, bin_end = min - 0.5, max + 0.5
        print(bin_start,bin_end)
        bins = np.arange(bin_start, bin_end+0.1, bin_size)
        return bins

    def cumulative_frequency_curve(self, key):
        values = self.innings_df[key]
        n = len(values)
        min,max, unique = self.limits[key]
        n = max-min
        values, base = np.histogram(values, bins=n)
        print(base)
        print(values)
        cumulative = np.cumsum(values)
        print(cumulative)
        fig, sample_chart = mp.subplots()
        sample_chart.plot(base[:-1], cumulative/10, c='blue')
        mp.yticks(np.arange(0, 100 + 1, 10.0))
        mp.xlabel(key)
        mp.show()

    def innings_histogram_from_file(self, filename, key):
        with open(filename,'r') as f:
            values = []
            v = f.readline()
            while v:
                values.append(int(v))
                v = f.readline()
            print(values[0:10])
            print(len(values))
            bins =  np.arange(-0.5, 500.51, 10)
            fig, sample_chart = mp.subplots()
            sample_chart.hist(values, bins=bins)
            mp.xlabel(key)
            mp.show()

    def get_stats_from_file(self, filename='evaluation_outcomes.txt'):
        with open(filename, 'r') as f:
            values = f.readlines()
            innings_list = []
            outcome_dict = MatchSim.MatchSim.initialiseOutcomes()
            need_new = set()
            for v in values:
                first_innings = MatchSim.inningsState()
                second_innings = MatchSim.inningsState()
                splittened = v.split('END')
                first = splittened[0].split(' ')[4:-1]
                second = splittened[1].split(' ')[5:-1]
                for outcome in first:
                    if outcome not in outcome_dict:
                        need_new.add(outcome)
                    else:
                        outcome_obj = outcome_dict[outcome]
                        first_innings.updateState(outcome_obj)
                for outcome in second:
                    if outcome not in outcome_dict:
                        need_new.add(outcome)
                    else:
                        outcome_obj = outcome_dict[outcome]
                        second_innings.updateState(outcome_obj)
                innings_list.append(first_innings)
                innings_list.append(second_innings)
            print('UNSUPPORTED OUTCOMES', need_new)
            print(len(innings_list), 'innings')
            dictified = self.dictify_innings(innings_list)
            dataframified = self.undictify_innings(dictified)
            #print(dataframified.head(5)) comparing to link shows correct stats
            return dataframified

    def innings_histogram_from_key(self, key, df=None):
        print('getting', key, 'distribution')
        if df is None:
            values = self.innings_df[key]
            bins = self.calculate_bin_limits(key)
            title='generated'
        else:
            values = df[key]
            bins = self.calculate_bin_limits(key, df=df)
            title='scraped'
        #print(bins)
        fig, sample_chart = mp.subplots()
        sample_chart.hist(values, bins=bins)
        mp.xlabel(key)
        mp.title(title)
        mp.show()

    def scatter_plot_histograms_from_keys(self, x_key, y_key):
        print('getting', x_key, 'against', y_key, 'distribution')
        x_values = self.innings_df[x_key]
        y_values = self.innings_df[y_key]
        left, width = 0.1, 0.65
        bottom, height = 0.1, 0.65
        spacing = 0.005
        rect_scatter = [left, bottom, width, height]
        rect_histx = [left, bottom + height + spacing, width, 0.2]
        rect_histy = [left + width + spacing, bottom, 0.2, height]
        fig = mp.figure(figsize=(8, 8))
        ax = fig.add_axes(rect_scatter)
        ax.scatter(x_values, y_values, alpha=0.05)
        ax_histx = fig.add_axes(rect_histx, sharex=ax)
        ax_histy = fig.add_axes(rect_histy, sharey=ax)
        ax_histx.hist(x_values, bins=self.calculate_bin_limits(x_key))
        ax_histy.hist(y_values, bins=self.calculate_bin_limits(y_key), orientation='horizontal')
        mp.xlabel(x_key)
        mp.ylabel(y_key)
        mp.show()

    def worm_plot(self,n=10,df=None):
        if df is None:
            df = self.innings_df
        fig, sample_chart = mp.subplots()
        alpha = 1 if n <= 10 else 0.05
        show_wickets = n <= 10
        col = None if n <= 10 else 'b'
        for index in range(n):
            #index = 3
            sample_points = df['total_and_wickets_each_over'][index]
            end_total = df['total'][index]
            end_overs = (df['legalBalls'][index]//6) + (df['legalBalls'][index]%6)/10
            end_wickets = df['wickets'][index]


            current_wickets = 0
            wicket_overs = []
            wicket_over_runs = []
            runs = [0]
            overs = [0]
            for over, pair in enumerate(sample_points,1):
                if pair[1] > current_wickets:
                    wicket_overs.append(over)
                    wicket_over_runs.append(pair[0])
                    current_wickets += 1
                runs.append(pair[0])
                overs.append(over)
            if runs[-1] != end_total:
                runs.append(end_total)
                overs.append(end_overs)
            if current_wickets != end_wickets:
                for k in range(end_wickets-current_wickets):
                    wicket_overs.append(end_overs)
                    wicket_over_runs.append(end_total)
            sample_chart.plot(overs, runs, c=col, alpha=alpha)
            if show_wickets:
                sample_chart.scatter(wicket_overs, wicket_over_runs)
        mp.xlabel('overs')
        mp.ylabel('runs')
        mp.show()

    def get_win_percentage(self,total, verbose=True):   # large number pre simulated innings
        values = self.innings_df['runs']                # so better to use those than recompute for monte carlo
        n = len(values)
        min, max, unique = self.limits['runs']
        if total < min:
            if verbose:
                print('lower than minimum simulated, close to 0% chance to win')
            return 0.
        if total > max:
            if verbose:
                print('higher than maximum simulated, close to 100% chance to win')
            return 1.
        n = max - min
        values, base = np.histogram(values, bins=n)
        cumulative = np.cumsum(values)
        if verbose:
            print(cumulative[total-min]/10, '% chance to win with', total,'runs')
        return cumulative[total-min]/1000

    def make_first_innings_win_prediction(self, runs, wickets, balls, search_num=50): # monte carlo to finish innings
        #finish simulating first innings, then use static win percentage              # and then use precomputed
        #can do monte carlo and simulate many times
        if self.match_simulator is None:
            self.create_match_sim()
        total_runs = 0
        total_prob = 0
        for i in range(search_num):
            innings_state = MatchSim.inningsState()
            innings_state.runs = runs
            innings_state.total = runs
            innings_state.wickets = wickets
            innings_state.totalBalls = balls
            innings_state.legalBalls = balls
            innings_state.fallOfWickets = {n+1: runs for n in range(wickets)}
            result = self.match_simulator.simulateOneInnings(continue_from=innings_state)
            total_prob += self.get_win_percentage(result.total,verbose=False)
            total_runs += result.total
        print('average:', total_runs/search_num)
        chance_to_win_1 = self.get_win_percentage(total_runs//search_num, verbose=False)
        print('chance to win based on chance to win with average runs:', chance_to_win_1)
        chance_to_win_2 = total_prob/search_num
        print('chance to win based on average of chance to win over all sims:', chance_to_win_2)


    def make_second_innings_win_prediction(self, runs, wickets, balls, first_innings_runs, search_num=200):
        #finish simulating first innings, then use static win percentage    # monte carlo forward to find % of sims won
        #can do monte carlo and simulate many times
        if self.match_simulator is None:
            self.create_match_sim()
        target_runs = first_innings_runs
        wins = 0
        draws = 0
        for i in range(search_num):
            innings_state = MatchSim.inningsState()
            innings_state.runs = runs
            innings_state.total = runs
            innings_state.wickets = wickets
            innings_state.totalBalls = balls
            innings_state.legalBalls = balls
            innings_state.fallOfWickets = {n+1: runs for n in range(wickets)}
            result = self.match_simulator.simulateOneInnings(target=target_runs,continue_from=innings_state)
            if result.total > target_runs:
                wins += 1
            elif result.total == target_runs:
                draws += 1
        losses = search_num - (wins + draws)
        print('win:', wins/search_num, ' draw:', draws/search_num, ' lose:', losses/search_num)

ME = MatchExperimenter()
#ME.run_and_load_in(1000)
ME.load_in()
stats = ME.get_stats_from_file()
ME.limits = ME.get_limits(df=stats)
ME.innings_histogram_from_key('total')
ME.innings_histogram_from_key('total', df=stats)
ME.innings_histogram_from_key('extras')
ME.innings_histogram_from_key('extras', df=stats)
ME.innings_histogram_from_key('fours')
ME.innings_histogram_from_key('fours', df=stats)
ME.innings_histogram_from_key('sixes')
ME.innings_histogram_from_key('sixes', df=stats)
ME.innings_histogram_from_key('wickets')
ME.innings_histogram_from_key('wickets', df=stats)
ME.innings_histogram_from_key('totalBalls')
ME.innings_histogram_from_key('totalBalls', df=stats)

ME.worm_plot(n=10)
ME.worm_plot(n=10,df=stats)
ME.worm_plot(n=100)
ME.worm_plot(n=100,df=stats)
'''
ME.make_first_innings_win_prediction(46, 4, 60)   # runs, wickets, balls
ME.make_second_innings_win_prediction(190, 6, 290, 200)   # runs, wickets, balls


ME.get_win_percentage(150)
ME.get_win_percentage(250)
ME.get_win_percentage(280)
ME.get_win_percentage(330)
ME.worm_plot(n=10)
ME.worm_plot(n=100)
ME.innings_histogram_from_key('total')
ME.innings_histogram_from_key('fours')
ME.innings_histogram_from_key('sixes')
ME.innings_histogram_from_key('wickets')
ME.innings_histogram_from_key('totalBalls')
ME.scatter_plot_histograms_from_keys('wickets', 'runs')
ME.cumulative_frequency_curve('total')
ME.cumulative_frequency_curve('wickets')
'''
