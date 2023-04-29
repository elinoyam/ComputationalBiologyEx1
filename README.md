# ComputationalBiologyEx1

menu:
* Parameter P - The percentage of the table filled with people.
0 means no people at all, 1 means all board is filled with people.

* Parameter L- for how many generations a person can't receive and spread the rumor again

* random board is for the first task, pre-defined board is for the second task where we had to implement a strategy to make the rumor spread slower.

  random board has 2 colors:
    Red - person who believed the rumor at the current iteration(generation)

    Yellow - a person who believed the rumor and now he can't get the rumor again for L generations.

  pre-defined board has 5 colors:

    Red - person who believed the rumor at the current iteration(generation)

    and the rest 4 colors are like Yellow in the random board but now split to S1,S2,S3,S4

    Yellow - represents person from S4 

    Orange - represents person from S3

    Pink - represents person from S2

    Blue - represents person from S1

* generations is the amount of generations to have in every single run.

* iterations is the amount of runs we want to have

* If you want to have GUI of the matrix and see the rumor spreads - Enter 1. else 0. (not seeing the GUI will make the process faster)

At the end will generate a graph. X axis is generation number, Y axis is the percentage of people believed the rumor at every generation.
All iterations are shown on the same graph.


