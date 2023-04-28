# This is a sample Python script.
import random
import time
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

L = 3
P = 0.5
IS_BOARD_RANDOM = True
ITERATIONS = 50
TEST_ITERATIONS = 10
RECTANGLE_SIZE = 6
LABEL_SIZE = 20
PADDING_Y = 30
PADDING_X = 100
ROWS = COLUMNS = 100


class Person:
    def __init__(self, row_index, column_index, belief_percentage=None):
        self.row_index = row_index
        self.column_index = column_index
        self.belief_percentage = None

        if belief_percentage is None:
            # get random float between 0 and 1 if it wasn't set by the user to be pre-defined board
            belief_percentage = random.uniform(0, 1)
        self.set_belief_percentage(belief_percentage)
        self.neighbors = None
        self.times_rumor_received = 0
        self.believed_rumor = False
        self.iteration_until_can_spread_rumor = 0

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def get_belief_percentage(self):
        return self.belief_percentage

    def set_belief_percentage(self, belief_percentage):
        # S1=~0.2, s2=~0.45, S3 =~0.25, S4=~0.1 (from paper)
        if belief_percentage <= 0.1:
            self.belief_percentage = 0.0
        elif belief_percentage >= 0.8:
            self.belief_percentage = 1.0
        elif 0.1 < belief_percentage <= 0.35:
            self.belief_percentage = 0.33
        else:
            self.belief_percentage = 0.66

    def receive_rumor(self):
        self.times_rumor_received += 1

    def spread_rumor(self):
        if self.times_rumor_received > 0 and self.iteration_until_can_spread_rumor == 0:
            add_to_belief = 0.33 * (self.times_rumor_received - 1)
            random_boolean = random.choices(
                [True, False],
                k=1,
                weights=[min(1, self.belief_percentage + add_to_belief),
                         max(1 - self.belief_percentage - add_to_belief, 0)],
            )
            self.believed_rumor = random_boolean[0]

        self.times_rumor_received = 0


def get_random_person_from_board():
    random_person = None
    while random_person is None:
        random_person_row = random.randint(0, 99)
        random_person_column = random.randint(0, 99)
        random_person = board[random_person_row][random_person_column]

    return random_person


def display_board_stage():
    canvas.delete("all")  # delete the previous stage of the board
    for i in range(ROWS):
        for j in range(COLUMNS):
            if board[i][j] is not None:
                if board[i][j].believed_rumor and board[i][j].iteration_until_can_spread_rumor > 0:
                    if IS_BOARD_RANDOM:
                        canvas.create_rectangle(i * RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + PADDING_Y, i * RECTANGLE_SIZE + RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + RECTANGLE_SIZE + PADDING_Y,
                                                fill="yellow")  # one who believed and spread the rumor in a previous iteration
                    else:  # if the board isn't random we want to see that the S1 people are only in the margin of the borad
                        if board[i][j].belief_percentage == 0:
                            canvas.create_rectangle(i * RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + PADDING_Y, i * RECTANGLE_SIZE + RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + RECTANGLE_SIZE + PADDING_Y,
                                                    fill="yellow")  # beliver from S4
                        elif board[i][j].belief_percentage == 0.33:
                            canvas.create_rectangle(i * RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + PADDING_Y, i * RECTANGLE_SIZE + RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + RECTANGLE_SIZE + PADDING_Y,
                                                    fill="orange")  # beliver from S3
                        elif board[i][j].belief_percentage == 0.66:
                            canvas.create_rectangle(i * RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + PADDING_Y, i * RECTANGLE_SIZE + RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + RECTANGLE_SIZE + PADDING_Y,
                                                    fill="pink")  # beliver from S2
                        else:
                            canvas.create_rectangle(i * RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + PADDING_Y, i * RECTANGLE_SIZE + RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + RECTANGLE_SIZE + PADDING_Y,
                                                    fill="blue")  # beliver from S1
                elif board[i][j].believed_rumor:
                    canvas.create_rectangle(i * RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + PADDING_Y, i * RECTANGLE_SIZE + RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + RECTANGLE_SIZE + PADDING_Y,
                                            fill="red")  # one that now starts to spread the rumor
                else:
                    canvas.create_rectangle(i * RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + PADDING_Y, i * RECTANGLE_SIZE + RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + RECTANGLE_SIZE + PADDING_Y,
                                            fill="white")  # one that didn't believe the rumor
            else:
                canvas.create_rectangle(i * RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + PADDING_Y, i * RECTANGLE_SIZE + RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + RECTANGLE_SIZE + PADDING_Y,
                                        fill="black")  # empty space
    # display changing iteration number in the top of the board (label)
    canvas.create_text(400, 15, text="Iteration: " + str(iter), font=("Purisa", LABEL_SIZE))
    root.update()


def fill_board():
    number_of_people = 0
    if IS_BOARD_RANDOM:
        for i in range(ROWS):
            for j in range(COLUMNS):
                random_boolean = random.choices(
                    [True, False],
                    k=1,
                    weights=[P,
                             1 - P],
                )
                if random_boolean[0]:
                    board[i][j] = Person(i, j)
                    number_of_people += 1
                else:
                    board[i][j] = None
    else:
        for i in range(ROWS):
            for j in range(COLUMNS):
                random_boolean = random.choices(
                    [True, False],
                    k=1,
                    weights=[P,
                             1 - P],
                )
                if random_boolean[0]:
                    if (i >= 10 and i <= 90) and (j >= 10 and j <= 90):
                        # if the person is in the middle of the board, set the belief to 0.09 or 0.25 at random - be from S4 or S3 groups at random
                        random_belief = random.choices(
                            [0.09, 0.25, 0.5],
                            k=1,
                            weights=[1 - 0.25 - 0.45, 0.25, 0.45],
                        )
                    else:
                        # if the person is in the edge of the board, set the belief to 0.9 or 0.5 at random - - be from S1 or S2 groups at random
                        random_belief = random.choices(
                            [0.9, 0.25, 0.5],
                            k=1,
                            weights=[0.2, 1 - 0.2 - 0.45, 0.45],
                        )
                    board[i][j] = Person(i, j, belief_percentage=random_belief[0])
                    number_of_people += 1
                else:
                    board[i][j] = None
    return number_of_people


def process_parameter():
    global P
    global L
    global IS_BOARD_RANDOM

    # Get the value of the entry widget
    P = float(entry_P.get())
    L = float(entry_L.get())
    IS_BOARD_RANDOM = entry_random_board.get() == "1" or entry_random_board.get() == ""  # the defult is random board

    # Process the parameter as needed
    print("The P parameter is:", P)
    print("The L parameter is:", L)
    root.destroy()


def display_board_empty_from_belivers():
    canvas.delete("all")
    for i in range(ROWS):
        for j in range(COLUMNS):
            if board[i][j] is not None:
                canvas.create_rectangle(i * RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + PADDING_Y, i * RECTANGLE_SIZE + RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + RECTANGLE_SIZE + PADDING_Y,
                                        fill="white")  # one that didn't believe the rumor
            else:
                canvas.create_rectangle(i * RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + PADDING_Y, i * RECTANGLE_SIZE + RECTANGLE_SIZE+PADDING_X, j * RECTANGLE_SIZE + RECTANGLE_SIZE + PADDING_Y,
                                        fill="black")  # empty space
    # display changing iteration number in the top of the board (label)
    canvas.create_text(400, 15, text="Iteration: " + str(iter), font=("Purisa", LABEL_SIZE))
    root.update()
    # sleep for 2 seconds
    time.sleep(2)
    canvas.delete("all")
    canvas.create_text(400, 300, text="Rumor vanished!", font=("Purisa", LABEL_SIZE*2))
    root.update()

def on_entryP_click(event):
    """Remove the placeholder when the entry widget is clicked."""
    if entry_P.get() == default_value_p:
        entry_P.delete(0, tk.END)

def on_entryP_leave(event):
    """Insert the placeholder if the user didn't enter anything."""
    if not entry_P.get():
        entry_P.insert(0, default_value_p)

def on_entryL_click(event):
    """Remove the placeholder when the entry widget is clicked."""
    if entry_L.get() == default_value_l:
        entry_L.delete(0, tk.END)

def on_entryL_leave(event):
    """Insert the placeholder if the user didn't enter anything."""
    if not entry_L.get():
        entry_L.insert(0, default_value_l)


def on_entryR_click(event):
    """Remove the placeholder when the entry widget is clicked."""
    if entry_random_board.get() == default_value_R:
        entry_random_board.delete(0, tk.END)

def on_entryR_leave(event):
    """Insert the placeholder if the user didn't enter anything."""
    if not entry_random_board.get():
        entry_random_board.insert(0, default_value_R)

if __name__ == '__main__':
    # set np array with size 100 on 100 with type Person
    board = np.empty((ROWS, COLUMNS), dtype=Person)

    # set the window attributes
    root = tk.Tk()
    root.title("Rumor Spreading")
    root.geometry("500x500")
    root.resizable(True, True)

    blank_label = tk.Label(root, pady=20)

    # Create a label and an entry widget for all the needed parameters
    label_P = tk.Label(root, text="Enter P parameter:", pady=5)
    entry_P = tk.Entry(root)
    #default value as placeholder
    default_value_p = "0.5"
    entry_P.insert(0, default_value_p)
    entry_P.bind('<FocusIn>', on_entryP_click)
    entry_P.bind('<FocusOut>', on_entryP_leave)


    label_L = tk.Label(root, text="Enter L parameter:", pady=5)
    entry_L = tk.Entry(root)
    default_value_l = "3"
    entry_L.insert(0, default_value_l)
    entry_L.bind('<FocusIn>', on_entryL_click)
    entry_L.bind('<FocusOut>', on_entryL_leave)

    label_random_board = tk.Label(root, text="Enter 1 for random board, 0 for pre-defined board:", pady=5)
    entry_random_board = tk.Entry(root)
    default_value_R = "1"
    entry_random_board.insert(0, default_value_R)
    entry_random_board.bind('<FocusIn>', on_entryR_click)
    entry_random_board.bind('<FocusOut>', on_entryR_leave)

    blank_label1 = tk.Label(root, pady=5)
    # Add the label and entry widgets to the root window using pack
    blank_label.pack()
    label_P.pack()
    entry_P.pack()
    label_L.pack()
    entry_L.pack()
    label_random_board.pack()
    entry_random_board.pack()
    blank_label1.pack()
    button = tk.Button(root, text="Process", command=process_parameter)
    button.pack()

    root.mainloop()
    root = tk.Tk()
    root.title("Rumor Spreading")
    root.geometry("800x800")
    root.resizable(True, True)
    canvas = tk.Canvas(root, width=800, height=800)
    # make the canvas scrollable
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_vertical = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar_vertical.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame = tk.Frame(canvas)

    #canvas.pack()

    # create numpy array to save the percentage of people who believed the rumor in each iteration and in every for loop
    test_results = np.zeros((TEST_ITERATIONS, ITERATIONS), dtype=float)

    for test_index in range(TEST_ITERATIONS):
        people_who_believe_rumor = []
        people_who_believe_rumor_but_cant_spread = []

        # fill board with people with random beliefs with P probability or according to the pre-defined board
        number_of_people = fill_board()

        for i in range(ROWS):
            for j in range(COLUMNS):
                if board[i][j] is not None:
                    # set all the people to not believe the rumor
                    board[i][j].believed_rumor = False
                    board[i][j].times_rumor_received = 0
                    board[i][j].iteration_until_can_spread_rumor = 0

                    # set neighbors - so each person could spread the rumor to all it's neighbours easily
                    neighbors = []
                    for k in range(i - 1, i + 2):
                        if k >= 0 and k < ROWS:
                            for l in range(j - 1, j + 2):
                                if l >= 0 and l < COLUMNS:
                                    if board[k][l] is not None and (k != i or l != j):
                                        neighbors.append(board[k][l])
                    board[i][j].set_neighbors(neighbors)

        # start with random person to spread rumor
        random_person = get_random_person_from_board()

        random_person.believed_rumor = True

        for iter in range(ITERATIONS):
            # display board
            display_board_stage()

            people_who_believe_rumor = []
            people_who_believe_rumor_but_cant_spread = []
            for i in range(ROWS):
                for j in range(COLUMNS):
                    if board[i][j] is not None:
                        # decrease iteration until can spread rumor
                        if board[i][j].iteration_until_can_spread_rumor > 0:
                            board[i][j].iteration_until_can_spread_rumor -= 1
                            if board[i][j].iteration_until_can_spread_rumor == 0:
                                board[i][j].believed_rumor = False
                        # find all the people who believe the rumor
                        if board[i][j] is not None and \
                                board[i][j].believed_rumor and board[i][j].iteration_until_can_spread_rumor == 0:
                            people_who_believe_rumor.append(board[i][j])
                        elif board[i][j] is not None and \
                                board[i][j].believed_rumor and board[i][j].iteration_until_can_spread_rumor > 0:
                            people_who_believe_rumor_but_cant_spread.append(board[i][j])

            # for testibg purposes:
            # print("Iteration: " + str(iter) + " P: " + str(P) + " L: " + str(L) + " people who believe rumor: " + str(len(people_who_believe_rumor)) + " people who believe rumor but can't spread: " + str(len(people_who_believe_rumor_but_cant_spread)))

            # if none of the people in the board belives the rumor then the rumor is vanished
            # we can stop this iteration of spreading the rumor
            if len(people_who_believe_rumor) == 0 and len(people_who_believe_rumor_but_cant_spread) == 0:
                display_board_empty_from_belivers()
                break

            # spread rumor to neighbors - increase the number of rumored recived in this stage
            for person in people_who_believe_rumor:
                for neighbor in person.neighbors:
                    neighbor.receive_rumor()

                person.iteration_until_can_spread_rumor = L

            # check for each person if he needs to spread rumor - by he's belief level and probability
            for i in range(ROWS):
                for j in range(COLUMNS):
                    for j in range(COLUMNS):
                        if board[i][j] is not None:
                            board[i][j].spread_rumor()

            # insert to test result the percentage of people who believe the rumor in the test_index row and the current iteration
            test_results[test_index][iter] = ((len(people_who_believe_rumor) + len(
                people_who_believe_rumor_but_cant_spread)) / number_of_people) * 100

    # display in the window the percentage of people who believed the rumor from all the people in the board
    canvas.delete("all")
    canvas.create_text(350, 200, text="P = " + str(P) + ", L = " + str(L), font=("Purisa", LABEL_SIZE * 2))
    belief_percentage = (
                (len(people_who_believe_rumor) + len(people_who_believe_rumor_but_cant_spread)) / number_of_people)
    belief_percentage = belief_percentage * 100
    canvas.create_text(350, 400, text="Percentage of people who believes \nthe rumor in the last iteration:\n" + str(
        belief_percentage) + "%",
                       font=("Purisa", int(LABEL_SIZE)), justify="center")
    root.update()
    # test_results.append({ "P": P, "L": L, "belief_percentage": belief_percentage})

    # print("P = " + str(P) + ", L = " + str(L) + ", percentage of people who believed the rumor: " + str(len(people_who_believe_rumor) / (10000 - len(people_who_believe_rumor_but_cant_spread)) * 100) + "%")
    root.after(2000)

# for tests purposes: print(test_results)

# display graph of believed percentage vs iteration number for all test_index together in the same graph
for test_index in range(len(test_results)):
    plt.plot(test_results[test_index])
plt.ylabel('Percentage of people who believed the rumor')
plt.xlabel('Iteration number')
plt.show()
root.after(2000)
root.destroy()  # close the window