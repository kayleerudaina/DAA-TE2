# code from GeeksForGeeks
from branch_bound_unbound_knapsack import eliminateDominated

def dpUnboundedKnapsack(W, n, value, weight):
    """
    Implements Unbounded Knapsack problem with
    Dynamic Programming.
    """
    dp = [0 for _ in range(W + 1)] 

    # Fill dp[] using above recursive formula 
    for i in range(W + 1): 
        for j in range(n): 
            if (weight[j] <= i): 
                dp[i] = max(dp[i], dp[i - weight[j]] + value[j]) 

    max_value = dp[W]
    return max_value

def main():
    W = 137
    value = [72, 48, 9, 19, 56, 10, 14, 5, 64, 12]
    weight = [27, 89, 14, 54, 76, 24, 8, 23, 65, 9]
    n = len(value)

    max_value = dpUnboundedKnapsack(W, n, value, weight)

    print(f"Value of items  : {value}")
    print(f"Weight of items : {weight}")
    print(f"Maximum Value   : {max_value}")

if __name__ == '__main__':
    main()