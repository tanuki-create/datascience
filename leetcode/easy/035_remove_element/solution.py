"""
Problem 35: Remove Element
Difficulty: Easy

Given an integer array nums and an integer val, remove all occurrences of val 
in-place. The order of the elements may be changed. Then return the number of 
elements in nums which are not equal to val.

Do not allocate extra space for another array. You must do this by modifying 
the input array in-place with O(1) extra memory.

Time Complexity: O(n) where n is the length of the array
Space Complexity: O(1) - in-place modification with constant extra space
"""

def remove_element(nums, val):
    """
    Remove all occurrences of val in-place and return the new length.
    
    Args:
        nums: List of integers to modify
        val: Value to remove from the array
        
    Returns:
        int: Number of elements not equal to val
    """
    j = 0  # Write pointer
    
    for i in range(len(nums)):
        if nums[i] != val:
            nums[j] = nums[i]
            j += 1
    
    return j


def remove_element_optimized(nums, val):
    """
    Remove all occurrences of val using optimized two-pointer approach.
    
    Args:
        nums: List of integers to modify
        val: Value to remove from the array
        
    Returns:
        int: Number of elements not equal to val
    """
    j = 0  # Write pointer
    
    for i in range(len(nums)):
        if nums[i] != val:
            nums[j] = nums[i]
            j += 1
    
    return j


def remove_element_with_counting(nums, val):
    """
    Remove all occurrences of val and return detailed statistics.
    
    Args:
        nums: List of integers to modify
        val: Value to remove from the array
        
    Returns:
        dict: Statistics about the removal process
    """
    j = 0  # Write pointer
    removed_count = 0
    
    for i in range(len(nums)):
        if nums[i] != val:
            nums[j] = nums[i]
            j += 1
        else:
            removed_count += 1
    
    return {
        'new_length': j,
        'removed_count': removed_count,
        'original_length': len(nums)
    }


def remove_element_verbose(nums, val):
    """
    Remove all occurrences of val with detailed step-by-step explanation.
    
    Args:
        nums: List of integers to modify
        val: Value to remove from the array
        
    Returns:
        int: Number of elements not equal to val
    """
    print(f"Removing all occurrences of {val} from {nums}")
    print(f"Original array: {nums}")
    print(f"Value to remove: {val}")
    
    j = 0  # Write pointer
    
    for i in range(len(nums)):
        print(f"\nStep {i + 1}:")
        print(f"  Reading nums[{i}] = {nums[i]}")
        print(f"  Write pointer j = {j}")
        
        if nums[i] != val:
            print(f"  nums[{i}] != {val}, copying to nums[{j}]")
            nums[j] = nums[i]
            j += 1
            print(f"  New write pointer j = {j}")
        else:
            print(f"  nums[{i}] == {val}, skipping")
        
        print(f"  Current array: {nums[:j]} + {nums[j:]}")
    
    print(f"\nFinal result: {j} elements remaining")
    print(f"Modified array: {nums[:j]} + {nums[j:]}")
    
    return j


def remove_element_with_validation(nums, val):
    """
    Remove all occurrences of val with validation.
    
    Args:
        nums: List of integers to modify
        val: Value to remove from the array
        
    Returns:
        dict: Detailed validation results
    """
    if not nums:
        return {
            'new_length': 0,
            'is_valid': True,
            'reason': 'Empty array',
            'modified_array': []
        }
    
    original_length = len(nums)
    j = 0  # Write pointer
    
    for i in range(len(nums)):
        if nums[i] != val:
            nums[j] = nums[i]
            j += 1
    
    return {
        'new_length': j,
        'is_valid': True,
        'reason': f'Removed {original_length - j} occurrences of {val}',
        'modified_array': nums[:j]
    }


def remove_element_with_comparison(nums, val):
    """
    Remove all occurrences of val and compare different approaches.
    
    Args:
        nums: List of integers to modify
        val: Value to remove from the array
        
    Returns:
        dict: Comparison of different approaches
    """
    # Two-pointer approach
    nums_copy1 = nums.copy()
    result1 = remove_element(nums_copy1, val)
    
    # Alternative approach using list comprehension
    nums_copy2 = nums.copy()
    result2 = len([x for x in nums_copy2 if x != val])
    
    return {
        'two_pointer': result1,
        'list_comprehension': result2
    }


def remove_element_with_performance(nums, val):
    """
    Remove all occurrences of val with performance metrics.
    
    Args:
        nums: List of integers to modify
        val: Value to remove from the array
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    start_time = time.time()
    operations = 0
    
    j = 0  # Write pointer
    
    for i in range(len(nums)):
        if nums[i] != val:
            nums[j] = nums[i]
            j += 1
        operations += 1
    
    end_time = time.time()
    
    return {
        'new_length': j,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def remove_element_with_debugging(nums, val):
    """
    Remove all occurrences of val with debugging information.
    
    Args:
        nums: List of integers to modify
        val: Value to remove from the array
        
    Returns:
        dict: Debugging information
    """
    if not nums:
        return {
            'new_length': 0,
            'debug_info': 'Empty array',
            'steps': 0
        }
    
    j = 0  # Write pointer
    steps = 0
    
    for i in range(len(nums)):
        if nums[i] != val:
            nums[j] = nums[i]
            j += 1
        steps += 1
    
    return {
        'new_length': j,
        'debug_info': f'Processed {steps} elements',
        'steps': steps
    }


def remove_element_with_statistics(nums, val):
    """
    Remove all occurrences of val and return detailed statistics.
    
    Args:
        nums: List of integers to modify
        val: Value to remove from the array
        
    Returns:
        dict: Detailed statistics
    """
    if not nums:
        return {
            'new_length': 0,
            'removed_count': 0,
            'original_length': 0,
            'removal_rate': 0.0
        }
    
    original_length = len(nums)
    j = 0  # Write pointer
    removed_count = 0
    
    for i in range(len(nums)):
        if nums[i] != val:
            nums[j] = nums[i]
            j += 1
        else:
            removed_count += 1
    
    removal_rate = removed_count / original_length if original_length > 0 else 0.0
    
    return {
        'new_length': j,
        'removed_count': removed_count,
        'original_length': original_length,
        'removal_rate': removal_rate
    }


def remove_element_with_analysis(nums, val):
    """
    Remove all occurrences of val and return analysis.
    
    Args:
        nums: List of integers to modify
        val: Value to remove from the array
        
    Returns:
        dict: Analysis results
    """
    if not nums:
        return {
            'new_length': 0,
            'analysis': 'Empty array',
            'efficiency': 'N/A'
        }
    
    original_length = len(nums)
    j = 0  # Write pointer
    removed_count = 0
    
    for i in range(len(nums)):
        if nums[i] != val:
            nums[j] = nums[i]
            j += 1
        else:
            removed_count += 1
    
    efficiency = (original_length - removed_count) / original_length if original_length > 0 else 0.0
    
    return {
        'new_length': j,
        'analysis': f'Removed {removed_count} out of {original_length} elements',
        'efficiency': efficiency
    }


def remove_element_with_optimization(nums, val):
    """
    Remove all occurrences of val with optimization techniques.
    
    Args:
        nums: List of integers to modify
        val: Value to remove from the array
        
    Returns:
        dict: Optimization results
    """
    if not nums:
        return {
            'new_length': 0,
            'optimization': 'Empty array',
            'space_saved': 0
        }
    
    original_length = len(nums)
    j = 0  # Write pointer
    
    for i in range(len(nums)):
        if nums[i] != val:
            nums[j] = nums[i]
            j += 1
    
    space_saved = original_length - j
    
    return {
        'new_length': j,
        'optimization': f'Space saved: {space_saved} elements',
        'space_saved': space_saved
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ([3, 2, 2, 3], 3, 2),
        ([0, 1, 2, 2, 3, 0, 4, 2], 2, 5),
        ([1, 2, 3, 4], 5, 4),
        ([2, 2, 2, 2], 2, 0),
        ([1], 1, 0),
        ([], 1, 0),
        ([1, 2, 3], 4, 3),
        ([1, 1, 1], 1, 0),
        ([1, 2, 3, 4, 5], 3, 4),
        ([1, 2, 3, 4, 5], 1, 4),
    ]
    
    for i, (nums, val, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: nums={nums}, val={val}")
        
        # Test basic approach
        nums_copy = nums.copy()
        result = remove_element(nums_copy, val)
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        print(f"Modified array: {nums_copy[:result]}")
        
        # Test with counting
        nums_copy2 = nums.copy()
        counting_result = remove_element_with_counting(nums_copy2, val)
        print(f"Counting result: {counting_result}")
        
        # Test with validation
        nums_copy3 = nums.copy()
        validation_result = remove_element_with_validation(nums_copy3, val)
        print(f"Validation result: {validation_result}")
        
        # Test with comparison
        nums_copy4 = nums.copy()
        comparison_result = remove_element_with_comparison(nums_copy4, val)
        print(f"Comparison result: {comparison_result}")
        
        # Test with performance
        nums_copy5 = nums.copy()
        performance_result = remove_element_with_performance(nums_copy5, val)
        print(f"Performance result: {performance_result}")
        
        # Test with debugging
        nums_copy6 = nums.copy()
        debugging_result = remove_element_with_debugging(nums_copy6, val)
        print(f"Debugging result: {debugging_result}")
        
        # Test with statistics
        nums_copy7 = nums.copy()
        statistics_result = remove_element_with_statistics(nums_copy7, val)
        print(f"Statistics result: {statistics_result}")
        
        # Test with analysis
        nums_copy8 = nums.copy()
        analysis_result = remove_element_with_analysis(nums_copy8, val)
        print(f"Analysis result: {analysis_result}")
        
        # Test with optimization
        nums_copy9 = nums.copy()
        optimization_result = remove_element_with_optimization(nums_copy9, val)
        print(f"Optimization result: {optimization_result}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    nums = [3, 2, 2, 3]
    val = 3
    remove_element_verbose(nums.copy(), val)
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large array for testing
    def generate_large_array(length):
        """Generate a large array for testing."""
        return [random.randint(0, 50) for _ in range(length)]
    
    large_nums = generate_large_array(10000)
    val = 25
    
    # Test two-pointer approach
    start_time = time.time()
    for _ in range(1000):
        remove_element(large_nums.copy(), val)
    two_pointer_time = time.time() - start_time
    
    # Test list comprehension approach
    start_time = time.time()
    for _ in range(1000):
        [x for x in large_nums if x != val]
    list_comp_time = time.time() - start_time
    
    print(f"Two-pointer approach: {two_pointer_time:.6f} seconds")
    print(f"List comprehension approach: {list_comp_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Use two pointers: read pointer (i) and write pointer (j)")
    print("2. For each element at position i:")
    print("   - If nums[i] != val, copy nums[i] to nums[j] and increment j")
    print("   - If nums[i] == val, skip the element")
    print("3. Return j as the count of remaining elements")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    nums = [3, 2, 2, 3]
    val = 3
    print(f"Array: {nums}")
    print(f"Value to remove: {val}")
    print("\nSteps:")
    j = 0
    for i in range(len(nums)):
        if nums[i] != val:
            print(f"  Step {i + 1}: nums[{i}] = {nums[i]} != {val}, copy to nums[{j}]")
            j += 1
        else:
            print(f"  Step {i + 1}: nums[{i}] = {nums[i]} == {val}, skip")
    print(f"Final result: {j} elements remaining")
    
    # Test with different values
    print("\nDifferent values:")
    test_nums = [1, 2, 3, 4, 5]
    for val in [1, 2, 3, 4, 5, 6]:
        result = remove_element(test_nums.copy(), val)
        print(f"Remove {val} from {test_nums}: {result} elements remaining")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        ([], 1),
        ([1], 1),
        ([1], 2),
        ([1, 1], 1),
        ([1, 2], 1),
        ([1, 2], 2),
        ([1, 2], 3),
    ]
    
    for nums, val in edge_cases:
        result = remove_element(nums.copy(), val)
        print(f"nums={nums}, val={val} -> {result} elements remaining")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for nums, val, _ in test_cases[:5]:
        stats = remove_element_with_statistics(nums.copy(), val)
        print(f"Array: {nums}, Value: {val}")
        print(f"  New length: {stats['new_length']}")
        print(f"  Removed count: {stats['removed_count']}")
        print(f"  Original length: {stats['original_length']}")
        print(f"  Removal rate: {stats['removal_rate']:.2f}")
        print()
