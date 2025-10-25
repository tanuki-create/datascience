"""
Problem 6: House Robber
Difficulty: Easy

You are a professional robber planning to rob houses along a street. Each house has a 
certain amount of money stashed, the only constraint stopping you from robbing each of 
them is that adjacent houses have security systems connected and it will automatically 
contact the police if two adjacent houses were broken into on the same night.

Time Complexity: O(n)
Space Complexity: O(1)
"""

def rob(nums):
    """
    Find maximum amount of money that can be robbed without alerting police.
    
    Args:
        nums: List of money in each house
        
    Returns:
        int: Maximum amount that can be robbed
    """
    if not nums:
        return 0
    
    if len(nums) == 1:
        return nums[0]
    
    # Use two variables to track previous two maximums
    prev2 = nums[0]  # Maximum money robbed up to house 0
    prev1 = max(nums[0], nums[1])  # Maximum money robbed up to house 1
    
    for i in range(2, len(nums)):
        # Either rob current house + max from 2 houses ago,
        # or don't rob current house and take max from previous house
        current = max(prev1, prev2 + nums[i])
        prev2 = prev1
        prev1 = current
    
    return prev1


def rob_recursive(nums):
    """
    Recursive approach with memoization - O(n) time complexity.
    
    Args:
        nums: List of money in each house
        
    Returns:
        int: Maximum amount that can be robbed
    """
    def rob_from(index, memo):
        if index >= len(nums):
            return 0
        
        if index in memo:
            return memo[index]
        
        # Either rob current house and skip next, or skip current house
        rob_current = nums[index] + rob_from(index + 2, memo)
        skip_current = rob_from(index + 1, memo)
        
        memo[index] = max(rob_current, skip_current)
        return memo[index]
    
    if not nums:
        return 0
    
    memo = {}
    return rob_from(0, memo)


def rob_dp_array(nums):
    """
    Dynamic programming with array - O(n) time and space complexity.
    
    Args:
        nums: List of money in each house
        
    Returns:
        int: Maximum amount that can be robbed
    """
    if not nums:
        return 0
    
    if len(nums) == 1:
        return nums[0]
    
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    
    for i in range(2, len(nums)):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    
    return dp[-1]


def rob_with_path(nums):
    """
    Find maximum amount and return the houses that should be robbed.
    
    Args:
        nums: List of money in each house
        
    Returns:
        tuple: (max_amount, list_of_house_indices)
    """
    if not nums:
        return 0, []
    
    if len(nums) == 1:
        return nums[0], [0]
    
    # Track both the maximum amount and the path
    dp = [(0, []) for _ in range(len(nums))]
    dp[0] = (nums[0], [0])
    dp[1] = (max(nums[0], nums[1]), [1] if nums[1] > nums[0] else [0])
    
    for i in range(2, len(nums)):
        # Option 1: Rob current house + max from 2 houses ago
        option1_amount = dp[i-2][0] + nums[i]
        option1_path = dp[i-2][1] + [i]
        
        # Option 2: Don't rob current house, take max from previous house
        option2_amount = dp[i-1][0]
        option2_path = dp[i-1][1]
        
        if option1_amount > option2_amount:
            dp[i] = (option1_amount, option1_path)
        else:
            dp[i] = (option2_amount, option2_path)
    
    return dp[-1]


def rob_circular(nums):
    """
    House Robber II - Circular street (first and last houses are adjacent).
    
    Args:
        nums: List of money in each house
        
    Returns:
        int: Maximum amount that can be robbed
    """
    if not nums:
        return 0
    
    if len(nums) == 1:
        return nums[0]
    
    if len(nums) == 2:
        return max(nums[0], nums[1])
    
    # Case 1: Rob first house, skip last house
    def rob_linear(houses):
        if not houses:
            return 0
        if len(houses) == 1:
            return houses[0]
        
        prev2 = houses[0]
        prev1 = max(houses[0], houses[1])
        
        for i in range(2, len(houses)):
            current = max(prev1, prev2 + houses[i])
            prev2 = prev1
            prev1 = current
        
        return prev1
    
    # Case 1: Rob houses 0 to n-2 (skip last house)
    case1 = rob_linear(nums[:-1])
    
    # Case 2: Rob houses 1 to n-1 (skip first house)
    case2 = rob_linear(nums[1:])
    
    return max(case1, case2)


# Test cases
if __name__ == "__main__":
    test_cases = [
        [1, 2, 3, 1],        # Expected: 4
        [2, 7, 9, 3, 1],     # Expected: 12
        [2, 1, 1, 2],        # Expected: 4
        [1, 2],              # Expected: 2
        [2, 1],              # Expected: 2
        [1],                 # Expected: 1
        [1, 3, 1],          # Expected: 3
        [5, 1, 2, 10],       # Expected: 15
    ]
    
    for i, nums in enumerate(test_cases, 1):
        print(f"Test case {i}: {nums}")
        
        # Test different approaches
        result_dp = rob(nums)
        result_recursive = rob_recursive(nums)
        result_array = rob_dp_array(nums)
        
        print(f"DP approach: {result_dp}")
        print(f"Recursive: {result_recursive}")
        print(f"Array DP: {result_array}")
        
        # Show which houses to rob
        max_amount, houses_to_rob = rob_with_path(nums)
        print(f"Max amount: {max_amount}")
        print(f"Houses to rob: {houses_to_rob}")
        print(f"Verification: {sum(nums[i] for i in houses_to_rob)}")
        
        # Test circular version
        if len(nums) > 2:
            circular_result = rob_circular(nums)
            print(f"Circular version: {circular_result}")
        
        print("-" * 50)
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large test case
    large_nums = [random.randint(1, 100) for _ in range(1000)]
    
    # Test DP approach
    start_time = time.time()
    for _ in range(1000):
        rob(large_nums)
    dp_time = time.time() - start_time
    
    # Test recursive approach
    start_time = time.time()
    for _ in range(100):
        rob_recursive(large_nums)
    recursive_time = time.time() - start_time
    
    print(f"DP approach: {dp_time:.6f} seconds")
    print(f"Recursive approach: {recursive_time:.6f} seconds")
    print(f"DP is {recursive_time/dp_time:.2f}x faster")
    
    # Edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],           # Empty array
        [5],          # Single house
        [1, 2],       # Two houses
        [1, 1, 1, 1], # All same values
        [100, 1, 1, 100], # High values at ends
    ]
    
    for case in edge_cases:
        result = rob(case)
        print(f"Houses: {case} -> Max amount: {result}")
