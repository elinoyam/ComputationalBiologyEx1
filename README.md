# ComputationalBiologyEx1
For running the code you need to have the following libraries:
Tkinter,numpy,matplotlib.

installation can be performed via cmd using the following commands:
pip install tkinter
pip install matplotlib
pip install numpy

Menu:
* Parameter P - The percentage of the table filled with people. number between 0 to 1.0
0 means no people at all, 1 means all board is filled with people.

* Parameter L- for how many generations a person can't receive and spread the rumor again

* random board is for the first task, pre-defined board is for the second task where we had to implement a strategy to make the rumor spread slower.

  random board has 4 colors:
    White - person who doesn't believe the rumor
    
    Black - The square has no person in it.
    
    Red - person who believed the rumor at the current iteration(generation)

    Yellow - a person who got and believed the rumor previous generation and it will stay yellow for L generation, after L generation the person doesn't believe the                rumor anymore, therefore the square becomes white   
    
    
  pre-defined board has 7 colors:
    White - person who doesn't believe the rumor
    
    Black - The square has no person in it.
    
    Red - person who believed the rumor at the current iteration(generation)

    and the rest 4 colors are like Yellow in random board but now it splits to S1,S2,S3,S4

    Yellow - represents person from S4 

    Orange - represents person from S3

    Pink - represents person from S2

    Blue - represents person from S1

* generations is the amount of generations to have in every single run.(be advised that counts begin from 0 and also considered as a generation. ie: Entering 6 will run from 0 to 5 includes.

* iterations is the amount of runs we want to have

* If you want to have GUI of the matrix and see the rumor spreads - Enter 1. else 0. (not seeing the GUI will make the process faster, console shows iteration and generation number)

At the end will generate a graph. X axis is generation number, Y axis is the percentage of people believed the rumor at every generation.
All iterations are shown on the same graph.

