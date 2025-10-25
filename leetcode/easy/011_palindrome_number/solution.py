"""
Problem 11: Palindrome Number
Difficulty: Easy

Given an integer x, return true if x is a palindrome integer.
An integer is a palindrome when it reads the same backward as forward.

Time Complexity: O(log n)
Space Complexity: O(1)
"""

def is_palindrome(x):
    """
    Check if an integer is a palindrome without converting to string.
    
    Args:
        x: Integer to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    # Negative numbers are not palindromes
    if x < 0:
        return False
    
    # Single digit numbers are palindromes
    if x < 10:
        return True
    
    # Numbers ending with 0 (except 0) are not palindromes
    if x % 10 == 0:
        return False
    
    # Reverse half of the number
    reversed_half = 0
    while x > reversed_half:
        reversed_half = reversed_half * 10 + x % 10
        x //= 10
    
    # For even number of digits: x == reversed_half
    # For odd number of digits: x == reversed_half // 10
    return x == reversed_half or x == reversed_half // 10


def is_palindrome_string(x):
    """
    Check if an integer is a palindrome using string conversion.
    
    Args:
        x: Integer to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if x < 0:
        return False
    
    s = str(x)
    return s == s[::-1]


def is_palindrome_full_reverse(x):
    """
    Check if an integer is a palindrome by fully reversing it.
    
    Args:
        x: Integer to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if x < 0:
        return False
    
    if x == 0:
        return True
    
    original = x
    reversed_num = 0
    
    while x > 0:
        reversed_num = reversed_num * 10 + x % 10
        x //= 10
    
    return original == reversed_num


def is_palindrome_with_overflow_check(x):
    """
    Check if an integer is a palindrome with overflow protection.
    
    Args:
        x: Integer to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if x < 0:
        return False
    
    if x == 0:
        return True
    
    # Check for potential overflow
    if x > 2**31 - 1:
        return False
    
    original = x
    reversed_num = 0
    
    while x > 0:
        # Check for overflow before multiplication
        if reversed_num > (2**31 - 1) // 10:
            return False
        
        reversed_num = reversed_num * 10 + x % 10
        x //= 10
    
    return original == reversed_num


def find_palindrome_numbers_in_range(start, end):
    """
    Find all palindrome numbers in a given range.
    
    Args:
        start: Start of range
        end: End of range
        
    Returns:
        list: List of palindrome numbers
    """
    palindromes = []
    for i in range(start, end + 1):
        if is_palindrome(i):
            palindromes.append(i)
    return palindromes


def is_palindrome_string_general(s):
    """
    Check if a string is a palindrome (bonus problem).
    
    Args:
        s: String to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    # Convert to lowercase and remove non-alphanumeric characters
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


def is_palindrome_string_optimized(s):
    """
    Check if a string is a palindrome using two pointers.
    
    Args:
        s: String to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric characters
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        # Compare characters (case insensitive)
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True


def count_palindrome_substrings(s):
    """
    Count the number of palindrome substrings in a string (bonus problem).
    
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


# Test cases
if __name__ == "__main__":
    test_cases = [
        121,        # True
        -121,       # False
        10,         # False
        0,          # True
        1,          # True
        -1,         # False
        12321,      # True
        12345,      # False
        1221,       # True
        123321,     # True
        1234321,    # True
        123456,     # False
    ]
    
    for i, x in enumerate(test_cases, 1):
        print(f"Test case {i}: {x}")
        
        # Test different approaches
        result_main = is_palindrome(x)
        result_string = is_palindrome_string(x)
        result_full = is_palindrome_full_reverse(x)
        result_overflow = is_palindrome_with_overflow_check(x)
        
        print(f"Half reverse: {result_main}")
        print(f"String method: {result_string}")
        print(f"Full reverse: {result_full}")
        print(f"Overflow check: {result_overflow}")
        
        print("-" * 50)
    
    # Test palindrome numbers in range
    print("\nPalindrome numbers in range 1-1000:")
    palindromes = find_palindrome_numbers_in_range(1, 1000)
    print(f"Found {len(palindromes)} palindromes")
    print(f"First 20: {palindromes[:20]}")
    
    # Test string palindrome
    print("\nString palindrome test:")
    string_tests = [
        "A man a plan a canal Panama",
        "race a car",
        "Was it a car or a cat I saw?",
        "hello",
        "level",
        "noon",
    ]
    
    for s in string_tests:
        result_general = is_palindrome_string_general(s)
        result_optimized = is_palindrome_string_optimized(s)
        print(f"'{s}' -> General: {result_general}, Optimized: {result_optimized}")
    
    # Test palindrome substrings
    print("\nPalindrome substrings count:")
    substring_tests = ["abc", "aaa", "abccba", "racecar"]
    for s in substring_tests:
        count = count_palindrome_substrings(s)
        print(f"'{s}' has {count} palindrome substrings")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    
    # Large test case
    large_x = 12345678987654321
    
    # Test half reverse approach
    start_time = time.time()
    for _ in range(100000):
        is_palindrome(large_x)
    half_time = time.time() - start_time
    
    # Test string approach
    start_time = time.time()
    for _ in range(100000):
        is_palindrome_string(large_x)
    string_time = time.time() - start_time
    
    # Test full reverse approach
    start_time = time.time()
    for _ in range(100000):
        is_palindrome_full_reverse(large_x)
    full_time = time.time() - start_time
    
    print(f"Half reverse: {half_time:.6f} seconds")
    print(f"String method: {string_time:.6f} seconds")
    print(f"Full reverse: {full_time:.6f} seconds")
    
    # Edge cases
    print("\nEdge cases:")
    edge_cases = [
        0,           # Zero
        1,           # Single digit
        -1,          # Negative single digit
        10,          # Ends with zero
        100,         # Multiple trailing zeros
        1001,        # Palindrome with zeros
        10001,       # Palindrome with multiple zeros
    ]
    
    for case in edge_cases:
        result = is_palindrome(case)
        print(f"{case} -> {result}")
    
    # Mathematical properties
    print("\nMathematical properties:")
    print("Properties of palindrome numbers:")
    print("1. All single digit numbers are palindromes")
    print("2. Negative numbers are not palindromes")
    print("3. Numbers ending with 0 (except 0) are not palindromes")
    print("4. Palindromes with even digits: first half == reversed second half")
    print("5. Palindromes with odd digits: first half == reversed second half (excluding middle)")
    
    # Generate some palindrome numbers
    print("\nGenerating palindrome numbers:")
    for i in range(1, 100):
        if is_palindrome(i):
            print(f"{i} is a palindrome")
            if i > 20:  # Limit output
                break
