# ComputationalBiologyEx1

P is the percentage of the table filled with people.
0 means no people at all, 1 means all board is filled with people.

random board is for the first task, pre-defined board is for the second task where we had to implement a strategy to make the rumor spread slower.

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

