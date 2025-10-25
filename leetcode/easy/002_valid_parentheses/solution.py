"""
Problem 2: Valid Parentheses
Difficulty: Easy

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', 
determine if the input string is valid.

Time Complexity: O(n)
Space Complexity: O(n)
"""

def is_valid(s):
    """
    Check if the parentheses string is valid using a stack.
    
    Args:
        s: String containing only parentheses characters
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Stack to keep track of opening brackets
    stack = []
    
    # Mapping of closing to opening brackets
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:  # Closing bracket
            # If stack is empty or top doesn't match, invalid
            if not stack or stack.pop() != mapping[char]:
                return False
        else:  # Opening bracket
            stack.append(char)
    
    # Valid if stack is empty (all brackets matched)
    return len(stack) == 0


def is_valid_optimized(s):
    """
    Optimized version with early termination.
    
    Args:
        s: String containing only parentheses characters
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Early termination for odd length strings
    if len(s) % 2 != 0:
        return False
    
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    
    return len(stack) == 0


def is_valid_with_counter(s):
    """
    Alternative approach using counters (only works for single type of brackets).
    This is just for educational purposes - not applicable to mixed brackets.
    
    Args:
        s: String containing only parentheses characters
        
    Returns:
        bool: True if valid, False otherwise
    """
    # This approach only works for single type of brackets
    # Not suitable for mixed brackets like "([)]"
    if not s:
        return True
    
    # Check if string has only one type of brackets
    bracket_types = set(s)
    if len(bracket_types) > 2:  # More than one type of bracket
        return False
    
    # Simple counter approach for single type
    count = 0
    for char in s:
        if char in '([{':
            count += 1
        else:
            count -= 1
            if count < 0:
                return False
    
    return count == 0


# Test cases
if __name__ == "__main__":
    test_cases = [
        "()",           # True
        "()[]{}",       # True
        "(]",           # False
        "([)]",         # False
        "{[]}",         # True
        "",             # True (empty string)
        "((()))",       # True
        "((())",        # False
        "())",          # False
        "{[()]}",       # True
        "{[()]",        # False
    ]
    
    for i, test in enumerate(test_cases, 1):
        result = is_valid(test)
        print(f"Test {i}: '{test}' -> {result}")
    
    print("\n" + "="*50)
    print("Performance comparison:")
    
    # Large test case
    large_string = "()" * 5000 + "[]" * 5000 + "{}" * 5000
    
    import time
    
    # Test stack approach
    start_time = time.time()
    for _ in range(100):
        is_valid(large_string)
    stack_time = time.time() - start_time
    
    # Test optimized approach
    start_time = time.time()
    for _ in range(100):
        is_valid_optimized(large_string)
    optimized_time = time.time() - start_time
    
    print(f"Stack approach: {stack_time:.6f} seconds")
    print(f"Optimized approach: {optimized_time:.6f} seconds")
    
    # Edge cases
    print("\n" + "="*50)
    print("Edge cases:")
    edge_cases = [
        "(",      # Single opening
        ")",      # Single closing
        "(((",    # Multiple openings
        ")))",    # Multiple closings
        "()()()", # Multiple valid pairs
    ]
    
    for case in edge_cases:
        result = is_valid(case)
        print(f"'{case}' -> {result}")
