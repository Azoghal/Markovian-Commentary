# Markovian-Commentary for Cricket
This personal project is a match simulation and commentary generation tool. Markov models are used to generate commentary that is relevant to the outcome of a ball, and also used to generate the sequence of balls that make up a match
## Commentary
See ```two-gram_match_example, three-gram_match_example, four-gram_match_example``` for a full match's commentary.
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

![all generated worms][generated_allworms]

[generated_allworms]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/generated_allworms.png
[generated_100worms]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/generated_100worms.png
[generated_10worms]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/generated_10worms.png
[generated_total]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/generated_total.png
[generated_extras]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/generated_extras.png
[generated_wickets]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/generated_wickets.png
[generated_fours]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/generated_fours.png
[generated_sixes]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/generated_sixes.png
[generated_totalBalls]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/generated_totalBalls.png

[scraped_allworms]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/scraped_allworms.png
[scraped_100worms]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/scraped_100worms.png
[scraped_10worms]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/scraped_10worms.png
[scraped_total]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/scraped_total.png
[scraped_extras]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/scraped_extras.png
[scraped_wickets]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/scraped_wickets.png
[scraped_fours]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/scraped_fours.png
[scraped_sixes]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/scraped_sixes.png
[scraped_totalBalls]: https://github.com/Azoghal/Markovian-Commentary/blob/master/plots/scraped_totalBalls.png
