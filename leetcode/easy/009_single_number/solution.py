"""
Problem 9: Single Number
Difficulty: Easy

Given a non-empty array of integers nums, every element appears twice except for one. 
Find that single one.

Time Complexity: O(n)
Space Complexity: O(1)
"""

def single_number(nums):
    """
    Find the single number using XOR properties.
    
    Args:
        nums: List of integers where all appear twice except one
        
    Returns:
        int: The single number
    """
    result = 0
    for num in nums:
        result ^= num
    return result


def single_number_hash_map(nums):
    """
    Find the single number using hash map (not optimal space).
    
    Args:
        nums: List of integers where all appear twice except one
        
    Returns:
        int: The single number
    """
    from collections import Counter
    count = Counter(nums)
    
    for num, freq in count.items():
        if freq == 1:
            return num
    
    return -1  # Should never reach here


def single_number_math(nums):
    """
    Find the single number using mathematical approach.
    
    Args:
        nums: List of integers where all appear twice except one
        
    Returns:
        int: The single number
    """
    # Sum of all unique elements * 2 - sum of all elements
    unique_sum = sum(set(nums))
    total_sum = sum(nums)
    return 2 * unique_sum - total_sum


def single_number_sorting(nums):
    """
    Find the single number using sorting.
    
    Args:
        nums: List of integers where all appear twice except one
        
    Returns:
        int: The single number
    """
    nums.sort()
    n = len(nums)
    
    # Check first element
    if n == 1 or nums[0] != nums[1]:
        return nums[0]
    
    # Check middle elements
    for i in range(1, n - 1):
        if nums[i] != nums[i - 1] and nums[i] != nums[i + 1]:
            return nums[i]
    
    # Check last element
    return nums[-1]


def single_number_ii(nums):
    """
    Single Number II - every element appears three times except one.
    
    Args:
        nums: List of integers where all appear three times except one
        
    Returns:
        int: The single number
    """
    ones = twos = 0
    
    for num in nums:
        # Update twos: if we had a 1 in ones and get another 1, we have 2
        twos |= (ones & num)
        
        # Update ones: XOR with num, but clear if we have 2
        ones ^= num
        
        # Clear both ones and twos if we have 3 (both are 1)
        threes = ones & twos
        ones &= ~threes
        twos &= ~threes
    
    return ones


def single_number_iii(nums):
    """
    Single Number III - two elements appear once, others appear twice.
    
    Args:
        nums: List of integers where two appear once, others twice
        
    Returns:
        list: The two single numbers
    """
    # XOR all numbers to get x ^ y
    xor_all = 0
    for num in nums:
        xor_all ^= num
    
    # Find the rightmost set bit
    rightmost_bit = xor_all & -xor_all
    
    # Separate numbers into two groups based on this bit
    x, y = 0, 0
    for num in nums:
        if num & rightmost_bit:
            x ^= num
        else:
            y ^= num
    
    return [x, y]


def find_single_numbers_general(nums, k):
    """
    General solution for k occurrences (bonus problem).
    
    Args:
        nums: List of integers
        k: Number of times each number appears (except one)
        
    Returns:
        int: The single number
    """
    result = 0
    
    # For each bit position
    for i in range(32):
        bit_count = 0
        
        # Count how many numbers have this bit set
        for num in nums:
            if num & (1 << i):
                bit_count += 1
        
        # If bit_count is not divisible by k, the single number has this bit set
        if bit_count % k != 0:
            result |= (1 << i)
    
    return result


def find_missing_number_xor(nums, n):
    """
    Find missing number in array of 1 to n using XOR.
    
    Args:
        nums: Array of numbers from 1 to n with one missing
        n: The maximum number
        
    Returns:
        int: The missing number
    """
    # XOR all numbers from 1 to n
    xor_all = 0
    for i in range(1, n + 1):
        xor_all ^= i
    
    # XOR all numbers in the array
    xor_nums = 0
    for num in nums:
        xor_nums ^= num
    
    return xor_all ^ xor_nums


# Test cases
if __name__ == "__main__":
    test_cases = [
        [2, 2, 1],           # Expected: 1
        [4, 1, 2, 1, 2],     # Expected: 4
        [1],                 # Expected: 1
        [1, 1, 2, 2, 3],     # Expected: 3
        [5, 3, 5, 3, 1],     # Expected: 1
        [7, 3, 5, 4, 5, 3, 4], # Expected: 7
    ]
    
    for i, nums in enumerate(test_cases, 1):
        print(f"Test case {i}: {nums}")
        
        # Test different approaches
        result_xor = single_number(nums)
        result_hash = single_number_hash_map(nums)
        result_math = single_number_math(nums)
        result_sort = single_number_sorting(nums)
        
        print(f"XOR approach: {result_xor}")
        print(f"Hash map: {result_hash}")
        print(f"Mathematical: {result_math}")
        print(f"Sorting: {result_sort}")
        
        print("-" * 50)
    
    # Test Single Number II
    print("\nSingle Number II (three occurrences):")
    nums_ii = [2, 2, 3, 2]  # Expected: 3
    result_ii = single_number_ii(nums_ii)
    print(f"Numbers: {nums_ii}")
    print(f"Single number: {result_ii}")
    
    # Test Single Number III
    print("\nSingle Number III (two single numbers):")
    nums_iii = [1, 2, 1, 3, 2, 5]  # Expected: [3, 5]
    result_iii = single_number_iii(nums_iii)
    print(f"Numbers: {nums_iii}")
    print(f"Single numbers: {result_iii}")
    
    # Test general solution
    print("\nGeneral solution (k occurrences):")
    nums_general = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4]  # k=3, single=4
    result_general = find_single_numbers_general(nums_general, 3)
    print(f"Numbers: {nums_general}")
    print(f"Single number: {result_general}")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large test case
    large_nums = []
    for i in range(1000):
        large_nums.extend([i, i])  # Each number appears twice
    large_nums.append(9999)  # Single number
    random.shuffle(large_nums)
    
    # Test XOR approach
    start_time = time.time()
    for _ in range(1000):
        single_number(large_nums)
    xor_time = time.time() - start_time
    
    # Test hash map approach
    start_time = time.time()
    for _ in range(1000):
        single_number_hash_map(large_nums)
    hash_time = time.time() - start_time
    
    # Test mathematical approach
    start_time = time.time()
    for _ in range(1000):
        single_number_math(large_nums)
    math_time = time.time() - start_time
    
    print(f"XOR approach: {xor_time:.6f} seconds")
    print(f"Hash map: {hash_time:.6f} seconds")
    print(f"Mathematical: {math_time:.6f} seconds")
    
    # Edge cases
    print("\nEdge cases:")
    edge_cases = [
        [1],                    # Single element
        [1, 1, 2],             # Single element at end
        [1, 2, 2],             # Single element at beginning
        [1, 1, 2, 2, 3, 3, 4], # Single element at end
    ]
    
    for case in edge_cases:
        result = single_number(case)
        print(f"Numbers: {case} -> Single: {result}")
    
    # XOR properties demonstration
    print("\nXOR properties demonstration:")
    print("XOR properties:")
    print("1. a ^ a = 0")
    print("2. a ^ 0 = a")
    print("3. a ^ b ^ a = b")
    print("4. XOR is commutative and associative")
    
    # Demonstrate with numbers
    a, b = 5, 3
    print(f"\nExample: a = {a}, b = {b}")
    print(f"a ^ a = {a} ^ {a} = {a ^ a}")
    print(f"a ^ 0 = {a} ^ 0 = {a ^ 0}")
    print(f"a ^ b ^ a = {a} ^ {b} ^ {a} = {a ^ b ^ a}")
    print(f"b = {b} (should be equal)")
