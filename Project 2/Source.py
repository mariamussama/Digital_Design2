import random
import math
import numpy as np
import copy


def HPWL(netlist, cell, r, c, n_nets):
    total = 0
    init_net = [0 for i in range(n_nets)]
    k = 0
    for net in netlist:
        l_max = 0
        l_min = r
        w_max = 0
        w_min = c
        loop = 0
        for i in net.split():
            if loop != 0:
                # print(i)
                if cell[int(i)][0] > l_max:
                    l_max = cell[int(i)][0]
                if cell[int(i)][0] < l_min:
                    l_min = cell[int(i)][0]
                if cell[int(i)][1] > w_max:
                    w_max = cell[int(i)][1]
                if cell[int(i)][1] < w_min:
                    w_min = cell[int(i)][1]
            loop = loop + 1
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
    mapp = [[0 for i in range(1)] for j in range(N)]
    for net in netlist:
        loop = 0
        for i in net.split():
            if loop != 0:
                # print(int(i))
                mapp[int(i)].append(count)
            loop = loop + 1
        count = count + 1

    return mapp


def HPWL_mod(init_NET, initial_HPWL, netlist, cel, mapping, c1, c2, r, c):

        mod = []
        if c1 != -1:
            mod.append(mapping[c1])
            if c2 != -1:
                for i in mapping[c2]:
                    if i in mapping[c1]:
                        t = 0
                    else:
                        mod.append(i)
        elif c2 != -1:
            mod.append(mapping[c2])
        if len(mod) != 0:
            loop = 0
            for j in mod:
                l_max = 0
                l_min = r
                w_max = 0
                w_min = c
                if loop != 0:
                    # print(i)
                    loop2 = 0
                    for i in netlist[j].split():
                        if loop2 != 0:
                            if cel[int(i)][0] > l_max:
                                l_max = cel[int(i)][0]
                            if cel[int(i)][0] < l_min:
                                l_min = cel[int(i)][0]
                            if cel[int(i)][1] > w_max:
                                w_max = cel[int(i)][1]
                            if cel[int(i)][1] < w_min:
                                w_min = cel[int(i)][1]
                        loop2 = loop2 + 1
                    # print(c1)
                    # print("lmax, lmin", l_max, l_min)
                    # print("wmax, wmin", w_max, w_min)
                    halfPara = abs(l_max - l_min) + abs(w_max - w_min)
                    # print(initial_HPWL, init_NET[j], halfPara)
                    initial_HPWL = initial_HPWL - init_NET[j]
                    init_NET[j] = halfPara
                    initial_HPWL = initial_HPWL + halfPara
                loop = loop + 1
        return init_NET, initial_HPWL
    # print("new")
    # if c1 != -1:
    #     loop = 0
    #     for j in mapping[c1]:
    #         l_max = 0
    #         l_min = r
    #         w_max = 0
    #         w_min = c
    #         if loop != 0:
    #             # print(i)
    #             loop2 = 0
    #             for i in netlist[j].split():
    #                 if loop2 != 0:
    #                     # print("cell", i, "x", cel[int(i)][1], "y", cel[int(i)][0])
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
    #             # print(initial_HPWL, init_NET[j], halfPara)
    #         loop = loop + 1
    #     # print("hpwl small= ", halfPara)
    # if c2 != -1:
    #     loop = 0
    #     for j in mapping[c2]:
    #         l_max = 0
    #         l_min = r
    #         w_max = 0
    #         w_min = c
    #         if loop != 0:
    #             # print(i)
    #             loop2 = 0
    #             for i in netlist[j].split():
    #                 if loop2 != 0:
    #                     # print("cell", i, "x", cel[int(i)][1], "y", cel[int(i)][0])
    #                     if cel[int(i)][0] > l_max:
    #                         l_max = cel[int(i)][0]
    #                     if cel[int(i)][0] < l_min:
    #                         l_min = cel[int(i)][0]
    #                     if cel[int(i)][1] > w_max:
    #                         w_max = cel[int(i)][1]
    #                     if cel[int(i)][1] < w_min:
    #                         w_min = cel[int(i)][1]
    #                 loop2 = loop2 + 1
    #             # print(c2)
    #             # print("lmax, lmin", l_max, l_min)
    #             # print("wmax, wmin", w_max, w_min)
    #             halfPara = abs(l_max - l_min) + abs(w_max - w_min)
    #             # print(initial_HPWL, init_NET[j], halfPara)
    #             initial_HPWL = initial_HPWL - init_NET[j]
    #             init_NET[j] = halfPara
    #             initial_HPWL = initial_HPWL + halfPara
    #             # print(initial_HPWL, init_NET[j], halfPara)
    #         loop = loop + 1



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
    cor = np.array(co)
    cor[y1][x1] = b
    cor[y2][x2] = a
    # print(co[y2][x2], co[y1][x1])
    return co, cor


def print_core(coree, rowss, colss):
    for row in range(0, rowss, 1):
        for col in range(0, colss, 1):
            if (coree[row][col] != -1) and (coree[row][col] != "-1"):
                print(coree[row][col], end="\t")
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
    array2 = np.array(arr)
    # for row in range(0, n, 1):
    #     for col in range(0, 2, 1):
    #         array2[row][col] = array[row][col]

    # array2[index_1], array2[index_2] = array2[index_2], array2[index_1]
    array2[[index_1, index_2]] = array2[[index_2, index_1]]

    # print(array2[index_2], array2[index_1])
    # print(arr[index_2], arr[index_1])
    return arr, array2


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
    # print(best_cells[index][0], best_cells[index][1])
    # cel2 = cell.copy()
    cel2 = np.array(cell)
    cel2[index][0] = x
    cel2[index][1] = y
    # print(cell[index][0], cell[index][1])
    # print(cel2[index][0], cel2[index][1])
    return cell, cel2


# create annealing algorithm
def annealing(current_core, cell, rows, cols, N, netlist, n_nets, mapping):
    # set current best solution

    best_core = current_core.copy()
    best_cells = cell.copy()
    # set initial temperature
    init_net, HPWL_initial = HPWL(netlist, cell, rows, cols, n_nets)
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

            if (best_core[y_2][x_2] != -1) and (best_core[y_1][x_1] != -1):
                best_cells, new_cells = swap(best_cells.copy(), best_core[y_1][x_1], best_core[y_2][x_2])
                # print("1")
            elif best_core[y_1][x_1] != -1:
                best_cells, new_cells = update(best_cells.copy(), best_core[y_1][x_1], y_2, x_2)
                # print("2")
            elif best_core[y_2][x_2] != -1:
                best_cells, new_cells = update(best_cells.copy(), best_core[y_2][x_2], y_1, x_1)
                # print("3")

            best_core, new_core = swap_core(best_core.copy(), x_1, x_2, y_1, y_2, best_core[y_1][x_1],
                                            best_core[y_2][x_2])
            # calculate wire length using HPWL
            new_init_net, new_hpwl = HPWL_mod(init_net.copy(), HPWL_before, netlist, new_cells.copy(), mapping,
                                              best_core[y_1][x_1], best_core[y_2][x_2], rows, cols)
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
                best_core = new_core.copy()
                best_cells = new_cells.copy()
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
                    best_core = new_core.copy()
                    best_cells = new_cells.copy()
                    HPWL_before = new_hpwl
                    init_net = new_init_net.copy()
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

init_Net, initial = HPWL(netlist, cells, rows, cols, n_nets)
print(init_Net)
print()
print_core(core, rows, cols)
print("Total wire length = ", end=" ")
print(initial)
print()
# swap_core(core, 0, 2, 0, 2)
final_hpwl, core2, cells2 = annealing(core, cells, rows, cols, N, netlist, n_nets, mapping)
# init_net2, initial2 = HPWL(netlist, cells2, rows, cols, n_nets)
print_core(core2, rows, cols)
print("Total wire length = ", end=" ")
print(final_hpwl)
# print(init_net2, initial2)
