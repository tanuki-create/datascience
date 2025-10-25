"""
Problem 44: Longest Palindromic Substring
Difficulty: Medium

Given a string s, return the longest palindromic substring in s.

Time Complexity: O(n²) where n is the length of the string
Space Complexity: O(1) for storing the result
"""

def longest_palindrome(s):
    """
    Find the longest palindromic substring using expand around centers.
    
    Args:
        s: Input string
        
    Returns:
        str: Longest palindromic substring
    """
    if not s:
        return ""
    
    start = 0
    max_length = 1
    
    def expand_around_center(left, right):
        """Expand around center and return palindrome length."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    for i in range(len(s)):
        # Check odd-length palindromes (center at character)
        len1 = expand_around_center(i, i)
        # Check even-length palindromes (center between characters)
        len2 = expand_around_center(i, i + 1)
        
        # Get the longer palindrome
        current_length = max(len1, len2)
        
        # Update longest palindrome if current is longer
        if current_length > max_length:
            max_length = current_length
            start = i - (current_length - 1) // 2
    
    return s[start:start + max_length]


def longest_palindrome_optimized(s):
    """
    Find the longest palindromic substring using optimized approach.
    
    Args:
        s: Input string
        
    Returns:
        str: Longest palindromic substring
    """
    if not s:
        return ""
    
    start = 0
    max_length = 1
    
    def expand_around_center(left, right):
        """Expand around center and return palindrome length."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    for i in range(len(s)):
        # Check odd-length palindromes (center at character)
        len1 = expand_around_center(i, i)
        # Check even-length palindromes (center between characters)
        len2 = expand_around_center(i, i + 1)
        
        # Get the longer palindrome
        current_length = max(len1, len2)
        
        # Update longest palindrome if current is longer
        if current_length > max_length:
            max_length = current_length
            start = i - (current_length - 1) // 2
    
    return s[start:start + max_length]


def longest_palindrome_with_dp(s):
    """
    Find the longest palindromic substring using dynamic programming.
    
    Args:
        s: Input string
        
    Returns:
        str: Longest palindromic substring
    """
    if not s:
        return ""
    
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start = 0
    max_length = 1
    
    # Single characters are palindromes
    for i in range(n):
        dp[i][i] = True
    
    # Check for palindromes of length 2
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start = i
            max_length = 2
    
    # Check for palindromes of length 3 and more
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > max_length:
                    start = i
                    max_length = length
    
    return s[start:start + max_length]


def longest_palindrome_verbose(s):
    """
    Find the longest palindromic substring with detailed step-by-step explanation.
    
    Args:
        s: Input string
        
    Returns:
        str: Longest palindromic substring
    """
    if not s:
        print("Empty string, returning ''")
        return ""
    
    print(f"Finding longest palindromic substring in '{s}'")
    print(f"String length: {len(s)}")
    
    start = 0
    max_length = 1
    
    def expand_around_center(left, right):
        """Expand around center and return palindrome length."""
        print(f"    Expanding around center: left={left}, right={right}")
        while left >= 0 and right < len(s) and s[left] == s[right]:
            print(f"      Characters match: s[{left}]='{s[left]}' == s[{right}]='{s[right]}'")
            left -= 1
            right += 1
        print(f"    Final positions: left={left}, right={right}")
        return right - left - 1
    
    for i in range(len(s)):
        print(f"\nStep {i + 1}: Checking center at position {i}")
        
        # Check odd-length palindromes (center at character)
        print(f"  Checking odd-length palindrome (center at s[{i}]='{s[i]}')")
        len1 = expand_around_center(i, i)
        print(f"  Odd-length palindrome length: {len1}")
        
        # Check even-length palindromes (center between characters)
        print(f"  Checking even-length palindrome (center between s[{i}] and s[{i+1}])")
        len2 = expand_around_center(i, i + 1)
        print(f"  Even-length palindrome length: {len2}")
        
        # Get the longer palindrome
        current_length = max(len1, len2)
        print(f"  Current palindrome length: {current_length}")
        
        # Update longest palindrome if current is longer
        if current_length > max_length:
            max_length = current_length
            start = i - (current_length - 1) // 2
            print(f"  New longest palindrome: start={start}, length={max_length}")
            print(f"  Longest palindrome so far: '{s[start:start + max_length]}'")
        else:
            print(f"  Current palindrome not longer than max ({max_length})")
    
    result = s[start:start + max_length]
    print(f"\nFinal result: '{result}'")
    return result


def longest_palindrome_with_stats(s):
    """
    Find the longest palindromic substring and return statistics.
    
    Args:
        s: Input string
        
    Returns:
        dict: Statistics about the search
    """
    if not s:
        return {
            'longest_palindrome': '',
            'length': 0,
            'total_centers': 0,
            'palindromes_found': 0
        }
    
    start = 0
    max_length = 1
    total_centers = 0
    palindromes_found = 0
    
    def expand_around_center(left, right):
        """Expand around center and return palindrome length."""
        nonlocal palindromes_found
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        length = right - left - 1
        if length > 0:
            palindromes_found += 1
        return length
    
    for i in range(len(s)):
        total_centers += 1
        
        # Check odd-length palindromes (center at character)
        len1 = expand_around_center(i, i)
        # Check even-length palindromes (center between characters)
        len2 = expand_around_center(i, i + 1)
        
        # Get the longer palindrome
        current_length = max(len1, len2)
        
        # Update longest palindrome if current is longer
        if current_length > max_length:
            max_length = current_length
            start = i - (current_length - 1) // 2
    
    return {
        'longest_palindrome': s[start:start + max_length],
        'length': max_length,
        'total_centers': total_centers,
        'palindromes_found': palindromes_found
    }


def longest_palindrome_with_validation(s):
    """
    Find the longest palindromic substring with validation.
    
    Args:
        s: Input string
        
    Returns:
        dict: Detailed validation results
    """
    if not s:
        return {
            'longest_palindrome': '',
            'is_valid': False,
            'reason': 'Empty string'
        }
    
    start = 0
    max_length = 1
    
    def expand_around_center(left, right):
        """Expand around center and return palindrome length."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    for i in range(len(s)):
        # Check odd-length palindromes (center at character)
        len1 = expand_around_center(i, i)
        # Check even-length palindromes (center between characters)
        len2 = expand_around_center(i, i + 1)
        
        # Get the longer palindrome
        current_length = max(len1, len2)
        
        # Update longest palindrome if current is longer
        if current_length > max_length:
            max_length = current_length
            start = i - (current_length - 1) // 2
    
    result = s[start:start + max_length]
    
    return {
        'longest_palindrome': result,
        'is_valid': True,
        'reason': f'Found longest palindrome of length {max_length}',
        'input': s
    }


def longest_palindrome_with_comparison(s):
    """
    Find the longest palindromic substring and compare different approaches.
    
    Args:
        s: Input string
        
    Returns:
        dict: Comparison of different approaches
    """
    # Expand around centers approach
    expand_result = longest_palindrome(s)
    
    # Dynamic programming approach
    dp_result = longest_palindrome_with_dp(s)
    
    return {
        'expand_around_centers': expand_result,
        'dynamic_programming': dp_result
    }


def longest_palindrome_with_performance(s):
    """
    Find the longest palindromic substring with performance metrics.
    
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
            'longest_palindrome': '',
            'execution_time': 0,
            'operations': 0
        }
    
    start = 0
    max_length = 1
    
    def expand_around_center(left, right):
        """Expand around center and return palindrome length."""
        nonlocal operations
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
            operations += 1
        return right - left - 1
    
    for i in range(len(s)):
        # Check odd-length palindromes (center at character)
        len1 = expand_around_center(i, i)
        # Check even-length palindromes (center between characters)
        len2 = expand_around_center(i, i + 1)
        
        # Get the longer palindrome
        current_length = max(len1, len2)
        
        # Update longest palindrome if current is longer
        if current_length > max_length:
            max_length = current_length
            start = i - (current_length - 1) // 2
        
        operations += 1
    
    end_time = time.time()
    
    return {
        'longest_palindrome': s[start:start + max_length],
        'execution_time': end_time - start_time,
        'operations': operations
    }


def longest_palindrome_with_debugging(s):
    """
    Find the longest palindromic substring with debugging information.
    
    Args:
        s: Input string
        
    Returns:
        dict: Debugging information
    """
    if not s:
        return {
            'longest_palindrome': '',
            'debug_info': 'Empty string',
            'steps': 0
        }
    
    start = 0
    max_length = 1
    steps = 0
    
    def expand_around_center(left, right):
        """Expand around center and return palindrome length."""
        nonlocal steps
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
            steps += 1
        return right - left - 1
    
    for i in range(len(s)):
        # Check odd-length palindromes (center at character)
        len1 = expand_around_center(i, i)
        # Check even-length palindromes (center between characters)
        len2 = expand_around_center(i, i + 1)
        
        # Get the longer palindrome
        current_length = max(len1, len2)
        
        # Update longest palindrome if current is longer
        if current_length > max_length:
            max_length = current_length
            start = i - (current_length - 1) // 2
        
        steps += 1
    
    return {
        'longest_palindrome': s[start:start + max_length],
        'debug_info': f'Processed {steps} operations',
        'steps': steps
    }


def longest_palindrome_with_analysis(s):
    """
    Find the longest palindromic substring and return analysis.
    
    Args:
        s: Input string
        
    Returns:
        dict: Analysis results
    """
    if not s:
        return {
            'longest_palindrome': '',
            'analysis': 'Empty string',
            'efficiency': 'N/A'
        }
    
    start = 0
    max_length = 1
    total_operations = 0
    
    def expand_around_center(left, right):
        """Expand around center and return palindrome length."""
        nonlocal total_operations
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
            total_operations += 1
        return right - left - 1
    
    for i in range(len(s)):
        # Check odd-length palindromes (center at character)
        len1 = expand_around_center(i, i)
        # Check even-length palindromes (center between characters)
        len2 = expand_around_center(i, i + 1)
        
        # Get the longer palindrome
        current_length = max(len1, len2)
        
        # Update longest palindrome if current is longer
        if current_length > max_length:
            max_length = current_length
            start = i - (current_length - 1) // 2
        
        total_operations += 1
    
    efficiency = max_length / len(s) if len(s) > 0 else 0.0
    
    return {
        'longest_palindrome': s[start:start + max_length],
        'analysis': f'Found longest palindrome of length {max_length} in {total_operations} operations',
        'efficiency': efficiency
    }


def longest_palindrome_with_optimization(s):
    """
    Find the longest palindromic substring with optimization techniques.
    
    Args:
        s: Input string
        
    Returns:
        dict: Optimization results
    """
    if not s:
        return {
            'longest_palindrome': '',
            'optimization': 'Empty string',
            'space_saved': 0
        }
    
    start = 0
    max_length = 1
    
    def expand_around_center(left, right):
        """Expand around center and return palindrome length."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    for i in range(len(s)):
        # Check odd-length palindromes (center at character)
        len1 = expand_around_center(i, i)
        # Check even-length palindromes (center between characters)
        len2 = expand_around_center(i, i + 1)
        
        # Get the longer palindrome
        current_length = max(len1, len2)
        
        # Update longest palindrome if current is longer
        if current_length > max_length:
            max_length = current_length
            start = i - (current_length - 1) // 2
    
    # Calculate space optimization
    original_space = len(s)
    optimized_space = max_length
    space_saved = original_space - optimized_space
    
    return {
        'longest_palindrome': s[start:start + max_length],
        'optimization': f'Space saved: {space_saved} characters',
        'space_saved': space_saved
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ("babad", "bab"),
        ("cbbd", "bb"),
        ("a", "a"),
        ("abc", "a"),
        ("racecar", "racecar"),
        ("", ""),
        ("abcdef", "a"),
        ("aab", "aa"),
        ("abacabad", "abacaba"),
        ("abcdefghijklmnopqrstuvwxyz", "a"),
    ]
    
    for i, (s, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: s='{s}'")
        
        # Test basic approach
        result = longest_palindrome(s)
        print(f"Result: '{result}'")
        print(f"Expected: '{expected}'")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = longest_palindrome_optimized(s)
        print(f"Optimized result: '{result_opt}'")
        
        # Test DP approach
        result_dp = longest_palindrome_with_dp(s)
        print(f"DP result: '{result_dp}'")
        
        # Test with statistics
        stats = longest_palindrome_with_stats(s)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = longest_palindrome_with_validation(s)
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = longest_palindrome_with_comparison(s)
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = longest_palindrome_with_performance(s)
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = longest_palindrome_with_debugging(s)
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        analysis = longest_palindrome_with_analysis(s)
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        optimization = longest_palindrome_with_optimization(s)
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    longest_palindrome_verbose("babad")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    import string
    
    # Generate large string for testing
    def generate_large_string(length):
        """Generate a large string for testing."""
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    large_s = generate_large_string(1000)
    
    # Test expand around centers approach
    start_time = time.time()
    for _ in range(100):
        longest_palindrome(large_s)
    expand_time = time.time() - start_time
    
    # Test DP approach
    start_time = time.time()
    for _ in range(100):
        longest_palindrome_with_dp(large_s)
    dp_time = time.time() - start_time
    
    print(f"Expand around centers: {expand_time:.6f} seconds")
    print(f"Dynamic programming: {dp_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. For each position in the string:")
    print("   - Check odd-length palindromes (center at character)")
    print("   - Check even-length palindromes (center between characters)")
    print("2. Expand around each center to find longest palindrome")
    print("3. Track the longest palindrome found")
    print("4. Return the longest palindromic substring")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    s = "babad"
    print(f"String: {s}")
    print("\nSteps:")
    print("1. Center at 'b' (position 0): odd='b', even=''")
    print("2. Center at 'a' (position 1): odd='aba', even=''")
    print("3. Center at 'b' (position 2): odd='b', even=''")
    print("4. Center at 'a' (position 3): odd='a', even=''")
    print("5. Center at 'd' (position 4): odd='d', even=''")
    print("Longest palindrome: 'aba'")
    
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
        result = longest_palindrome(s)
        print(f"String: '{s}' -> Longest palindrome: '{result}'")
    
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
        result = longest_palindrome(s)
        print(f"String: '{s}' -> Longest palindrome: '{result}'")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for s, _ in test_cases[:5]:
        stats = longest_palindrome_with_stats(s)
        print(f"String: '{s}'")
        print(f"  Longest palindrome: '{stats['longest_palindrome']}'")
        print(f"  Length: {stats['length']}")
        print(f"  Total centers: {stats['total_centers']}")
        print(f"  Palindromes found: {stats['palindromes_found']}")
        print()
