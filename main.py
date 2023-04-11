# This is a sample Python script.
import random
import time
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

L = 3
P = 0.5
ITERATIONS = 50
TEST_ITERATIONS = 10
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
        # self.belief_percentage = 0.0
        # return None
        if belief_percentage < 0.1:
            self.belief_percentage = 0.0
        elif belief_percentage > 0.65:
            self.belief_percentage = 1.0
        elif 0.1 <= belief_percentage <= 0.2:
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

    root = tk.Tk()
    root.title("Rumor Spreading")
    root.geometry("1050x1050")
    root.resizable(True, True)


    # Create a label and an entry widget
    label_P = tk.Label(root, text="Enter P parameter:")
    entry_P = tk.Entry(root)
    label_L = tk.Label(root, text="Enter L parameter:")
    entry_L = tk.Entry(root)

    # Add the label and entry widgets to the root window using pack
    label_P.pack()
    entry_P.pack()
    label_L.pack()
    entry_L.pack()

    def process_parameter():
        global P
        global L

        # Get the value of the entry widget
        P = float(entry_P.get())
        L = float(entry_L.get())

        # Process the parameter as needed
        print("The P parameter is:", P)
        print("The L parameter is:", L)
        root.destroy()


    button = tk.Button(root, text="Process", command=process_parameter)
    button.pack()

    root.mainloop()
    root = tk.Tk()
    root.title("Rumor Spreading")
    root.geometry("1050x1050")
    root.resizable(True, True)
    canvas = tk.Canvas(root, width=1000, height=1020)
    canvas.pack()

    rectangle_size = 10
    label_size = 20
    padding = 30

    # create numpy array to save the percentage of people who believed the rumor in each iteration and in every for loop
    test_results = np.zeros((TEST_ITERATIONS, ITERATIONS), dtype=float)


    for test_index in range(TEST_ITERATIONS):
        people_who_believe_rumor = []
        people_who_believe_rumor_but_cant_spread = []


        # fill board with people with random beliefs with P probability
        number_of_people = 0
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
                    number_of_people += 1
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

        # set all the people to not believe the rumor
        for i in range(100):
            for j in range(100):
                if board[i][j] is not None:
                    board[i][j].believed_rumor = False
                    board[i][j].times_rumor_received = 0
                    board[i][j].iteration_until_can_spread_rumor = 0

        # start with random person to spread rumor
        random_person = None
        while random_person is None:
            random_person_row = random.randint(0, 99)
            random_person_column = random.randint(0, 99)
            random_person = board[random_person_row][random_person_column]

        random_person.believed_rumor = True

        for iter in range(ITERATIONS):
           # display board
            canvas.delete("all")
            for i in range(100):
                for j in range(100):
                    if board[i][j] is not None:
                        if board[i][j].believed_rumor and board[i][j].iteration_until_can_spread_rumor > 0:
                            canvas.create_rectangle(i*10, j*10+ padding, i*10+10, j*10+10+ padding, fill="yellow") # one who believed and spread the rumor in a previous iteration
                        elif board[i][j].believed_rumor:
                            canvas.create_rectangle(i*10, j*10+ padding, i*10+10, j*10+10+ padding, fill="red") # one that now starts to spread the rumor
                        else:
                            canvas.create_rectangle(i*10, j*10+ padding, i*10+10, j*10+10+ padding, fill="white") # one that didn't believe the rumor
                    else:
                        canvas.create_rectangle(i*10, j*10+ padding, i*10+10, j*10+10+ padding, fill="black") # empty space
            # display changing iteration number in the top of the board (label)
            canvas.create_text(500, 15, text="Iteration: " + str(iter), font=("Purisa", label_size))
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
            people_who_believe_rumor_but_cant_spread = []
            for i in range(100):
                for j in range(100):
                    if board[i][j] is not None and board[i][j].believed_rumor and board[i][j].iteration_until_can_spread_rumor == 0:
                        people_who_believe_rumor.append(board[i][j])
                    elif board[i][j] is not None and board[i][j].believed_rumor and board[i][j].iteration_until_can_spread_rumor > 0:
                        people_who_believe_rumor_but_cant_spread.append(board[i][j])

            print("Iteration: " + str(iter) + " P: " + str(P) + " L: " + str(L) + " people who believe rumor: " + str(len(people_who_believe_rumor)) + " people who believe rumor but can't spread: " + str(len(people_who_believe_rumor_but_cant_spread)))
            if len(people_who_believe_rumor) == 0 and len(people_who_believe_rumor_but_cant_spread) == 0:
                canvas.delete("all")
                for i in range(100):
                    for j in range(100):
                        if board[i][j] is not None:
                            canvas.create_rectangle(i * 10, j * 10 + padding, i * 10 + 10, j * 10 + 10 + padding,
                                                        fill="white")  # one that didn't believe the rumor
                        else:
                            canvas.create_rectangle(i * 10, j * 10 + padding, i * 10 + 10, j * 10 + 10 + padding,
                                                    fill="black")  # empty space
                # display changing iteration number in the top of the board (label)
                canvas.create_text(500, 15, text="Iteration: " + str(iter), font=("Purisa", label_size))
                root.update()
                # sleep for 2 seconds
                time.sleep(2)
                canvas.delete("all")
                canvas.create_text(500, 500, text="Rumor vanished!", font=("Purisa", label_size*5))
                root.update()
                break

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

            # insert to test result the percentage of people who believe the rumor in the test_index row and the current iteration
            test_results[test_index][iter] = ((len(people_who_believe_rumor) + len(people_who_believe_rumor_but_cant_spread)) / number_of_people) * 100


        # display in the window the percentage of people who believed the rumor from all the people in the board
        canvas.delete("all")
        canvas.create_text(500, 200, text="P = " + str(P) + ", L = " + str(L), font=("Purisa", label_size*2))
        belief_percentage = ((len(people_who_believe_rumor) + len(people_who_believe_rumor_but_cant_spread)) / number_of_people)
        belief_percentage = belief_percentage * 100
        canvas.create_text(500, 500, text="Percentage of people who believes \nthe rumor in the last iteration:\n" + str(belief_percentage) + "%",
                           font=("Purisa", int(label_size*1.5)), justify="center")
        root.update()
        # test_results.append({ "P": P, "L": L, "belief_percentage": belief_percentage})

        # print("P = " + str(P) + ", L = " + str(L) + ", percentage of people who believed the rumor: " + str(len(people_who_believe_rumor) / (10000 - len(people_who_believe_rumor_but_cant_spread)) * 100) + "%")
        root.after(3000)



    # print(test_results)
    # display graph of believed percentage vs iteration number for all test_index together in the same graph
    for test_index in range(len(test_results)):
        plt.plot(test_results[test_index])
    plt.ylabel('Percentage of people who believed the rumor')
    plt.xlabel('Iteration number')
    plt.show()




    # plt.plot([x["iteration"] for x in test_results], [x["belief_percentage"] for x in test_results])
    # plt.show()



    root.after(5000)
    root.destroy()

