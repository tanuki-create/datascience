"""
Problem 14: Valid Palindrome
Difficulty: Easy

A phrase is a palindrome if, after converting all uppercase letters into lowercase 
letters and removing all non-alphanumeric characters, it reads the same forward 
and backward.

Time Complexity: O(n)
Space Complexity: O(1)
"""

def is_palindrome(s):
    """
    Check if a string is a palindrome using two pointers.
    
    Args:
        s: String to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric characters from left
        while left < right and not s[left].isalnum():
            left += 1
        
        # Skip non-alphanumeric characters from right
        while left < right and not s[right].isalnum():
            right -= 1
        
        # Compare characters (case insensitive)
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True


def is_palindrome_clean_first(s):
    """
    Check if a string is a palindrome by cleaning first, then checking.
    
    Args:
        s: String to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    # Clean the string: keep only alphanumeric characters and convert to lowercase
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    
    # Check if cleaned string is a palindrome
    return cleaned == cleaned[::-1]


def is_palindrome_recursive(s):
    """
    Check if a string is a palindrome using recursion.
    
    Args:
        s: String to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    def is_palindrome_helper(left, right):
        if left >= right:
            return True
        
        # Skip non-alphanumeric characters
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        # Compare characters
        if s[left].lower() != s[right].lower():
            return False
        
        return is_palindrome_helper(left + 1, right - 1)
    
    return is_palindrome_helper(0, len(s) - 1)


def is_palindrome_with_details(s):
    """
    Check if a string is a palindrome and return detailed information.
    
    Args:
        s: String to check
        
    Returns:
        dict: Detailed information about the palindrome check
    """
    left, right = 0, len(s) - 1
    comparisons = 0
    skipped_chars = []
    
    while left < right:
        # Skip non-alphanumeric characters from left
        while left < right and not s[left].isalnum():
            skipped_chars.append((left, s[left], 'left'))
            left += 1
        
        # Skip non-alphanumeric characters from right
        while left < right and not s[right].isalnum():
            skipped_chars.append((right, s[right], 'right'))
            right -= 1
        
        # Compare characters
        comparisons += 1
        if s[left].lower() != s[right].lower():
            return {
                'is_palindrome': False,
                'comparisons': comparisons,
                'skipped_chars': skipped_chars,
                'failed_at': (left, right, s[left], s[right])
            }
        
        left += 1
        right -= 1
    
    return {
        'is_palindrome': True,
        'comparisons': comparisons,
        'skipped_chars': skipped_chars
    }


def find_longest_palindrome_substring(s):
    """
    Find the longest palindrome substring (bonus problem).
    
    Args:
        s: String to analyze
        
    Returns:
        str: Longest palindrome substring
    """
    if not s:
        return ""
    
    def expand_around_center(left, right):
        """Expand around center to find palindrome."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]
    
    longest = ""
    
    for i in range(len(s)):
        # Check for odd length palindromes
        odd_palindrome = expand_around_center(i, i)
        if len(odd_palindrome) > len(longest):
            longest = odd_palindrome
        
        # Check for even length palindromes
        even_palindrome = expand_around_center(i, i + 1)
        if len(even_palindrome) > len(longest):
            longest = even_palindrome
    
    return longest


def count_palindrome_substrings(s):
    """
    Count the number of palindrome substrings (bonus problem).
    
    Args:
        s: String to analyze
        
    Returns:
        int: Number of palindrome substrings
    """
    count = 0
    n = len(s)
    
    # Check for odd length palindromes
    for center in range(n):
        left = right = center
        while left >= 0 and right < n and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
    
    # Check for even length palindromes
    for center in range(n - 1):
        left = center
        right = center + 1
        while left >= 0 and right < n and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
    
    return count


def is_palindrome_ignore_case(s):
    """
    Check if a string is a palindrome ignoring case.
    
    Args:
        s: String to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    s = s.lower()
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    
    return True


def is_palindrome_word_by_word(s):
    """
    Check if a string is a palindrome word by word.
    
    Args:
        s: String to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    words = s.split()
    return words == words[::-1]


# Test cases
if __name__ == "__main__":
    test_cases = [
        "A man, a plan, a canal: Panama",  # True
        "race a car",                      # False
        " ",                               # True
        "a",                              # True
        "ab",                             # False
        "aba",                            # True
        "abba",                           # True
        "abcba",                          # True
        "A man a plan a canal Panama",    # True
        "race a car",                     # False
        "Madam, I'm Adam",                # True
        "No 'x' in Nixon",                # True
        "Was it a car or a cat I saw?",   # True
    ]
    
    for i, s in enumerate(test_cases, 1):
        print(f"Test case {i}: '{s}'")
        
        # Test different approaches
        result_two_pointers = is_palindrome(s)
        result_clean_first = is_palindrome_clean_first(s)
        result_recursive = is_palindrome_recursive(s)
        
        print(f"Two pointers: {result_two_pointers}")
        print(f"Clean first: {result_clean_first}")
        print(f"Recursive: {result_recursive}")
        
        # Test detailed analysis
        details = is_palindrome_with_details(s)
        print(f"Details: {details}")
        
        print("-" * 50)
    
    # Test bonus problems
    print("\nBonus problems:")
    
    # Test longest palindrome substring
    substring_tests = [
        "babad",      # "bab" or "aba"
        "cbbd",       # "bb"
        "a",          # "a"
        "ac",         # "a" or "c"
        "racecar",    # "racecar"
    ]
    
    for s in substring_tests:
        longest = find_longest_palindrome_substring(s)
        print(f"Longest palindrome in '{s}': '{longest}'")
    
    # Test palindrome substring count
    count_tests = [
        "abc",        # 3 (a, b, c)
        "aaa",        # 6 (a, a, a, aa, aa, aaa)
        "racecar",    # 7 (r, a, c, e, c, a, r)
    ]
    
    for s in count_tests:
        count = count_palindrome_substrings(s)
        print(f"Palindrome substrings in '{s}': {count}")
    
    # Test case insensitive palindrome
    print("\nCase insensitive palindrome:")
    case_tests = ["Aba", "AbBa", "Abc"]
    for s in case_tests:
        result = is_palindrome_ignore_case(s)
        print(f"'{s}' is palindrome (case insensitive): {result}")
    
    # Test word by word palindrome
    print("\nWord by word palindrome:")
    word_tests = [
        "hello world",           # False
        "hello world hello",     # True
        "a b a",                # True
        "a b c",                # False
    ]
    
    for s in word_tests:
        result = is_palindrome_word_by_word(s)
        print(f"'{s}' is word palindrome: {result}")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    
    # Large test case
    large_string = "A man, a plan, a canal: Panama" * 1000
    
    # Test two pointers approach
    start_time = time.time()
    for _ in range(1000):
        is_palindrome(large_string)
    two_pointers_time = time.time() - start_time
    
    # Test clean first approach
    start_time = time.time()
    for _ in range(1000):
        is_palindrome_clean_first(large_string)
    clean_first_time = time.time() - start_time
    
    # Test recursive approach
    start_time = time.time()
    for _ in range(1000):
        is_palindrome_recursive(large_string)
    recursive_time = time.time() - start_time
    
    print(f"Two pointers: {two_pointers_time:.6f} seconds")
    print(f"Clean first: {clean_first_time:.6f} seconds")
    print(f"Recursive: {recursive_time:.6f} seconds")
    
    # Edge cases
    print("\nEdge cases:")
    edge_cases = [
        "",                    # Empty string
        "a",                   # Single character
        "aa",                  # Two same characters
        "ab",                  # Two different characters
        "a b",                 # Space between characters
        "a!b",                 # Non-alphanumeric between characters
        "12321",               # Numeric palindrome
        "a1b2c3c2b1a",         # Mixed alphanumeric
    ]
    
    for case in edge_cases:
        result = is_palindrome(case)
        print(f"'{case}' -> {result}")
    
    # Character analysis
    print("\nCharacter analysis:")
    test_string = "A man, a plan, a canal: Panama"
    print(f"Original: '{test_string}'")
    
    # Show which characters are kept
    kept_chars = [c for c in test_string if c.isalnum()]
    print(f"Kept characters: {kept_chars}")
    
    # Show the cleaned string
    cleaned = ''.join(c.lower() for c in test_string if c.isalnum())
    print(f"Cleaned string: '{cleaned}'")
    
    # Show the reversed cleaned string
    reversed_cleaned = cleaned[::-1]
    print(f"Reversed: '{reversed_cleaned}'")
    print(f"Is palindrome: {cleaned == reversed_cleaned}")
