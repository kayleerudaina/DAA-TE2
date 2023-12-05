import random, time, tracemalloc
from dp_unbound_knapsack import dpUnboundedKnapsack
from branch_bound_unbound_knapsack import branchBoundKnapsack, eliminateDominated

# generate datasets according to size and types
def generate_dataset(n):
    W = 10*2*n
    value = [random.randint(1, 10*n) for _ in range(n)]
    weight = [random.randint(1, 10*n) for _ in range(n)]
    return W, value, weight

# calculate Running Time & Memory Usage for each algorithm
def count_time_memory(algorithm, W, n, value, weight):
    tracemalloc.start()
    start = time.time()
    if algorithm == 1:
        max_value = dpUnboundedKnapsack(W, n, value, weight)
        max_solution = []   # not implemented in this algorithm
    elif algorithm == 2:
        max_value, max_solution = branchBoundKnapsack(W, n, value, weight)
    
    end = time.time()
    running_time = (end-start)*1000
    
    memory_usage = tracemalloc.get_traced_memory()[1]
    tracemalloc.reset_peak()
    tracemalloc.stop()

    return running_time, memory_usage, max_value, max_solution

def main():
    sizes = [100, 1000, 10000]
    for i in range(3):
        print(f"Time complexity and results for size {sizes[i]}")
        W, value, weight = generate_dataset(sizes[i])
        n = sizes[i]

        print("- Unbounded Knapsack with Dynamic Programming -")
        print(f"Weight Capacity (W) : {W}")
        running_time, memory_usage, max_value, max_solution = count_time_memory(1, W, n, value, weight)

        print(f"Maximum Value       : {max_value}")
        print(f"Running Time        : {running_time}")
        print(f"Memory Usage        : {memory_usage}")

        print("- Unbounded Knapsack with  Branch  and  Bound -")
        print(f"Weight Capacity (W) : {W}")
        running_time, memory_usage, max_value, max_solution = count_time_memory(2, W, n, value, weight)

        print(f"Maximum Value       : {max_value}")
        print(f"Maximum Solution    : {max_solution}")
        print(f"Running Time        : {running_time}")
        print(f"Memory Usage        : {memory_usage}")
        print("===============================================")
    print("Program Done")

if __name__ == '__main__':
    main()
