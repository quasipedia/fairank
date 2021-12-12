# FAIRANK™

Fairank™ tries to make the ranking in Advent of Code (AoC) private boards a bit fairer.

## Rationale

The main problem of the default system (which awards 100 points to the first submission, and then 99, 98, 97...) is that it awards points as one would do during a motorsport championship.  However, while in a motorsport championship the same pilots will show up at the same time, and will race undistracted under the same conditions and with vehicles of comparable performance, in AoC participants are spread across different timezones, use different languages, and they often have other personal commitments that interfere with being able to solve one puzzle every 24 hours.

No ranking system for a competition that involves multiple timezones, programming languages, and that intertwines with everyday life will ever be perfect.  And all of them will be biased.  This one has been designed to try to **give more weight to those things that everybody is likely to be able to achieve if they apply themselves, and less to those things that you can achieve only under particular conditions**.

## Point System
Fairank™ rewards _perseverance, consistency and proficiency_.  Points are awarded as follows:
- **Each star is awarded 1.5 points, regardless of when it has been obtained**.  This intended to reward _perseverance_: everybody is likely to eventually find a solution to each puzzle, throwing enough time at it. (75 points max)
- **Each star that is obtained within 24 hours from puzzle publication is awarded 0.3 points**. This is intended to reward _consistency_: most day it is likely that a participants could find the time to solve the puzzle, if they want. (15 points max)
- **Being the first to get a star is rewarded with 0.2 points** (there is an initial simplification, read the section on "Speed Ranking" below to learn how this really works).  This is intended to reward _proficiency_: more skilled participants - all things being the same - are likely to solve the puzzle first. (10 points max)

A participant who would consistently be the first to solve all the puzzles, on the day they are published would score: **100 points** (0 * 1.5 + 50 * 0.3 + 50 * 0.2)

### Speed Ranking
Ranking fairly speed is particularly tricky.

The default AoC method - for boards with less than 100 participants - has two big problems related to the number of participants typically tapering off during the event:
- **Being unable to participate is treated as being the slowest participant**.  In reality, it is often a matter of life happening (kids, business travel, sickness, power/internet outage...)
- **Late starters are at huge disadvantage**: the delta in points between first and last on the first days - where they are last - is a lot bigger than the delta during later days - when even if they are the fastest they don't gain as much over the slower participants.
- **The slowest participant get rewarded even if they have shown to have no speed at all.**  In fact, the least participants, the higher the reward.

Fairank™ tries to mitigate the above points by:
- **Looking at a participant's speed only if they entered the solution on the day the puzzle was published**.  This solves the problem of late starters.  And for people who couldn't commit to AoC on a given day for whatever reason.
- **Computing speed on a linear continuum between 1 for the fastest participant, and close-to-0 for the slowest one** (the actual formula is 1 - <finish-position-minus-one>/<number-of-finishers>). This means for example that if there were 4 participants their speed would be 1-0/4 = **1.0**, 1-1/4 = **0.75**, 1-2/4 = **0.5** and 1-3/4 = **0.25**.
- **Assuming participants will have consistent speed throughout the competition** (i.e.: if a participant has been very fast in solving most of the puzzles, it is fair to imagine they would have been so in the other puzzles too).  Concretely this means that **the 10 points assigned for _proficiency_ are computed as 10 * average_speed**.  A participant' average speed is computed on a sample of at least 30 stars, missing ones being considered speed=0.