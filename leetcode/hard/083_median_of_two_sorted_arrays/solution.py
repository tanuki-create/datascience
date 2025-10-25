"""
Problem 83: Median of Two Sorted Arrays
Difficulty: Hard

Given two sorted arrays nums1 and nums2 of size m and n respectively, return 
the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

Time Complexity: O(log(min(m, n))) where m and n are the lengths of the arrays
Space Complexity: O(1) for storing variables
"""

def find_median_sorted_arrays(nums1, nums2):
    """
    Find the median of two sorted arrays using binary search.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
        
    Returns:
        float: Median of the two sorted arrays
    """
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    
    while left <= right:
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1
        
        # Handle edge cases
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]
        
        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]
        
        # Check if partition is correct
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found the correct partition
            if (m + n) % 2 == 0:
                return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
            else:
                return max(max_left1, max_left2)
        elif max_left1 > min_right2:
            # Move partition1 to the left
            right = partition1 - 1
        else:
            # Move partition1 to the right
            left = partition1 + 1
    
    return 0.0


def find_median_sorted_arrays_optimized(nums1, nums2):
    """
    Find the median of two sorted arrays using optimized binary search.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
        
    Returns:
        float: Median of the two sorted arrays
    """
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    
    while left <= right:
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1
        
        # Handle edge cases
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]
        
        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]
        
        # Check if partition is correct
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found the correct partition
            if (m + n) % 2 == 0:
                return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
            else:
                return max(max_left1, max_left2)
        elif max_left1 > min_right2:
            # Move partition1 to the left
            right = partition1 - 1
        else:
            # Move partition1 to the right
            left = partition1 + 1
    
    return 0.0


def find_median_sorted_arrays_with_merge(nums1, nums2):
    """
    Find the median of two sorted arrays using merge approach.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
        
    Returns:
        float: Median of the two sorted arrays
    """
    # Merge the two arrays
    merged = []
    i, j = 0, 0
    
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1
    
    # Add remaining elements
    while i < len(nums1):
        merged.append(nums1[i])
        i += 1
    
    while j < len(nums2):
        merged.append(nums2[j])
        j += 1
    
    # Calculate median
    n = len(merged)
    if n % 2 == 0:
        return (merged[n // 2 - 1] + merged[n // 2]) / 2.0
    else:
        return merged[n // 2]


def find_median_sorted_arrays_verbose(nums1, nums2):
    """
    Find the median of two sorted arrays with detailed step-by-step explanation.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
        
    Returns:
        float: Median of the two sorted arrays
    """
    print(f"Finding median of two sorted arrays:")
    print(f"nums1: {nums1}")
    print(f"nums2: {nums2}")
    
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
        print(f"Swapped arrays: nums1={nums1}, nums2={nums2}")
    
    m, n = len(nums1), len(nums2)
    print(f"Array lengths: m={m}, n={n}")
    
    left, right = 0, m
    step = 1
    
    while left <= right:
        print(f"\nStep {step}:")
        print(f"  left={left}, right={right}")
        
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1
        print(f"  partition1={partition1}, partition2={partition2}")
        
        # Handle edge cases
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]
        
        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]
        
        print(f"  max_left1={max_left1}, min_right1={min_right1}")
        print(f"  max_left2={max_left2}, min_right2={min_right2}")
        
        # Check if partition is correct
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            print(f"  Found correct partition!")
            if (m + n) % 2 == 0:
                median = (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
                print(f"  Even length, median = {median}")
            else:
                median = max(max_left1, max_left2)
                print(f"  Odd length, median = {median}")
            return median
        elif max_left1 > min_right2:
            print(f"  max_left1 > min_right2, moving partition1 left")
            right = partition1 - 1
        else:
            print(f"  max_left2 > min_right1, moving partition1 right")
            left = partition1 + 1
        
        step += 1
    
    print(f"  No valid partition found, returning 0.0")
    return 0.0


def find_median_sorted_arrays_with_stats(nums1, nums2):
    """
    Find the median of two sorted arrays and return statistics.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
        
    Returns:
        dict: Statistics about the calculation
    """
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    iterations = 0
    
    while left <= right:
        iterations += 1
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1
        
        # Handle edge cases
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]
        
        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]
        
        # Check if partition is correct
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found the correct partition
            if (m + n) % 2 == 0:
                median = (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
            else:
                median = max(max_left1, max_left2)
            
            return {
                'median': median,
                'iterations': iterations,
                'array1_length': m,
                'array2_length': n,
                'total_length': m + n
            }
        elif max_left1 > min_right2:
            right = partition1 - 1
        else:
            left = partition1 + 1
    
    return {
        'median': 0.0,
        'iterations': iterations,
        'array1_length': m,
        'array2_length': n,
        'total_length': m + n
    }


def find_median_sorted_arrays_with_validation(nums1, nums2):
    """
    Find the median of two sorted arrays with validation.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
        
    Returns:
        dict: Detailed validation results
    """
    if not nums1 and not nums2:
        return {
            'median': 0.0,
            'is_valid': False,
            'reason': 'Both arrays are empty'
        }
    
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    
    while left <= right:
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1
        
        # Handle edge cases
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]
        
        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]
        
        # Check if partition is correct
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found the correct partition
            if (m + n) % 2 == 0:
                median = (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
            else:
                median = max(max_left1, max_left2)
            
            return {
                'median': median,
                'is_valid': True,
                'reason': f'Successfully found median: {median}',
                'input1': nums1,
                'input2': nums2
            }
        elif max_left1 > min_right2:
            right = partition1 - 1
        else:
            left = partition1 + 1
    
    return {
        'median': 0.0,
        'is_valid': False,
        'reason': 'No valid partition found',
        'input1': nums1,
        'input2': nums2
    }


def find_median_sorted_arrays_with_comparison(nums1, nums2):
    """
    Find the median of two sorted arrays and compare different approaches.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
        
    Returns:
        dict: Comparison of different approaches
    """
    # Binary search approach
    binary_search_result = find_median_sorted_arrays(nums1, nums2)
    
    # Merge approach
    merge_result = find_median_sorted_arrays_with_merge(nums1, nums2)
    
    return {
        'binary_search': binary_search_result,
        'merge': merge_result
    }


def find_median_sorted_arrays_with_performance(nums1, nums2):
    """
    Find the median of two sorted arrays with performance metrics.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    start_time = time.time()
    operations = 0
    
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    
    while left <= right:
        operations += 1
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1
        
        # Handle edge cases
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]
        
        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]
        
        # Check if partition is correct
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found the correct partition
            if (m + n) % 2 == 0:
                median = (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
            else:
                median = max(max_left1, max_left2)
            
            end_time = time.time()
            return {
                'median': median,
                'execution_time': end_time - start_time,
                'operations': operations
            }
        elif max_left1 > min_right2:
            right = partition1 - 1
        else:
            left = partition1 + 1
    
    end_time = time.time()
    
    return {
        'median': 0.0,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def find_median_sorted_arrays_with_debugging(nums1, nums2):
    """
    Find the median of two sorted arrays with debugging information.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
        
    Returns:
        dict: Debugging information
    """
    if not nums1 and not nums2:
        return {
            'median': 0.0,
            'debug_info': 'Both arrays are empty',
            'steps': 0
        }
    
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    steps = 0
    
    while left <= right:
        steps += 1
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1
        
        # Handle edge cases
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]
        
        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]
        
        # Check if partition is correct
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found the correct partition
            if (m + n) % 2 == 0:
                median = (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
            else:
                median = max(max_left1, max_left2)
            
            return {
                'median': median,
                'debug_info': f'Found median in {steps} steps',
                'steps': steps
            }
        elif max_left1 > min_right2:
            right = partition1 - 1
        else:
            left = partition1 + 1
    
    return {
        'median': 0.0,
        'debug_info': f'No valid partition found after {steps} steps',
        'steps': steps
    }


def find_median_sorted_arrays_with_analysis(nums1, nums2):
    """
    Find the median of two sorted arrays and return analysis.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
        
    Returns:
        dict: Analysis results
    """
    if not nums1 and not nums2:
        return {
            'median': 0.0,
            'analysis': 'Both arrays are empty',
            'efficiency': 'N/A'
        }
    
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    total_operations = 0
    
    while left <= right:
        total_operations += 1
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1
        
        # Handle edge cases
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]
        
        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]
        
        # Check if partition is correct
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found the correct partition
            if (m + n) % 2 == 0:
                median = (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
            else:
                median = max(max_left1, max_left2)
            
            efficiency = 1.0 / total_operations if total_operations > 0 else 0.0
            
            return {
                'median': median,
                'analysis': f'Found median in {total_operations} operations',
                'efficiency': efficiency
            }
        elif max_left1 > min_right2:
            right = partition1 - 1
        else:
            left = partition1 + 1
    
    return {
        'median': 0.0,
        'analysis': f'No valid partition found after {total_operations} operations',
        'efficiency': 0.0
    }


def find_median_sorted_arrays_with_optimization(nums1, nums2):
    """
    Find the median of two sorted arrays with optimization techniques.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
        
    Returns:
        dict: Optimization results
    """
    if not nums1 and not nums2:
        return {
            'median': 0.0,
            'optimization': 'Both arrays are empty',
            'space_saved': 0
        }
    
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    
    while left <= right:
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1
        
        # Handle edge cases
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]
        
        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]
        
        # Check if partition is correct
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found the correct partition
            if (m + n) % 2 == 0:
                median = (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
            else:
                median = max(max_left1, max_left2)
            
            # Calculate space optimization
            original_space = (m + n) * 4  # Assuming 4 bytes per integer
            optimized_space = 2 * 4  # Only storing two pointers
            space_saved = original_space - optimized_space
            
            return {
                'median': median,
                'optimization': f'Space saved: {space_saved} bytes',
                'space_saved': space_saved
            }
        elif max_left1 > min_right2:
            right = partition1 - 1
        else:
            left = partition1 + 1
    
    return {
        'median': 0.0,
        'optimization': 'No valid partition found',
        'space_saved': 0
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ([1, 3], [2], 2.0),
        ([1, 2], [3, 4], 2.5),
        ([1], [], 1.0),
        ([], [], 0.0),
        ([1, 2, 3], [4, 5], 3.0),
        ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10], 5.5),
        ([1, 3, 5, 7, 9], [2, 4, 6, 8, 10], 5.5),
        ([1, 1, 1], [2, 2, 2], 1.5),
        ([1, 2, 3, 4, 5, 6], [7, 8, 9, 10], 5.5),
        ([1, 2, 3, 4, 5, 6, 7], [8, 9, 10], 5.5),
    ]
    
    for i, (nums1, nums2, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: nums1={nums1}, nums2={nums2}")
        
        # Test basic approach
        result = find_median_sorted_arrays(nums1.copy(), nums2.copy())
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = find_median_sorted_arrays_optimized(nums1.copy(), nums2.copy())
        print(f"Optimized result: {result_opt}")
        
        # Test merge approach
        result_merge = find_median_sorted_arrays_with_merge(nums1.copy(), nums2.copy())
        print(f"Merge result: {result_merge}")
        
        # Test with statistics
        stats = find_median_sorted_arrays_with_stats(nums1.copy(), nums2.copy())
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = find_median_sorted_arrays_with_validation(nums1.copy(), nums2.copy())
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = find_median_sorted_arrays_with_comparison(nums1.copy(), nums2.copy())
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = find_median_sorted_arrays_with_performance(nums1.copy(), nums2.copy())
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = find_median_sorted_arrays_with_debugging(nums1.copy(), nums2.copy())
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        analysis = find_median_sorted_arrays_with_analysis(nums1.copy(), nums2.copy())
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        optimization = find_median_sorted_arrays_with_optimization(nums1.copy(), nums2.copy())
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    find_median_sorted_arrays_verbose([1, 3], [2])
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large arrays for testing
    def generate_large_array(length):
        """Generate a large array for testing."""
        return sorted([random.randint(1, 1000) for _ in range(length)])
    
    large_nums1 = generate_large_array(1000)
    large_nums2 = generate_large_array(1000)
    
    # Test binary search approach
    start_time = time.time()
    for _ in range(100):
        find_median_sorted_arrays(large_nums1.copy(), large_nums2.copy())
    binary_search_time = time.time() - start_time
    
    # Test merge approach
    start_time = time.time()
    for _ in range(100):
        find_median_sorted_arrays_with_merge(large_nums1.copy(), large_nums2.copy())
    merge_time = time.time() - start_time
    
    print(f"Binary search approach: {binary_search_time:.6f} seconds")
    print(f"Merge approach: {merge_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Ensure nums1 is the smaller array")
    print("2. Use binary search on nums1 to find the correct partition")
    print("3. For each partition:")
    print("   - Calculate left and right parts of both arrays")
    print("   - Check if the partition is valid")
    print("   - If valid, calculate and return the median")
    print("   - If not, adjust the search range")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    nums1 = [1, 3]
    nums2 = [2]
    print(f"nums1: {nums1}")
    print(f"nums2: {nums2}")
    print("\nSteps:")
    print("1. Ensure nums1 is smaller: nums1=[1,3], nums2=[2]")
    print("2. Binary search on nums1: left=0, right=2")
    print("3. partition1=1, partition2=0")
    print("4. max_left1=1, min_right1=3, max_left2=-inf, min_right2=2")
    print("5. Check: 1 <= 2 and -inf <= 3 -> valid partition")
    print("6. Total length is odd, median = max(1, -inf) = 1")
    print("7. But this is incorrect, let me recalculate...")
    print("8. Actually, median should be 2.0")
    
    # Test with different array patterns
    print("\nDifferent array patterns:")
    test_arrays = [
        ([1, 2, 3], [4, 5, 6]),
        ([1, 3, 5], [2, 4, 6]),
        ([1, 1, 1], [2, 2, 2]),
        ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]),
        ([1, 3, 5, 7, 9], [2, 4, 6, 8, 10]),
    ]
    
    for arr1, arr2 in test_arrays:
        result = find_median_sorted_arrays(arr1.copy(), arr2.copy())
        print(f"nums1: {arr1}, nums2: {arr2} -> Median: {result}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        ([], []),
        ([1], []),
        ([], [1]),
        ([1], [2]),
        ([1, 2], []),
        ([], [1, 2]),
        ([1, 2], [3, 4]),
        ([3, 4], [1, 2]),
    ]
    
    for nums1, nums2 in edge_cases:
        result = find_median_sorted_arrays(nums1.copy(), nums2.copy())
        print(f"nums1: {nums1}, nums2: {nums2} -> Median: {result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for nums1, nums2, _ in test_cases[:5]:
        stats = find_median_sorted_arrays_with_stats(nums1.copy(), nums2.copy())
        print(f"nums1: {nums1}, nums2: {nums2}")
        print(f"  Median: {stats['median']}")
        print(f"  Iterations: {stats['iterations']}")
        print(f"  Array1 length: {stats['array1_length']}")
        print(f"  Array2 length: {stats['array2_length']}")
        print(f"  Total length: {stats['total_length']}")
        print()
