"""
Problem 84: Longest Valid Parentheses
Difficulty: Hard

Given a string containing just the characters '(' and ')', find the length of 
the longest valid (well-formed) parentheses substring.

Time Complexity: O(n) where n is the length of the string
Space Complexity: O(n) for the dp array
"""

def longest_valid_parentheses(s):
    """
    Find the length of the longest valid parentheses substring using DP.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        int: Length of the longest valid parentheses substring
    """
    if not s:
        return 0
    
    n = len(s)
    dp = [0] * n
    max_length = 0
    
    for i in range(1, n):
        if s[i] == ')':
            if s[i-1] == '(':
                # Immediate pair
                dp[i] = (dp[i-2] if i >= 2 else 0) + 2
            elif i - dp[i-1] > 0 and s[i - dp[i-1] - 1] == '(':
                # Nested pair
                dp[i] = dp[i-1] + (dp[i - dp[i-1] - 2] if i - dp[i-1] >= 2 else 0) + 2
            
            max_length = max(max_length, dp[i])
    
    return max_length


def longest_valid_parentheses_optimized(s):
    """
    Find the length of the longest valid parentheses substring using optimized DP.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        int: Length of the longest valid parentheses substring
    """
    if not s:
        return 0
    
    n = len(s)
    dp = [0] * n
    max_length = 0
    
    for i in range(1, n):
        if s[i] == ')':
            if s[i-1] == '(':
                # Immediate pair
                dp[i] = (dp[i-2] if i >= 2 else 0) + 2
            elif i - dp[i-1] > 0 and s[i - dp[i-1] - 1] == '(':
                # Nested pair
                dp[i] = dp[i-1] + (dp[i - dp[i-1] - 2] if i - dp[i-1] >= 2 else 0) + 2
            
            max_length = max(max_length, dp[i])
    
    return max_length


def longest_valid_parentheses_with_stack(s):
    """
    Find the length of the longest valid parentheses substring using stack.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        int: Length of the longest valid parentheses substring
    """
    if not s:
        return 0
    
    stack = [-1]  # Initialize with -1 to handle edge cases
    max_length = 0
    
    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        else:  # char == ')'
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                max_length = max(max_length, i - stack[-1])
    
    return max_length


def longest_valid_parentheses_verbose(s):
    """
    Find the length of the longest valid parentheses substring with detailed step-by-step explanation.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        int: Length of the longest valid parentheses substring
    """
    if not s:
        print("Empty string, returning 0")
        return 0
    
    print(f"Finding longest valid parentheses in '{s}'")
    print(f"String length: {len(s)}")
    
    n = len(s)
    dp = [0] * n
    max_length = 0
    
    print(f"Initialized dp array: {dp}")
    
    for i in range(1, n):
        print(f"\nStep {i}: Processing character '{s[i]}' at position {i}")
        print(f"  Current dp array: {dp}")
        
        if s[i] == ')':
            print(f"  Found closing parenthesis at position {i}")
            
            if s[i-1] == '(':
                print(f"  Previous character is '(', forming immediate pair")
                dp[i] = (dp[i-2] if i >= 2 else 0) + 2
                print(f"  dp[{i}] = {dp[i-2] if i >= 2 else 0} + 2 = {dp[i]}")
            elif i - dp[i-1] > 0 and s[i - dp[i-1] - 1] == '(':
                print(f"  Found nested pair at position {i - dp[i-1] - 1}")
                dp[i] = dp[i-1] + (dp[i - dp[i-1] - 2] if i - dp[i-1] >= 2 else 0) + 2
                print(f"  dp[{i}] = {dp[i-1]} + {dp[i - dp[i-1] - 2] if i - dp[i-1] >= 2 else 0} + 2 = {dp[i]}")
            else:
                print(f"  No valid pair found")
                dp[i] = 0
            
            max_length = max(max_length, dp[i])
            print(f"  Updated max_length to {max_length}")
        else:
            print(f"  Found opening parenthesis, cannot form valid pair ending here")
            dp[i] = 0
    
    print(f"\nFinal result: {max_length}")
    return max_length


def longest_valid_parentheses_with_stats(s):
    """
    Find the length of the longest valid parentheses substring and return statistics.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Statistics about the calculation
    """
    if not s:
        return {
            'max_length': 0,
            'total_characters': 0,
            'valid_pairs': 0,
            'dp_array': []
        }
    
    n = len(s)
    dp = [0] * n
    max_length = 0
    valid_pairs = 0
    
    for i in range(1, n):
        if s[i] == ')':
            if s[i-1] == '(':
                # Immediate pair
                dp[i] = (dp[i-2] if i >= 2 else 0) + 2
                valid_pairs += 1
            elif i - dp[i-1] > 0 and s[i - dp[i-1] - 1] == '(':
                # Nested pair
                dp[i] = dp[i-1] + (dp[i - dp[i-1] - 2] if i - dp[i-1] >= 2 else 0) + 2
                valid_pairs += 1
            
            max_length = max(max_length, dp[i])
    
    return {
        'max_length': max_length,
        'total_characters': n,
        'valid_pairs': valid_pairs,
        'dp_array': dp
    }


def longest_valid_parentheses_with_validation(s):
    """
    Find the length of the longest valid parentheses substring with validation.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Detailed validation results
    """
    if not s:
        return {
            'max_length': 0,
            'is_valid': True,
            'reason': 'Empty string'
        }
    
    if not all(c in '()' for c in s):
        return {
            'max_length': 0,
            'is_valid': False,
            'reason': 'String contains invalid characters'
        }
    
    n = len(s)
    dp = [0] * n
    max_length = 0
    
    for i in range(1, n):
        if s[i] == ')':
            if s[i-1] == '(':
                # Immediate pair
                dp[i] = (dp[i-2] if i >= 2 else 0) + 2
            elif i - dp[i-1] > 0 and s[i - dp[i-1] - 1] == '(':
                # Nested pair
                dp[i] = dp[i-1] + (dp[i - dp[i-1] - 2] if i - dp[i-1] >= 2 else 0) + 2
            
            max_length = max(max_length, dp[i])
    
    return {
        'max_length': max_length,
        'is_valid': True,
        'reason': f'Found longest valid parentheses of length {max_length}',
        'input': s
    }


def longest_valid_parentheses_with_comparison(s):
    """
    Find the length of the longest valid parentheses substring and compare different approaches.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Comparison of different approaches
    """
    # DP approach
    dp_result = longest_valid_parentheses(s)
    
    # Stack approach
    stack_result = longest_valid_parentheses_with_stack(s)
    
    return {
        'dp_approach': dp_result,
        'stack_approach': stack_result
    }


def longest_valid_parentheses_with_performance(s):
    """
    Find the length of the longest valid parentheses substring with performance metrics.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    start_time = time.time()
    operations = 0
    
    if not s:
        return {
            'max_length': 0,
            'execution_time': 0,
            'operations': 0
        }
    
    n = len(s)
    dp = [0] * n
    max_length = 0
    
    for i in range(1, n):
        operations += 1
        if s[i] == ')':
            if s[i-1] == '(':
                # Immediate pair
                dp[i] = (dp[i-2] if i >= 2 else 0) + 2
            elif i - dp[i-1] > 0 and s[i - dp[i-1] - 1] == '(':
                # Nested pair
                dp[i] = dp[i-1] + (dp[i - dp[i-1] - 2] if i - dp[i-1] >= 2 else 0) + 2
            
            max_length = max(max_length, dp[i])
            operations += 1
    
    end_time = time.time()
    
    return {
        'max_length': max_length,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def longest_valid_parentheses_with_debugging(s):
    """
    Find the length of the longest valid parentheses substring with debugging information.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Debugging information
    """
    if not s:
        return {
            'max_length': 0,
            'debug_info': 'Empty string',
            'steps': 0
        }
    
    n = len(s)
    dp = [0] * n
    max_length = 0
    steps = 0
    
    for i in range(1, n):
        steps += 1
        if s[i] == ')':
            if s[i-1] == '(':
                # Immediate pair
                dp[i] = (dp[i-2] if i >= 2 else 0) + 2
            elif i - dp[i-1] > 0 and s[i - dp[i-1] - 1] == '(':
                # Nested pair
                dp[i] = dp[i-1] + (dp[i - dp[i-1] - 2] if i - dp[i-1] >= 2 else 0) + 2
            
            max_length = max(max_length, dp[i])
    
    return {
        'max_length': max_length,
        'debug_info': f'Processed {steps} operations',
        'steps': steps
    }


def longest_valid_parentheses_with_analysis(s):
    """
    Find the length of the longest valid parentheses substring and return analysis.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Analysis results
    """
    if not s:
        return {
            'max_length': 0,
            'analysis': 'Empty string',
            'efficiency': 'N/A'
        }
    
    n = len(s)
    dp = [0] * n
    max_length = 0
    total_operations = 0
    
    for i in range(1, n):
        total_operations += 1
        if s[i] == ')':
            if s[i-1] == '(':
                # Immediate pair
                dp[i] = (dp[i-2] if i >= 2 else 0) + 2
            elif i - dp[i-1] > 0 and s[i - dp[i-1] - 1] == '(':
                # Nested pair
                dp[i] = dp[i-1] + (dp[i - dp[i-1] - 2] if i - dp[i-1] >= 2 else 0) + 2
            
            max_length = max(max_length, dp[i])
            total_operations += 1
    
    efficiency = max_length / total_operations if total_operations > 0 else 0.0
    
    return {
        'max_length': max_length,
        'analysis': f'Found longest valid parentheses of length {max_length} in {total_operations} operations',
        'efficiency': efficiency
    }


def longest_valid_parentheses_with_optimization(s):
    """
    Find the length of the longest valid parentheses substring with optimization techniques.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Optimization results
    """
    if not s:
        return {
            'max_length': 0,
            'optimization': 'Empty string',
            'space_saved': 0
        }
    
    n = len(s)
    dp = [0] * n
    max_length = 0
    
    for i in range(1, n):
        if s[i] == ')':
            if s[i-1] == '(':
                # Immediate pair
                dp[i] = (dp[i-2] if i >= 2 else 0) + 2
            elif i - dp[i-1] > 0 and s[i - dp[i-1] - 1] == '(':
                # Nested pair
                dp[i] = dp[i-1] + (dp[i - dp[i-1] - 2] if i - dp[i-1] >= 2 else 0) + 2
            
            max_length = max(max_length, dp[i])
    
    # Calculate space optimization
    original_space = n * 4  # Assuming 4 bytes per integer
    optimized_space = 1 * 4  # Only storing max_length
    space_saved = original_space - optimized_space
    
    return {
        'max_length': max_length,
        'optimization': f'Space saved: {space_saved} bytes',
        'space_saved': space_saved
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ("(()", 2),
        (")()())", 4),
        ("", 0),
        ("(((", 0),
        ("()()", 4),
        ("()(()", 2),
        ("(()())", 6),
        ("((()))", 6),
        ("()(())", 6),
        ("((()())", 6),
    ]
    
    for i, (s, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: s='{s}'")
        
        # Test basic approach
        result = longest_valid_parentheses(s)
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = longest_valid_parentheses_optimized(s)
        print(f"Optimized result: {result_opt}")
        
        # Test stack approach
        result_stack = longest_valid_parentheses_with_stack(s)
        print(f"Stack result: {result_stack}")
        
        # Test with statistics
        stats = longest_valid_parentheses_with_stats(s)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = longest_valid_parentheses_with_validation(s)
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = longest_valid_parentheses_with_comparison(s)
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = longest_valid_parentheses_with_performance(s)
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = longest_valid_parentheses_with_debugging(s)
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        analysis = longest_valid_parentheses_with_analysis(s)
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        optimization = longest_valid_parentheses_with_optimization(s)
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    longest_valid_parentheses_verbose("(()")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large string for testing
    def generate_large_string(length):
        """Generate a large string for testing."""
        return ''.join(random.choices('()', k=length))
    
    large_s = generate_large_string(10000)
    
    # Test DP approach
    start_time = time.time()
    for _ in range(100):
        longest_valid_parentheses(large_s)
    dp_time = time.time() - start_time
    
    # Test stack approach
    start_time = time.time()
    for _ in range(100):
        longest_valid_parentheses_with_stack(large_s)
    stack_time = time.time() - start_time
    
    print(f"DP approach: {dp_time:.6f} seconds")
    print(f"Stack approach: {stack_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Initialize dp array with zeros")
    print("2. For each position i:")
    print("   - If s[i] == '(', set dp[i] = 0")
    print("   - If s[i] == ')':")
    print("     - Check if it forms a valid pair with previous character")
    print("     - Update dp[i] accordingly")
    print("3. Return the maximum value in dp array")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    s = "(()"
    print(f"String: {s}")
    print("\nSteps:")
    print("1. i=1, s[1]='(', dp[1]=0")
    print("2. i=2, s[2]=')', s[1]='(' -> immediate pair")
    print("3. dp[2] = dp[0] + 2 = 0 + 2 = 2")
    print("4. max_length = max(0, 2) = 2")
    print("5. Result: 2")
    
    # Test with different string patterns
    print("\nDifferent string patterns:")
    test_strings = [
        "()",
        "()()",
        "(()())",
        "((()))",
        "()(())",
        "((()())",
        "()(()",
        "(((",
        ")))",
        "()()()",
    ]
    
    for s in test_strings:
        result = longest_valid_parentheses(s)
        print(f"String: '{s}' -> Length: {result}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        "",
        "(",
        ")",
        "()",
        "(((",
        ")))",
        "()(",
        ")()",
        "()()",
        "(()())",
    ]
    
    for s in edge_cases:
        result = longest_valid_parentheses(s)
        print(f"String: '{s}' -> Length: {result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for s, _ in test_cases[:5]:
        stats = longest_valid_parentheses_with_stats(s)
        print(f"String: '{s}'")
        print(f"  Max length: {stats['max_length']}")
        print(f"  Total characters: {stats['total_characters']}")
        print(f"  Valid pairs: {stats['valid_pairs']}")
        print(f"  DP array: {stats['dp_array']}")
        print()
