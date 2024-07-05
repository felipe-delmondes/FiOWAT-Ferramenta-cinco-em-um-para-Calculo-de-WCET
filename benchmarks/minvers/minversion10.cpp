/* MDH WCET BENCHMARK SUITE. File version $Id: minver.c 7801 2018-01-19 13:33:32Z lkg02 $ */

/* 2012/09/28, Jan Gustafsson <jan.gustafsson@mdh.se>
 * Changes:
 *  - Missing braces around initialization of subobject added
 *  - This program redefines the standard C function fabs. Therefore, the
 *  function has been renamed to minver_fabs.
 */

/*************************************************************************/
/*                                                                       */
/*   SNU-RT Benchmark Suite for Worst Case Timing Analysis               */
/*   =====================================================               */
/*                              Collected and Modified by S.-S. Lim      */
/*                                           sslim@archi.snu.ac.kr       */
/*                                         Real-Time Research Group      */
/*                                        Seoul National University      */
/*                                                                       */
/*                                                                       */
/*        < Features > - restrictions for our experimental environment   */
/*                                                                       */
/*          1. Completely structured.                                    */
/*               - There are no unconditional jumps.                     */
/*               - There are no exit from loop bodies.                   */
/*                 (There are no 'break' or 'return' in loop bodies)     */
/*          2. No 'switch' statements.                                   */
/*          3. No 'do..while' statements.                                */
/*          4. Expressions are restricted.                               */
/*               - There are no multiple expressions joined by 'or',     */
/*                'and' operations.                                      */
/*          5. No library calls.                                         */
/*               - All the functions needed are implemented in the       */
/*                 source file.                                          */
/*                                                                       */
/*                                                                       */
/*************************************************************************/
/*                                                                       */
/*  FILE: minver.c                                                       */
/*  SOURCE : Turbo C Programming for Engineering by Hyun Soo Ahn         */
/*                                                                       */
/*  DESCRIPTION :                                                        */
/*                                                                       */
/*     Matrix inversion for 3x3 floating point matrix.                   */
/*                                                                       */
/*  REMARK :                                                             */
/*                                                                       */
/*  EXECUTION TIME :                                                     */
/*                                                                       */
/*                                                                       */
/*************************************************************************/

#include "m_inversion_10.h"

int minver(int row, int col, double eps);
int mmul(int row_a, int col_a, int row_b, int col_b);

const int MATRIX_SIZE = 10; // 5X5

static double a[MATRIX_SIZE][MATRIX_SIZE] = {
    {3.0, -6.0, 7.0, -4, 1.1, 12.0, 6.0, 17.0, -14, 0.1},
    {3.0, -6.0, 7.0, 2, 3.2, 13.0, 0, 7.0, 4, 1.1},
    {9.0, 0, -5.0, 9, 3, 3.0, 3, 0, -4, 10},
    {5.0, -8.0, 6.0, -7, 2.1, 30, 0, 8.0, -40, 15},
    {2.0, -20.0, 1.0, -7, 8, 27, 10, 9.0, 0, 13},
    {1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.1},
    {2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 12, 21, 3, 4.5},
    {
        5.0,
        -8.0,
        6.0,
        -6.0,
        7.0,
        2,
        -6.0,
        7.0,
        2,
        3.2,
    },
    {5.0, -8.0, 6.0, -7, 2.1, 10, 11, 13, 15, 17},
    {2.0, -20.0, 1.0, -7, 8, 2.0, -20.0, 1.0, -7, 8}};

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

int m_inversion_10()
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

int main()
{
    m_inversion_10();

    return 0;
}