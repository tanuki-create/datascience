"""
Problem 1: Two Sum
Difficulty: Easy

Given an array of integers nums and an integer target, return indices of the two numbers 
such that they add up to target.

Time Complexity: O(n)
Space Complexity: O(n)
"""

def two_sum(nums, target):
    """
    Find two numbers in the array that add up to target.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        List of two indices that sum to target
    """
    # Hash map to store number and its index
    num_to_index = {}
    
    for i, num in enumerate(nums):
        # Calculate the complement (what we need to reach target)
        complement = target - num
        
        # If complement exists in our hash map, we found the pair
        if complement in num_to_index:
            return [num_to_index[complement], i]
        
        # Store current number and its index
        num_to_index[num] = i
    
    # This should never be reached given the problem constraints
    return []


def two_sum_brute_force(nums, target):
    """
    Brute force approach - O(n²) time complexity
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        List of two indices that sum to target
    """
    n = len(nums)
    
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    
    return []


# Test cases
if __name__ == "__main__":
    # Test case 1
    nums1 = [2, 7, 11, 15]
    target1 = 9
    result1 = two_sum(nums1, target1)
    print(f"Test 1: nums={nums1}, target={target1}")
    print(f"Result: {result1}")
    print(f"Verification: {nums1[result1[0]]} + {nums1[result1[1]]} = {nums1[result1[0]] + nums1[result1[1]]}")
    print()
    
    # Test case 2
    nums2 = [3, 2, 4]
    target2 = 6
    result2 = two_sum(nums2, target2)
    print(f"Test 2: nums={nums2}, target={target2}")
    print(f"Result: {result2}")
    print(f"Verification: {nums2[result2[0]]} + {nums2[result2[1]]} = {nums2[result2[0]] + nums2[result2[1]]}")
    print()
    
    # Test case 3
    nums3 = [3, 3]
    target3 = 6
    result3 = two_sum(nums3, target3)
    print(f"Test 3: nums={nums3}, target={target3}")
    print(f"Result: {result3}")
    print(f"Verification: {nums3[result3[0]]} + {nums3[result3[1]]} = {nums3[result3[0]] + nums3[result3[1]]}")
    print()
    
    # Performance comparison
    import time
    
    # Large test case for performance comparison
    large_nums = list(range(1000))
    large_target = 1998  # 999 + 999
    
    # Hash map approach
    start_time = time.time()
    result_hash = two_sum(large_nums, large_target)
    hash_time = time.time() - start_time
    
    # Brute force approach
    start_time = time.time()
    result_brute = two_sum_brute_force(large_nums, large_target)
    brute_time = time.time() - start_time
    
    print(f"Performance comparison on large input (1000 elements):")
    print(f"Hash map approach: {hash_time:.6f} seconds")
    print(f"Brute force approach: {brute_time:.6f} seconds")
    print(f"Speed improvement: {brute_time/hash_time:.2f}x faster")
