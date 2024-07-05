

#include "m_inversion_5.h"

int minver(int row, int col, double eps);
int mmul(int row_a, int col_a, int row_b, int col_b);

const int MATRIX_SIZE = 5; // 5X5

static double a[MATRIX_SIZE][MATRIX_SIZE] = {
    {3.0, -6.0, 7.0, -4, 1.1},
    {3.0, -6.0, 7.0, 2, 3.2},
    {9.0, 0, -5.0, 9, 3},
    {5.0, -8.0, 6.0, -7, 2.1},
    {2.0, -20.0, 1.0, -7, 8}};

double b[MATRIX_SIZE][MATRIX_SIZE],
    c[MATRIX_SIZE][MATRIX_SIZE],
    aa[MATRIX_SIZE][MATRIX_SIZE],
    a_i[MATRIX_SIZE][MATRIX_SIZE],
    e[MATRIX_SIZE][MATRIX_SIZE],
    det;

double minver_fabs(double n)
{
    double f;

    if (n >= 0)
        f = n;
    else
        f = -n;
    return f;
}

int m_inversion_5()
{
    int i, j;
    double eps;

    eps = 1.0e-6;

    for (i = 0; i < MATRIX_SIZE; i++)
        for (j = 0; j < MATRIX_SIZE; j++)
            aa[i][j] = a[i][j];

    minver(MATRIX_SIZE, MATRIX_SIZE, eps);
    for (i = 0; i < MATRIX_SIZE; i++)
        for (j = 0; j < MATRIX_SIZE; j++)
            a_i[i][j] = a[i][j];

    mmul(MATRIX_SIZE, MATRIX_SIZE, MATRIX_SIZE, MATRIX_SIZE);
    return 0;
}

int mmul(int row_a, int col_a, int row_b, int col_b)
{
    int i, j, k, row_c, col_c;
    double w;

    row_c = row_a;
    col_c = col_b;

    if (row_c < 1 || row_b < 1 || col_c < 1 || col_a != row_b)
        return (999);
    for (i = 0; i < row_c; i++)
    {
        for (j = 0; j < col_c; j++)
        {
            w = 0.0;
            for (k = 0; k < row_b; k++)
                w += a[i][k] * b[k][j];
            c[i][j] = w;
        }
    }
    return (0);
}

int minver(int row, int col, double eps)
{

    int work[500], i, j, k, r, iw, s, t, u, v;
    double w, wmax, pivot, api, w1;

    if (row < 2 || row > 500 || eps <= 0.0)
        return (999);
    w1 = 1.0;
    for (i = 0; i < row; i++)
        work[i] = i;
    for (k = 0; k < row; k++)
    {
        wmax = 0.0;
        for (i = k; i < row; i++)
        {
            w = minver_fabs(a[i][k]);
            if (w > wmax)
            {
                wmax = w;
                r = i;
            }
        }
        pivot = a[r][k];
        api = minver_fabs(pivot);
        if (api <= eps)
        {
            det = w1;
            return (1);
        }
        w1 *= pivot;
        u = k * col;
        v = r * col;
        if (r != k)
        {
            w1 = -w;
            iw = work[k];
            work[k] = work[r];
            work[r] = iw;
            for (j = 0; j < row; j++)
            {
                s = u + j;
                t = v + j;
                w = a[k][j];
                a[k][j] = a[r][j];
                a[r][j] = w;
            }
        }
        for (i = 0; i < row; i++)
            a[k][i] /= pivot;
        for (i = 0; i < row; i++)
        {
            if (i != k)
            {
                v = i * col;
                s = v + k;
                w = a[i][k];
                if (w != 0.0)
                {
                    for (j = 0; j < row; j++)
                        if (j != k)
                            a[i][j] -= w * a[k][j];
                    a[i][k] = -w / pivot;
                }
            }
        }
        a[k][k] = 1.0 / pivot;
    }
    for (i = 0; i < row; i++)
    {
        while (1)
        {
            k = work[i];
            if (k == i)
                break;
            iw = work[k];
            work[k] = work[i];
            work[i] = iw;
            for (j = 0; j < row; j++)
            {
                u = j * col;
                s = u + i;
                t = u + k;
                w = a[k][i];
                a[k][i] = a[k][k];
                a[k][k] = w;
            }
        }
    }
    det = w1;
    return (0);
}

//-------------
//  MAIN
//-------------

int main()
{
    m_inversion_5();

    return 0;
}