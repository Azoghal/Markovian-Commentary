# Markovian-Commentary for Cricket
This personal project is a match simulation and commentary generation tool. Markov models are used to generate commentary that is relevant to the outcome of a ball, and also used to generate the sequence of balls that make up a match. This can also be used to predict the winner of a match from a certain state, by doing a Monte Carlo search over possible futures of the match.

## Commentary
See ```two-gram_match_example```, ```three-gram_match_example```, ```four-gram_match_example``` for a full match's commentary.
Here are some samples:
```no_run          :  tapped down into the covers
no_run          :  punched into the covers
1_run           :  short of a length outside off , punched off the back foot down to third man
no_run          :  length outside off , opens the face and dabs towards point - still no run
no_run          :  length outside off , gets forward to defend
6_runs          :  down on one knee , in his arc , and dispatched against the spin over deep midwicket ! Reaching for the wide one , and pounding it
4_runs          :  steps out to drive , pinged back fine of mid-off and that will be the first boundary of the England innings
OUT             :  bowled him ! BATTER slides back into his crease , in anticipation of the short ball , but he ended up hopping late into line as the ball skidded through
```
##### 4-grams
We see examples such as the following prove that a single model has the capacity to generate novel commentary from the same starting state:
```1_run           :  back of a length , sliding through , clonked to mid-on
1_run           :  back of a length , BATTER sprints like it 's 1999 all over again , and through he comes for his second hundred of the series !
1_run           :  back of a length to start , swished aerially through point out to the sweeper for one , not particularly convincingly
1_run           :  back of a length , a stiff-armed pull through midwicket
1_run           :  back of a length , round the wicket , BATTER goes back and cuts in front of square on the off side
1_run           :  back of a length , slashed in the air , flamingo-style
1_run           :  back of a length , and carved out to extra cover on the bounce
1_run           :  back of a length , poked to point . BATTER keeps the strike
1_run           :  back of a length , poked off the pads to the leg side
1_run           :  back of a length , a bit wider . Punches hard , away from his body and steers to third man
1_run           :  back of a length on middle stump , BATTER stretches out and sweeps from a leg-stump line to long leg
1_run           :  back of a length , BATTER resumes with his leg-dominant play to ease off the mark with a deflection to third man
1_run           :  back of a length , rides the bounce and secures a single down to third man - 50 stand between these two
```
These examples were generated with a window of length 4. This helps make the generated commentary coherent, but limits the mixing and matching done by the model, which can lead to the model reproducing training sentences rather than generating anew.
##### 3-grams
```sensible examples
1_run           :  tossed up , very loopy above the eyeline , pushed out to long-on
1_run           :  tossed up , very loopy above the eyeline and it turns into a slightly cramped cut , out to deep midwicket
1_run           :  tossed up , lots of air outside off stump , goes right back and punches through cover
1_run           :  tossed up , but drops well short of him
# incoherent or contradictory
no_run          :  and that is splintering the stumps . Defended back to BOWLER
1_run           :  nurdled to the on-side , it 's not a terrible response , BATTER rocks onto the back foot , and bashed into the covers
no_run          :  shoulders arms to complete another economical over
```
3-grams give more variation to the commentary, but sometimes causes long-distance contradictions.
##### 2-grams
```
#sensible examples
1_run           :  good length on the pull but mistimed , just clipped towards midwicket
no_run          :  good length , BATTER blocks it in short again , this time , angled down the line !
no_run          :  flat delivery outside off , he reverse-swipes across the left-hander . Utilising the bounce , turns into a defensive block
2_runs          :  floated up outside off , post point and returns for two . Good running to get a couple
4_runs          :  turned inside-out by a few inches , BATTER hammers it out of answers . Another last-ball four , slapping BOWLER in his follow-through
4_runs          :  thrashed through point
#incoherent or contradictory
1_run           :  up comes the hundred , South Africa , dare one say it , parries it to long-on
1_run           :  fine leg
no_run          :  angled bat
4_runs          :  whump , there
1_run           :  loops up the SA 100
no_run          :  cutter , runs his fingers down the track
1_run           :  deeper into the covers
```
These examples show the trade off between novelty/variation and coherency of the generated commentary. The markov models were trained from 29 ODI matches between 2018 and 2022, totalling over 15000 balls. With a larger training set, one could expect suitable levels of variation with higher window sizes.

## Match Simulation

### Match Length
New matches can be simulated with a markov model over the outcomes. Properties of these simulations can then be compared to those of 718 scraped ODI matches from 2013 to 2018.
While the simulated innings and matches only finish when the match was concluded with a win, tie, or loss, many of the scraped matches were curtailed by rain and therefore were made up of artificially shortened innings. None of the training innings were shortened in such a way. The differing distributions can be seen below.

![totalBalls][totalBalls]

In the simulations, all innings save those with 10 wickets falling would reach 300 legal balls in the innings. We see that the 10-wicket innings account for the roughly linear part of the distribution until the 300th ball. Some balls are classed as extras, and extras such as wides and no balls must be rebowled. These follow a roughly normal distribution with a mean of around 12 extra runs (there are at most 1 balls rebowled per extra run) which accounts for the spike occurring *after* the 300 legal ball requirement.

![extras][extras]

Here is a zoomed in view of the vaguely normal spike between 300 and 320 balls.

![totalBallsZoom][totalBallsZoom]

### Match Totals, Wickets, Stats

Now we will look at how close the model's distribution of runs, wickets, fours etc. are to the reality. One thing to bear in mind is that there are weather shortened matches in the scraped evaluation trend, so we would expect to see a slightly lower number of wickets, fours and sixes for example. Another point is that while the training data for the model was made of matches involving England, Sri Lanka, India, Pakistan, Ireland*, Australia, South Africa, West Indies, all of which are Test-playing nations (of the highest quality) \*(Ireland are typically the weakest team in this list, but still play Tests). The evaluation data includes all ODI matches going back 718 matches from 2018, with much weaker teams included.

![total][total]

The total run distributions seem fairly normal, with means around 280 for the generated matches, and a fair bit lower for the real matches, around 230. The simulated distribution has a long left hand tail which we would expect to come from innings where all wickets fell before the full 50 overs were bowled. The real distribution looks to have a greater spread, and also more extreme values at each end

![wickets][wickets]

The distribution of wickets for the generated matches compares well with real data, apart from having fewer low wicket results. This makes sense due to the inclusion of rain-shortened matches in the evaluation data but not training. Intuitively it feels like the next ball being a wicket is a bernouli trial, with the probability an aggregate over all the transitions into the wicket state, and over the course of a match a binomial distribution is formed.

The distributions of fours and sixes are interesting, as on a basic level these two outcomes are very similar - occasional boundaries. While fours are more common, and sixes are more likely to occur later in the innings, it was unexpected to see that they had such different distributions.

![fours][fours]
![sixes][sixes]

The model has managed to capture the skew of the sixes distribution.

### Worm Plots

Worm plots are a standard way of showing how an innings has progressed, with overs on the x axis, runs on the y, and wickets marked onto the trace. The gradient at any point is the run rate for that over. An innings progresses from the origin upwards and rightwards until all wickets have fallen or all overs bowled.

Sampling just 10 worm plots from the generated and scraped sets we see that the model has captured the trends of the worms, but has less variation between innings, as well as within innings. Notably the 10 scraped plots includes the ODI record of 481/6 posted by England against Australia in 2018. This innings is an outlier, but even without it, it can be seen that the generated innings follow more similar paths than the real matches.

![worms10][worms10]

Looking at 100 worms we start to see the difference between what the model has captured and the reality of an innings

![worms100][worms100]

Typically in cricket, the run rate decreases as wickets fall, and increases as the remaining balls decrease. This would typically lead to a curve with increasing gradient. 
In ODIs, there is a period at the beginning of an innings called a powerplay, that favours the batting side and allows them to score faster than they usually would at the start of a match. This is the explanation for the small curve at the beginning that has decreasing gradient - as the powerplay ends it becomes harder to score runs. 

![wormsall][wormsall]

The markov model for finding the next outcome has a window size of 2, meaning that trends such as those mentioned above are far too long term for the model to capture. In the absence of those trends, the model has captured the more simple notion of average run rate, which is uniform throughout the progression of a generated innings. As the model generated a higher total distribution than the scraped matches, we can conclude that this run rate is too high, which can be explained by the higher quality of teams in the training data, and the lack of the curtailed innings.

## Result Prediction

### Static Predictions

Building a cumulative frequency curve for total runs gives us a way to simply calculate the chance of winning when given a score for an innings.

![cumfreq][cumfreq]

We see the expected shape, with an earlier/lower midpoint for the real innings. This precalculated curve, over some large number of simulated innings, gives us the proportion of innings that are expected to be above or below that score, in other words the proportion of precomputed possible outcomes that are wins or losses. The following values are based on 1000 simulated matches

```
1.6 % chance to win with 150 runs

27.0 % chance to win with 250 runs

56.5 % chance to win with 280 runs

96.0 % chance to win with 330 runs
```

That technique works when the total of one innings is known, but cannot give a chance to win from the middle of a game. There are two cases to consider - partway through the first innings, and having finished the first innings and being partway through the second innings.

### Partway through first innings



[totalBalls]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/totalBalls.png
[totalBallsZoom]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/totalBallsZoom.png
[extras]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/extras.png
[total]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/total.png
[wickets]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/wickets.png
[fours]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/fours.png
[sixes]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/sixes.png
[worms10]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/worms10.png
[worms100]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/worms100.png
[wormsall]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/wormsall.png
[cumfreq]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/cumfreq.png






