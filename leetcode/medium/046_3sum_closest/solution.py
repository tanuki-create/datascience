"""
Problem 46: 3Sum Closest
Difficulty: Medium

Given an integer array nums of length n and an integer target, find three 
integers in nums such that the sum is closest to target. Return the sum of 
the three integers.

You may assume that each input would have exactly one solution.

Time Complexity: O(n²) where n is the length of the array
Space Complexity: O(1) excluding the output
"""

def three_sum_closest(nums, target):
    """
    Find three integers whose sum is closest to target using two-pointer technique.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        int: Sum of three integers closest to target
    """
    nums.sort()
    closest_sum = float('inf')
    
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            # Update closest sum if current is closer to target
            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum
            
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                return current_sum  # Exact match found
    
    return closest_sum


def three_sum_closest_optimized(nums, target):
    """
    Find three integers whose sum is closest to target using optimized approach.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        int: Sum of three integers closest to target
    """
    nums.sort()
    closest_sum = float('inf')
    
    for i in range(len(nums) - 2):
        # Skip duplicates for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            # Update closest sum if current is closer to target
            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum
            
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                return current_sum  # Exact match found
    
    return closest_sum


def three_sum_closest_with_brute_force(nums, target):
    """
    Find three integers whose sum is closest to target using brute force approach.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        int: Sum of three integers closest to target
    """
    closest_sum = float('inf')
    
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            for k in range(j + 1, len(nums)):
                current_sum = nums[i] + nums[j] + nums[k]
                
                if abs(current_sum - target) < abs(closest_sum - target):
                    closest_sum = current_sum
    
    return closest_sum


def three_sum_closest_verbose(nums, target):
    """
    Find three integers whose sum is closest to target with detailed step-by-step explanation.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        int: Sum of three integers closest to target
    """
    print(f"Finding three integers whose sum is closest to {target} in {nums}")
    print(f"Array length: {len(nums)}")
    
    nums.sort()
    print(f"Sorted array: {nums}")
    
    closest_sum = float('inf')
    print(f"Initial closest sum: {closest_sum}")
    
    for i in range(len(nums) - 2):
        print(f"\nStep {i + 1}: Checking first element nums[{i}] = {nums[i]}")
        
        left, right = i + 1, len(nums) - 1
        print(f"  Two pointers: left = {left}, right = {right}")
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            print(f"    Checking: {nums[i]} + {nums[left]} + {nums[right]} = {current_sum}")
            
            # Update closest sum if current is closer to target
            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum
                print(f"    New closest sum: {closest_sum} (distance: {abs(current_sum - target)})")
            else:
                print(f"    Current sum not closer (distance: {abs(current_sum - target)})")
            
            if current_sum < target:
                left += 1
                print(f"    Sum too small, moving left pointer to {left}")
            elif current_sum > target:
                right -= 1
                print(f"    Sum too large, moving right pointer to {right}")
            else:
                print(f"    Exact match found: {current_sum}")
                return current_sum
    
    print(f"\nFinal result: {closest_sum}")
    return closest_sum


def three_sum_closest_with_stats(nums, target):
    """
    Find three integers whose sum is closest to target and return statistics.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        dict: Statistics about the search
    """
    nums.sort()
    closest_sum = float('inf')
    total_combinations = 0
    exact_matches = 0
    
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            total_combinations += 1
            current_sum = nums[i] + nums[left] + nums[right]
            
            # Update closest sum if current is closer to target
            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum
            
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                exact_matches += 1
                return {
                    'closest_sum': current_sum,
                    'total_combinations': total_combinations,
                    'exact_matches': exact_matches,
                    'array_length': len(nums)
                }
    
    return {
        'closest_sum': closest_sum,
        'total_combinations': total_combinations,
        'exact_matches': exact_matches,
        'array_length': len(nums)
    }


def three_sum_closest_with_validation(nums, target):
    """
    Find three integers whose sum is closest to target with validation.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        dict: Detailed validation results
    """
    if not nums:
        return {
            'closest_sum': 0,
            'is_valid': False,
            'reason': 'Empty array'
        }
    
    if len(nums) < 3:
        return {
            'closest_sum': 0,
            'is_valid': False,
            'reason': f'Array too short: {len(nums)} < 3'
        }
    
    nums.sort()
    closest_sum = float('inf')
    
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            # Update closest sum if current is closer to target
            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum
            
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                return {
                    'closest_sum': current_sum,
                    'is_valid': True,
                    'reason': f'Exact match found: {current_sum}',
                    'input': nums,
                    'target': target
                }
    
    return {
        'closest_sum': closest_sum,
        'is_valid': True,
        'reason': f'Found closest sum: {closest_sum}',
        'input': nums,
        'target': target
    }


def three_sum_closest_with_comparison(nums, target):
    """
    Find three integers whose sum is closest to target and compare different approaches.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        dict: Comparison of different approaches
    """
    # Two-pointer approach
    two_pointer_result = three_sum_closest(nums.copy(), target)
    
    # Brute force approach
    brute_force_result = three_sum_closest_with_brute_force(nums.copy(), target)
    
    return {
        'two_pointer': two_pointer_result,
        'brute_force': brute_force_result
    }


def three_sum_closest_with_performance(nums, target):
    """
    Find three integers whose sum is closest to target with performance metrics.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    start_time = time.time()
    operations = 0
    
    nums.sort()
    closest_sum = float('inf')
    
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            operations += 1
            current_sum = nums[i] + nums[left] + nums[right]
            
            # Update closest sum if current is closer to target
            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum
            
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                end_time = time.time()
                return {
                    'closest_sum': current_sum,
                    'execution_time': end_time - start_time,
                    'operations': operations
                }
    
    end_time = time.time()
    
    return {
        'closest_sum': closest_sum,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def three_sum_closest_with_debugging(nums, target):
    """
    Find three integers whose sum is closest to target with debugging information.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        dict: Debugging information
    """
    if not nums:
        return {
            'closest_sum': 0,
            'debug_info': 'Empty array',
            'steps': 0
        }
    
    nums.sort()
    closest_sum = float('inf')
    steps = 0
    
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            steps += 1
            current_sum = nums[i] + nums[left] + nums[right]
            
            # Update closest sum if current is closer to target
            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum
            
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                return {
                    'closest_sum': current_sum,
                    'debug_info': f'Exact match found after {steps} operations',
                    'steps': steps
                }
    
    return {
        'closest_sum': closest_sum,
        'debug_info': f'Processed {steps} operations',
        'steps': steps
    }


def three_sum_closest_with_analysis(nums, target):
    """
    Find three integers whose sum is closest to target and return analysis.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        dict: Analysis results
    """
    if not nums:
        return {
            'closest_sum': 0,
            'analysis': 'Empty array',
            'efficiency': 'N/A'
        }
    
    nums.sort()
    closest_sum = float('inf')
    total_operations = 0
    
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            total_operations += 1
            current_sum = nums[i] + nums[left] + nums[right]
            
            # Update closest sum if current is closer to target
            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum
            
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                return {
                    'closest_sum': current_sum,
                    'analysis': f'Exact match found in {total_operations} operations',
                    'efficiency': 1.0
                }
    
    efficiency = abs(closest_sum - target) / abs(target) if target != 0 else 0.0
    
    return {
        'closest_sum': closest_sum,
        'analysis': f'Found closest sum {closest_sum} in {total_operations} operations',
        'efficiency': efficiency
    }


def three_sum_closest_with_optimization(nums, target):
    """
    Find three integers whose sum is closest to target with optimization techniques.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        dict: Optimization results
    """
    if not nums:
        return {
            'closest_sum': 0,
            'optimization': 'Empty array',
            'space_saved': 0
        }
    
    nums.sort()
    closest_sum = float('inf')
    
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            # Update closest sum if current is closer to target
            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum
            
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                return {
                    'closest_sum': current_sum,
                    'optimization': 'Exact match found',
                    'space_saved': 0
                }
    
    # Calculate space optimization
    original_space = len(nums) * 4  # Assuming 4 bytes per integer
    optimized_space = 3 * 4  # Only storing three integers
    space_saved = original_space - optimized_space
    
    return {
        'closest_sum': closest_sum,
        'optimization': f'Space saved: {space_saved} bytes',
        'space_saved': space_saved
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ([-1, 2, 1, -4], 1, 2),
        ([0, 0, 0], 1, 0),
        ([1, 1, 1, 0], -100, 2),
        ([1, 1, 1, 0], 100, 3),
        ([1, 1, 1, 0], 1, 2),
        ([], 1, 0),
        ([1], 1, 0),
        ([1, 2], 1, 0),
        ([1, 2, 3], 1, 6),
        ([-1, 2, 1, -4], 1, 2),
    ]
    
    for i, (nums, target, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: nums={nums}, target={target}")
        
        # Test basic approach
        result = three_sum_closest(nums.copy(), target)
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = three_sum_closest_optimized(nums.copy(), target)
        print(f"Optimized result: {result_opt}")
        
        # Test brute force approach
        result_brute = three_sum_closest_with_brute_force(nums.copy(), target)
        print(f"Brute force result: {result_brute}")
        
        # Test with statistics
        stats = three_sum_closest_with_stats(nums.copy(), target)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = three_sum_closest_with_validation(nums.copy(), target)
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = three_sum_closest_with_comparison(nums.copy(), target)
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = three_sum_closest_with_performance(nums.copy(), target)
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = three_sum_closest_with_debugging(nums.copy(), target)
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        analysis = three_sum_closest_with_analysis(nums.copy(), target)
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        optimization = three_sum_closest_with_optimization(nums.copy(), target)
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    three_sum_closest_verbose([-1, 2, 1, -4], 1)
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large array for testing
    def generate_large_array(length):
        """Generate a large array for testing."""
        return [random.randint(-100, 100) for _ in range(length)]
    
    large_nums = generate_large_array(1000)
    target = 50
    
    # Test two-pointer approach
    start_time = time.time()
    for _ in range(100):
        three_sum_closest(large_nums.copy(), target)
    two_pointer_time = time.time() - start_time
    
    # Test brute force approach
    start_time = time.time()
    for _ in range(100):
        three_sum_closest_with_brute_force(large_nums.copy(), target)
    brute_force_time = time.time() - start_time
    
    print(f"Two-pointer approach: {two_pointer_time:.6f} seconds")
    print(f"Brute force approach: {brute_force_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Sort the array to enable two-pointer technique")
    print("2. For each element at position i:")
    print("   - Use two pointers: left = i + 1, right = len(nums) - 1")
    print("   - While left < right:")
    print("     - Calculate sum of three elements")
    print("     - If sum is closer to target, update closest sum")
    print("     - If sum < target, move left pointer right")
    print("     - If sum > target, move right pointer left")
    print("3. Return closest sum")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    nums = [-1, 2, 1, -4]
    target = 1
    print(f"Array: {nums}")
    print(f"Target: {target}")
    print("\nSteps:")
    print("1. i=0, nums[0]=-1, left=1, right=3: sum = -1+2+1 = 2, distance = 1")
    print("2. i=0, nums[0]=-1, left=2, right=3: sum = -1+1+1 = 1, distance = 0")
    print("3. i=1, nums[1]=2, left=2, right=3: sum = 2+1+1 = 4, distance = 3")
    print("4. i=2, nums[2]=1, left=3, right=3: sum = 1+1+1 = 3, distance = 2")
    print("Closest sum: 2")
    
    # Test with different targets
    print("\nDifferent targets:")
    test_nums = [-1, 2, 1, -4]
    targets = [0, 1, 2, 3, 4, 5]
    
    for target in targets:
        result = three_sum_closest(test_nums.copy(), target)
        print(f"Target: {target} -> Closest sum: {result}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        ([], 1),
        ([1], 1),
        ([1, 2], 1),
        ([1, 2, 3], 1),
        ([1, 1, 1], 1),
        ([1, 2, 3, 4], 1),
    ]
    
    for nums, target in edge_cases:
        result = three_sum_closest(nums.copy(), target)
        print(f"Array: {nums}, Target: {target} -> Closest sum: {result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for nums, target, _ in test_cases[:5]:
        stats = three_sum_closest_with_stats(nums.copy(), target)
        print(f"Array: {nums}, Target: {target}")
        print(f"  Closest sum: {stats['closest_sum']}")
        print(f"  Total combinations: {stats['total_combinations']}")
        print(f"  Exact matches: {stats['exact_matches']}")
        print(f"  Array length: {stats['array_length']}")
        print()
