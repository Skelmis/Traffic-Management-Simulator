# Traffic-Management-Simulator

A project devoted to fun times and creating a program to handle the efficient & safe control of traffic lights at a given intersection.

---

We were given a baseline set of code, see [here](https://github.com/Skelmis/Traffic-Management-Simulator/tree/master/Baseline%20Traffic%20code). Then, based off of that we were asked to create the best simulator we could, that was both as efficient as possible and also conformed to the nzta road rules.

Some cool stats about our implementation:

> Required Knowledge
> Concept 1 being lights just rotate through clockwise changing lights
> Concept 3 being based on both lane length & wait times

Using a set traffic amount of 25 new cars everytime the intersection was clear I found the following.
Concept 1 had a total cars count of: `210 after 5 minutes`
Concept 3 had a total cars count of: `285 after 5 minutes`
This means Concept 3 had 75 more cars then Concept 1 are running for the same timeframe
This means Concept 3 is 135% more efficient then Concept 1

Our final design implementation is 135% more efficient then all comparisions & the efficiency increases over time as it slowly gets further and further ahead of prior implementations.

After running for about 15 minutes:
[![GRAPHIC](https://imgur.com/a/OXCzUmq)]()

After 70 hours:
https://gyazo.com/9f60436c8d2193732e314776aa2db713

After running for around 101 hours:
[![GRAPHIC](https://imgur.com/a/WiDHC6L)]()

After 141 hours:
[![GRAPHIC](https://imgur.com/a/iknKnHI)]()
