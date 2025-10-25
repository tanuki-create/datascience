"""
Problem 41: 3Sum
Difficulty: Medium

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] 
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Time Complexity: O(n²) where n is the length of the array
Space Complexity: O(1) excluding the output array
"""

def three_sum(nums):
    """
    Find all unique triplets that sum to zero using two-pointer technique.
    
    Args:
        nums: List of integers
        
    Returns:
        list: List of unique triplets that sum to zero
    """
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for the second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for the third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    
    return result


def three_sum_optimized(nums):
    """
    Find all unique triplets that sum to zero using optimized approach.
    
    Args:
        nums: List of integers
        
    Returns:
        list: List of unique triplets that sum to zero
    """
    if len(nums) < 3:
        return []
    
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # Early termination if the smallest element is positive
        if nums[i] > 0:
            break
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for the second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for the third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    
    return result


def three_sum_with_hashmap(nums):
    """
    Find all unique triplets that sum to zero using hashmap approach.
    
    Args:
        nums: List of integers
        
    Returns:
        list: List of unique triplets that sum to zero
    """
    if len(nums) < 3:
        return []
    
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        target = -nums[i]
        seen = set()
        
        for j in range(i + 1, len(nums)):
            complement = target - nums[j]
            
            if complement in seen:
                triplet = [nums[i], complement, nums[j]]
                if triplet not in result:
                    result.append(triplet)
            
            seen.add(nums[j])
    
    return result


def three_sum_verbose(nums):
    """
    Find all unique triplets that sum to zero with detailed step-by-step explanation.
    
    Args:
        nums: List of integers
        
    Returns:
        list: List of unique triplets that sum to zero
    """
    print(f"Finding triplets that sum to zero in {nums}")
    print(f"Array length: {len(nums)}")
    
    if len(nums) < 3:
        print("Array too short, returning []")
        return []
    
    nums.sort()
    print(f"Sorted array: {nums}")
    
    result = []
    
    for i in range(len(nums) - 2):
        print(f"\nStep {i + 1}: Checking first element nums[{i}] = {nums[i]}")
        
        # Skip duplicates for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            print(f"  Skipping duplicate first element: {nums[i]}")
            continue
        
        left, right = i + 1, len(nums) - 1
        print(f"  Two pointers: left = {left}, right = {right}")
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            print(f"    Checking: {nums[i]} + {nums[left]} + {nums[right]} = {current_sum}")
            
            if current_sum == 0:
                triplet = [nums[i], nums[left], nums[right]]
                result.append(triplet)
                print(f"    Found triplet: {triplet}")
                
                # Skip duplicates for the second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                    print(f"    Skipping duplicate second element: {nums[left]}")
                # Skip duplicates for the third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                    print(f"    Skipping duplicate third element: {nums[right]}")
                
                left += 1
                right -= 1
                print(f"    Moving pointers: left = {left}, right = {right}")
            elif current_sum < 0:
                left += 1
                print(f"    Sum too small, moving left pointer to {left}")
            else:
                right -= 1
                print(f"    Sum too large, moving right pointer to {right}")
    
    print(f"\nFinal result: {result}")
    return result


def three_sum_with_stats(nums):
    """
    Find all unique triplets that sum to zero and return statistics.
    
    Args:
        nums: List of integers
        
    Returns:
        dict: Statistics about the search
    """
    if len(nums) < 3:
        return {
            'triplets': [],
            'total_combinations': 0,
            'valid_combinations': 0,
            'array_length': len(nums)
        }
    
    nums.sort()
    result = []
    total_combinations = 0
    valid_combinations = 0
    
    for i in range(len(nums) - 2):
        # Skip duplicates for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            total_combinations += 1
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                valid_combinations += 1
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for the second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for the third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    
    return {
        'triplets': result,
        'total_combinations': total_combinations,
        'valid_combinations': valid_combinations,
        'array_length': len(nums)
    }


def three_sum_with_validation(nums):
    """
    Find all unique triplets that sum to zero with validation.
    
    Args:
        nums: List of integers
        
    Returns:
        dict: Detailed validation results
    """
    if not nums:
        return {
            'triplets': [],
            'is_valid': False,
            'reason': 'Empty array'
        }
    
    if len(nums) < 3:
        return {
            'triplets': [],
            'is_valid': False,
            'reason': f'Array too short: {len(nums)} < 3'
        }
    
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for the second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for the third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    
    return {
        'triplets': result,
        'is_valid': True,
        'reason': f'Found {len(result)} unique triplets',
        'array': nums
    }


def three_sum_with_comparison(nums):
    """
    Find all unique triplets that sum to zero and compare different approaches.
    
    Args:
        nums: List of integers
        
    Returns:
        dict: Comparison of different approaches
    """
    if len(nums) < 3:
        return {
            'two_pointer': [],
            'hashmap': []
        }
    
    # Two-pointer approach
    two_pointer_result = three_sum(nums.copy())
    
    # Hashmap approach
    hashmap_result = three_sum_with_hashmap(nums.copy())
    
    return {
        'two_pointer': two_pointer_result,
        'hashmap': hashmap_result
    }


def three_sum_with_performance(nums):
    """
    Find all unique triplets that sum to zero with performance metrics.
    
    Args:
        nums: List of integers
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    if len(nums) < 3:
        return {
            'triplets': [],
            'execution_time': 0,
            'operations': 0
        }
    
    start_time = time.time()
    operations = 0
    
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            operations += 1
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for the second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for the third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    
    end_time = time.time()
    
    return {
        'triplets': result,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def three_sum_with_debugging(nums):
    """
    Find all unique triplets that sum to zero with debugging information.
    
    Args:
        nums: List of integers
        
    Returns:
        dict: Debugging information
    """
    if len(nums) < 3:
        return {
            'triplets': [],
            'debug_info': 'Array too short',
            'steps': 0
        }
    
    nums.sort()
    result = []
    steps = 0
    
    for i in range(len(nums) - 2):
        # Skip duplicates for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            steps += 1
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for the second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for the third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    
    return {
        'triplets': result,
        'debug_info': f'Processed {steps} combinations',
        'steps': steps
    }


def three_sum_with_analysis(nums):
    """
    Find all unique triplets that sum to zero and return analysis.
    
    Args:
        nums: List of integers
        
    Returns:
        dict: Analysis results
    """
    if len(nums) < 3:
        return {
            'triplets': [],
            'analysis': 'Array too short',
            'efficiency': 'N/A'
        }
    
    nums.sort()
    result = []
    total_combinations = 0
    
    for i in range(len(nums) - 2):
        # Skip duplicates for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            total_combinations += 1
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for the second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for the third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    
    efficiency = len(result) / total_combinations if total_combinations > 0 else 0.0
    
    return {
        'triplets': result,
        'analysis': f'Found {len(result)} triplets out of {total_combinations} combinations',
        'efficiency': efficiency
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 1, 1], []),
        ([0, 0, 0], [[0, 0, 0]]),
        ([-2, 0, 1, 1, 2], [[-2, 0, 2], [-2, 1, 1]]),
        ([0, 0, 0, 0], [[0, 0, 0]]),
        ([], []),
        ([1, 2], []),
        ([1, 2, 3], []),
        ([-1, 0, 1], [[-1, 0, 1]]),
        ([-2, -1, 0, 1, 2], [[-2, 0, 2], [-1, 0, 1]]),
    ]
    
    for i, (nums, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: nums={nums}")
        
        # Test basic approach
        result = three_sum(nums.copy())
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = three_sum_optimized(nums.copy())
        print(f"Optimized result: {result_opt}")
        
        # Test hashmap approach
        result_hash = three_sum_with_hashmap(nums.copy())
        print(f"Hashmap result: {result_hash}")
        
        # Test with statistics
        stats = three_sum_with_stats(nums.copy())
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = three_sum_with_validation(nums.copy())
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = three_sum_with_comparison(nums.copy())
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = three_sum_with_performance(nums.copy())
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = three_sum_with_debugging(nums.copy())
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        analysis = three_sum_with_analysis(nums.copy())
        print(f"Analysis: {analysis}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    three_sum_verbose([-1, 0, 1, 2, -1, -4])
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large array for testing
    def generate_large_array(length):
        """Generate a large array for testing."""
        return [random.randint(-100, 100) for _ in range(length)]
    
    large_nums = generate_large_array(1000)
    
    # Test two-pointer approach
    start_time = time.time()
    for _ in range(100):
        three_sum(large_nums.copy())
    two_pointer_time = time.time() - start_time
    
    # Test hashmap approach
    start_time = time.time()
    for _ in range(100):
        three_sum_with_hashmap(large_nums.copy())
    hashmap_time = time.time() - start_time
    
    print(f"Two-pointer approach: {two_pointer_time:.6f} seconds")
    print(f"Hashmap approach: {hashmap_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Sort the array to enable two-pointer technique")
    print("2. For each element at position i:")
    print("   - Skip if it's the same as the previous element (avoid duplicates)")
    print("   - Use two pointers: left = i + 1, right = len(nums) - 1")
    print("   - While left < right:")
    print("     - Calculate sum of three elements")
    print("     - If sum == 0, add triplet and skip duplicates")
    print("     - If sum < 0, move left pointer right")
    print("     - If sum > 0, move right pointer left")
    print("3. Return all unique triplets")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    nums = [-1, 0, 1, 2, -1, -4]
    print(f"Array: {nums}")
    print("Sorted array: [-4, -1, -1, 0, 1, 2]")
    print("\nSteps:")
    print("1. i=0, nums[0]=-4, left=1, right=5")
    print("2. i=1, nums[1]=-1, left=2, right=5")
    print("3. i=2, nums[2]=-1, left=3, right=5")
    print("4. i=3, nums[3]=0, left=4, right=5")
    print("5. i=4, nums[4]=1, left=5, right=5")
    print("6. i=5, nums[5]=2, left=6, right=5")
    
    # Test with different arrays
    print("\nDifferent arrays:")
    test_arrays = [
        [-1, 0, 1],
        [-2, -1, 0, 1, 2],
        [0, 0, 0],
        [1, 2, 3],
        [-1, -1, 2],
    ]
    
    for arr in test_arrays:
        result = three_sum(arr.copy())
        print(f"Array: {arr} -> Triplets: {result}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],
        [1],
        [1, 2],
        [1, 2, 3],
        [0, 0, 0],
        [1, 1, 1],
    ]
    
    for nums in edge_cases:
        result = three_sum(nums.copy())
        print(f"Array: {nums} -> Triplets: {result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for nums, _ in test_cases[:5]:
        stats = three_sum_with_stats(nums.copy())
        print(f"Array: {nums}")
        print(f"  Triplets: {stats['triplets']}")
        print(f"  Total combinations: {stats['total_combinations']}")
        print(f"  Valid combinations: {stats['valid_combinations']}")
        print(f"  Array length: {stats['array_length']}")
        print()
