"""
Problem 5: Climbing Stairs
Difficulty: Easy

You are climbing a staircase. It takes n steps to reach the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways 
can you climb to the top?

This is essentially the Fibonacci sequence problem.

Time Complexity: O(n)
Space Complexity: O(1)
"""

def climb_stairs(n):
    """
    Find number of ways to climb n stairs using dynamic programming.
    
    Args:
        n: Number of steps
        
    Returns:
        int: Number of distinct ways to climb
    """
    if n <= 2:
        return n
    
    # Use only two variables to track previous two values
    prev2 = 1  # ways to reach step 1
    prev1 = 2  # ways to reach step 2
    
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1


def climb_stairs_recursive(n):
    """
    Recursive approach - O(2^n) time complexity (inefficient).
    
    Args:
        n: Number of steps
        
    Returns:
        int: Number of distinct ways to climb
    """
    if n <= 2:
        return n
    
    return climb_stairs_recursive(n - 1) + climb_stairs_recursive(n - 2)


def climb_stairs_memo(n, memo=None):
    """
    Recursive approach with memoization - O(n) time complexity.
    
    Args:
        n: Number of steps
        memo: Dictionary to store computed results
        
    Returns:
        int: Number of distinct ways to climb
    """
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 2:
        return n
    
    memo[n] = climb_stairs_memo(n - 1, memo) + climb_stairs_memo(n - 2, memo)
    return memo[n]


def climb_stairs_dp_array(n):
    """
    Dynamic programming with array - O(n) time and space complexity.
    
    Args:
        n: Number of steps
        
    Returns:
        int: Number of distinct ways to climb
    """
    if n <= 2:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]


def climb_stairs_matrix(n):
    """
    Matrix exponentiation approach - O(log n) time complexity.
    This is the most efficient approach for very large n.
    
    Args:
        n: Number of steps
        
    Returns:
        int: Number of distinct ways to climb
    """
    if n <= 2:
        return n
    
    def matrix_multiply(A, B):
        """Multiply two 2x2 matrices."""
        return [
            [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]
        ]
    
    def matrix_power(matrix, power):
        """Raise matrix to the given power."""
        if power == 1:
            return matrix
        
        if power % 2 == 0:
            half_power = matrix_power(matrix, power // 2)
            return matrix_multiply(half_power, half_power)
        else:
            return matrix_multiply(matrix, matrix_power(matrix, power - 1))
    
    # Transformation matrix: [[1, 1], [1, 0]]
    transform = [[1, 1], [1, 0]]
    result_matrix = matrix_power(transform, n - 1)
    
    # The result is in the top-left corner
    return result_matrix[0][0]


def print_climbing_ways(n):
    """
    Print all possible ways to climb n stairs.
    
    Args:
        n: Number of steps
    """
    def generate_ways(current_way, remaining_steps):
        if remaining_steps == 0:
            print(" + ".join(map(str, current_way)))
            return
        
        if remaining_steps >= 1:
            generate_ways(current_way + [1], remaining_steps - 1)
        
        if remaining_steps >= 2:
            generate_ways(current_way + [2], remaining_steps - 2)
    
    print(f"All ways to climb {n} stairs:")
    generate_ways([], n)


# Test cases
if __name__ == "__main__":
    test_cases = [1, 2, 3, 4, 5, 6, 10, 20]
    
    for n in test_cases:
        print(f"\nFor n = {n}:")
        
        # Test different approaches
        result_dp = climb_stairs(n)
        result_memo = climb_stairs_memo(n)
        result_array = climb_stairs_dp_array(n)
        result_matrix = climb_stairs_matrix(n)
        
        print(f"DP approach: {result_dp}")
        print(f"Memoization: {result_memo}")
        print(f"Array DP: {result_array}")
        print(f"Matrix: {result_matrix}")
        
        # Show all ways for small n
        if n <= 5:
            print_climbing_ways(n)
    
    # Performance comparison
    print("\n" + "="*60)
    print("Performance comparison:")
    import time
    
    large_n = 40
    
    # Test DP approach
    start_time = time.time()
    for _ in range(1000):
        climb_stairs(large_n)
    dp_time = time.time() - start_time
    
    # Test memoization
    start_time = time.time()
    for _ in range(1000):
        climb_stairs_memo(large_n)
    memo_time = time.time() - start_time
    
    # Test matrix approach
    start_time = time.time()
    for _ in range(1000):
        climb_stairs_matrix(large_n)
    matrix_time = time.time() - start_time
    
    print(f"DP approach: {dp_time:.6f} seconds")
    print(f"Memoization: {memo_time:.6f} seconds")
    print(f"Matrix approach: {matrix_time:.6f} seconds")
    
    # Test recursive approach (only for small n)
    print(f"\nRecursive approach for n=10:")
    start_time = time.time()
    result_recursive = climb_stairs_recursive(10)
    recursive_time = time.time() - start_time
    print(f"Result: {result_recursive}, Time: {recursive_time:.6f} seconds")
    
    # Fibonacci sequence verification
    print(f"\nFibonacci sequence verification:")
    print("n: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10")
    print("F: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55")
    print("Ways to climb stairs:")
    for i in range(1, 11):
        print(f"n={i}: {climb_stairs(i)}")
