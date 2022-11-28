import random
import math
import copy

import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


def HPWL(netlist, cells, r, c):
    total = 0
    for net in netlist:
        l_max = 0
        l_min = r
        w_max = 0
        w_min = c
        loop = 0
        for i in net.split():
            if loop != 0:
                # print(i)
                if cells[int(i)][0] > l_max:
                    l_max = cells[int(i)][0]
                if cells[int(i)][0] < l_min:
                    l_min = cells[int(i)][0]
                if cells[int(i)][1] > w_max:
                    w_max = cells[int(i)][1]
                if cells[int(i)][1] < w_min:
                    w_min = cells[int(i)][1]
            loop = loop + 1
        # print("lmax, lmin", l_max, l_min)
        # print("wmax, wmin", w_max, w_min)
        halfPara = abs(l_max - l_min) + abs(w_max - w_min)
        # print("hpwl small= ", halfPara)
        total = total + halfPara
    return total


def readfile(path):
    with open(path, 'r') as file:
        # reading each line
        first_line = file.readline()
        N = first_line.split()
        print(N[0])
        rows, cols = (int(N[2]), int(N[3]))
        core = [[0 for i in range(cols)] for j in range(rows)]
        for row in range(0, rows, 1):
            for col in range(0, cols, 1):
                core[row][col] = -1
        # print(core)
        cells = [[0 for i in range(2)] for j in range(int(N[0]))]
        for n in range(0, int(N[0]), 1):
            y = random.randint(0, rows - 1)
            x = random.randint(0, cols - 1)
            # print(y, x)
            while core[y][x] != -1:
                y = random.randint(0, rows - 1)
                x = random.randint(0, cols - 1)
            cells[n][0] = x
            cells[n][1] = y
            core[y][x] = n
        # print(cells)
        # print(core)
        netlist = []
        for line in file:
            netlist.append(line)

        print("here")
        # print(netlist)
    return core, cells, rows, cols, int(N[0]), netlist, int(N[1])


def swap_core(co, x1, x2, y1, y2, rows, cols):
    core2 = [[0 for i in range(cols)] for j in range(rows)]
    for row in range(0, rows, 1):
        for col in range(0, cols, 1):
            core2[row][col] = co[row][col]
    # num1 = co[y2][x2]
    # num2 = co[y1][x1]
    # core2[y1][x1] = num2
    # core2[y2][x2] =num1
    core2[y1][x1], core2[y2][x2] = core2[y2][x2], core2[y1][x1]

    # print(co[y2][x2], co[y1][x1])
    # print(core2[y2][x2], core2[y1][x1])
    return core2


def print_core(coree, rowss, colss):
    for row in range(0, rowss, 1):
        for col in range(0, colss, 1):
            if (coree[row][col] != -1) and (coree[row][col] != "-1") :
                print(coree[row][col], end="\t")
            else:
                print("__", end="\t")
        print()
    print()


def swap(array, index_1, index_2,n):
    # swaps 2 current_cells together
    # array2= array.copy()
    # array2[index_1]=array[index_2].copy()
    # array2[index_2]=array[index_1].copy()

    array2 = [[0 for i in range(2)] for j in range(n)]
    for row in range(0, n, 1):
        for col in range(0, 2, 1):
            array2[row][col] = array[row][col]

    array2[index_1], array2[index_2] = array2[index_2], array2[index_1]

    # print(array2[index_2], array2[index_1])
    # print(array[index_2], array[index_1])
    return array2


def schedule_temp(t):
    return t * 0.95


def equation(change_length, tem):
    return (1 - math.exp(-(change_length) / tem))


def update(best_cells, index, y_2, x_2,n):
    array2 = [[0 for i in range(2)] for j in range(n)]
    for row in range(0, n, 1):
        for col in range(0, 2, 1):
            array2[row][col] = best_cells[row][col]
    array2[index][0] = x_2
    array2[index][1] = y_2
    return array2


# create annealing algorithm
def annealing(current_core, cell, rows, cols, N, netlist, n_nets):
    # set current best solution

    best_core = current_core.copy()
    best_cells = cell.copy()

    # set initial temperature
    HPWL_initial = HPWL(netlist, cell, rows, cols)
    T = 500 * HPWL_initial
    # set cooling rate
    T_final = (5 * 0.000001 * HPWL_initial) / n_nets

    moves_per_temp = 10 * N

    # loop until system has cooled
    while T > T_final:
        for i in range(0, moves_per_temp, 1):
            x_1 = random.randint(0, cols - 1)
            x_2 = random.randint(0, cols - 1)
            y_1 = random.randint(0, rows - 1)
            y_2 = random.randint(0, rows - 1)

            while (x_1 == x_2) and (y_1 == y_2):
                # choose another cell for cell_2
                x_2 = random.randint(0, cols - 1)
                y_2 = random.randint(0, rows - 1)

            HPWL_before = HPWL(netlist, best_cells, rows, cols)
            # swaps 2 current_cells together
            new_core = swap_core(best_core.copy(), x_1, x_2, y_1, y_2, rows, cols)

            if (best_core[y_2][x_2] != -1) and (best_core[y_1][x_1] != -1):
                new_cells = swap(best_cells, int(best_core[y_1][x_1]), int(best_core[y_2][x_2]), N)
            elif best_core[y_1][x_1] != -1:
                new_cells = update(best_cells, best_core[y_1][x_1], y_2, x_2, N)
            elif best_core[y_2][x_2] != -1:
                new_cells = update(best_cells, best_core[y_2][x_2], y_1, x_1, N)
            #
            # print("x1, y1", x_1, y_1)
            # print("x2, y2", x_2, y_2)
            # print("cells", best_cells)
            # print("new cells", new_cells)
            # print("core", best_core)
            # print("new core", new_core)

            # calculate wire length using HPWL
            change_length = HPWL(netlist, new_cells, rows, cols) - HPWL_before

            if change_length < 0:
                # accept the change
                best_core = new_core.copy()
                best_cells = new_cells.copy()
                # core = new_core
                # cells = new_cells
            else:
                # calculate rejection probability
                if random.random() > equation(change_length, T):
                    best_core = new_core.copy()
                    best_cells = new_cells.copy()
                # else:
                # #best_core = current_core
                # if i == moves_per_temp:
                #     T = schedule_temp(T)
                #     i = -1
        T = schedule_temp(T)
        # print("i", i, "moves per temp", moves_per_temp)
        # print(T_final)
        # print(T)
    return best_core, best_cells


# core, cells, rows, cols, N, netlist, n_nets = readfile("d0.txt")
# print_core(core, rows, cols)
# print("Total wire length = ", end=" ")
# print(HPWL(netlist, cells, rows, cols))
# # swap_core(core, 0, 2, 0, 2)
# core2, cells2 = annealing(core, cells, rows, cols, N, netlist, n_nets)
# print_core(core2, rows, cols)
# print("Total wire length = ", end=" ")
# print(HPWL(netlist, cells2, rows, cols))


def window():
    app = QApplication(sys.argv)
    win = QWidget()
    grid = QGridLayout()
    
    core, cells, rows, cols, N, netlist, n_nets = readfile("d0.txt")
    core2, cells2 = annealing(core, cells, rows, cols, N, netlist, n_nets)
    
    grid.addWidget(QLabel("Cell Placement Tool"))

    for row in range(0, rows, 1):
        for col in range(0, cols, 1):
            if core2[row][col] != -1:
                grid.addWidget(QPushButton(str(core[row][col])),row+1,col)
            else:
                grid.addWidget(QPushButton("__"),row+1,col)
    
    
    grid.addWidget(QLabel("Wire Length = " + str(HPWL(netlist, cells2, rows, cols))), row+3, 0)

            
    win.setLayout(grid)
    win.setWindowTitle("Simulated-Annealing Cell Placement Tool - By: Maya Hussein & Mariam Abdelaziz")
    win.setGeometry(50,50,200,200)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   window()
   
   

