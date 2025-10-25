"""
Problem 8: Missing Number
Difficulty: Easy

Given an array nums containing n distinct numbers in the range [0, n], return the only 
number in the range that is missing from the array.

Time Complexity: O(n)
Space Complexity: O(1)
"""

def missing_number(nums):
    """
    Find missing number using mathematical formula.
    
    Args:
        nums: List of numbers from 0 to n with one missing
        
    Returns:
        int: The missing number
    """
    n = len(nums)
    # Sum of numbers from 0 to n is n*(n+1)/2
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return expected_sum - actual_sum


def missing_number_xor(nums):
    """
    Find missing number using XOR properties.
    
    Args:
        nums: List of numbers from 0 to n with one missing
        
    Returns:
        int: The missing number
    """
    n = len(nums)
    # XOR all numbers from 0 to n
    xor_all = 0
    for i in range(n + 1):
        xor_all ^= i
    
    # XOR all numbers in the array
    xor_nums = 0
    for num in nums:
        xor_nums ^= num
    
    # The missing number is the XOR of the two results
    return xor_all ^ xor_nums


def missing_number_set(nums):
    """
    Find missing number using set (hash set approach).
    
    Args:
        nums: List of numbers from 0 to n with one missing
        
    Returns:
        int: The missing number
    """
    num_set = set(nums)
    n = len(nums)
    
    for i in range(n + 1):
        if i not in num_set:
            return i
    
    return -1  # Should never reach here


def missing_number_sorting(nums):
    """
    Find missing number using sorting.
    
    Args:
        nums: List of numbers from 0 to n with one missing
        
    Returns:
        int: The missing number
    """
    nums.sort()
    
    # Check if 0 is missing
    if nums[0] != 0:
        return 0
    
    # Check for missing number in the middle
    for i in range(1, len(nums)):
        if nums[i] != nums[i-1] + 1:
            return nums[i-1] + 1
    
    # If no missing number found, it must be the last number
    return len(nums)


def missing_number_binary_search(nums):
    """
    Find missing number using binary search on sorted array.
    
    Args:
        nums: List of numbers from 0 to n with one missing
        
    Returns:
        int: The missing number
    """
    nums.sort()
    left, right = 0, len(nums)
    
    while left < right:
        mid = (left + right) // 2
        if nums[mid] == mid:
            left = mid + 1
        else:
            right = mid
    
    return left


def find_all_missing_numbers(nums):
    """
    Find all missing numbers in a range (bonus problem).
    
    Args:
        nums: List of numbers (may have duplicates and multiple missing)
        
    Returns:
        list: List of all missing numbers
    """
    if not nums:
        return []
    
    # Find the range
    min_num = min(nums)
    max_num = max(nums)
    
    # Create a set for O(1) lookup
    num_set = set(nums)
    
    # Find all missing numbers in the range
    missing = []
    for i in range(min_num, max_num + 1):
        if i not in num_set:
            missing.append(i)
    
    return missing


def find_duplicate_and_missing(nums):
    """
    Find both duplicate and missing numbers (bonus problem).
    
    Args:
        nums: List of numbers with one duplicate and one missing
        
    Returns:
        tuple: (duplicate, missing)
    """
    n = len(nums)
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    
    # Sum of squares
    expected_sum_squares = sum(i * i for i in range(n + 1))
    actual_sum_squares = sum(num * num for num in nums)
    
    # Let x be the duplicate and y be the missing
    # x - y = actual_sum - expected_sum
    # x^2 - y^2 = actual_sum_squares - expected_sum_squares
    # (x - y)(x + y) = actual_sum_squares - expected_sum_squares
    # x + y = (actual_sum_squares - expected_sum_squares) / (x - y)
    
    diff = actual_sum - expected_sum
    diff_squares = actual_sum_squares - expected_sum_squares
    
    x_plus_y = diff_squares // diff
    x = (diff + x_plus_y) // 2
    y = x_plus_y - x
    
    return x, y


# Test cases
if __name__ == "__main__":
    test_cases = [
        [3, 0, 1],                    # Expected: 2
        [0, 1],                       # Expected: 2
        [9, 6, 4, 2, 3, 5, 7, 0, 1], # Expected: 8
        [1],                          # Expected: 0
        [0],                          # Expected: 1
        [0, 1, 2, 3, 4, 5, 6, 7, 9], # Expected: 8
        [1, 2, 3, 4, 5, 6, 7, 8, 9], # Expected: 0
    ]
    
    for i, nums in enumerate(test_cases, 1):
        print(f"Test case {i}: {nums}")
        
        # Test different approaches
        result_math = missing_number(nums)
        result_xor = missing_number_xor(nums)
        result_set = missing_number_set(nums)
        result_sort = missing_number_sorting(nums)
        result_binary = missing_number_binary_search(nums)
        
        print(f"Mathematical formula: {result_math}")
        print(f"XOR approach: {result_xor}")
        print(f"Set approach: {result_set}")
        print(f"Sorting approach: {result_sort}")
        print(f"Binary search: {result_binary}")
        
        # Verify the result
        n = len(nums)
        expected_range = set(range(n + 1))
        actual_set = set(nums)
        missing_verification = expected_range - actual_set
        print(f"Verification: {missing_verification}")
        
        print("-" * 50)
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large test case
    n = 10000
    large_nums = list(range(n + 1))
    # Remove one random number
    missing_num = random.randint(0, n)
    large_nums.remove(missing_num)
    random.shuffle(large_nums)
    
    # Test mathematical approach
    start_time = time.time()
    for _ in range(1000):
        missing_number(large_nums)
    math_time = time.time() - start_time
    
    # Test XOR approach
    start_time = time.time()
    for _ in range(1000):
        missing_number_xor(large_nums)
    xor_time = time.time() - start_time
    
    # Test set approach
    start_time = time.time()
    for _ in range(1000):
        missing_number_set(large_nums)
    set_time = time.time() - start_time
    
    print(f"Mathematical formula: {math_time:.6f} seconds")
    print(f"XOR approach: {xor_time:.6f} seconds")
    print(f"Set approach: {set_time:.6f} seconds")
    
    # Bonus problems
    print(f"\nBonus problems:")
    
    # Find all missing numbers
    nums_with_gaps = [1, 3, 5, 7, 9]
    all_missing = find_all_missing_numbers(nums_with_gaps)
    print(f"Numbers: {nums_with_gaps}")
    print(f"All missing: {all_missing}")
    
    # Find duplicate and missing
    nums_with_duplicate = [1, 2, 2, 4, 5]  # duplicate: 2, missing: 3
    duplicate, missing = find_duplicate_and_missing(nums_with_duplicate)
    print(f"Numbers: {nums_with_duplicate}")
    print(f"Duplicate: {duplicate}, Missing: {missing}")
    
    # Edge cases
    print(f"\nEdge cases:")
    edge_cases = [
        [],           # Empty array
        [0],          # Single element, missing 1
        [1],          # Single element, missing 0
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # No missing (should return 10)
    ]
    
    for case in edge_cases:
        if case:
            result = missing_number(case)
            print(f"Numbers: {case} -> Missing: {result}")
        else:
            print(f"Empty array -> Missing: 0")
