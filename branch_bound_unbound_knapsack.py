import math

def upperBound(W_a, VN, i, weight, value):
    """
    Find Upper Bound for Knapsack Problem
    """

    weight = weight
    value = value
    n = len(value)

    if i + 2 < n:
        v1, v2, v3 = value[i], value[i+1], value[i+2]
        w1, w2, w3 = weight[i], weight[i+1], weight[i+2]

        z_a = VN + (W_a//w2) * v2
        W_a_a = W_a - (W_a//w2) * w2
        U_a = z_a + (W_a_a*(v3//w3))

        ceil = math.ceil((w2 - W_a_a)/w1)
        U_a_a = z_a + math.floor((W_a_a + w1*ceil)*v2/w2 - ceil/v1)

        U = max(U_a, U_a_a)
    else:
        U = VN

    return U

def eliminateDominated(n, value, weight):
    """
    Eliminate dominated items to reduce computing time
    """
    N = list(range(n))
    j = 0

    while j < len(N)-1:
        k = j + 1
        while k < len(N):
            if (weight[N[k]]//weight[N[j]])*value[N[j]] >= value[N[k]]:
                N.pop(k)
            elif (weight[N[j]]//weight[N[k]])*value[N[k]] >= value[N[j]]:
                N.pop(j)
                k = len(N)
            else:
                k += 1
        j += 1
    
    value_updated = [value[i] for i in N]
    weight_updated = [weight[i] for i in N]
    n_updated = len(value_updated)

    return n_updated, value_updated, weight_updated

def initialize(W, n, value, weight):
    """
    Initialize all parameters needed to calculate solution
    """
    
    n, value, weight = eliminateDominated(n, value, weight)
    
    barang = list(zip(value, weight))
    barang_sort = sorted(barang, key=lambda x: x[0]/x[1], reverse=True)
    value, weight = zip(*barang_sort)

    max_solution = [0 for _ in range(n)]
    x = [0 for _ in range(n)]
    i = 0
    max_value = 0

    M = [[0 for _ in range(W+1)] for _ in range(n)]
    x[0] = W//weight[0]
    W_a = W - W//weight[0]*x[0]
    VN = value[0] * x[0]
    U = upperBound(W_a, VN, i, weight, value)

    max_solution = x.copy()

    m = []
    for i in range(n):
        min_weight = 100000
        for j in range(n):
            curr_w = weight[j]
            if j > i and curr_w < min_weight:
                min_weight = curr_w
        m.append(min_weight)
      
    return x, i, VN, W_a, U, m, M, max_value, max_solution, weight, value

def develop(x, i, VN, W_a, U, m, M, max_value, max_solution, weight, value):
    x, i, VN, W_a, max_value, max_solution = x, i, VN, W_a, max_value, max_solution
    weight, value, M = weight, value, M
    n = len(weight)

    while True:
        if W_a < m[i]:
            if max_value < VN:
                max_value = VN
                max_solution = x

                if max_value == U:
                    return x, i, VN, W_a, max_value, max_solution, M, 5
                
                return x, i, VN, W_a, max_value, max_solution, M, 3
        else:
            min_j = 100000
            for j in range(i+1, n):
                if min_j > j > i and weight[j] <= W_a:
                    min_j = j

            if VN + upperBound(W_a, VN, min_j, weight, value) <= max_value:
                return x, i, VN, W_a, max_value, max_solution, M, 3
            if M[i][W_a] >= VN:
                return x, i, VN, W_a, max_value, max_solution, M, 3

            x[min_j] = W_a//weight[min_j]
            VN = VN + value[min_j]*x[min_j]
            W_a = W_a - weight[min_j]*x[min_j]
            M[i][W_a] = VN
            i = min_j

def backtrack(x, i, VN, W_a, m, max_value, max_solution, weight, value):
    x, i, VN, W_a, max_value, max_solution = x, i, VN, W_a, max_value, max_solution
    weight, value = weight, value
    n = len(weight)

    while True: 
        max_j = 0
        for j in range(i+1, n):
            if max_j < j <= i and x[j] > 0:
                max_j = j 
        
        if max_j < 1:
            return x, i, VN, W_a, max_value, max_solution, 5
        
        i = max_j
        x[i] = x[i] - 1
        VN = VN - value[i]
        W_a = W_a + weight[i]

        if W_a < m[i]:
            continue
        
        if VN + math.floor(W_a*value[i+1]/weight[i+1]) <= max_value:
            VN -= value[i]*x[i]
            W_a = W_a + weight[i]*x[i]
            x[i] = 0
            continue

        if W_a - weight[i] >= m[i]:
            return x, i, VN, W_a, max_value, max_solution, 2

def replaceItem(x, i, VN, W_a, m, max_value, max_solution, weight, value): 
    x, i, VN, W_a, max_value, max_solution = x, i, VN, W_a, max_value, max_solution
    weight, value = weight, value
    n = len(weight)
    j = i
    h = j + 1

    while True:
        if max_value >= VN + math.floor(W_a*value[h]/weight[h]):
            return x, i, VN, W_a, max_value, max_solution, 3
        
        if weight[h] >= weight[j]:
            if weight[h] == weight[j] or weight[h] > W_a or max_value >= VN+value[h]:
                h += 1
                continue
            
            max_value = VN + value[h]
            max_solution = x
            x[h] = 1

            if max_value == upperBound(W_a, VN, h, weight, value):
                return x, i, VN, W_a, max_value, max_solution, 5
            j = h
            h = h + 1
            continue        
        else:
            if W_a - weight[h] < m[h-1]:
                h += 1
                continue
            i = h
            x[i] = W_a//weight[i]
            VN += value[i]*x[i]
            W_a -= weight[i]*x[i]
            return x, i, VN, W_a, max_value, max_solution, 2

def branchBoundKnapsack(W, n, value, weight):
    W, n, value, weight = W, n, value, weight
    x, i, VN, W_a, U, m, M, max_value, max_solution, weight, value = initialize(W, n, value, weight)
    step = 2
    while True: 
        if step == 2:
            x, i, VN, W_a, max_value, max_solution, M, step = develop(x, i, VN, W_a, U, m, M, max_value, max_solution, weight, value)
        if step == 3:
            x, i, VN, W_a, max_value, max_solution, step = backtrack(x, i, VN, W_a, m, max_value, max_solution, weight, value)
        if step == 4:
            x, i, VN, W_a, max_value, max_solution, step = replaceItem(x, i, VN, W_a, m, max_value, max_solution, weight, value)
        if step == 5:
            break
    return max_value, max_solution

def main():
    W = 137
    value = [72, 48, 9, 19, 56, 10, 14, 5, 64, 12]
    weight = [27, 89, 14, 54, 76, 24, 8, 23, 65, 9]
    n = len(value)

    max_value, max_solution = branchBoundKnapsack(W, n, value, weight)

    print(f"Value of items  : {value}")
    print(f"Weight of items : {weight}")
    print(f"Maximum Value   : {max_value}")
    print(f"Best Solution   : {max_solution}")

if __name__ == '__main__':
    main()