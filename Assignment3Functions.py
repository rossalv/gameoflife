import matplotlib.pyplot as plt
import random
from datetime import datetime
import numpy


class Cell:
    def __init__(self, s):
        self.state = s


class Board:
    def __init__(self, s):
        self.size = s
        self.grid = numpy.array([[Cell("D")] * s for i in range(s)])

    def plot(self, plot):
        xliving = []
        yliving = []
        xdead = []
        ydead = []

        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y].state == "D" and ((x == 0 or y == 0) or (x == self.size - 1 or y == self.size - 1)):
                    xdead.append(x)
                    ydead.append(y)
                elif self.grid[x][y].state == "L":
                    xliving.append(x)
                    yliving.append(y)
        plot.scatter(xliving, yliving, c="Blue", marker="$X$", s=10)
        plot.scatter(xdead, ydead, c="Black", marker="None", s=10)
        #plot.title("Generation " + str(gen))
        ax = plot.gca()
        plot.axis('off')
        plot.draw()

    def update(self, plot, f):
        plot.pause(0.001)
        f.clear()
        self.plot(plot)


def conway_assignment_2(board):
    temp = Board(board.size)
    for x in range(board.size):
        for y in range(board.size):
            live = 0
            if x < board.size - 1:
                if board.grid[x + 1][y].state == "L":
                    live += 1
            if y < board.size - 1:
                if board.grid[x][y + 1].state == "L":
                    live += 1
            if x > 0:
                if board.grid[x - 1][y].state == "L":
                    live += 1
            if y > 0:
                if board.grid[x][y - 1].state == "L":
                    live += 1
            if x < board.size - 1 and y < board.size - 1:
                if board.grid[x + 1][y + 1].state == "L":
                    live += 1
            if x > 0 and y > 0:
                if board.grid[x - 1][y - 1].state == "L":
                    live += 1
            if x < board.size - 1 and y > 0:
                if board.grid[x + 1][y - 1].state == "L":
                    live += 1
            if x > 0 and y < board.size - 1:
                if board.grid[x - 1][y + 1].state == "L":
                    live += 1
            if board.grid[x][y].state == "D" and live == 3:
                temp.grid[x][y] = Cell("L")
            elif (board.grid[x][y].state == "L" and live < 2) or (board.grid[x][y].state == "L" and live > 3):
                temp.grid[x][y] = Cell("D")
            elif board.grid[x][y].state == "L":
                temp.grid[x][y] = Cell("L")
    return temp


def board_history(n, board, hist, s):
    temp = Board(board.size)
    for x in range(n):
        board = conway_assignment_2(board, temp)
        if s:
            hist.append(board)
    if s:
        return hist
    return s


def conway_assignment_3(neighbor, ar):

    neighbor[:, :] = 0

    neighbor[:-1, :] += ar[1:, :]
    neighbor[1:, :] += ar[:-1, :]
    neighbor[:, :-1] += ar[:, 1:]
    neighbor[:, 1:] += ar[:, :-1]

    neighbor[1:, :-1] += ar[:-1, 1:]
    neighbor[1:, 1:] += ar[:-1, :-1]
    neighbor[:-1, :-1] += ar[1:, 1:]
    neighbor[:-1, 1:] += ar[1:, :-1]

    neighbor[-1, :] += ar[0, :]
    neighbor[0, :] += ar[-1, :]
    neighbor[:, -1] += ar[:, 0]
    neighbor[:, 0] += ar[:, -1]

    val = (ar == 1) & ((neighbor == 2) | (neighbor == 3))
    val2 = (ar == 0) & (neighbor == 3)
    ar = val + val2

    return neighbor, ar


class RandomBoard(Board):
    def setBoard(self):
        for x in range(self.size):
            for y in range(self.size):
                a = random.random()
                if a < 0.5:
                    self.grid[x][y] = Cell("D")
                else:
                    self.grid[x][y] = Cell("L")


class BlinkerBoard(Board):
    def setBoard(self):
        p = int(self.size / 2)
        self.grid[p][p] = Cell("L")
        self.grid[p - 1][p] = Cell("L")
        self.grid[p + 1][p] = Cell("L")


class GliderBoard(Board):
    def setBoard(self):
        p = int(self.size / 2)
        self.grid[p][p] = Cell("L")
        self.grid[p - 1][p] = Cell("L")
        self.grid[p + 1][p] = Cell("L")
        self.grid[p + 1][p + 1] = Cell("L")
        self.grid[p][p + 2] = Cell("L")


class BulletBoard(Board):
    def setBoard(self):
        p = int(self.size / 2)
        self.grid[p][p] = Cell("L")
        self.grid[p + 1][p] = Cell("L")
        self.grid[p - 1][p] = Cell("L")
        self.grid[p][p + 1] = Cell("L")
        self.grid[p + 1][p + 1] = Cell("L")
        self.grid[p - 1][p + 1] = Cell("L")
        self.grid[p][p + 2] = Cell("L")

class TestBoard(Board):
    def setBoard(self):
        self.grid[self.size - 1][self.size - 1] = Cell("L")
        self.grid[0][0] = Cell("L")
        self.grid[self.size - 1][0] = Cell("L")
        self.grid[0][self.size - 1] = Cell("L")

def IncrementSize():
    xs3 = []
    ys3 = []
    trials = 100
    n = 1000
    for x in range(6):
        print('Running conway_assignment_3 for a board size of ' + str(n) + ' x ' + str(n) + '...')
        neighbor = numpy.zeros((n, n))
        ar = numpy.random.randint(0, 2, size=(n, n))
        starttime = datetime.now()
        for z in range(trials):
            neighbor, ar = conway_assignment_3(neighbor, ar)
        endtime = datetime.now()
        starts = starttime.timestamp()
        ends = endtime.timestamp()
        elapsed = (ends - starts) * 1000
        ts = trials / elapsed
        print(str(n) + " x " + str(n) + " " + str(ts) + " time steps / ms " + str(elapsed) + " total time\n")
        xs3.append(n)
        ys3.append(ts)
        n += 250
    plot1 = plt.figure(1)
    plt.title('conway_assignment_3')
    plt.xlabel('Grid Size')
    plt.ylabel('Time Steps / MS')
    plt.plot(xs3, ys3)

    n = 20
    xs2 = []
    ys2 = []
    '''
    for x in range(3):
        print('Running conway_assignment_2 for a board size of ' + str(n) + ' x ' + str(n) + '...')
        b = RandomBoard(n)
        b.setBoard()
        starttime = datetime.now()
        for y in range(trials):
            b = conway_assignment_2(b)
        endtime = datetime.now()
        starts = starttime.timestamp()
        ends = endtime.timestamp()
        elapsed = (ends - starts) * 1000
        ts = trials / elapsed
        xs2.append(n)
        ys2.append(ts)
        print(str(n) + " x " + str(n) + " " + str(ts) + " time steps / ms " + str(elapsed) + " total time\n")
        n += 25

    plot2 = plt.figure(2)
    plt.title('conway_assignment_2')
    plt.xlabel('Grid Size')
    plt.ylabel('Time Steps / MS')
    plt.plot(xs2, ys2)
    '''
    plt.show()

def DynamicCells():
    n = 1000
    trials = 500
    neighbor = numpy.zeros((n, n))
    ar = numpy.random.randint(0, 2, size=(n, n))
    plot = plt
    fig = plot.figure()
    xs = [0]
    ysl = [ar.sum()]
    ysd = [(n * n) - ar.sum()]
    plot.plot(xs, ysl, label="Living")
    plot.plot(xs, ysd, label="Dead")
    plot.draw()
    for z in range(trials):
        plot.pause(0.1)
        fig.clear()
        neighbor, ar = conway_assignment_3(neighbor, ar)
        xs.append(z)
        ysl.append(ar.sum())
        ysd.append((n * n) - ar.sum())
        plot.plot(xs, ysl, label = "Living")
        plot.plot(xs, ysd, label = "Dead")
        plot.draw()


def RunGame(n, trials, type, animate):
    gen = 1
    if type.lower() == "random":
        ar = numpy.random.randint(0, 2, size=(n, n), dtype=int)
    if type.lower() == "blinker":
        ar = numpy.zeros((n, n))
        half = int(n / 2)
        print(half)
        ar[half][half] = 1
        ar[half + 1][half] = 1
        ar[half - 1][half] = 1
    if type.lower() == "glider":
        ar = numpy.zeros((n, n))
        half = int(n / 2)
        ar[half][half] = 1
        ar[half - 1][half] = 1
        ar[half + 1][half] = 1
        ar[half + 1][half + 1] = 1
        ar[half][half + 2] = 1
    neighbor = numpy.zeros((n, n))
    if animate == "True":
        plot = plt
        fig = plot.figure()
        xliv = []
        yliv = []
        for x in range(n):
            for y in range(n):
                if ar[x][y] == 1:
                    xliv.append(x)
                    yliv.append(y)
        plot.scatter(xliv, yliv, c="Blue", marker="$X$", s=10)
        plot.xlim(-1, n + 1)
        plot.ylim(-1, n + 1)
        plot.title("Generation " + str(gen))
        ax = plot.gca()
        plot.axis('off')
        plot.draw()
    starttime = datetime.now()
    gen += 1
    for z in range(trials):
        neighbor, ar = conway_assignment_3(neighbor, ar)
        if animate == "True":
            xliv = []
            yliv = []
            for x in range(n):
                for y in range(n):
                    if ar[x][y] == 1:
                        xliv.append(x)
                        yliv.append(y)
            # print(ar)
            # print(xliv)
            plot.pause(0.0000000000000001)
            fig.clear()
            plot.scatter(xliv, yliv, c="Blue", marker="$X$", s=10)
            plot.xlim(-1, n + 1)
            plot.ylim(-1, n + 1)
            plot.title("Generation " + str(gen))
            ax = plot.gca()
            plot.axis('off')
            plot.draw()
        gen += 1
    endtime = datetime.now()
    starts = starttime.timestamp()
    ends = endtime.timestamp()
    elapsed = (ends - starts) * 1000
    print(elapsed)
