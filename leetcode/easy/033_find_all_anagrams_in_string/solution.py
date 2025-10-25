"""
Problem 33: Find All Anagrams in String
Difficulty: Easy

Given two strings s and p, return an array of all the start indices of p's 
anagrams in s. You may return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different 
word or phrase, typically using all the original letters exactly once.

Time Complexity: O(n + m) where n is length of s and m is length of p
Space Complexity: O(1) since we use fixed-size arrays for character counting
"""

def find_anagrams(s, p):
    """
    Find all anagrams of p in s using sliding window technique.
    
    Args:
        s: The main string to search in
        p: The pattern string to find anagrams of
        
    Returns:
        list: List of start indices where anagrams are found
    """
    if len(p) > len(s):
        return []
    
    # Count characters in pattern
    p_count = [0] * 26
    for char in p:
        p_count[ord(char) - ord('a')] += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(p)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s[i]) - ord('a')] += 1
    
    result = []
    
    # Check first window
    if window_count == p_count:
        result.append(0)
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s)):
        # Remove leftmost character
        window_count[ord(s[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s[i]) - ord('a')] += 1
        
        # Check if current window matches pattern
        if window_count == p_count:
            result.append(i - window_size + 1)
    
    return result


def find_anagrams_optimized(s, p):
    """
    Find all anagrams using optimized sliding window with character difference tracking.
    
    Args:
        s: The main string to search in
        p: The pattern string to find anagrams of
        
    Returns:
        list: List of start indices where anagrams are found
    """
    if len(p) > len(s)):
        return []
    
    # Count characters in pattern
    p_count = [0] * 26
    for char in p:
        p_count[ord(char) - ord('a')] += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(p)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s[i]) - ord('a')] += 1
    
    result = []
    
    # Check first window
    if window_count == p_count:
        result.append(0)
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s)):
        # Remove leftmost character
        window_count[ord(s[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s[i]) - ord('a')] += 1
        
        # Check if current window matches pattern
        if window_count == p_count:
            result.append(i - window_size + 1)
    
    return result


def find_anagrams_with_hashmap(s, p):
    """
    Find all anagrams using hashmap for character counting.
    
    Args:
        s: The main string to search in
        p: The pattern string to find anagrams of
        
    Returns:
        list: List of start indices where anagrams are found
    """
    if len(p) > len(s):
        return []
    
    from collections import defaultdict
    
    # Count characters in pattern
    p_count = defaultdict(int)
    for char in p:
        p_count[char] += 1
    
    # Initialize sliding window
    window_count = defaultdict(int)
    window_size = len(p)
    
    # Initialize first window
    for i in range(window_size):
        window_count[s[i]] += 1
    
    result = []
    
    # Check first window
    if window_count == p_count:
        result.append(0)
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s)):
        # Remove leftmost character
        left_char = s[i - window_size]
        window_count[left_char] -= 1
        if window_count[left_char] == 0:
            del window_count[left_char]
        
        # Add new character
        window_count[s[i]] += 1
        
        # Check if current window matches pattern
        if window_count == p_count:
            result.append(i - window_size + 1)
    
    return result


def find_anagrams_verbose(s, p):
    """
    Find all anagrams with detailed step-by-step explanation.
    
    Args:
        s: The main string to search in
        p: The pattern string to find anagrams of
        
    Returns:
        list: List of start indices where anagrams are found
    """
    if len(p) > len(s):
        print(f"Pattern length ({len(p)}) > string length ({len(s)}), returning []")
        return []
    
    print(f"Finding anagrams of '{p}' in '{s}'")
    print(f"String length: {len(s)}, Pattern length: {len(p)}")
    
    # Count characters in pattern
    p_count = [0] * 26
    for char in p:
        p_count[ord(char) - ord('a')] += 1
    
    print(f"Pattern character counts: {p_count}")
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(p)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s[i]) - ord('a')] += 1
    
    print(f"Initial window: '{s[:window_size]}'")
    print(f"Initial window counts: {window_count}")
    
    result = []
    
    # Check first window
    if window_count == p_count:
        print(f"Found anagram at index 0: '{s[:window_size]}'")
        result.append(0)
    else:
        print(f"No anagram at index 0: '{s[:window_size]}'")
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s)):
        # Remove leftmost character
        left_char = s[i - window_size]
        window_count[ord(left_char) - ord('a')] -= 1
        
        # Add new character
        new_char = s[i]
        window_count[ord(new_char) - ord('a')] += 1
        
        current_window = s[i - window_size + 1:i + 1]
        print(f"Window at index {i - window_size + 1}: '{current_window}'")
        print(f"Window counts: {window_count}")
        
        # Check if current window matches pattern
        if window_count == p_count:
            print(f"Found anagram at index {i - window_size + 1}: '{current_window}'")
            result.append(i - window_size + 1)
        else:
            print(f"No anagram at index {i - window_size + 1}: '{current_window}'")
    
    print(f"Final result: {result}")
    return result


def find_anagrams_with_stats(s, p):
    """
    Find all anagrams and return statistics.
    
    Args:
        s: The main string to search in
        p: The pattern string to find anagrams of
        
    Returns:
        dict: Statistics about the search
    """
    if len(p) > len(s):
        return {
            'anagrams': [],
            'total_windows': 0,
            'anagram_count': 0,
            'pattern_length': len(p),
            'string_length': len(s)
        }
    
    # Count characters in pattern
    p_count = [0] * 26
    for char in p:
        p_count[ord(char) - ord('a')] += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(p)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s[i]) - ord('a')] += 1
    
    result = []
    total_windows = 1
    
    # Check first window
    if window_count == p_count:
        result.append(0)
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s)):
        # Remove leftmost character
        window_count[ord(s[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s[i]) - ord('a')] += 1
        
        total_windows += 1
        
        # Check if current window matches pattern
        if window_count == p_count:
            result.append(i - window_size + 1)
    
    return {
        'anagrams': result,
        'total_windows': total_windows,
        'anagram_count': len(result),
        'pattern_length': len(p),
        'string_length': len(s)
    }


def find_anagrams_with_validation(s, p):
    """
    Find all anagrams with validation.
    
    Args:
        s: The main string to search in
        p: The pattern string to find anagrams of
        
    Returns:
        dict: Detailed validation results
    """
    if not s or not p:
        return {
            'anagrams': [],
            'is_valid': False,
            'reason': 'Empty string or pattern'
        }
    
    if len(p) > len(s):
        return {
            'anagrams': [],
            'is_valid': False,
            'reason': f'Pattern length ({len(p)}) > string length ({len(s)})'
        }
    
    # Count characters in pattern
    p_count = [0] * 26
    for char in p:
        p_count[ord(char) - ord('a')] += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(p)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s[i]) - ord('a')] += 1
    
    result = []
    
    # Check first window
    if window_count == p_count:
        result.append(0)
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s)):
        # Remove leftmost character
        window_count[ord(s[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s[i]) - ord('a')] += 1
        
        # Check if current window matches pattern
        if window_count == p_count:
            result.append(i - window_size + 1)
    
    return {
        'anagrams': result,
        'is_valid': True,
        'reason': f'Found {len(result)} anagram(s)',
        'pattern': p,
        'string': s
    }


def find_anagrams_with_comparison(s, p):
    """
    Find all anagrams and compare different approaches.
    
    Args:
        s: The main string to search in
        p: The pattern string to find anagrams of
        
    Returns:
        dict: Comparison of different approaches
    """
    if len(p) > len(s):
        return {
            'array_approach': [],
            'hashmap_approach': []
        }
    
    # Array approach
    array_result = find_anagrams(s, p)
    
    # Hashmap approach
    hashmap_result = find_anagrams_with_hashmap(s, p)
    
    return {
        'array_approach': array_result,
        'hashmap_approach': hashmap_result
    }


def find_anagrams_with_performance(s, p):
    """
    Find all anagrams with performance metrics.
    
    Args:
        s: The main string to search in
        p: The pattern string to find anagrams of
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    if len(p) > len(s):
        return {
            'anagrams': [],
            'execution_time': 0,
            'operations': 0
        }
    
    start_time = time.time()
    operations = 0
    
    # Count characters in pattern
    p_count = [0] * 26
    for char in p:
        p_count[ord(char) - ord('a')] += 1
        operations += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(p)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s[i]) - ord('a')] += 1
        operations += 1
    
    result = []
    
    # Check first window
    if window_count == p_count:
        result.append(0)
    operations += 1
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s)):
        # Remove leftmost character
        window_count[ord(s[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s[i]) - ord('a')] += 1
        
        # Check if current window matches pattern
        if window_count == p_count:
            result.append(i - window_size + 1)
        operations += 1
    
    end_time = time.time()
    
    return {
        'anagrams': result,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def find_anagrams_with_debugging(s, p):
    """
    Find all anagrams with debugging information.
    
    Args:
        s: The main string to search in
        p: The pattern string to find anagrams of
        
    Returns:
        dict: Debugging information
    """
    if len(p) > len(s):
        return {
            'anagrams': [],
            'debug_info': 'Pattern longer than string',
            'windows_checked': 0
        }
    
    # Count characters in pattern
    p_count = [0] * 26
    for char in p:
        p_count[ord(char) - ord('a')] += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(p)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s[i]) - ord('a')] += 1
    
    result = []
    windows_checked = 1
    
    # Check first window
    if window_count == p_count:
        result.append(0)
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s)):
        # Remove leftmost character
        window_count[ord(s[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s[i]) - ord('a')] += 1
        
        windows_checked += 1
        
        # Check if current window matches pattern
        if window_count == p_count:
            result.append(i - window_size + 1)
    
    return {
        'anagrams': result,
        'debug_info': f'Checked {windows_checked} windows',
        'windows_checked': windows_checked
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ("cbaebabacd", "abc", [0, 6]),
        ("abab", "ab", [0, 1, 2]),
        ("abcdef", "xyz", []),
        ("aaaa", "a", [0, 1, 2, 3]),
        ("a", "a", [0]),
        ("ab", "ba", [0]),
        ("abc", "bca", [0]),
        ("ababab", "ab", [0, 1, 2, 3, 4]),
        ("", "a", []),
        ("a", "", []),
        ("", "", []),
    ]
    
    for i, (s, p, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: s='{s}', p='{p}'")
        
        # Test basic approach
        result = find_anagrams(s, p)
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = find_anagrams_optimized(s, p)
        print(f"Optimized result: {result_opt}")
        
        # Test hashmap approach
        result_hash = find_anagrams_with_hashmap(s, p)
        print(f"Hashmap result: {result_hash}")
        
        # Test with statistics
        stats = find_anagrams_with_stats(s, p)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = find_anagrams_with_validation(s, p)
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = find_anagrams_with_comparison(s, p)
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = find_anagrams_with_performance(s, p)
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = find_anagrams_with_debugging(s, p)
        print(f"Debugging: {debugging}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    find_anagrams_verbose("cbaebabacd", "abc")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    import string
    
    # Generate large strings for testing
    def generate_large_string(length):
        """Generate a large string for testing."""
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    large_s = generate_large_string(10000)
    large_p = generate_large_string(100)
    
    # Test array approach
    start_time = time.time()
    for _ in range(100):
        find_anagrams(large_s, large_p)
    array_time = time.time() - start_time
    
    # Test hashmap approach
    start_time = time.time()
    for _ in range(100):
        find_anagrams_with_hashmap(large_s, large_p)
    hashmap_time = time.time() - start_time
    
    print(f"Array approach: {array_time:.6f} seconds")
    print(f"Hashmap approach: {hashmap_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Count characters in pattern p")
    print("2. Use sliding window of size len(p) to check each substring in s")
    print("3. For each window, compare character frequencies with pattern")
    print("4. If frequencies match, add start index to result")
    print("5. Move window to next position and repeat")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    s = "cbaebabacd"
    p = "abc"
    print(f"String: {s}")
    print(f"Pattern: {p}")
    print("Pattern character counts: a=1, b=1, c=1")
    print("\nWindow positions:")
    for i in range(len(s) - len(p) + 1):
        window = s[i:i+len(p)]
        print(f"  Position {i}: '{window}'")
    
    # Test with different patterns
    print("\nDifferent patterns:")
    patterns = ["a", "ab", "abc", "abcd"]
    for pattern in patterns:
        result = find_anagrams(s, pattern)
        print(f"Pattern '{pattern}': {result}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        ("", "a"),
        ("a", ""),
        ("", ""),
        ("a", "a"),
        ("aa", "a"),
        ("aaa", "aa"),
    ]
    
    for s, p in edge_cases:
        result = find_anagrams(s, p)
        print(f"s='{s}', p='{p}' -> {result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for s, p, _ in test_cases[:5]:
        stats = find_anagrams_with_stats(s, p)
        print(f"String: '{s}', Pattern: '{p}'")
        print(f"  Anagrams: {stats['anagrams']}")
        print(f"  Total windows: {stats['total_windows']}")
        print(f"  Anagram count: {stats['anagram_count']}")
        print(f"  Pattern length: {stats['pattern_length']}")
        print(f"  String length: {stats['string_length']}")
        print()
