"""
Problem 43: Longest Substring Without Repeating Characters
Difficulty: Medium

Given a string s, find the length of the longest substring without repeating 
characters.

Time Complexity: O(n) where n is the length of the string
Space Complexity: O(min(m, n)) where m is the size of the character set
"""

def length_of_longest_substring(s):
    """
    Find the length of the longest substring without repeating characters.
    
    Args:
        s: Input string
        
    Returns:
        int: Length of the longest substring without repeating characters
    """
    if not s:
        return 0
    
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # If character is already in set, remove characters from left
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character to set
        char_set.add(s[right])
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length


def length_of_longest_substring_optimized(s):
    """
    Find the length of the longest substring using optimized sliding window.
    
    Args:
        s: Input string
        
    Returns:
        int: Length of the longest substring without repeating characters
    """
    if not s:
        return 0
    
    char_map = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # If character is already in map, update left pointer
        if s[right] in char_map and char_map[s[right]] >= left:
            left = char_map[s[right]] + 1
        
        # Update character position
        char_map[s[right]] = right
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length


def length_of_longest_substring_with_hashmap(s):
    """
    Find the length of the longest substring using hashmap approach.
    
    Args:
        s: Input string
        
    Returns:
        int: Length of the longest substring without repeating characters
    """
    if not s:
        return 0
    
    char_map = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # If character is already in map, update left pointer
        if s[right] in char_map and char_map[s[right]] >= left:
            left = char_map[s[right]] + 1
        
        # Update character position
        char_map[s[right]] = right
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length


def length_of_longest_substring_verbose(s):
    """
    Find the length of the longest substring with detailed step-by-step explanation.
    
    Args:
        s: Input string
        
    Returns:
        int: Length of the longest substring without repeating characters
    """
    if not s:
        print("Empty string, returning 0")
        return 0
    
    print(f"Finding longest substring without repeating characters in '{s}'")
    print(f"String length: {len(s)}")
    
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        print(f"\nStep {right + 1}: Processing character '{s[right]}' at position {right}")
        print(f"  Current window: '{s[left:right+1]}'")
        print(f"  Character set: {char_set}")
        
        # If character is already in set, remove characters from left
        while s[right] in char_set:
            print(f"    Character '{s[right]}' already in set, removing '{s[left]}' from left")
            char_set.remove(s[left])
            left += 1
            print(f"    Updated window: '{s[left:right+1]}'")
            print(f"    Updated character set: {char_set}")
        
        # Add current character to set
        char_set.add(s[right])
        print(f"  Added '{s[right]}' to set: {char_set}")
        
        # Update maximum length
        current_length = right - left + 1
        max_length = max(max_length, current_length)
        print(f"  Current length: {current_length}, Max length: {max_length}")
    
    print(f"\nFinal result: {max_length}")
    return max_length


def length_of_longest_substring_with_stats(s):
    """
    Find the length of the longest substring and return statistics.
    
    Args:
        s: Input string
        
    Returns:
        dict: Statistics about the search
    """
    if not s:
        return {
            'max_length': 0,
            'total_characters': 0,
            'unique_characters': 0,
            'window_changes': 0
        }
    
    char_set = set()
    left = 0
    max_length = 0
    window_changes = 0
    
    for right in range(len(s)):
        # If character is already in set, remove characters from left
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
            window_changes += 1
        
        # Add current character to set
        char_set.add(s[right])
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return {
        'max_length': max_length,
        'total_characters': len(s),
        'unique_characters': len(set(s)),
        'window_changes': window_changes
    }


def length_of_longest_substring_with_validation(s):
    """
    Find the length of the longest substring with validation.
    
    Args:
        s: Input string
        
    Returns:
        dict: Detailed validation results
    """
    if not s:
        return {
            'max_length': 0,
            'is_valid': True,
            'reason': 'Empty string',
            'substring': ''
        }
    
    char_set = set()
    left = 0
    max_length = 0
    max_start = 0
    max_end = 0
    
    for right in range(len(s)):
        # If character is already in set, remove characters from left
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character to set
        char_set.add(s[right])
        
        # Update maximum length
        current_length = right - left + 1
        if current_length > max_length:
            max_length = current_length
            max_start = left
            max_end = right
    
    return {
        'max_length': max_length,
        'is_valid': True,
        'reason': f'Found longest substring of length {max_length}',
        'substring': s[max_start:max_end + 1]
    }


def length_of_longest_substring_with_comparison(s):
    """
    Find the length of the longest substring and compare different approaches.
    
    Args:
        s: Input string
        
    Returns:
        dict: Comparison of different approaches
    """
    # Set approach
    set_result = length_of_longest_substring(s)
    
    # Hashmap approach
    hashmap_result = length_of_longest_substring_with_hashmap(s)
    
    return {
        'set_approach': set_result,
        'hashmap_approach': hashmap_result
    }


def length_of_longest_substring_with_performance(s):
    """
    Find the length of the longest substring with performance metrics.
    
    Args:
        s: Input string
        
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
    
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # If character is already in set, remove characters from left
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
            operations += 1
        
        # Add current character to set
        char_set.add(s[right])
        operations += 1
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
        operations += 1
    
    end_time = time.time()
    
    return {
        'max_length': max_length,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def length_of_longest_substring_with_debugging(s):
    """
    Find the length of the longest substring with debugging information.
    
    Args:
        s: Input string
        
    Returns:
        dict: Debugging information
    """
    if not s:
        return {
            'max_length': 0,
            'debug_info': 'Empty string',
            'steps': 0
        }
    
    char_set = set()
    left = 0
    max_length = 0
    steps = 0
    
    for right in range(len(s)):
        # If character is already in set, remove characters from left
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
            steps += 1
        
        # Add current character to set
        char_set.add(s[right])
        steps += 1
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return {
        'max_length': max_length,
        'debug_info': f'Processed {steps} operations',
        'steps': steps
    }


def length_of_longest_substring_with_analysis(s):
    """
    Find the length of the longest substring and return analysis.
    
    Args:
        s: Input string
        
    Returns:
        dict: Analysis results
    """
    if not s:
        return {
            'max_length': 0,
            'analysis': 'Empty string',
            'efficiency': 'N/A'
        }
    
    char_set = set()
    left = 0
    max_length = 0
    total_operations = 0
    
    for right in range(len(s)):
        # If character is already in set, remove characters from left
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
            total_operations += 1
        
        # Add current character to set
        char_set.add(s[right])
        total_operations += 1
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    efficiency = max_length / len(s) if len(s) > 0 else 0.0
    
    return {
        'max_length': max_length,
        'analysis': f'Found longest substring of length {max_length} in {total_operations} operations',
        'efficiency': efficiency
    }


def length_of_longest_substring_with_optimization(s):
    """
    Find the length of the longest substring with optimization techniques.
    
    Args:
        s: Input string
        
    Returns:
        dict: Optimization results
    """
    if not s:
        return {
            'max_length': 0,
            'optimization': 'Empty string',
            'space_saved': 0
        }
    
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # If character is already in set, remove characters from left
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character to set
        char_set.add(s[right])
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    # Calculate space optimization
    original_space = len(s)
    optimized_space = max_length
    space_saved = original_space - optimized_space
    
    return {
        'max_length': max_length,
        'optimization': f'Space saved: {space_saved} characters',
        'space_saved': space_saved
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ("abcabcbb", 3),
        ("bbbbb", 1),
        ("pwwkew", 3),
        ("", 0),
        ("a", 1),
        ("abcdef", 6),
        ("aab", 2),
        ("dvdf", 3),
        ("tmmzuxt", 5),
        ("abcabcbb", 3),
    ]
    
    for i, (s, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: s='{s}'")
        
        # Test basic approach
        result = length_of_longest_substring(s)
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = length_of_longest_substring_optimized(s)
        print(f"Optimized result: {result_opt}")
        
        # Test hashmap approach
        result_hash = length_of_longest_substring_with_hashmap(s)
        print(f"Hashmap result: {result_hash}")
        
        # Test with statistics
        stats = length_of_longest_substring_with_stats(s)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = length_of_longest_substring_with_validation(s)
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = length_of_longest_substring_with_comparison(s)
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = length_of_longest_substring_with_performance(s)
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = length_of_longest_substring_with_debugging(s)
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        analysis = length_of_longest_substring_with_analysis(s)
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        optimization = length_of_longest_substring_with_optimization(s)
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    length_of_longest_substring_verbose("abcabcbb")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    import string
    
    # Generate large string for testing
    def generate_large_string(length):
        """Generate a large string for testing."""
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    large_s = generate_large_string(10000)
    
    # Test set approach
    start_time = time.time()
    for _ in range(100):
        length_of_longest_substring(large_s)
    set_time = time.time() - start_time
    
    # Test hashmap approach
    start_time = time.time()
    for _ in range(100):
        length_of_longest_substring_with_hashmap(large_s)
    hashmap_time = time.time() - start_time
    
    print(f"Set approach: {set_time:.6f} seconds")
    print(f"Hashmap approach: {hashmap_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Use sliding window technique with two pointers")
    print("2. Use hash set to track characters in current window")
    print("3. For each character:")
    print("   - If character is not in set, add it and expand window")
    print("   - If character is in set, remove characters from left until duplicate is removed")
    print("4. Track maximum length found")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    s = "abcabcbb"
    print(f"String: {s}")
    print("\nSteps:")
    print("1. Window: 'a', length: 1")
    print("2. Window: 'ab', length: 2")
    print("3. Window: 'abc', length: 3")
    print("4. Window: 'bca', length: 3 (removed 'a' from left)")
    print("5. Window: 'cab', length: 3 (removed 'b' from left)")
    print("6. Window: 'abc', length: 3 (removed 'c' from left)")
    print("7. Window: 'cb', length: 2 (removed 'a' from left)")
    print("8. Window: 'b', length: 1 (removed 'c' from left)")
    print("Maximum length: 3")
    
    # Test with different string patterns
    print("\nDifferent string patterns:")
    test_strings = [
        "abcdef",
        "aabbcc",
        "abcabc",
        "aaaaaa",
        "abcdefghijklmnopqrstuvwxyz",
    ]
    
    for s in test_strings:
        result = length_of_longest_substring(s)
        print(f"String: '{s}' -> Length: {result}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        "",
        "a",
        "aa",
        "ab",
        "abc",
        "aab",
        "abb",
        "abab",
    ]
    
    for s in edge_cases:
        result = length_of_longest_substring(s)
        print(f"String: '{s}' -> Length: {result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for s, _ in test_cases[:5]:
        stats = length_of_longest_substring_with_stats(s)
        print(f"String: '{s}'")
        print(f"  Max length: {stats['max_length']}")
        print(f"  Total characters: {stats['total_characters']}")
        print(f"  Unique characters: {stats['unique_characters']}")
        print(f"  Window changes: {stats['window_changes']}")
        print()
