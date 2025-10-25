"""
Problem 3: Maximum Subarray (Kadane's Algorithm)
Difficulty: Easy

Given an integer array nums, find the contiguous subarray (containing at least one number) 
which has the largest sum and return its sum.

Time Complexity: O(n)
Space Complexity: O(1)
"""

def max_subarray(nums):
    """
    Find maximum sum of contiguous subarray using Kadane's algorithm.
    
    Args:
        nums: List of integers
        
    Returns:
        int: Maximum sum of contiguous subarray
    """
    if not nums:
        return 0
    
    # Initialize with first element
    max_sum = current_sum = nums[0]
    
    # Start from second element
    for i in range(1, len(nums)):
        # Either extend previous subarray or start new one
        current_sum = max(nums[i], current_sum + nums[i])
        # Update maximum sum found so far
        max_sum = max(max_sum, current_sum)
    
    return max_sum


def max_subarray_brute_force(nums):
    """
    Brute force approach - O(n²) time complexity.
    
    Args:
        nums: List of integers
        
    Returns:
        int: Maximum sum of contiguous subarray
    """
    if not nums:
        return 0
    
    max_sum = float('-inf')
    n = len(nums)
    
    # Try all possible subarrays
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += nums[j]
            max_sum = max(max_sum, current_sum)
    
    return max_sum


def max_subarray_divide_conquer(nums):
    """
    Divide and conquer approach - O(n log n) time complexity.
    
    Args:
        nums: List of integers
        
    Returns:
        int: Maximum sum of contiguous subarray
    """
    def max_subarray_rec(left, right):
        if left == right:
            return nums[left]
        
        mid = (left + right) // 2
        
        # Maximum subarray in left half
        left_max = max_subarray_rec(left, mid)
        
        # Maximum subarray in right half
        right_max = max_subarray_rec(mid + 1, right)
        
        # Maximum subarray crossing the middle
        # Find maximum sum ending at mid
        left_sum = float('-inf')
        current_sum = 0
        for i in range(mid, left - 1, -1):
            current_sum += nums[i]
            left_sum = max(left_sum, current_sum)
        
        # Find maximum sum starting at mid + 1
        right_sum = float('-inf')
        current_sum = 0
        for i in range(mid + 1, right + 1):
            current_sum += nums[i]
            right_sum = max(right_sum, current_sum)
        
        cross_sum = left_sum + right_sum
        
        return max(left_max, right_max, cross_sum)
    
    if not nums:
        return 0
    
    return max_subarray_rec(0, len(nums) - 1)


def max_subarray_with_indices(nums):
    """
    Find maximum subarray and return both sum and indices.
    
    Args:
        nums: List of integers
        
    Returns:
        tuple: (max_sum, start_index, end_index)
    """
    if not nums:
        return 0, 0, 0
    
    max_sum = current_sum = nums[0]
    start = end = 0
    temp_start = 0
    
    for i in range(1, len(nums)):
        if current_sum < 0:
            current_sum = nums[i]
            temp_start = i
        else:
            current_sum += nums[i]
        
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i
    
    return max_sum, start, end


# Test cases
if __name__ == "__main__":
    test_cases = [
        [-2, 1, -3, 4, -1, 2, 1, -5, 4],  # Expected: 6
        [1],                               # Expected: 1
        [5, 4, -1, 7, 8],                 # Expected: 23
        [-1],                             # Expected: -1
        [-2, -1, -3],                     # Expected: -1
        [1, 2, 3, 4, 5],                  # Expected: 15
        [-5, -4, -3, -2, -1],            # Expected: -1
    ]
    
    for i, nums in enumerate(test_cases, 1):
        print(f"Test case {i}: {nums}")
        
        # Test Kadane's algorithm
        result_kadane = max_subarray(nums)
        print(f"Kadane's algorithm: {result_kadane}")
        
        # Test brute force
        result_brute = max_subarray_brute_force(nums)
        print(f"Brute force: {result_brute}")
        
        # Test divide and conquer
        result_dc = max_subarray_divide_conquer(nums)
        print(f"Divide and conquer: {result_dc}")
        
        # Test with indices
        max_sum, start, end = max_subarray_with_indices(nums)
        print(f"Max sum: {max_sum}, subarray: {nums[start:end+1]}")
        print("-" * 50)
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large test case
    large_nums = [random.randint(-1000, 1000) for _ in range(1000)]
    
    # Test Kadane's algorithm
    start_time = time.time()
    for _ in range(100):
        max_subarray(large_nums)
    kadane_time = time.time() - start_time
    
    # Test divide and conquer
    start_time = time.time()
    for _ in range(100):
        max_subarray_divide_conquer(large_nums)
    dc_time = time.time() - start_time
    
    print(f"Kadane's algorithm: {kadane_time:.6f} seconds")
    print(f"Divide and conquer: {dc_time:.6f} seconds")
    print(f"Kadane's is {dc_time/kadane_time:.2f}x faster")
