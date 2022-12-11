import random
import math
import numpy as np
import copy


def HPWL(netlist, cell, r, c, n_nets):
    total = 0
    init_net = {}
    k = 0
    for net in netlist:
        l_max = 0
        l_min = r
        w_max = 0
        w_min = c
        for i in net:
            if cell[int(i)][0] > l_max:
                l_max = cell[int(i)][0]
            elif cell[int(i)][0] < l_min:
                l_min = cell[int(i)][0]
            if cell[int(i)][1] > w_max:
                w_max = cell[int(i)][1]
            elif cell[int(i)][1] < w_min:
                w_min = cell[int(i)][1]
        # print("lmax, lmin", l_max, l_min)
        # print("wmax, wmin", w_max, w_min)
        halfPara = abs(l_max - l_min) + abs(w_max - w_min)
        init_net[k] = halfPara
        # print("hpwl small= ", halfPara)
        total = total + halfPara
        # print(k)
        k = k + 1
    return init_net, total


def mapping_cells(netlist, N):
    count = 0
    # mapp = [[0 for i in range(1)] for j in range(N)]
    mapp = [[] for j in range(N)]
    for net in netlist:
        for i in net:
            mapp[int(i)].append(count)
        count = count + 1
    return mapp


def HPWL_mod(init_NET, initial_HPWL, netlist, cel, mapping, c1, c2, r, c):
    # mod = []
    # if c1 == -1:
    #     mod.append(mapping[c2])
    # elif c2 == -1:
    #     mod.append(mapping[c1])
    # else:
    #     mod.append(mapping[c1])
    #
    # if len(mod) != 0:
    #     loop = 0
    #     for j in mod:
    #         l_max = 0
    #         l_min = r
    #         w_max = 0
    #         w_min = c
    #         if loop != 0:
    #             # print(i)
    #             loop2 = 0
    #             for i in netlist[j].split():
    #                 if loop2 != 0:
    #                     if cel[int(i)][0] > l_max:
    #                         l_max = cel[int(i)][0]
    #                     if cel[int(i)][0] < l_min:
    #                         l_min = cel[int(i)][0]
    #                     if cel[int(i)][1] > w_max:
    #                         w_max = cel[int(i)][1]
    #                     if cel[int(i)][1] < w_min:
    #                         w_min = cel[int(i)][1]
    #                 loop2 = loop2 + 1
    #             # print(c1)
    #             # print("lmax, lmin", l_max, l_min)
    #             # print("wmax, wmin", w_max, w_min)
    #             halfPara = abs(l_max - l_min) + abs(w_max - w_min)
    #             # print(initial_HPWL, init_NET[j], halfPara)
    #             initial_HPWL = initial_HPWL - init_NET[j]
    #             init_NET[j] = halfPara
    #             initial_HPWL = initial_HPWL + halfPara
    #         loop = loop + 1
    #
    #     if c1 != -1 and c2 != -1:
    #         for j in mapping[c2]:
    #             if j not in mod:
    #                 l_max = 0
    #                 l_min = r
    #                 w_max = 0
    #                 w_min = c
    #                 if loop != 0:
    #                     # print(i)
    #                     loop2 = 0
    #                     for i in netlist[j].split():
    #                         if loop2 != 0:
    #                             if cel[int(i)][0] > l_max:
    #                                 l_max = cel[int(i)][0]
    #                             if cel[int(i)][0] < l_min:
    #                                 l_min = cel[int(i)][0]
    #                             if cel[int(i)][1] > w_max:
    #                                 w_max = cel[int(i)][1]
    #                             if cel[int(i)][1] < w_min:
    #                                 w_min = cel[int(i)][1]
    #                         loop2 = loop2 + 1
    #                     # print(c1)
    #                     # print("lmax, lmin", l_max, l_min)
    #                     # print("wmax, wmin", w_max, w_min)
    #                     halfPara = abs(l_max - l_min) + abs(w_max - w_min)
    #                     # print(initial_HPWL, init_NET[j], halfPara)
    #                     initial_HPWL = initial_HPWL - init_NET[j]
    #                     init_NET[j] = halfPara
    #                     initial_HPWL = initial_HPWL + halfPara
    if c1 != -1:
        for j in mapping[c1]:
            l_max = 0
            l_min = r
            w_max = 0
            w_min = c
            for i in netlist[j]:
                if cel[int(i)][0] > l_max:
                    l_max = cel[int(i)][0]
                elif cel[int(i)][0] < l_min:
                    l_min = cel[int(i)][0]
                if cel[int(i)][1] > w_max:
                    w_max = cel[int(i)][1]
                elif cel[int(i)][1] < w_min:
                    w_min = cel[int(i)][1]
            # print(c1)
            # print("lmax, lmin", l_max, l_min)
            # print("wmax, wmin", w_max, w_min)
            halfPara = abs(l_max - l_min) + abs(w_max - w_min)
            # print(initial_HPWL, init_NET[j], halfPara)
            initial_HPWL = initial_HPWL - init_NET[j]
            init_NET[j] = halfPara
            initial_HPWL = initial_HPWL + halfPara
    if c2 != -1:
        for j in mapping[c2]:
            if j not in mapping[c1]:
                # mod.append(i)
                l_max = 0
                l_min = r
                w_max = 0
                w_min = c
                for i in netlist[j]:
                    if cel[int(i)][0] > l_max:
                        l_max = cel[int(i)][0]
                    elif cel[int(i)][0] < l_min:
                        l_min = cel[int(i)][0]
                    if cel[int(i)][1] > w_max:
                        w_max = cel[int(i)][1]
                    elif cel[int(i)][1] < w_min:
                        w_min = cel[int(i)][1]
                halfPara = abs(l_max - l_min) + abs(w_max - w_min)
                # print(initial_HPWL, init_NET[j], halfPara)
                initial_HPWL = initial_HPWL - init_NET[j]
                init_NET[j] = halfPara
                initial_HPWL = initial_HPWL + halfPara
    # else:
    # if len(mod) != 0:
    #     loop = 0
    #     for j in mod:
    #         l_max = 0
    #         l_min = r
    #         w_max = 0
    #         w_min = c
    #         if loop != 0:
    #             # print(i)
    #             loop2 = 0
    #             for i in netlist[j].split():
    #                 if loop2 != 0:
    #                     if cel[int(i)][0] > l_max:
    #                         l_max = cel[int(i)][0]
    #                     if cel[int(i)][0] < l_min:
    #                         l_min = cel[int(i)][0]
    #                     if cel[int(i)][1] > w_max:
    #                         w_max = cel[int(i)][1]
    #                     if cel[int(i)][1] < w_min:
    #                         w_min = cel[int(i)][1]
    #                 loop2 = loop2 + 1
    #             # print(c1)
    #             # print("lmax, lmin", l_max, l_min)
    #             # print("wmax, wmin", w_max, w_min)
    #             halfPara = abs(l_max - l_min) + abs(w_max - w_min)
    #             # print(initial_HPWL, init_NET[j], halfPara)
    #             initial_HPWL = initial_HPWL - init_NET[j]
    #             init_NET[j] = halfPara
    #             initial_HPWL = initial_HPWL + halfPara
    #         loop = loop + 1
    # return init_NET, initial_HPWL

    return init_NET, initial_HPWL


def readfile(path):
    with open(path, 'r') as file:
        # reading each line
        first_line = file.readline()
        N = first_line.split()
        print(N[0])
        cells = {}
        rows, cols = (int(N[2]), int(N[3]))
        c = [[-1 for i in range(cols)] for j in range(rows)]

        # cells = [[0 for i in range(2)] for j in range(int(N[0]))]
        # core = np.array(c)
        core = {}
        for row in range(0, rows, 1):
            for col in range(0, cols, 1):
                core[row, col] = -1

        for n in range(0, int(N[0]), 1):
            y = random.randint(0, rows - 1)
            x = random.randint(0, cols - 1)
            # print(y, x)
            while core[y, x] != -1:
                y = random.randint(0, rows - 1)
                x = random.randint(0, cols - 1)
            # cells[n][0] = x
            # cells[n][1] = y
            core[y, x] = n
            cells[n] = (x, y)

        # print(cells)
        # print(core)
        netlist = []
        for line in file:
            line = line.split()
            line.pop(0)
            # print(line)
            netlist.append(line)
        mapping = mapping_cells(netlist, int(N[0]))
        print("mapping")
        print(mapping)
        print()
        # print(netlist)
    return mapping, core, cells, rows, cols, int(N[0]), netlist, int(N[1])


def swap_core(co, x1, x2, y1, y2, a, b):
    # for row in range(0, rows, 1):
    #     for col in range(0, cols, 1):
    #         core2[row][col] = co[row][col]

    # num1 = co[y2][x2]
    # num2 = co[y1][x1]
    # core2[y1][x1] = num2
    # core2[y2][x2] =num1
    # coree = [[0 for i in range(cols)] for j in range(rows)]
    # coree = co.copy()
    # # num1 = co[y2][x2]
    # # num2 = co[y1][x1]
    # # coree[y1][x1] = num1
    # # coree[y2][x2] = num2
    # coree[y1][x1], coree[y2][x2] = coree[y2][x2], coree[y1][x1]
    # print(co[y2][x2], co[y1][x1])

    # cor = np.array(co)
    co[y1, x1] = b
    co[y2, x2] = a
    # co[[y1, x1]] = co[[y2, x2]]
    # print(co[y2][x2], co[y1][x1])
    return co


def print_core(coree, rowss, colss):
    for row in range(0, rowss, 1):
        for col in range(0, colss, 1):
            if (coree[row, col] != -1) and (coree[row, col] != "-1"):
                print(coree[row, col], end="\t")
            else:
                print("__", end="\t")
        print()
    print()


def swap(arr, index_1, index_2):
    # swaps 2 current_cells together
    # array2= array.copy()
    # array2[index_1]=array[index_2].copy()
    # array2[index_2]=array[index_1].copy()

    # array2 = [[0 for i in range(2)] for j in range(n)]
    #     array2 = array.copy()

    # array2 = np.array(arr)

    # for row in range(0, n, 1):
    #     for col in range(0, 2, 1):
    #         array2[row][col] = array[row][col]

    # array2[index_1], array2[index_2] = array2[index_2], array2[index_1]
    # array2[[index_1, index_2]] = array2[[index_2, index_1]]
    # print(arr[index_2], arr[index_1])
    temp = arr[index_1]
    arr[index_1] = arr[index_2]
    arr[index_2] = temp
    # print(array2[index_2], array2[index_1])
    # print(arr[index_2], arr[index_1])
    return arr


def schedule_temp(t):
    return t * 0.95


def equation(change_length, tem):
    return (1 - math.exp(-(change_length) / tem))


def update(cell, index, y, x):
    # array2 = [[0 for i in range(2)] for j in range(n)]
    # for row in range(0, n, 1):
    #     for col in range(0, 2, 1):
    #         array2[row][col] = best_cells[row][col]
    # array2 = best_cells.copy()
    # array2[index][0] = x_2
    # array2[index][1] = y_2
    # print(cell[index][0], cell[index][1])
    # cel2 = cell.copy()
    # cel2 = np.array(cell)
    cell[index] = (x, y)
    # print(cell[index][0], cell[index][1])
    # print(cel2[index][0], cel2[index][1])
    return cell #, cel2


# create annealing algorithm
def annealing(current_core, cell, rows, cols, N, netlist, n_nets, mapping):
    # set current best solution

    best_core = current_core.copy()
    best_cells = cell.copy()
    # set initial temperature
    init_net, HPWL_initial = HPWL(netlist, cell, rows, cols, n_nets)
    print("Total wire length = ", end=" ")
    print(HPWL_initial)
    T = 500 * HPWL_initial
    # set cooling rate
    T_final = (5 * 0.000001 * HPWL_initial) / n_nets

    moves_per_temp = 10 * N
    HPWL_before = HPWL_initial
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

            # HPWL_before = HPWL_initial
            # swaps 2 current_cells together
            # new_core = swap_core(best_core.copy(), x_1, x_2, y_1, y_2, rows, cols)
            # print("new")

            if (best_core[y_2, x_2] != -1) and (best_core[y_1, x_1] != -1):
                new_cells = swap(best_cells.copy(), best_core[y_1, x_1], best_core[y_2, x_2])
                # print("1")
            elif best_core[y_1, x_1] != -1:
                new_cells = update(best_cells.copy(), best_core[y_1, x_1], y_2, x_2)
                # print("2")
            elif best_core[y_2, x_2] != -1:
                new_cells = update(best_cells.copy(), best_core[y_2, x_2], y_1, x_1)
                # print("3")

            # calculate wire length using HPWL
            new_init_net, new_hpwl = HPWL_mod(init_net.copy(), HPWL_before, netlist, new_cells.copy(), mapping,
                                              best_core[y_1, x_1], best_core[y_2, x_2], rows, cols)
            # print(best_core[y_1][x_1], best_core[y_2][x_2])
            # print("x1", x_1, "y1", y_1, "x2", x_2, "y2", y_2)
            # print(best_cells)
            # print(best_core)
            # print(new_cells)
            # print(new_core)
            # print(init_net)
            # print(HPWL_before)
            # print(new_init_net)
            # print(new_hpwl)
            change_length = new_hpwl - HPWL_before

            if change_length < 0:
                # accept the change
                # print(init_net, HPWL_before, new_init_net, new_hpwl, int(best_core[y_1][x_1]), "x", x_1, "y", y_1,
                #       int(best_core[y_2][x_2]), "x", x_2, "y", y_2)
                new_core = swap_core(best_core.copy(), x_1, x_2, y_1, y_2, best_core[y_1, x_1],
                                                best_core[y_2, x_2])
                best_core = new_core
                best_cells = new_cells
                HPWL_before = new_hpwl
                init_net = new_init_net.copy()
                # print("taken")
                # core = new_core
                # cells = new_cells
            else:
                # calculate rejection probability
                if random.random() > equation(change_length, T):
                    # print(init_net, HPWL_before, new_init_net, new_hpwl, int(best_core[y_1][x_1]), "x", x_1, "y", y_1,
                    #       int(best_core[y_2][x_2]), "x", x_2, "y", y_2)
                    new_core = swap_core(best_core.copy(), x_1, x_2, y_1, y_2, best_core[y_1, x_1],
                                                    best_core[y_2, x_2])
                    best_core = new_core
                    best_cells = new_cells
                    HPWL_before = new_hpwl
                    init_net = new_init_net
                #     print("taken")
                # else:
                #     print("not taken")
                # else:
                # #best_core = current_core
                # if i == moves_per_temp:
                #     T = schedule_temp(T)
                #     i = -1
        T = schedule_temp(T)
        # print("i", i, "moves per temp", moves_per_temp)
        # print(T_final)
        # print(T)
    return HPWL_before, best_core, best_cells


mapping, core, cells, rows, cols, N, netlist, n_nets = readfile("t1.txt")
print(netlist)
print_core(core, rows, cols)
print()
final_hpwl, core2, cells2 = annealing(core, cells, rows, cols, N, netlist, n_nets, mapping)
print_core(core2, rows, cols)
print()
print("Total wire length = ", end=" ")
print(final_hpwl)

