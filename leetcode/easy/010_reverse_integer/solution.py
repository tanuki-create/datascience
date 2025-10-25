"""
Problem 10: Reverse Integer
Difficulty: Easy

Given a signed 32-bit integer x, return x with its digits reversed. If reversing x 
causes the value to go outside the signed 32-bit integer range [-2^31, 2^31 - 1], 
then return 0.

Time Complexity: O(log n)
Space Complexity: O(1)
"""

def reverse(x):
    """
    Reverse the digits of an integer.
    
    Args:
        x: Integer to reverse
        
    Returns:
        int: Reversed integer, or 0 if overflow
    """
    # Handle negative numbers
    sign = -1 if x < 0 else 1
    x = abs(x)
    
    result = 0
    while x > 0:
        # Check for overflow before adding new digit
        if result > (2**31 - 1) // 10:
            return 0
        
        result = result * 10 + x % 10
        x //= 10
    
    result *= sign
    
    # Check final result is within 32-bit range
    if result < -2**31 or result > 2**31 - 1:
        return 0
    
    return result


def reverse_string_method(x):
    """
    Reverse using string conversion (not recommended for interview).
    
    Args:
        x: Integer to reverse
        
    Returns:
        int: Reversed integer, or 0 if overflow
    """
    if x == 0:
        return 0
    
    # Convert to string and reverse
    s = str(abs(x))
    reversed_s = s[::-1]
    
    # Remove leading zeros
    reversed_s = reversed_s.lstrip('0')
    if not reversed_s:
        return 0
    
    # Convert back to integer
    result = int(reversed_s)
    
    # Apply sign
    if x < 0:
        result = -result
    
    # Check for overflow
    if result < -2**31 or result > 2**31 - 1:
        return 0
    
    return result


def reverse_with_overflow_check(x):
    """
    Reverse with detailed overflow checking.
    
    Args:
        x: Integer to reverse
        
    Returns:
        int: Reversed integer, or 0 if overflow
    """
    if x == 0:
        return 0
    
    # Handle negative numbers
    is_negative = x < 0
    x = abs(x)
    
    result = 0
    max_int = 2**31 - 1
    min_int = -2**31
    
    while x > 0:
        digit = x % 10
        
        # Check for overflow before multiplication
        if result > max_int // 10:
            return 0
        
        # Check for overflow before addition
        if result == max_int // 10 and digit > max_int % 10:
            return 0
        
        result = result * 10 + digit
        x //= 10
    
    # Apply sign
    if is_negative:
        result = -result
    
    # Final overflow check
    if result < min_int or result > max_int:
        return 0
    
    return result


def reverse_using_stack(x):
    """
    Reverse using stack-like approach.
    
    Args:
        x: Integer to reverse
        
    Returns:
        int: Reversed integer, or 0 if overflow
    """
    if x == 0:
        return 0
    
    # Handle negative numbers
    is_negative = x < 0
    x = abs(x)
    
    # Extract digits
    digits = []
    while x > 0:
        digits.append(x % 10)
        x //= 10
    
    # Reconstruct number
    result = 0
    for digit in digits:
        # Check for overflow
        if result > (2**31 - 1) // 10:
            return 0
        
        result = result * 10 + digit
    
    # Apply sign
    if is_negative:
        result = -result
    
    # Final overflow check
    if result < -2**31 or result > 2**31 - 1:
        return 0
    
    return result


def is_palindrome_number(x):
    """
    Check if a number is a palindrome (bonus problem).
    
    Args:
        x: Integer to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if x < 0:
        return False
    
    if x == 0:
        return True
    
    # Reverse the number
    original = x
    reversed_num = 0
    
    while x > 0:
        reversed_num = reversed_num * 10 + x % 10
        x //= 10
    
    return original == reversed_num


def reverse_bits(n):
    """
    Reverse bits of a 32-bit unsigned integer (bonus problem).
    
    Args:
        n: 32-bit unsigned integer
        
    Returns:
        int: Integer with reversed bits
    """
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


def count_digits(x):
    """
    Count the number of digits in an integer.
    
    Args:
        x: Integer to count digits for
        
    Returns:
        int: Number of digits
    """
    if x == 0:
        return 1
    
    count = 0
    while x != 0:
        count += 1
        x //= 10
    
    return count


# Test cases
if __name__ == "__main__":
    test_cases = [
        123,        # Expected: 321
        -123,       # Expected: -321
        120,        # Expected: 21
        0,          # Expected: 0
        1,          # Expected: 1
        -1,         # Expected: -1
        1534236469, # Expected: 0 (overflow)
        -1534236469, # Expected: 0 (overflow)
        2147483647, # Expected: 0 (overflow)
        -2147483648, # Expected: 0 (overflow)
        123456789,  # Expected: 987654321
        -123456789, # Expected: -987654321
    ]
    
    for i, x in enumerate(test_cases, 1):
        print(f"Test case {i}: {x}")
        
        # Test different approaches
        result_main = reverse(x)
        result_string = reverse_string_method(x)
        result_detailed = reverse_with_overflow_check(x)
        result_stack = reverse_using_stack(x)
        
        print(f"Main approach: {result_main}")
        print(f"String method: {result_string}")
        print(f"Detailed check: {result_detailed}")
        print(f"Stack approach: {result_stack}")
        
        # Verify no overflow
        if result_main != 0:
            print(f"Verification: {result_main} reversed = {reverse(result_main)}")
        
        print("-" * 50)
    
    # Test palindrome checking
    print("\nPalindrome number test:")
    palindrome_tests = [121, -121, 10, 0, 1, 12321, 12345]
    for num in palindrome_tests:
        is_pal = is_palindrome_number(num)
        print(f"{num} is palindrome: {is_pal}")
    
    # Test bit reversal
    print("\nBit reversal test:")
    bit_tests = [43261596, 0, 1, 4294967295]
    for num in bit_tests:
        reversed_bits = reverse_bits(num)
        print(f"{num} -> {reversed_bits}")
    
    # Test digit counting
    print("\nDigit counting:")
    digit_tests = [123, 0, 1, 123456789, -123]
    for num in digit_tests:
        count = count_digits(abs(num))
        print(f"{num} has {count} digits")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    
    # Large test case
    large_x = 123456789
    
    # Test main approach
    start_time = time.time()
    for _ in range(100000):
        reverse(large_x)
    main_time = time.time() - start_time
    
    # Test string approach
    start_time = time.time()
    for _ in range(100000):
        reverse_string_method(large_x)
    string_time = time.time() - start_time
    
    print(f"Main approach: {main_time:.6f} seconds")
    print(f"String approach: {string_time:.6f} seconds")
    print(f"Main is {string_time/main_time:.2f}x faster")
    
    # Edge cases
    print("\nEdge cases:")
    edge_cases = [
        0,           # Zero
        1,           # Single digit
        -1,          # Single negative digit
        10,          # Ends with zero
        -10,         # Negative, ends with zero
        100,         # Multiple trailing zeros
        -100,        # Negative, multiple trailing zeros
    ]
    
    for case in edge_cases:
        result = reverse(case)
        print(f"{case} -> {result}")
    
    # Overflow examples
    print("\nOverflow examples:")
    overflow_cases = [
        2147483647,   # Max 32-bit int
        -2147483648,  # Min 32-bit int
        1534236469,   # Overflows when reversed
        -1534236469,  # Overflows when reversed
    ]
    
    for case in overflow_cases:
        result = reverse(case)
        print(f"{case} -> {result} (overflow: {result == 0})")
