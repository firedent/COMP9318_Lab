import numpy as np


def v_opt_dp(x, num_bins):
    """
    dp from bottom to top
    >>> x = [3, 1, 18, 11, 13, 17]
    >>> num_bins = 4
    >>> M, Bins = v_opt_dp(x, num_bins)
    >>> Bins
    [[3, 1], [18], [11, 13], [17]]
    >>> M
    [[-1, -1, -1, 18.666666666666664, 8.0, 0.0], [-1, -1, 18.666666666666664, 2.0, 0.0, -1], [-1, 18.666666666666664, 2.0, 0.0, -1, -1], [4.0, 2.0, 0.0, -1, -1, -1]]
    """
    SSE = lambda l: np.var(l)*len(l)
    matrix = [[-1]*len(x) for _ in range(num_bins)]
    d = dict()
    for i in range(num_bins):
        for j in range(len(x)-1-i, num_bins-2-i, -1):
            if i == 0:
                matrix[i][j] = SSE(x[j:])
            else:
                # matrix[i][j] = min((SSE(x[j:k]) + matrix[i - 1][k]) for k in range(j + 1, len(x)))
                min_opt = SSE(x[j:j+1]) + matrix[i - 1][j+1]
                p = j+1
                for k in range(j+2, len(x)):
                    tmp = SSE(x[j:k]) + matrix[i - 1][k]
                    if tmp < min_opt:
                        p = k
                        min_opt = tmp
                matrix[i][j] = min_opt
                d[(i, j)] = (i-1, p)
    
    p = (num_bins-1, 0)
    split_point = [0]
    while p[0] > 0:
        p = d[p]
        split_point.append(p[1])
    split_point.append(len(x))
    x_nex = []
    for i in range(len(split_point)-1):
        x_nex.append(x[split_point[i]:split_point[i+1]])

    return matrix, x_nex

