import random
import math


def HPWL(netlist, cell, r, c, n_nets):
    total = 0
    init_net = {}
    k = 0
    for net in netlist:
        X = []
        Y = []
        for i in net:
            X.append(cell[i][0])
            Y.append(cell[i][1])
        halfPara = (max(X)-min(X))+(max(Y)-min(Y))
        init_net[k] = halfPara
        total = total + halfPara
        k = k + 1
    return init_net, total


def mapping_cells(netlist, N):
    count = 0
    mapp = [[] for j in range(N)]
    for net in netlist:
        for i in net:
            mapp[i].append(count)
        count = count + 1
    return mapp


def HPWL_mod_2(init_NET, initial_HPWL, netlist, cel, mapping, c1, c2):
    k = 0
    vec = {}
    for j in mapping[c1]:
        X = []
        Y = []
        for i in netlist[j]:
            X.append(cel[i][0])
            Y.append(cel[i][1])
        halfPara = (max(X)-min(X))+(max(Y)-min(Y))
        initial_HPWL = initial_HPWL - init_NET[j] + halfPara
        # init_NET[j] = halfPara
        vec[k] = halfPara
        k = k + 1

    for j in mapping[c2]:
        if j not in mapping[c1]:
            X = []
            Y = []
            for i in netlist[j]:
                X.append(cel[i][0])
                Y.append(cel[i][1])
            halfPara = (max(X)-min(X))+(max(Y)-min(Y))
            initial_HPWL = initial_HPWL - init_NET[j] + halfPara
            # init_NET[j] = halfPara
            vec[k] = halfPara
            k = k + 1

    return vec, initial_HPWL


def HPWL_mod_1(init_NET, initial_HPWL, netlist, cel, mapping, c):
    k = 0
    vec = {}
    for j in mapping[c]:
        X = []
        Y = []
        for i in netlist[j]:
            X.append(cel[i][0])
            Y.append(cel[i][1])
        halfPara = (max(X)-min(X))+(max(Y)-min(Y))
        initial_HPWL = initial_HPWL - init_NET[j] + halfPara
        vec[k] = halfPara
        k = k + 1
    return vec, initial_HPWL
    #     init_NET[j] = halfPara
    #
    # return init_NET, initial_HPWL


def mod_1(init_NET, vec, mapping, c):
    i = 0
    for j in mapping[c]:
        init_NET[j] = vec[i]
        i = i + 1


def mod_2(init_NET, vec1, mapping, c1, c2):
    i = 0
    for j in mapping[c1]:
        init_NET[j] = vec1[i]
        i = i + 1

    for j in mapping[c2]:
        if j not in mapping[c1]:
            init_NET[j] = vec1[i]
            i = i + 1


def readfile(path):
    with open(path, 'r') as file:
        # reading each line
        first_line = file.readline()
        N = first_line.split()
        print(N[0])
        cells = {}
        rows, cols = (int(N[2]), int(N[3]))
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
            core[y, x] = n
            cells[n] = (x, y)

        netlist = []
        for line in file:
            line = line.split()
            line.pop(0)
            line = [eval(i) for i in line]
            netlist.append(line)
        mapping = mapping_cells(netlist, int(N[0]))
        print("mapping")
        print(mapping)
        print()
    return mapping, core, cells, rows, cols, int(N[0]), netlist, int(N[1])


def swap_core(co, x1, x2, y1, y2, a, b):
    co[y1, x1] = b
    co[y2, x2] = a
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
    temp = arr[index_1]
    arr[index_1] = arr[index_2]
    arr[index_2] = temp
    return arr


def schedule_temp(t):
    return t * 0.95


def equation(change_length, tem):
    return (1 - math.exp(-(change_length) / tem))


def update(cell, index, y, x):
    cell[index] = (x, y)

    return cell


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
    T_final = (5 * 0.00001 * HPWL_initial) / n_nets

    moves_per_temp = 10 * N
    HPWL_before = HPWL_initial
    # loop until system has cooled
    while T > T_final:
        for i in range(0, moves_per_temp, 1):
            x_1 = random.randint(0, cols - 1)
            x_2 = random.randint(0, cols - 1)
            y_1 = random.randint(0, rows - 1)
            y_2 = random.randint(0, rows - 1)

            while ((x_1 == x_2) and (y_1 == y_2)) or (best_core[y_1, x_1] == -1 and best_core[y_2, x_2] == -1):
                # choose another cell for cell_2
                x_2 = random.randint(0, cols - 1)
                y_2 = random.randint(0, rows - 1)
            c2 = best_core[y_2, x_2]
            c1 = best_core[y_1, x_1]
            if (c2 != -1) and (c1 != -1):
                # new_cells = best_cells.copy()
                temp = best_cells[c1]
                best_cells[c1] = best_cells[c2]
                best_cells[c2] = temp
                vec, new_hpwl = HPWL_mod_2(init_net, HPWL_before, netlist, best_cells, mapping, c1, c2)
                change_length = new_hpwl - HPWL_before
                if change_length < 0:
                    mod_2(init_net, vec, mapping, c1, c2)
                    temp = best_core[y_2, x_2]
                    best_core[y_2, x_2] = best_core[y_1, x_1]
                    best_core[y_1, x_1] = temp
                    # best_cells = new_cells
                    HPWL_before = new_hpwl
                    # init_net = new_init_net

                else:
                    # calculate rejection probability
                    if random.random() > equation(change_length, T):
                        mod_2(init_net, vec, mapping, c1, c2)
                        temp = best_core[y_2, x_2]
                        best_core[y_2, x_2] = best_core[y_1, x_1]
                        best_core[y_1, x_1] = temp
                        # best_cells = new_cells
                        HPWL_before = new_hpwl
                        # init_net = new_init_net
                    else:  # new_cells = best_cells.copy()
                        temp = best_cells[c1]
                        best_cells[c1] = best_cells[c2]
                        best_cells[c2] = temp

            elif c1 != -1:
                # new_cells = best_cells.copy()
                best_cells[c1] = (x_2, y_2)
                vec, new_hpwl = HPWL_mod_1(init_net, HPWL_before, netlist, best_cells, mapping, c1)
                change_length = new_hpwl - HPWL_before
                if change_length < 0:
                    mod_1(init_net, vec, mapping, c1)
                    temp = best_core[y_2, x_2]
                    best_core[y_2, x_2] = best_core[y_1, x_1]
                    best_core[y_1, x_1] = temp
                    # best_cells = new_cells
                    HPWL_before = new_hpwl
                    # init_net = new_init_net

                else:
                    # calculate rejection probability
                    if random.random() > equation(change_length, T):
                        mod_1(init_net, vec, mapping, c1)
                        temp = best_core[y_2, x_2]
                        best_core[y_2, x_2] = best_core[y_1, x_1]
                        best_core[y_1, x_1] = temp
                        # best_cells = new_cells
                        HPWL_before = new_hpwl
                        # init_net = new_init_net
                    else:
                        best_cells[c1] = (x_1, y_1)
                # print("2")
            elif c2 != -1:
                # new_cells = best_cells.copy()
                best_cells[c2] = (x_1, y_1)
                vec, new_hpwl = HPWL_mod_1(init_net, HPWL_before, netlist, best_cells, mapping, c2)
                change_length = new_hpwl - HPWL_before
                if change_length < 0:
                    mod_1(init_net, vec, mapping, c2)
                    temp = best_core[y_2, x_2]
                    best_core[y_2, x_2] = best_core[y_1, x_1]
                    best_core[y_1, x_1] = temp
                    # best_cells = new_cells
                    HPWL_before = new_hpwl
                    # init_net = new_init_net

                else:
                    # calculate rejection probability
                    if random.random() > equation(change_length, T):
                        mod_1(init_net, vec, mapping, c2)
                        temp = best_core[y_2, x_2]
                        best_core[y_2, x_2] = best_core[y_1, x_1]
                        best_core[y_1, x_1] = temp
                        # best_cells = new_cells
                        HPWL_before = new_hpwl
                        # init_net = new_init_net
                    else:                   # new_cells = best_cells.copy()
                        best_cells[c2] = (x_2, y_2)

        T = schedule_temp(T)

    return HPWL_before, best_core, best_cells


random.seed(10)
mapping, core, cells, rows, cols, N, netlist, n_nets = readfile("d0.txt")
print(netlist)
print_core(core, rows, cols)
print()
final_hpwl, core2, cells2 = annealing(core, cells, rows, cols, N, netlist, n_nets, mapping)
print_core(core2, rows, cols)
print()
print("Total wire length = ", end=" ")
print(final_hpwl)
