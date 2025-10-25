"""
Problem 49: Valid Parentheses
Difficulty: Medium

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', 
determine if the input string is valid.

An input string is valid if:

1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Time Complexity: O(n) where n is the length of the string
Space Complexity: O(n) for the stack in the worst case
"""

def is_valid(s):
    """
    Check if the string has valid parentheses using stack.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        bool: True if parentheses are valid
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:  # Closing bracket
            if not stack or stack.pop() != mapping[char]:
                return False
        else:  # Opening bracket
            stack.append(char)
    
    return len(stack) == 0


def is_valid_optimized(s):
    """
    Check if the string has valid parentheses using optimized stack approach.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        bool: True if parentheses are valid
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:  # Closing bracket
            if not stack or stack.pop() != mapping[char]:
                return False
        else:  # Opening bracket
            stack.append(char)
    
    return len(stack) == 0


def is_valid_with_counter(s):
    """
    Check if the string has valid parentheses using counter approach.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        bool: True if parentheses are valid
    """
    if len(s) % 2 != 0:
        return False
    
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:  # Closing bracket
            if not stack or stack.pop() != mapping[char]:
                return False
        else:  # Opening bracket
            stack.append(char)
    
    return len(stack) == 0


def is_valid_verbose(s):
    """
    Check if the string has valid parentheses with detailed step-by-step explanation.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        bool: True if parentheses are valid
    """
    print(f"Checking if '{s}' has valid parentheses")
    print(f"String length: {len(s)}")
    
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    print(f"Mapping: {mapping}")
    
    for i, char in enumerate(s):
        print(f"\nStep {i + 1}: Processing character '{char}' at position {i}")
        print(f"  Current stack: {stack}")
        
        if char in mapping:  # Closing bracket
            print(f"  '{char}' is a closing bracket")
            if not stack:
                print(f"  Stack is empty, invalid parentheses")
                return False
            elif stack.pop() != mapping[char]:
                print(f"  Top of stack '{stack[-1] if stack else None}' doesn't match '{mapping[char]}', invalid parentheses")
                return False
            else:
                print(f"  Matched with '{mapping[char]}', removed from stack")
        else:  # Opening bracket
            print(f"  '{char}' is an opening bracket, added to stack")
            stack.append(char)
        
        print(f"  Updated stack: {stack}")
    
    result = len(stack) == 0
    print(f"\nFinal result: {result}")
    print(f"Stack is empty: {len(stack) == 0}")
    
    return result


def is_valid_with_stats(s):
    """
    Check if the string has valid parentheses and return statistics.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Statistics about the validation
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    opening_count = 0
    closing_count = 0
    matches = 0
    
    for char in s:
        if char in mapping:  # Closing bracket
            closing_count += 1
            if stack and stack.pop() == mapping[char]:
                matches += 1
        else:  # Opening bracket
            opening_count += 1
            stack.append(char)
    
    return {
        'is_valid': len(stack) == 0,
        'opening_count': opening_count,
        'closing_count': closing_count,
        'matches': matches,
        'stack_size': len(stack)
    }


def is_valid_with_validation(s):
    """
    Check if the string has valid parentheses with validation.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Detailed validation results
    """
    if not s:
        return {
            'is_valid': True,
            'is_input_valid': True,
            'reason': 'Empty string is valid'
        }
    
    if len(s) % 2 != 0:
        return {
            'is_valid': False,
            'is_input_valid': True,
            'reason': 'Odd length string cannot be valid'
        }
    
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:  # Closing bracket
            if not stack or stack.pop() != mapping[char]:
                return {
                    'is_valid': False,
                    'is_input_valid': True,
                    'reason': f'Mismatched brackets at character {char}'
                }
        else:  # Opening bracket
            stack.append(char)
    
    return {
        'is_valid': len(stack) == 0,
        'is_input_valid': True,
        'reason': f'Valid parentheses with {len(stack)} unmatched opening brackets' if stack else 'Valid parentheses'
    }


def is_valid_with_comparison(s):
    """
    Check if the string has valid parentheses and compare different approaches.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Comparison of different approaches
    """
    # Stack approach
    stack_result = is_valid(s)
    
    # Counter approach
    counter_result = is_valid_with_counter(s)
    
    return {
        'stack_approach': stack_result,
        'counter_approach': counter_result
    }


def is_valid_with_performance(s):
    """
    Check if the string has valid parentheses with performance metrics.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    start_time = time.time()
    operations = 0
    
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        operations += 1
        if char in mapping:  # Closing bracket
            if not stack or stack.pop() != mapping[char]:
                end_time = time.time()
                return {
                    'is_valid': False,
                    'execution_time': end_time - start_time,
                    'operations': operations
                }
        else:  # Opening bracket
            stack.append(char)
    
    end_time = time.time()
    
    return {
        'is_valid': len(stack) == 0,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def is_valid_with_debugging(s):
    """
    Check if the string has valid parentheses with debugging information.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Debugging information
    """
    if not s:
        return {
            'is_valid': True,
            'debug_info': 'Empty string',
            'steps': 0
        }
    
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    steps = 0
    
    for char in s:
        steps += 1
        if char in mapping:  # Closing bracket
            if not stack or stack.pop() != mapping[char]:
                return {
                    'is_valid': False,
                    'debug_info': f'Invalid at step {steps}',
                    'steps': steps
                }
        else:  # Opening bracket
            stack.append(char)
    
    return {
        'is_valid': len(stack) == 0,
        'debug_info': f'Processed {steps} characters',
        'steps': steps
    }


def is_valid_with_analysis(s):
    """
    Check if the string has valid parentheses and return analysis.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Analysis results
    """
    if not s:
        return {
            'is_valid': True,
            'analysis': 'Empty string is valid',
            'efficiency': 1.0
        }
    
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    total_operations = 0
    
    for char in s:
        total_operations += 1
        if char in mapping:  # Closing bracket
            if not stack or stack.pop() != mapping[char]:
                return {
                    'is_valid': False,
                    'analysis': f'Invalid parentheses at character {char}',
                    'efficiency': 0.0
                }
        else:  # Opening bracket
            stack.append(char)
    
    efficiency = 1.0 if len(stack) == 0 else 0.0
    
    return {
        'is_valid': len(stack) == 0,
        'analysis': f'Valid parentheses with {len(stack)} unmatched opening brackets' if stack else 'Valid parentheses',
        'efficiency': efficiency
    }


def is_valid_with_optimization(s):
    """
    Check if the string has valid parentheses with optimization techniques.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        dict: Optimization results
    """
    if not s:
        return {
            'is_valid': True,
            'optimization': 'Empty string',
            'space_saved': 0
        }
    
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:  # Closing bracket
            if not stack or stack.pop() != mapping[char]:
                return {
                    'is_valid': False,
                    'optimization': 'Early termination',
                    'space_saved': 0
                }
        else:  # Opening bracket
            stack.append(char)
    
    # Calculate space optimization
    original_space = len(s)
    optimized_space = len(stack)
    space_saved = original_space - optimized_space
    
    return {
        'is_valid': len(stack) == 0,
        'optimization': f'Space saved: {space_saved} characters',
        'space_saved': space_saved
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([)]", False),
        ("{[]}", True),
        ("", True),
        ("(", False),
        (")", False),
        ("((", False),
        ("))", False),
    ]
    
    for i, (s, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: s='{s}'")
        
        # Test basic approach
        result = is_valid(s)
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = is_valid_optimized(s)
        print(f"Optimized result: {result_opt}")
        
        # Test counter approach
        result_counter = is_valid_with_counter(s)
        print(f"Counter result: {result_counter}")
        
        # Test with statistics
        stats = is_valid_with_stats(s)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = is_valid_with_validation(s)
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = is_valid_with_comparison(s)
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = is_valid_with_performance(s)
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = is_valid_with_debugging(s)
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        analysis = is_valid_with_analysis(s)
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        optimization = is_valid_with_optimization(s)
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    is_valid_verbose("()")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    
    # Generate large string for testing
    def generate_large_string(length):
        """Generate a large string for testing."""
        return "()" * (length // 2)
    
    large_s = generate_large_string(10000)
    
    # Test stack approach
    start_time = time.time()
    for _ in range(1000):
        is_valid(large_s)
    stack_time = time.time() - start_time
    
    # Test counter approach
    start_time = time.time()
    for _ in range(1000):
        is_valid_with_counter(large_s)
    counter_time = time.time() - start_time
    
    print(f"Stack approach: {stack_time:.6f} seconds")
    print(f"Counter approach: {counter_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Use stack to track opening brackets")
    print("2. For each character in the string:")
    print("   - If it's an opening bracket, push to stack")
    print("   - If it's a closing bracket:")
    print("     - If stack is empty or top doesn't match, return false")
    print("     - Otherwise, pop from stack")
    print("3. Return true if stack is empty, false otherwise")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    s = "()"
    print(f"String: {s}")
    print("\nSteps:")
    print("1. Process '(': opening bracket, push to stack -> stack: ['(']")
    print("2. Process ')': closing bracket, check if stack is empty -> stack is not empty")
    print("3. Check if top of stack matches: '(' == '(' -> match, pop from stack -> stack: []")
    print("4. Stack is empty, return true")
    
    # Test with different string patterns
    print("\nDifferent string patterns:")
    test_strings = [
        "()",
        "()[]{}",
        "([)]",
        "{[]}",
        "((()))",
        "([{}])",
        "((())",
        "())",
        "([)]",
        "{[}]",
    ]
    
    for s in test_strings:
        result = is_valid(s)
        print(f"String: '{s}' -> Valid: {result}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        "",
        "(",
        ")",
        "((",
        "))",
        "()(",
        ")()",
        "((()))",
        "((())",
        "())",
    ]
    
    for s in edge_cases:
        result = is_valid(s)
        print(f"String: '{s}' -> Valid: {result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for s, _ in test_cases[:5]:
        stats = is_valid_with_stats(s)
        print(f"String: '{s}'")
        print(f"  Is valid: {stats['is_valid']}")
        print(f"  Opening count: {stats['opening_count']}")
        print(f"  Closing count: {stats['closing_count']}")
        print(f"  Matches: {stats['matches']}")
        print(f"  Stack size: {stats['stack_size']}")
        print()
