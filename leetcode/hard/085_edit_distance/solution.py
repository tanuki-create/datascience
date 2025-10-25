"""
Problem 85: Edit Distance
Difficulty: Hard

Given two strings word1 and word2, return the minimum number of operations 
required to convert word1 to word2.

You have the following three operations permitted on a word:

1. Insert a character
2. Delete a character
3. Replace a character

Time Complexity: O(m * n) where m and n are the lengths of the strings
Space Complexity: O(m * n) for the dp array
"""

def min_distance(word1, word2):
    """
    Find the minimum number of operations to convert word1 to word2 using DP.
    
    Args:
        word1: First string
        word2: Second string
        
    Returns:
        int: Minimum number of operations
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill the dp array
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    return dp[m][n]


def min_distance_optimized(word1, word2):
    """
    Find the minimum number of operations using optimized DP with space optimization.
    
    Args:
        word1: First string
        word2: Second string
        
    Returns:
        int: Minimum number of operations
    """
    m, n = len(word1), len(word2)
    
    # Use only two rows for space optimization
    prev = [j for j in range(n + 1)]
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                curr[j] = prev[j-1]
            else:
                curr[j] = 1 + min(prev[j], curr[j-1], prev[j-1])
        
        prev, curr = curr, prev
    
    return prev[n]


def min_distance_verbose(word1, word2):
    """
    Find the minimum number of operations with detailed step-by-step explanation.
    
    Args:
        word1: First string
        word2: Second string
        
    Returns:
        int: Minimum number of operations
    """
    print(f"Finding minimum edit distance between '{word1}' and '{word2}'")
    print(f"String lengths: {len(word1)}, {len(word2)}")
    
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    print(f"Initialized base cases:")
    print(f"  dp[i][0] = i for all i")
    print(f"  dp[0][j] = j for all j")
    print(f"  DP table:")
    for row in dp:
        print(f"    {row}")
    
    # Fill the dp array
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            print(f"\nStep ({i}, {j}): Processing word1[{i-1}]='{word1[i-1]}' and word2[{j-1}]='{word2[j-1]}'")
            
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
                print(f"  Characters match, dp[{i}][{j}] = dp[{i-1}][{j-1}] = {dp[i][j]}")
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                print(f"  Characters don't match, dp[{i}][{j}] = 1 + min({dp[i-1][j]}, {dp[i][j-1]}, {dp[i-1][j-1]}) = {dp[i][j]}")
            
            print(f"  Current DP table:")
            for row in dp:
                print(f"    {row}")
    
    print(f"\nFinal result: {dp[m][n]}")
    return dp[m][n]


def min_distance_with_stats(word1, word2):
    """
    Find the minimum number of operations and return statistics.
    
    Args:
        word1: First string
        word2: Second string
        
    Returns:
        dict: Statistics about the calculation
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    operations = 0
    matches = 0
    
    # Fill the dp array
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            operations += 1
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
                matches += 1
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    return {
        'min_distance': dp[m][n],
        'total_operations': operations,
        'matches': matches,
        'word1_length': m,
        'word2_length': n
    }


def min_distance_with_validation(word1, word2):
    """
    Find the minimum number of operations with validation.
    
    Args:
        word1: First string
        word2: Second string
        
    Returns:
        dict: Detailed validation results
    """
    if not word1 and not word2:
        return {
            'min_distance': 0,
            'is_valid': True,
            'reason': 'Both strings are empty'
        }
    
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill the dp array
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    return {
        'min_distance': dp[m][n],
        'is_valid': True,
        'reason': f'Successfully calculated minimum distance: {dp[m][n]}',
        'word1': word1,
        'word2': word2
    }


def min_distance_with_comparison(word1, word2):
    """
    Find the minimum number of operations and compare different approaches.
    
    Args:
        word1: First string
        word2: Second string
        
    Returns:
        dict: Comparison of different approaches
    """
    # Standard DP approach
    dp_result = min_distance(word1, word2)
    
    # Optimized DP approach
    optimized_result = min_distance_optimized(word1, word2)
    
    return {
        'standard_dp': dp_result,
        'optimized_dp': optimized_result
    }


def min_distance_with_performance(word1, word2):
    """
    Find the minimum number of operations with performance metrics.
    
    Args:
        word1: First string
        word2: Second string
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    start_time = time.time()
    operations = 0
    
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
        operations += 1
    for j in range(n + 1):
        dp[0][j] = j
        operations += 1
    
    # Fill the dp array
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            operations += 1
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
            operations += 1
    
    end_time = time.time()
    
    return {
        'min_distance': dp[m][n],
        'execution_time': end_time - start_time,
        'operations': operations
    }


def min_distance_with_debugging(word1, word2):
    """
    Find the minimum number of operations with debugging information.
    
    Args:
        word1: First string
        word2: Second string
        
    Returns:
        dict: Debugging information
    """
    if not word1 and not word2:
        return {
            'min_distance': 0,
            'debug_info': 'Both strings are empty',
            'steps': 0
        }
    
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    steps = 0
    # Fill the dp array
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            steps += 1
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    return {
        'min_distance': dp[m][n],
        'debug_info': f'Processed {steps} operations',
        'steps': steps
    }


def min_distance_with_analysis(word1, word2):
    """
    Find the minimum number of operations and return analysis.
    
    Args:
        word1: First string
        word2: Second string
        
    Returns:
        dict: Analysis results
    """
    if not word1 and not word2:
        return {
            'min_distance': 0,
            'analysis': 'Both strings are empty',
            'efficiency': 1.0
        }
    
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    total_operations = 0
    # Fill the dp array
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            total_operations += 1
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    efficiency = dp[m][n] / total_operations if total_operations > 0 else 0.0
    
    return {
        'min_distance': dp[m][n],
        'analysis': f'Found minimum distance {dp[m][n]} in {total_operations} operations',
        'efficiency': efficiency
    }


def min_distance_with_optimization(word1, word2):
    """
    Find the minimum number of operations with optimization techniques.
    
    Args:
        word1: First string
        word2: Second string
        
    Returns:
        dict: Optimization results
    """
    if not word1 and not word2:
        return {
            'min_distance': 0,
            'optimization': 'Both strings are empty',
            'space_saved': 0
        }
    
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill the dp array
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    # Calculate space optimization
    original_space = (m + 1) * (n + 1) * 4  # Assuming 4 bytes per integer
    optimized_space = 2 * (n + 1) * 4  # Only storing two rows
    space_saved = original_space - optimized_space
    
    return {
        'min_distance': dp[m][n],
        'optimization': f'Space saved: {space_saved} bytes',
        'space_saved': space_saved
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ("horse", "ros", 3),
        ("intention", "execution", 5),
        ("abc", "abc", 0),
        ("", "", 0),
        ("abc", "", 3),
        ("", "abc", 3),
        ("abc", "def", 3),
        ("abc", "ab", 1),
        ("ab", "abc", 1),
        ("kitten", "sitting", 3),
    ]
    
    for i, (word1, word2, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: word1='{word1}', word2='{word2}'")
        
        # Test basic approach
        result = min_distance(word1, word2)
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = min_distance_optimized(word1, word2)
        print(f"Optimized result: {result_opt}")
        
        # Test with statistics
        stats = min_distance_with_stats(word1, word2)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = min_distance_with_validation(word1, word2)
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = min_distance_with_comparison(word1, word2)
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = min_distance_with_performance(word1, word2)
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = min_distance_with_debugging(word1, word2)
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        analysis = min_distance_with_analysis(word1, word2)
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        optimization = min_distance_with_optimization(word1, word2)
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    min_distance_verbose("horse", "ros")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    import string
    
    # Generate large strings for testing
    def generate_large_string(length):
        """Generate a large string for testing."""
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    large_word1 = generate_large_string(100)
    large_word2 = generate_large_string(100)
    
    # Test standard DP approach
    start_time = time.time()
    for _ in range(100):
        min_distance(large_word1, large_word2)
    standard_time = time.time() - start_time
    
    # Test optimized DP approach
    start_time = time.time()
    for _ in range(100):
        min_distance_optimized(large_word1, large_word2)
    optimized_time = time.time() - start_time
    
    print(f"Standard DP approach: {standard_time:.6f} seconds")
    print(f"Optimized DP approach: {optimized_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Create a 2D dp array of size (m+1) x (n+1)")
    print("2. Initialize base cases")
    print("3. Fill the dp array using the state transition")
    print("4. Return dp[m][n]")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    word1 = "horse"
    word2 = "ros"
    print(f"word1: {word1}")
    print(f"word2: {word2}")
    print("\nSteps:")
    print("1. Initialize base cases: dp[i][0] = i, dp[0][j] = j")
    print("2. Fill DP table:")
    print("   - dp[1][1]: 'h' vs 'r' -> 1 + min(1, 1, 0) = 1")
    print("   - dp[1][2]: 'h' vs 'o' -> 1 + min(1, 2, 1) = 2")
    print("   - dp[1][3]: 'h' vs 's' -> 1 + min(1, 3, 2) = 2")
    print("   - dp[2][1]: 'o' vs 'r' -> 1 + min(2, 1, 1) = 2")
    print("   - dp[2][2]: 'o' vs 'o' -> dp[1][1] = 1")
    print("   - dp[2][3]: 'o' vs 's' -> 1 + min(2, 2, 1) = 2")
    print("   - dp[3][1]: 'r' vs 'r' -> dp[2][0] = 2")
    print("   - dp[3][2]: 'r' vs 'o' -> 1 + min(2, 3, 2) = 3")
    print("   - dp[3][3]: 'r' vs 's' -> 1 + min(2, 3, 2) = 3")
    print("   - dp[4][1]: 's' vs 'r' -> 1 + min(3, 2, 2) = 3")
    print("   - dp[4][2]: 's' vs 'o' -> 1 + min(3, 3, 3) = 4")
    print("   - dp[4][3]: 's' vs 's' -> dp[3][2] = 3")
    print("   - dp[5][1]: 'e' vs 'r' -> 1 + min(4, 3, 3) = 4")
    print("   - dp[5][2]: 'e' vs 'o' -> 1 + min(4, 4, 3) = 4")
    print("   - dp[5][3]: 'e' vs 's' -> 1 + min(4, 4, 3) = 4")
    print("3. Result: dp[5][3] = 4")
    
    # Test with different string patterns
    print("\nDifferent string patterns:")
    test_strings = [
        ("abc", "def"),
        ("abc", "ab"),
        ("ab", "abc"),
        ("abc", "abc"),
        ("", "abc"),
        ("abc", ""),
        ("", ""),
        ("a", "b"),
        ("ab", "cd"),
        ("abc", "abcd"),
    ]
    
    for word1, word2 in test_strings:
        result = min_distance(word1, word2)
        print(f"word1: '{word1}', word2: '{word2}' -> Distance: {result}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        ("", ""),
        ("a", ""),
        ("", "a"),
        ("a", "a"),
        ("a", "b"),
        ("ab", "a"),
        ("a", "ab"),
        ("ab", "ab"),
    ]
    
    for word1, word2 in edge_cases:
        result = min_distance(word1, word2)
        print(f"word1: '{word1}', word2: '{word2}' -> Distance: {result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for word1, word2, _ in test_cases[:5]:
        stats = min_distance_with_stats(word1, word2)
        print(f"word1: '{word1}', word2: '{word2}'")
        print(f"  Min distance: {stats['min_distance']}")
        print(f"  Total operations: {stats['total_operations']}")
        print(f"  Matches: {stats['matches']}")
        print(f"  Word1 length: {stats['word1_length']}")
        print(f"  Word2 length: {stats['word2_length']}")
        print()
