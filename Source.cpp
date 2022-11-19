#include <iostream>
#include <fstream>
using namespace std;

void fill_grid(int* data, int size, int** grid)
{
    for (int i = 0; i < size - 1; i++)
    {
        grid[data[i]][data[i + 1]] = 1;
        grid[data[i + 1]][data[i]] = 1;
    }
}
int** read_file(int& N, int& n_con, int& row, int& col)
{
    ifstream read;
    read.open("d0.txt");
    read >> N >> n_con >> row >> col;
    int** grid;
    grid = new int* [N];

    for (int i = 0; i < N; i++)
    {
        grid[i] = new int[N];
    }
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            grid[i][j] = 0;
        }
    }
    for (int i = 0; i < n_con; i++)
    {
        int comp;
        read >> comp;
        int* x = new int[comp];
        for (int i = 0; i < comp; i++)
        {
            read >> x[i];
        }
        fill_grid(x, comp, grid);
    }

    read.close();
    return grid;
}


int main()
{
    int row, col;
    int N, n_con;
    int** core=0, ** grid=0;
    grid=read_file(N, n_con, row, col);
    core = new int* [row];
    for (int i = 0; i < row; i++)
    {
        core[i] = new int[col];
    }
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            cout << grid[i][j] << " ";
        }
        cout << endl;
    }
    return 0;
}