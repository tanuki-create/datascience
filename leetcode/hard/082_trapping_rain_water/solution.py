"""
Problem 82: Trapping Rain Water
Difficulty: Hard

Given n non-negative integers representing an elevation map where the width of 
each bar is 1, compute how much water it can trap after raining.

Time Complexity: O(n) where n is the length of the array
Space Complexity: O(1) for storing variables
"""

def trap(height):
    """
    Calculate trapped rainwater using two-pointer technique.
    
    Args:
        height: List of heights
        
    Returns:
        int: Total amount of water trapped
    """
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += max(0, left_max - height[left])
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += max(0, right_max - height[right])
    
    return water


def trap_optimized(height):
    """
    Calculate trapped rainwater using optimized two-pointer technique.
    
    Args:
        height: List of heights
        
    Returns:
        int: Total amount of water trapped
    """
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += max(0, left_max - height[left])
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += max(0, right_max - height[right])
    
    return water


def trap_with_arrays(height):
    """
    Calculate trapped rainwater using arrays to store maximums.
    
    Args:
        height: List of heights
        
    Returns:
        int: Total amount of water trapped
    """
    if not height:
        return 0
    
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n
    
    # Calculate left maximums
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])
    
    # Calculate right maximums
    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])
    
    # Calculate water trapped
    water = 0
    for i in range(n):
        water += max(0, min(left_max[i], right_max[i]) - height[i])
    
    return water


def trap_verbose(height):
    """
    Calculate trapped rainwater with detailed step-by-step explanation.
    
    Args:
        height: List of heights
        
    Returns:
        int: Total amount of water trapped
    """
    if not height:
        print("Empty array, returning 0")
        return 0
    
    print(f"Calculating trapped rainwater for {height}")
    print(f"Array length: {len(height)}")
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    
    step = 1
    while left < right:
        print(f"\nStep {step}:")
        print(f"  left={left}, right={right}")
        print(f"  left_max={left_max}, right_max={right_max}")
        print(f"  height[left]={height[left]}, height[right]={height[right]}")
        
        if left_max < right_max:
            left += 1
            print(f"  left_max < right_max, moving left pointer to {left}")
            left_max = max(left_max, height[left])
            print(f"  Updated left_max to {left_max}")
            water_at_left = max(0, left_max - height[left])
            water += water_at_left
            print(f"  Water trapped at position {left}: {water_at_left}")
            print(f"  Total water so far: {water}")
        else:
            right -= 1
            print(f"  left_max >= right_max, moving right pointer to {right}")
            right_max = max(right_max, height[right])
            print(f"  Updated right_max to {right_max}")
            water_at_right = max(0, right_max - height[right])
            water += water_at_right
            print(f"  Water trapped at position {right}: {water_at_right}")
            print(f"  Total water so far: {water}")
        
        step += 1
    
    print(f"\nFinal result: {water}")
    return water


def trap_with_stats(height):
    """
    Calculate trapped rainwater and return statistics.
    
    Args:
        height: List of heights
        
    Returns:
        dict: Statistics about the calculation
    """
    if not height:
        return {
            'water': 0,
            'total_positions': 0,
            'water_positions': 0,
            'max_height': 0
        }
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    water_positions = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water_at_left = max(0, left_max - height[left])
            water += water_at_left
            if water_at_left > 0:
                water_positions += 1
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water_at_right = max(0, right_max - height[right])
            water += water_at_right
            if water_at_right > 0:
                water_positions += 1
    
    return {
        'water': water,
        'total_positions': len(height),
        'water_positions': water_positions,
        'max_height': max(height)
    }


def trap_with_validation(height):
    """
    Calculate trapped rainwater with validation.
    
    Args:
        height: List of heights
        
    Returns:
        dict: Detailed validation results
    """
    if not height:
        return {
            'water': 0,
            'is_valid': True,
            'reason': 'Empty array'
        }
    
    if len(height) < 3:
        return {
            'water': 0,
            'is_valid': True,
            'reason': f'Array too short: {len(height)} < 3'
        }
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += max(0, left_max - height[left])
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += max(0, right_max - height[right])
    
    return {
        'water': water,
        'is_valid': True,
        'reason': f'Successfully calculated {water} units of water',
        'input': height
    }


def trap_with_comparison(height):
    """
    Calculate trapped rainwater and compare different approaches.
    
    Args:
        height: List of heights
        
    Returns:
        dict: Comparison of different approaches
    """
    # Two-pointer approach
    two_pointer_result = trap(height)
    
    # Array approach
    array_result = trap_with_arrays(height)
    
    return {
        'two_pointer': two_pointer_result,
        'array': array_result
    }


def trap_with_performance(height):
    """
    Calculate trapped rainwater with performance metrics.
    
    Args:
        height: List of heights
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    start_time = time.time()
    operations = 0
    
    if not height:
        return {
            'water': 0,
            'execution_time': 0,
            'operations': 0
        }
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    
    while left < right:
        operations += 1
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += max(0, left_max - height[left])
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += max(0, right_max - height[right])
    
    end_time = time.time()
    
    return {
        'water': water,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def trap_with_debugging(height):
    """
    Calculate trapped rainwater with debugging information.
    
    Args:
        height: List of heights
        
    Returns:
        dict: Debugging information
    """
    if not height:
        return {
            'water': 0,
            'debug_info': 'Empty array',
            'steps': 0
        }
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    steps = 0
    
    while left < right:
        steps += 1
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += max(0, left_max - height[left])
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += max(0, right_max - height[right])
    
    return {
        'water': water,
        'debug_info': f'Processed {steps} operations',
        'steps': steps
    }


def trap_with_analysis(height):
    """
    Calculate trapped rainwater and return analysis.
    
    Args:
        height: List of heights
        
    Returns:
        dict: Analysis results
    """
    if not height:
        return {
            'water': 0,
            'analysis': 'Empty array',
            'efficiency': 'N/A'
        }
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    total_operations = 0
    
    while left < right:
        total_operations += 1
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += max(0, left_max - height[left])
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += max(0, right_max - height[right])
    
    efficiency = water / total_operations if total_operations > 0 else 0.0
    
    return {
        'water': water,
        'analysis': f'Trapped {water} units of water in {total_operations} operations',
        'efficiency': efficiency
    }


def trap_with_optimization(height):
    """
    Calculate trapped rainwater with optimization techniques.
    
    Args:
        height: List of heights
        
    Returns:
        dict: Optimization results
    """
    if not height:
        return {
            'water': 0,
            'optimization': 'Empty array',
            'space_saved': 0
        }
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += max(0, left_max - height[left])
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += max(0, right_max - height[right])
    
    # Calculate space optimization
    original_space = len(height) * 4  # Assuming 4 bytes per integer
    optimized_space = 2 * 4  # Only storing two pointers
    space_saved = original_space - optimized_space
    
    return {
        'water': water,
        'optimization': f'Space saved: {space_saved} bytes',
        'space_saved': space_saved
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([4, 2, 0, 3, 2, 5], 9),
        ([1, 2, 3, 4, 5], 0),
        ([5], 0),
        ([], 0),
        ([3, 0, 2, 0, 4], 7),
        ([0, 1, 0, 2, 0, 3], 3),
        ([3, 2, 1, 0, 1, 2, 3], 9),
        ([1, 0, 1], 1),
        ([0, 1, 0, 1, 0], 1),
    ]
    
    for i, (height, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: height={height}")
        
        # Test basic approach
        result = trap(height.copy())
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = trap_optimized(height.copy())
        print(f"Optimized result: {result_opt}")
        
        # Test array approach
        result_array = trap_with_arrays(height.copy())
        print(f"Array result: {result_array}")
        
        # Test with statistics
        stats = trap_with_stats(height.copy())
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = trap_with_validation(height.copy())
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = trap_with_comparison(height.copy())
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = trap_with_performance(height.copy())
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = trap_with_debugging(height.copy())
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        analysis = trap_with_analysis(height.copy())
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        optimization = trap_with_optimization(height.copy())
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    trap_verbose([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large array for testing
    def generate_large_array(length):
        """Generate a large array for testing."""
        return [random.randint(0, 100) for _ in range(length)]
    
    large_height = generate_large_array(10000)
    
    # Test two-pointer approach
    start_time = time.time()
    for _ in range(100):
        trap(large_height.copy())
    two_pointer_time = time.time() - start_time
    
    # Test array approach
    start_time = time.time()
    for _ in range(100):
        trap_with_arrays(large_height.copy())
    array_time = time.time() - start_time
    
    print(f"Two-pointer approach: {two_pointer_time:.6f} seconds")
    print(f"Array approach: {array_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Use two pointers at the start and end of the array")
    print("2. Keep track of the maximum height seen from left and right")
    print("3. For each position, the water trapped is the minimum of left and right maximums minus the current height")
    print("4. Move the pointer pointing to the smaller maximum")
    print("5. Return total water trapped")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(f"Height: {height}")
    print("\nSteps:")
    print("1. left=0, right=11: left_max=0, right_max=0")
    print("2. left_max < right_max, move left: left=1, left_max=1")
    print("3. left_max < right_max, move left: left=2, left_max=1")
    print("4. left_max < right_max, move left: left=3, left_max=2")
    print("5. left_max < right_max, move left: left=4, left_max=2")
    print("6. left_max < right_max, move left: left=5, left_max=2")
    print("7. left_max < right_max, move left: left=6, left_max=2")
    print("8. left_max < right_max, move left: left=7, left_max=3")
    print("9. left_max >= right_max, move right: right=10, right_max=2")
    print("10. left_max >= right_max, move right: right=9, right_max=2")
    print("11. left_max >= right_max, move right: right=8, right_max=2")
    print("12. left_max >= right_max, move right: right=7, right_max=3")
    print("Total water trapped: 6")
    
    # Test with different array patterns
    print("\nDifferent array patterns:")
    test_arrays = [
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [1, 0, 1],
        [0, 1, 0, 1, 0],
        [3, 0, 2, 0, 4],
    ]
    
    for arr in test_arrays:
        result = trap(arr.copy())
        print(f"Array: {arr} -> Water trapped: {result}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],
        [1],
        [1, 2],
        [2, 1],
        [1, 0, 1],
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0],
    ]
    
    for height in edge_cases:
        result = trap(height.copy())
        print(f"Array: {height} -> Water trapped: {result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for height, _ in test_cases[:5]:
        stats = trap_with_stats(height.copy())
        print(f"Array: {height}")
        print(f"  Water trapped: {stats['water']}")
        print(f"  Total positions: {stats['total_positions']}")
        print(f"  Water positions: {stats['water_positions']}")
        print(f"  Max height: {stats['max_height']}")
        print()
