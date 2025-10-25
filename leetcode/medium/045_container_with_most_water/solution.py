"""
Problem 45: Container With Most Water
Difficulty: Medium

You are given an integer array height of length n. There are n vertical lines 
drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines, which, together with the x-axis forms a container, such that 
the container contains the most water.

Return the maximum amount of water a container can store.

Time Complexity: O(n) where n is the length of the array
Space Complexity: O(1) for storing variables
"""

def max_area(height):
    """
    Find the maximum area of water that can be contained using two pointers.
    
    Args:
        height: List of integers representing heights
        
    Returns:
        int: Maximum area of water that can be contained
    """
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        # Calculate area with current two lines
        area = min(height[left], height[right]) * (right - left)
        max_area = max(max_area, area)
        
        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area


def max_area_optimized(height):
    """
    Find the maximum area of water using optimized two-pointer approach.
    
    Args:
        height: List of integers representing heights
        
    Returns:
        int: Maximum area of water that can be contained
    """
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        # Calculate area with current two lines
        area = min(height[left], height[right]) * (right - left)
        max_area = max(max_area, area)
        
        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area


def max_area_with_brute_force(height):
    """
    Find the maximum area of water using brute force approach.
    
    Args:
        height: List of integers representing heights
        
    Returns:
        int: Maximum area of water that can be contained
    """
    max_area = 0
    
    for i in range(len(height)):
        for j in range(i + 1, len(height)):
            area = min(height[i], height[j]) * (j - i)
            max_area = max(max_area, area)
    
    return max_area


def max_area_verbose(height):
    """
    Find the maximum area of water with detailed step-by-step explanation.
    
    Args:
        height: List of integers representing heights
        
    Returns:
        int: Maximum area of water that can be contained
    """
    print(f"Finding maximum area of water in {height}")
    print(f"Array length: {len(height)}")
    
    left, right = 0, len(height) - 1
    max_area = 0
    
    step = 1
    while left < right:
        print(f"\nStep {step}: left={left}, right={right}")
        print(f"  Heights: height[{left}]={height[left]}, height[{right}]={height[right]}")
        
        # Calculate area with current two lines
        area = min(height[left], height[right]) * (right - left)
        print(f"  Area = min({height[left]}, {height[right]}) * ({right} - {left}) = {area}")
        
        max_area = max(max_area, area)
        print(f"  Max area so far: {max_area}")
        
        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            print(f"  height[{left}] < height[{right}], moving left pointer")
            left += 1
        else:
            print(f"  height[{left}] >= height[{right}], moving right pointer")
            right -= 1
        
        step += 1
    
    print(f"\nFinal result: {max_area}")
    return max_area


def max_area_with_stats(height):
    """
    Find the maximum area of water and return statistics.
    
    Args:
        height: List of integers representing heights
        
    Returns:
        dict: Statistics about the search
    """
    left, right = 0, len(height) - 1
    max_area = 0
    total_pairs = 0
    areas_calculated = 0
    
    while left < right:
        total_pairs += 1
        
        # Calculate area with current two lines
        area = min(height[left], height[right]) * (right - left)
        areas_calculated += 1
        max_area = max(max_area, area)
        
        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return {
        'max_area': max_area,
        'total_pairs': total_pairs,
        'areas_calculated': areas_calculated,
        'array_length': len(height)
    }


def max_area_with_validation(height):
    """
    Find the maximum area of water with validation.
    
    Args:
        height: List of integers representing heights
        
    Returns:
        dict: Detailed validation results
    """
    if not height:
        return {
            'max_area': 0,
            'is_valid': False,
            'reason': 'Empty array'
        }
    
    if len(height) < 2:
        return {
            'max_area': 0,
            'is_valid': False,
            'reason': f'Array too short: {len(height)} < 2'
        }
    
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        # Calculate area with current two lines
        area = min(height[left], height[right]) * (right - left)
        max_area = max(max_area, area)
        
        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return {
        'max_area': max_area,
        'is_valid': True,
        'reason': f'Found maximum area of {max_area}',
        'input': height
    }


def max_area_with_comparison(height):
    """
    Find the maximum area of water and compare different approaches.
    
    Args:
        height: List of integers representing heights
        
    Returns:
        dict: Comparison of different approaches
    """
    # Two-pointer approach
    two_pointer_result = max_area(height.copy())
    
    # Brute force approach
    brute_force_result = max_area_with_brute_force(height.copy())
    
    return {
        'two_pointer': two_pointer_result,
        'brute_force': brute_force_result
    }


def max_area_with_performance(height):
    """
    Find the maximum area of water with performance metrics.
    
    Args:
        height: List of integers representing heights
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    start_time = time.time()
    operations = 0
    
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        # Calculate area with current two lines
        area = min(height[left], height[right]) * (right - left)
        max_area = max(max_area, area)
        operations += 1
        
        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
        operations += 1
    
    end_time = time.time()
    
    return {
        'max_area': max_area,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def max_area_with_debugging(height):
    """
    Find the maximum area of water with debugging information.
    
    Args:
        height: List of integers representing heights
        
    Returns:
        dict: Debugging information
    """
    if not height:
        return {
            'max_area': 0,
            'debug_info': 'Empty array',
            'steps': 0
        }
    
    left, right = 0, len(height) - 1
    max_area = 0
    steps = 0
    
    while left < right:
        # Calculate area with current two lines
        area = min(height[left], height[right]) * (right - left)
        max_area = max(max_area, area)
        steps += 1
        
        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return {
        'max_area': max_area,
        'debug_info': f'Processed {steps} operations',
        'steps': steps
    }


def max_area_with_analysis(height):
    """
    Find the maximum area of water and return analysis.
    
    Args:
        height: List of integers representing heights
        
    Returns:
        dict: Analysis results
    """
    if not height:
        return {
            'max_area': 0,
            'analysis': 'Empty array',
            'efficiency': 'N/A'
        }
    
    left, right = 0, len(height) - 1
    max_area = 0
    total_operations = 0
    
    while left < right:
        # Calculate area with current two lines
        area = min(height[left], height[right]) * (right - left)
        max_area = max(max_area, area)
        total_operations += 1
        
        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    efficiency = max_area / (len(height) * max(height)) if height and max(height) > 0 else 0.0
    
    return {
        'max_area': max_area,
        'analysis': f'Found maximum area of {max_area} in {total_operations} operations',
        'efficiency': efficiency
    }


def max_area_with_optimization(height):
    """
    Find the maximum area of water with optimization techniques.
    
    Args:
        height: List of integers representing heights
        
    Returns:
        dict: Optimization results
    """
    if not height:
        return {
            'max_area': 0,
            'optimization': 'Empty array',
            'space_saved': 0
        }
    
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        # Calculate area with current two lines
        area = min(height[left], height[right]) * (right - left)
        max_area = max(max_area, area)
        
        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    # Calculate space optimization
    original_space = len(height) * 4  # Assuming 4 bytes per integer
    optimized_space = 2 * 4  # Only storing two pointers
    space_saved = original_space - optimized_space
    
    return {
        'max_area': max_area,
        'optimization': f'Space saved: {space_saved} bytes',
        'space_saved': space_saved
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([1, 2, 3, 4, 5], 6),
        ([5, 4, 3, 2, 1], 6),
        ([3, 3, 3, 3, 3], 12),
        ([], 0),
        ([1], 0),
        ([1, 2], 1),
        ([2, 1], 1),
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
    ]
    
    for i, (height, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: height={height}")
        
        # Test basic approach
        result = max_area(height.copy())
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = max_area_optimized(height.copy())
        print(f"Optimized result: {result_opt}")
        
        # Test brute force approach
        result_brute = max_area_with_brute_force(height.copy())
        print(f"Brute force result: {result_brute}")
        
        # Test with statistics
        stats = max_area_with_stats(height.copy())
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = max_area_with_validation(height.copy())
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = max_area_with_comparison(height.copy())
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = max_area_with_performance(height.copy())
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = max_area_with_debugging(height.copy())
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        analysis = max_area_with_analysis(height.copy())
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        optimization = max_area_with_optimization(height.copy())
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    max_area_verbose([1, 8, 6, 2, 5, 4, 8, 3, 7])
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large array for testing
    def generate_large_array(length):
        """Generate a large array for testing."""
        return [random.randint(1, 100) for _ in range(length)]
    
    large_height = generate_large_array(10000)
    
    # Test two-pointer approach
    start_time = time.time()
    for _ in range(100):
        max_area(large_height.copy())
    two_pointer_time = time.time() - start_time
    
    # Test brute force approach
    start_time = time.time()
    for _ in range(100):
        max_area_with_brute_force(large_height.copy())
    brute_force_time = time.time() - start_time
    
    print(f"Two-pointer approach: {two_pointer_time:.6f} seconds")
    print(f"Brute force approach: {brute_force_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Use two pointers at the start and end of the array")
    print("2. For each pair of lines, calculate the area of water that can be contained")
    print("3. Move the pointer pointing to the shorter line inward")
    print("4. Track the maximum area found")
    print("5. Return the maximum area")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(f"Array: {height}")
    print("\nSteps:")
    print("1. left=0, right=8: area = min(1,7) * 8 = 8")
    print("2. left=1, right=8: area = min(8,7) * 7 = 49")
    print("3. left=1, right=7: area = min(8,3) * 6 = 18")
    print("4. left=2, right=7: area = min(6,3) * 5 = 15")
    print("5. left=3, right=7: area = min(2,3) * 4 = 8")
    print("6. left=4, right=7: area = min(5,3) * 3 = 9")
    print("7. left=5, right=7: area = min(4,3) * 2 = 6")
    print("8. left=6, right=7: area = min(8,3) * 1 = 3")
    print("Maximum area: 49")
    
    # Test with different array patterns
    print("\nDifferent array patterns:")
    test_arrays = [
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [1, 1, 1, 1, 1],
        [1, 8, 6, 2, 5, 4, 8, 3, 7],
        [1, 2, 1, 2, 1],
    ]
    
    for arr in test_arrays:
        result = max_area(arr.copy())
        print(f"Array: {arr} -> Max area: {result}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],
        [1],
        [1, 2],
        [2, 1],
        [1, 1],
        [1, 2, 1],
        [2, 1, 2],
    ]
    
    for height in edge_cases:
        result = max_area(height.copy())
        print(f"Array: {height} -> Max area: {result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for height, _ in test_cases[:5]:
        stats = max_area_with_stats(height.copy())
        print(f"Array: {height}")
        print(f"  Max area: {stats['max_area']}")
        print(f"  Total pairs: {stats['total_pairs']}")
        print(f"  Areas calculated: {stats['areas_calculated']}")
        print(f"  Array length: {stats['array_length']}")
        print()
