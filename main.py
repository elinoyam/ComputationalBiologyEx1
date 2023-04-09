# This is a sample Python script.
import random
import tkinter as tk
import numpy as np

L = 2
P = 0.5
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class Person:
    def __init__(self, row_index, column_index):
        self.row_index = row_index
        self.column_index = column_index
        self.belief_percentage = None
        # get random float between 0 and 1
        rand = random.uniform(0, 1)
        self.set_belief_percentage(rand)
        self.neighbors = None
        self.times_rumor_received = 0
        self.believed_rumor = False
        self.iteration_until_can_spread_rumor = 0


    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def get_belief_percentage(self):
        return self.belief_percentage

    def set_belief_percentage(self, belief_percentage):
        # self.belief_percentage = 1.0
        # return None
        if belief_percentage < 0.1:
            self.belief_percentage = 0.0
        elif belief_percentage > 0.8:
            self.belief_percentage = 1.0
        elif 0.1 <= belief_percentage <= 0.35:
            self.belief_percentage = 0.33
        else:
            self.belief_percentage = 0.66

    def receive_rumor(self):
        self.times_rumor_received += 1

    def spread_rumor(self):
        if self.times_rumor_received > 0 and self.iteration_until_can_spread_rumor == 0:
            add_to_belief = 0.33 * (self.times_rumor_received-1)
            random_boolean = random.choices(
                [True, False],
                k=1,
                weights=[min(1,self.belief_percentage + add_to_belief),
                         max(1 - self.belief_percentage - add_to_belief, 0)],
            )
            self.believed_rumor = random_boolean[0]

        self.times_rumor_received = 0






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # set np array with size 100 on 100 with type Person
    board = np.empty((100,100), dtype=Person)

    # fill board with people with random beliefs with P probability
    for i in range(100):
        for j in range(100):
            random_boolean = random.choices(
                [True, False],
                k=1,
                weights=[P,
                         1-P],
            )
            if random_boolean[0]:
                board[i][j] = Person(i, j)
            else:
                board[i][j] = None

    # set neighbors
    for i in range(100):
        for j in range(100):
            if board[i][j] is not None:
                neighbors = []
                for k in range(i-1, i+2):
                    if k >= 0 and k < 100:
                        for l in range(j-1, j+2):
                            if l >= 0 and l < 100:
                                if board[k][l] is not None and (k != i or l != j):
                                    neighbors.append(board[k][l])
                board[i][j].set_neighbors(neighbors)

    # start with random person to spread rumor
    random_person = None
    while random_person is None:
        random_person_row = random.randint(0, 99)
        random_person_column = random.randint(0, 99)
        random_person = board[random_person_row][random_person_column]

    random_person.believed_rumor = True

    root = tk.Tk()
    root.title("Rumor Spreading")
    root.geometry("1000x1000")
    root.resizable(False, False)
    canvas = tk.Canvas(root, width=1000, height=1000)
    canvas.pack()

    # while True:
    for iter in range(1000):
       # display board
        for i in range(100):
            for j in range(100):
                if board[i][j] is not None:
                    if board[i][j].believed_rumor and board[i][j].iteration_until_can_spread_rumor > 0:
                        canvas.create_rectangle(i*10, j*10, i*10+10, j*10+10, fill="yellow") # one who believed and spread the rumor in a previous iteration
                    elif board[i][j].believed_rumor:
                        canvas.create_rectangle(i*10, j*10, i*10+10, j*10+10, fill="red") # one that now starts to spread the rumor
                    else:
                        canvas.create_rectangle(i*10, j*10, i*10+10, j*10+10, fill="white") # one that didn't believe the rumor
                else:
                    canvas.create_rectangle(i*10, j*10, i*10+10, j*10+10, fill="black") # empty space
        root.update()

        # decrease iteration until can spread rumor
        for i in range(100):
            for j in range(100):
                if board[i][j] is not None:
                    if board[i][j].iteration_until_can_spread_rumor > 0:
                        board[i][j].iteration_until_can_spread_rumor -= 1
                        if board[i][j].iteration_until_can_spread_rumor == 0:
                            board[i][j].believed_rumor = False

        # find all the people who believe the rumor
        people_who_believe_rumor = []
        for i in range(100):
            for j in range(100):
                if board[i][j] is not None and board[i][j].believed_rumor and board[i][j].iteration_until_can_spread_rumor == 0:
                    people_who_believe_rumor.append(board[i][j])

        # spread rumor to neighbors
        for person in people_who_believe_rumor:
            for neighbor in person.neighbors:
                neighbor.receive_rumor()

            person.iteration_until_can_spread_rumor = L
            # person.believed_rumor = False

        # check for each person if he needs to spread rumor
        for i in range(100):
            for j in range(100):
                if board[i][j] is not None:
                    board[i][j].spread_rumor()




    root.after(100)
    root.destroy()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
