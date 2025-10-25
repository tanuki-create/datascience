"""
Problem 12: Roman to Integer
Difficulty: Easy

Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.
Convert a roman numeral to an integer.

Time Complexity: O(n)
Space Complexity: O(1)
"""

def roman_to_int(s):
    """
    Convert roman numeral to integer.
    
    Args:
        s: Roman numeral string
        
    Returns:
        int: Converted integer
    """
    # Mapping of roman symbols to values
    roman_values = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    total = 0
    prev_value = 0
    
    # Process from right to left
    for char in reversed(s):
        current_value = roman_values[char]
        
        # If current value is less than previous,
        # it means we need to subtract (like IV, IX, etc.)
        if current_value < prev_value:
            total -= current_value
        else:
            total += current_value
        
        prev_value = current_value
    
    return total


def roman_to_int_left_to_right(s):
    """
    Convert roman numeral to integer processing left to right.
    
    Args:
        s: Roman numeral string
        
    Returns:
        int: Converted integer
    """
    roman_values = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    total = 0
    i = 0
    
    while i < len(s):
        # Check for subtraction cases
        if i + 1 < len(s):
            current = roman_values[s[i]]
            next_val = roman_values[s[i + 1]]
            
            if current < next_val:
                total += next_val - current
                i += 2  # Skip both characters
            else:
                total += current
                i += 1
        else:
            total += roman_values[s[i]]
            i += 1
    
    return total


def int_to_roman(num):
    """
    Convert integer to roman numeral (bonus problem).
    
    Args:
        num: Integer to convert
        
    Returns:
        str: Roman numeral string
    """
    if num <= 0 or num > 3999:
        return ""
    
    # Define roman symbols and their values
    symbols = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I')
    ]
    
    result = []
    
    for value, symbol in symbols:
        count = num // value
        if count > 0:
            result.append(symbol * count)
            num %= value
    
    return ''.join(result)


def validate_roman_numeral(s):
    """
    Validate if a string is a valid roman numeral.
    
    Args:
        s: String to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not s:
        return False
    
    valid_symbols = {'I', 'V', 'X', 'L', 'C', 'D', 'M'}
    
    # Check if all characters are valid
    for char in s:
        if char not in valid_symbols:
            return False
    
    # Check for invalid patterns
    invalid_patterns = [
        'IIII',  # 4 I's in a row
        'VV',    # 2 V's in a row
        'XXXX',  # 4 X's in a row
        'LL',    # 2 L's in a row
        'CCCC',  # 4 C's in a row
        'DD',    # 2 D's in a row
        'MMMM',  # 4 M's in a row
    ]
    
    for pattern in invalid_patterns:
        if pattern in s:
            return False
    
    return True


def roman_to_int_with_validation(s):
    """
    Convert roman numeral to integer with validation.
    
    Args:
        s: Roman numeral string
        
    Returns:
        int: Converted integer, or -1 if invalid
    """
    if not validate_roman_numeral(s):
        return -1
    
    return roman_to_int(s)


def find_roman_patterns(s):
    """
    Find and analyze roman numeral patterns.
    
    Args:
        s: Roman numeral string
        
    Returns:
        dict: Analysis of patterns found
    """
    patterns = {
        'subtraction_cases': [],
        'repeated_symbols': [],
        'symbol_counts': {}
    }
    
    # Count symbols
    for char in s:
        patterns['symbol_counts'][char] = patterns['symbol_counts'].get(char, 0) + 1
    
    # Find subtraction cases
    subtraction_cases = ['IV', 'IX', 'XL', 'XC', 'CD', 'CM']
    for i in range(len(s) - 1):
        pair = s[i:i+2]
        if pair in subtraction_cases:
            patterns['subtraction_cases'].append((pair, i))
    
    # Find repeated symbols
    i = 0
    while i < len(s):
        char = s[i]
        count = 1
        j = i + 1
        while j < len(s) and s[j] == char:
            count += 1
            j += 1
        
        if count > 1:
            patterns['repeated_symbols'].append((char, count, i))
        
        i = j
    
    return patterns


def generate_roman_numbers(max_num=100):
    """
    Generate roman numbers from 1 to max_num.
    
    Args:
        max_num: Maximum number to generate
        
    Returns:
        list: List of (number, roman) tuples
    """
    result = []
    for i in range(1, max_num + 1):
        roman = int_to_roman(i)
        result.append((i, roman))
    return result


# Test cases
if __name__ == "__main__":
    test_cases = [
        "III",      # 3
        "LVIII",    # 58
        "MCMXC",    # 1994
        "IV",       # 4
        "IX",       # 9
        "XL",       # 40
        "XC",       # 90
        "CD",       # 400
        "CM",       # 900
        "I",        # 1
        "V",        # 5
        "X",        # 10
        "L",        # 50
        "C",        # 100
        "D",        # 500
        "M",        # 1000
    ]
    
    for i, s in enumerate(test_cases, 1):
        print(f"Test case {i}: '{s}'")
        
        # Test different approaches
        result_right_to_left = roman_to_int(s)
        result_left_to_right = roman_to_int_left_to_right(s)
        
        print(f"Right to left: {result_right_to_left}")
        print(f"Left to right: {result_left_to_right}")
        
        # Test validation
        is_valid = validate_roman_numeral(s)
        print(f"Valid roman: {is_valid}")
        
        # Test pattern analysis
        patterns = find_roman_patterns(s)
        print(f"Patterns: {patterns}")
        
        print("-" * 50)
    
    # Test integer to roman conversion
    print("\nInteger to Roman conversion:")
    int_tests = [1, 4, 9, 40, 90, 400, 900, 1994, 3999]
    for num in int_tests:
        roman = int_to_roman(num)
        back_to_int = roman_to_int(roman)
        print(f"{num} -> '{roman}' -> {back_to_int}")
    
    # Test validation
    print("\nRoman numeral validation:")
    validation_tests = [
        "III",      # Valid
        "IIII",     # Invalid (4 I's)
        "VV",       # Invalid (2 V's)
        "IX",       # Valid
        "IC",       # Invalid pattern
        "IM",       # Invalid pattern
        "MCMXC",    # Valid
    ]
    
    for s in validation_tests:
        is_valid = validate_roman_numeral(s)
        if is_valid:
            result = roman_to_int(s)
            print(f"'{s}' is valid -> {result}")
        else:
            print(f"'{s}' is invalid")
    
    # Generate some roman numbers
    print("\nGenerated roman numbers (1-20):")
    roman_numbers = generate_roman_numbers(20)
    for num, roman in roman_numbers:
        print(f"{num}: {roman}")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    
    # Large test case
    large_roman = "MCMXC" * 100  # Repeat to make it longer
    
    # Test right to left approach
    start_time = time.time()
    for _ in range(10000):
        roman_to_int(large_roman)
    right_to_left_time = time.time() - start_time
    
    # Test left to right approach
    start_time = time.time()
    for _ in range(10000):
        roman_to_int_left_to_right(large_roman)
    left_to_right_time = time.time() - start_time
    
    print(f"Right to left: {right_to_left_time:.6f} seconds")
    print(f"Left to right: {left_to_right_time:.6f} seconds")
    
    # Edge cases
    print("\nEdge cases:")
    edge_cases = [
        "",         # Empty string
        "I",        # Single character
        "II",       # Two same characters
        "IV",       # Subtraction case
        "IX",       # Subtraction case
        "MMMCMXCIX", # 3999 (maximum)
    ]
    
    for case in edge_cases:
        if case:
            result = roman_to_int(case)
            print(f"'{case}' -> {result}")
        else:
            print("Empty string -> 0")
    
    # Roman numeral rules
    print("\nRoman numeral rules:")
    print("1. I can be placed before V and X to make 4 and 9")
    print("2. X can be placed before L and C to make 40 and 90")
    print("3. C can be placed before D and M to make 400 and 900")
    print("4. Symbols are added from left to right")
    print("5. When a smaller symbol appears before a larger one, subtract")
    print("6. Maximum value is 3999 (MMMCMXCIX)")
