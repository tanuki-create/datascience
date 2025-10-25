"""
Problem 34: Permutation in String
Difficulty: Easy

Given two strings s1 and s2, return true if s2 contains a permutation of s1, 
or false otherwise.

In other words, return true if one of the first string's permutations is the 
substring of the second string.

Time Complexity: O(n + m) where n is length of s2 and m is length of s1
Space Complexity: O(1) since we use fixed-size arrays for character counting
"""

def check_inclusion(s1, s2):
    """
    Check if s2 contains a permutation of s1 using sliding window technique.
    
    Args:
        s1: The string to find permutation of
        s2: The string to search in
        
    Returns:
        bool: True if s2 contains a permutation of s1
    """
    if len(s1) > len(s2):
        return False
    
    # Count characters in s1
    s1_count = [0] * 26
    for char in s1:
        s1_count[ord(char) - ord('a')] += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(s1)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s2[i]) - ord('a')] += 1
    
    # Check first window
    if window_count == s1_count:
        return True
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s2)):
        # Remove leftmost character
        window_count[ord(s2[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s2[i]) - ord('a')] += 1
        
        # Check if current window matches s1
        if window_count == s1_count:
            return True
    
    return False


def check_inclusion_optimized(s1, s2):
    """
    Check if s2 contains a permutation of s1 using optimized sliding window.
    
    Args:
        s1: The string to find permutation of
        s2: The string to search in
        
    Returns:
        bool: True if s2 contains a permutation of s1
    """
    if len(s1) > len(s2):
        return False
    
    # Count characters in s1
    s1_count = [0] * 26
    for char in s1:
        s1_count[ord(char) - ord('a')] += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(s1)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s2[i]) - ord('a')] += 1
    
    # Check first window
    if window_count == s1_count:
        return True
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s2)):
        # Remove leftmost character
        window_count[ord(s2[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s2[i]) - ord('a')] += 1
        
        # Check if current window matches s1
        if window_count == s1_count:
            return True
    
    return False


def check_inclusion_with_hashmap(s1, s2):
    """
    Check if s2 contains a permutation of s1 using hashmap for character counting.
    
    Args:
        s1: The string to find permutation of
        s2: The string to search in
        
    Returns:
        bool: True if s2 contains a permutation of s1
    """
    if len(s1) > len(s2):
        return False
    
    from collections import defaultdict
    
    # Count characters in s1
    s1_count = defaultdict(int)
    for char in s1:
        s1_count[char] += 1
    
    # Initialize sliding window
    window_count = defaultdict(int)
    window_size = len(s1)
    
    # Initialize first window
    for i in range(window_size):
        window_count[s2[i]] += 1
    
    # Check first window
    if window_count == s1_count:
        return True
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s2)):
        # Remove leftmost character
        left_char = s2[i - window_size]
        window_count[left_char] -= 1
        if window_count[left_char] == 0:
            del window_count[left_char]
        
        # Add new character
        window_count[s2[i]] += 1
        
        # Check if current window matches s1
        if window_count == s1_count:
            return True
    
    return False


def check_inclusion_verbose(s1, s2):
    """
    Check if s2 contains a permutation of s1 with detailed step-by-step explanation.
    
    Args:
        s1: The string to find permutation of
        s2: The string to search in
        
    Returns:
        bool: True if s2 contains a permutation of s1
    """
    if len(s1) > len(s2):
        print(f"String s1 length ({len(s1)}) > s2 length ({len(s2)}), returning False")
        return False
    
    print(f"Checking if '{s2}' contains a permutation of '{s1}'")
    print(f"String s1 length: {len(s1)}, String s2 length: {len(s2)}")
    
    # Count characters in s1
    s1_count = [0] * 26
    for char in s1:
        s1_count[ord(char) - ord('a')] += 1
    
    print(f"String s1 character counts: {s1_count}")
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(s1)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s2[i]) - ord('a')] += 1
    
    print(f"Initial window: '{s2[:window_size]}'")
    print(f"Initial window counts: {window_count}")
    
    # Check first window
    if window_count == s1_count:
        print(f"Found permutation at index 0: '{s2[:window_size]}'")
        return True
    else:
        print(f"No permutation at index 0: '{s2[:window_size]}'")
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s2)):
        # Remove leftmost character
        left_char = s2[i - window_size]
        window_count[ord(left_char) - ord('a')] -= 1
        
        # Add new character
        new_char = s2[i]
        window_count[ord(new_char) - ord('a')] += 1
        
        current_window = s2[i - window_size + 1:i + 1]
        print(f"Window at index {i - window_size + 1}: '{current_window}'")
        print(f"Window counts: {window_count}")
        
        # Check if current window matches s1
        if window_count == s1_count:
            print(f"Found permutation at index {i - window_size + 1}: '{current_window}'")
            return True
        else:
            print(f"No permutation at index {i - window_size + 1}: '{current_window}'")
    
    print("No permutation found")
    return False


def check_inclusion_with_stats(s1, s2):
    """
    Check if s2 contains a permutation of s1 and return statistics.
    
    Args:
        s1: The string to find permutation of
        s2: The string to search in
        
    Returns:
        dict: Statistics about the search
    """
    if len(s1) > len(s2):
        return {
            'contains_permutation': False,
            'total_windows': 0,
            'windows_checked': 0,
            's1_length': len(s1),
            's2_length': len(s2)
        }
    
    # Count characters in s1
    s1_count = [0] * 26
    for char in s1:
        s1_count[ord(char) - ord('a')] += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(s1)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s2[i]) - ord('a')] += 1
    
    windows_checked = 1
    
    # Check first window
    if window_count == s1_count:
        return {
            'contains_permutation': True,
            'total_windows': 1,
            'windows_checked': 1,
            's1_length': len(s1),
            's2_length': len(s2)
        }
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s2)):
        # Remove leftmost character
        window_count[ord(s2[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s2[i]) - ord('a')] += 1
        
        windows_checked += 1
        
        # Check if current window matches s1
        if window_count == s1_count:
            return {
                'contains_permutation': True,
                'total_windows': windows_checked,
                'windows_checked': windows_checked,
                's1_length': len(s1),
                's2_length': len(s2)
            }
    
    return {
        'contains_permutation': False,
        'total_windows': windows_checked,
        'windows_checked': windows_checked,
        's1_length': len(s1),
        's2_length': len(s2)
    }


def check_inclusion_with_validation(s1, s2):
    """
    Check if s2 contains a permutation of s1 with validation.
    
    Args:
        s1: The string to find permutation of
        s2: The string to search in
        
    Returns:
        dict: Detailed validation results
    """
    if not s1 or not s2:
        return {
            'contains_permutation': False,
            'is_valid': False,
            'reason': 'Empty string'
        }
    
    if len(s1) > len(s2):
        return {
            'contains_permutation': False,
            'is_valid': False,
            'reason': f'String s1 length ({len(s1)}) > s2 length ({len(s2)})'
        }
    
    # Count characters in s1
    s1_count = [0] * 26
    for char in s1:
        s1_count[ord(char) - ord('a')] += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(s1)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s2[i]) - ord('a')] += 1
    
    # Check first window
    if window_count == s1_count:
        return {
            'contains_permutation': True,
            'is_valid': True,
            'reason': f'Found permutation of "{s1}" in "{s2}"',
            's1': s1,
            's2': s2
        }
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s2)):
        # Remove leftmost character
        window_count[ord(s2[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s2[i]) - ord('a')] += 1
        
        # Check if current window matches s1
        if window_count == s1_count:
            return {
                'contains_permutation': True,
                'is_valid': True,
                'reason': f'Found permutation of "{s1}" in "{s2}"',
                's1': s1,
                's2': s2
            }
    
    return {
        'contains_permutation': False,
        'is_valid': True,
        'reason': f'No permutation of "{s1}" found in "{s2}"',
        's1': s1,
        's2': s2
    }


def check_inclusion_with_comparison(s1, s2):
    """
    Check if s2 contains a permutation of s1 and compare different approaches.
    
    Args:
        s1: The string to find permutation of
        s2: The string to search in
        
    Returns:
        dict: Comparison of different approaches
    """
    if len(s1) > len(s2):
        return {
            'array_approach': False,
            'hashmap_approach': False
        }
    
    # Array approach
    array_result = check_inclusion(s1, s2)
    
    # Hashmap approach
    hashmap_result = check_inclusion_with_hashmap(s1, s2)
    
    return {
        'array_approach': array_result,
        'hashmap_approach': hashmap_result
    }


def check_inclusion_with_performance(s1, s2):
    """
    Check if s2 contains a permutation of s1 with performance metrics.
    
    Args:
        s1: The string to find permutation of
        s2: The string to search in
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    if len(s1) > len(s2):
        return {
            'contains_permutation': False,
            'execution_time': 0,
            'operations': 0
        }
    
    start_time = time.time()
    operations = 0
    
    # Count characters in s1
    s1_count = [0] * 26
    for char in s1:
        s1_count[ord(char) - ord('a')] += 1
        operations += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(s1)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s2[i]) - ord('a')] += 1
        operations += 1
    
    # Check first window
    if window_count == s1_count:
        end_time = time.time()
        return {
            'contains_permutation': True,
            'execution_time': end_time - start_time,
            'operations': operations
        }
    operations += 1
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s2)):
        # Remove leftmost character
        window_count[ord(s2[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s2[i]) - ord('a')] += 1
        
        # Check if current window matches s1
        if window_count == s1_count:
            end_time = time.time()
            return {
                'contains_permutation': True,
                'execution_time': end_time - start_time,
                'operations': operations
            }
        operations += 1
    
    end_time = time.time()
    
    return {
        'contains_permutation': False,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def check_inclusion_with_debugging(s1, s2):
    """
    Check if s2 contains a permutation of s1 with debugging information.
    
    Args:
        s1: The string to find permutation of
        s2: The string to search in
        
    Returns:
        dict: Debugging information
    """
    if len(s1) > len(s2):
        return {
            'contains_permutation': False,
            'debug_info': 'String s1 longer than s2',
            'windows_checked': 0
        }
    
    # Count characters in s1
    s1_count = [0] * 26
    for char in s1:
        s1_count[ord(char) - ord('a')] += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(s1)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s2[i]) - ord('a')] += 1
    
    windows_checked = 1
    
    # Check first window
    if window_count == s1_count:
        return {
            'contains_permutation': True,
            'debug_info': f'Found permutation in first window',
            'windows_checked': 1
        }
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s2)):
        # Remove leftmost character
        window_count[ord(s2[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s2[i]) - ord('a')] += 1
        
        windows_checked += 1
        
        # Check if current window matches s1
        if window_count == s1_count:
            return {
                'contains_permutation': True,
                'debug_info': f'Found permutation after checking {windows_checked} windows',
                'windows_checked': windows_checked
            }
    
    return {
        'contains_permutation': False,
        'debug_info': f'No permutation found after checking {windows_checked} windows',
        'windows_checked': windows_checked
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ("ab", "eidbaooo", True),
        ("ab", "eidboaoo", False),
        ("a", "ab", True),
        ("ab", "ab", True),
        ("ab", "a", False),
        ("ab", "ba", True),
        ("abc", "bca", True),
        ("", "a", False),
        ("a", "", False),
        ("", "", True),
    ]
    
    for i, (s1, s2, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: s1='{s1}', s2='{s2}'")
        
        # Test basic approach
        result = check_inclusion(s1, s2)
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = check_inclusion_optimized(s1, s2)
        print(f"Optimized result: {result_opt}")
        
        # Test hashmap approach
        result_hash = check_inclusion_with_hashmap(s1, s2)
        print(f"Hashmap result: {result_hash}")
        
        # Test with statistics
        stats = check_inclusion_with_stats(s1, s2)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = check_inclusion_with_validation(s1, s2)
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = check_inclusion_with_comparison(s1, s2)
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = check_inclusion_with_performance(s1, s2)
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = check_inclusion_with_debugging(s1, s2)
        print(f"Debugging: {debugging}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    check_inclusion_verbose("ab", "eidbaooo")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    import string
    
    # Generate large strings for testing
    def generate_large_string(length):
        """Generate a large string for testing."""
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    large_s1 = generate_large_string(100)
    large_s2 = generate_large_string(10000)
    
    # Test array approach
    start_time = time.time()
    for _ in range(100):
        check_inclusion(large_s1, large_s2)
    array_time = time.time() - start_time
    
    # Test hashmap approach
    start_time = time.time()
    for _ in range(100):
        check_inclusion_with_hashmap(large_s1, large_s2)
    hashmap_time = time.time() - start_time
    
    print(f"Array approach: {array_time:.6f} seconds")
    print(f"Hashmap approach: {hashmap_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Count characters in string s1")
    print("2. Use sliding window of size len(s1) to check each substring in s2")
    print("3. For each window, compare character frequencies with s1")
    print("4. If frequencies match, return True immediately")
    print("5. If no match found after checking all windows, return False")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    s1 = "ab"
    s2 = "eidbaooo"
    print(f"String s1: {s1}")
    print(f"String s2: {s2}")
    print("String s1 character counts: a=1, b=1")
    print("\nWindow positions:")
    for i in range(len(s2) - len(s1) + 1):
        window = s2[i:i+len(s1)]
        print(f"  Position {i}: '{window}'")
    
    # Test with different strings
    print("\nDifferent strings:")
    strings = ["a", "ab", "abc", "abcd"]
    for s1 in strings:
        result = check_inclusion(s1, s2)
        print(f"String s1 '{s1}': {result}")
    
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
    
    for s1, s2 in edge_cases:
        result = check_inclusion(s1, s2)
        print(f"s1='{s1}', s2='{s2}' -> {result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for s1, s2, _ in test_cases[:5]:
        stats = check_inclusion_with_stats(s1, s2)
        print(f"String s1: '{s1}', String s2: '{s2}'")
        print(f"  Contains permutation: {stats['contains_permutation']}")
        print(f"  Total windows: {stats['total_windows']}")
        print(f"  Windows checked: {stats['windows_checked']}")
        print(f"  String s1 length: {stats['s1_length']}")
        print(f"  String s2 length: {stats['s2_length']}")
        print()
