import random
import math
import numpy as np
import copy

random.seed(10)

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
   
    cel2 = np.array(cell)
    cel2[index][0] = x
    cel2[index][1] = y
    # print(cell[index][0], cell[index][1])
    # print(cel2[index][0], cel2[index][1])
    return cell, cel2

# create annealing algorithm
def annealing(current_core, cell, rows, cols, N, netlist, n_nets, mapping):
    temp = []
    hpwl = []
    best_core = current_core.copy()
    best_cells = cell.copy()
    # set initial temperature
    init_net, HPWL_initial = HPWL(netlist, cell, rows, cols, n_nets)
    # hpwl.append(HPWL_initial)
    T = 500 * HPWL_initial
    # temp.append(T)
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
      
            change_length = new_hpwl - HPWL_before

            if change_length < 0:
                # accept the change
                best_core = new_core.copy()
                best_cells = new_cells.copy()
                HPWL_before = new_hpwl
                init_net = new_init_net.copy()
  
            else:
                # calculate rejection probability
                if random.random() > equation(change_length, T):
                    # print(init_net, HPWL_before, new_init_net, new_hpwl, int(best_core[y_1][x_1]), "x", x_1, "y", y_1,
                    #       int(best_core[y_2][x_2]), "x", x_2, "y", y_2)
                    best_core = new_core.copy()
                    best_cells = new_cells.copy()
                    HPWL_before = new_hpwl
                    init_net = new_init_net.copy()
                #     i = -1
        T = schedule_temp(T)
        temp.append(T)
        hpwl.append(HPWL_before)
    return HPWL_before, best_core, best_cells, temp, hpwl


mapping, core, cells, rows, cols, N, netlist, n_nets = readfile("d0.txt")

init_Net, initial = HPWL(netlist, cells, rows, cols, n_nets)
print(init_Net)
print()
print_core(core, rows, cols)
print("Total wire length = ", end=" ")
print(initial)
print()
# swap_core(core, 0, 2, 0, 2)
final_hpwl, core2, cells2, temp, hpwl = annealing(core, cells, rows, cols, N, netlist, n_nets, mapping)
# init_net2, initial2 = HPWL(netlist, cells2, rows, cols, n_nets)
print_core(core2, rows, cols)
print("Total wire length = ", end=" ")
print(final_hpwl)
# print(init_net2, initial2)


from matplotlib import pyplot as plt

# Median Developer Salaries by Age
dev_x = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.97]

dev_y = [62, 60, 60, 51, 46,
         40, 38]

plt.plot(temp, hpwl)
plt.xlabel('Temperature')
plt.ylabel('Total Wire Length')
plt.title('TWL vs Temperature')
plt.show()


import os
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio




filenames = []
for i in range(len(hpwl)):
    # plot the line chart
    
    # naming the x axis
    plt.xlabel('Time')
    # naming the y axis
    plt.ylabel('Wire Length')
    # giving a title to my graph
    plt.title('Wire Length vs Time')

    plt.plot(hpwl[:i])
    
    # create file name and append it to a list
    filename = f'{i}.png'
    filenames.append(filename)
    
    # save frame
    plt.savefig(filename)
    plt.close()
# build gif
with imageio.get_writer('d0.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)
        
# Remove files
for filename in set(filenames):
    os.remove(filename)
























# time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ]

# import matplotlib.pyplot as plt
# import imageio


# def create_frame(t):
#     fig = plt.figure(figsize=(10, 10))
#     plt.plot(temp[:(t+1)], hpwl[:(t+1)], color = 'grey' )
#     plt.plot(temp[t], hpwl[t], color = 'black', marker = 'o' )
#     plt.xlim([0,5])
#     plt.xlabel('x', fontsize = 14)
#     plt.ylim([0,5])
#     plt.ylabel('y', fontsize = 14)
#     plt.title(f'Relationship between x and y at step {t}',
#               fontsize=14)
#     plt.savefig(f'img_{t}.png', 
#                 transparent = False,  
#                 facecolor = 'white'
#                )
#     plt.close()

# for t in time:
#     create_frame(t)
    
    
# frames = []
# for t in time:
#     image = imageio.v2.imread(f'img_{t}.png')
#     frames.append(image)
    
# imageio.mimsave('./example.gif', # output gif
#                 frames,          # array of input frames
#                 fps = 5)         # optional: frames per second