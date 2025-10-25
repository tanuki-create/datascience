"""
Problem 16: Plus One
Difficulty: Easy

You are given a large integer represented as an integer array digits, where each 
digits[i] is the ith digit of the integer. The digits are ordered from most 
significant to least significant in left-to-right order.

Time Complexity: O(n)
Space Complexity: O(1)
"""

def plus_one(digits):
    """
    Add one to the large integer represented as an array of digits.
    
    Args:
        digits: Array of digits representing a large integer
        
    Returns:
        list: Array of digits after adding one
    """
    # Start from the rightmost digit
    for i in range(len(digits) - 1, -1, -1):
        # If current digit is less than 9, just increment and return
        if digits[i] < 9:
            digits[i] += 1
            return digits
        
        # If current digit is 9, set it to 0 and continue
        digits[i] = 0
    
    # If we reach here, all digits were 9, so we need to add a new digit
    return [1] + digits


def plus_one_verbose(digits):
    """
    Add one with detailed step-by-step explanation.
    
    Args:
        digits: Array of digits representing a large integer
        
    Returns:
        list: Array of digits after adding one
    """
    print(f"Original digits: {digits}")
    print(f"Original number: {''.join(map(str, digits))}")
    
    # Start from the rightmost digit
    for i in range(len(digits) - 1, -1, -1):
        print(f"Processing digit at index {i}: {digits[i]}")
        
        if digits[i] < 9:
            digits[i] += 1
            print(f"Digit {digits[i] - 1} -> {digits[i]}")
            print(f"Result: {digits}")
            return digits
        else:
            digits[i] = 0
            print(f"Digit 9 -> 0 (carry over)")
    
    # If we reach here, all digits were 9
    print("All digits were 9, adding new digit")
    result = [1] + digits
    print(f"Result: {result}")
    return result


def plus_one_recursive(digits):
    """
    Add one using recursive approach.
    
    Args:
        digits: Array of digits representing a large integer
        
    Returns:
        list: Array of digits after adding one
    """
    def add_one_recursive(index):
        if index < 0:
            return [1] + digits
        
        if digits[index] < 9:
            digits[index] += 1
            return digits
        else:
            digits[index] = 0
            return add_one_recursive(index - 1)
    
    return add_one_recursive(len(digits) - 1)


def plus_one_with_carry(digits):
    """
    Add one using explicit carry handling.
    
    Args:
        digits: Array of digits representing a large integer
        
    Returns:
        list: Array of digits after adding one
    """
    carry = 1  # We want to add 1
    
    for i in range(len(digits) - 1, -1, -1):
        total = digits[i] + carry
        digits[i] = total % 10
        carry = total // 10
        
        if carry == 0:
            break
    
    if carry > 0:
        digits = [carry] + digits
    
    return digits


def plus_one_convert_back(digits):
    """
    Add one by converting to integer, adding 1, and converting back.
    
    Args:
        digits: Array of digits representing a large integer
        
    Returns:
        list: Array of digits after adding one
    """
    # Convert to integer
    num = 0
    for digit in digits:
        num = num * 10 + digit
    
    # Add one
    num += 1
    
    # Convert back to array
    result = []
    while num > 0:
        result.append(num % 10)
        num //= 10
    
    return result[::-1]


def plus_one_general(digits, addend):
    """
    Add any number to the large integer (bonus problem).
    
    Args:
        digits: Array of digits representing a large integer
        addend: Number to add
        
    Returns:
        list: Array of digits after adding the number
    """
    if addend == 0:
        return digits
    
    # Convert addend to array of digits
    addend_digits = []
    while addend > 0:
        addend_digits.append(addend % 10)
        addend //= 10
    addend_digits = addend_digits[::-1]
    
    # Add the two arrays
    result = []
    carry = 0
    i, j = len(digits) - 1, len(addend_digits) - 1
    
    while i >= 0 or j >= 0 or carry > 0:
        total = carry
        if i >= 0:
            total += digits[i]
            i -= 1
        if j >= 0:
            total += addend_digits[j]
            j -= 1
        
        result.append(total % 10)
        carry = total // 10
    
    return result[::-1]


def subtract_one(digits):
    """
    Subtract one from the large integer (bonus problem).
    
    Args:
        digits: Array of digits representing a large integer
        
    Returns:
        list: Array of digits after subtracting one
    """
    if not digits:
        return []
    
    # If the number is 0, return -1 (or handle as needed)
    if digits == [0]:
        return [-1]
    
    # Start from the rightmost digit
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] > 0:
            digits[i] -= 1
            return digits
        else:
            digits[i] = 9
    
    # If we reach here, the number was 0
    return [-1]


def multiply_by_two(digits):
    """
    Multiply the large integer by 2 (bonus problem).
    
    Args:
        digits: Array of digits representing a large integer
        
    Returns:
        list: Array of digits after multiplying by 2
    """
    result = []
    carry = 0
    
    for i in range(len(digits) - 1, -1, -1):
        total = digits[i] * 2 + carry
        result.append(total % 10)
        carry = total // 10
    
    if carry > 0:
        result.append(carry)
    
    return result[::-1]


def is_power_of_ten(digits):
    """
    Check if the large integer is a power of 10 (bonus problem).
    
    Args:
        digits: Array of digits representing a large integer
        
    Returns:
        bool: True if the number is a power of 10
    """
    if not digits:
        return False
    
    # Check if first digit is 1 and all others are 0
    if digits[0] != 1:
        return False
    
    for i in range(1, len(digits)):
        if digits[i] != 0:
            return False
    
    return True


# Test cases
if __name__ == "__main__":
    test_cases = [
        [1, 2, 3],        # Expected: [1, 2, 4]
        [4, 3, 2, 1],     # Expected: [4, 3, 2, 2]
        [9],              # Expected: [1, 0]
        [1, 9],           # Expected: [2, 0]
        [9, 9],           # Expected: [1, 0, 0]
        [9, 9, 9],         # Expected: [1, 0, 0, 0]
        [0],              # Expected: [1]
        [1, 0, 0],        # Expected: [1, 0, 1]
    ]
    
    for i, digits in enumerate(test_cases, 1):
        print(f"Test case {i}: {digits}")
        
        # Test different approaches
        result_main = plus_one(digits.copy())
        result_recursive = plus_one_recursive(digits.copy())
        result_carry = plus_one_with_carry(digits.copy())
        result_convert = plus_one_convert_back(digits.copy())
        
        print(f"Main approach: {result_main}")
        print(f"Recursive: {result_recursive}")
        print(f"Carry approach: {result_carry}")
        print(f"Convert approach: {result_convert}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            plus_one_verbose(digits.copy())
        
        print("-" * 50)
    
    # Test bonus problems
    print("\nBonus problems:")
    
    # Test adding different numbers
    add_tests = [
        ([1, 2, 3], 5),      # Add 5
        ([9, 9], 1),         # Add 1
        ([1, 0, 0], 50),     # Add 50
    ]
    
    for digits, addend in add_tests:
        result = plus_one_general(digits.copy(), addend)
        print(f"{digits} + {addend} = {result}")
    
    # Test subtracting one
    subtract_tests = [
        [1, 2, 4],          # 124 - 1 = 123
        [1, 0],             # 10 - 1 = 9
        [1, 0, 0],          # 100 - 1 = 99
        [0],                # 0 - 1 = -1
    ]
    
    for digits in subtract_tests:
        result = subtract_one(digits.copy())
        print(f"{digits} - 1 = {result}")
    
    # Test multiplying by 2
    multiply_tests = [
        [1, 2, 3],          # 123 * 2 = 246
        [9, 9],             # 99 * 2 = 198
        [5],                # 5 * 2 = 10
    ]
    
    for digits in multiply_tests:
        result = multiply_by_two(digits.copy())
        print(f"{digits} * 2 = {result}")
    
    # Test power of 10
    power_tests = [
        [1],                # 1 = 10^0
        [1, 0],             # 10 = 10^1
        [1, 0, 0],          # 100 = 10^2
        [1, 0, 0, 0],        # 1000 = 10^3
        [1, 2, 3],          # 123 (not power of 10)
        [1, 0, 1],          # 101 (not power of 10)
    ]
    
    for digits in power_tests:
        result = is_power_of_ten(digits)
        print(f"{digits} is power of 10: {result}")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    
    # Large test case
    large_digits = [9] * 1000  # 999...999 (1000 digits)
    
    # Test main approach
    start_time = time.time()
    for _ in range(100):
        plus_one(large_digits.copy())
    main_time = time.time() - start_time
    
    # Test convert approach
    start_time = time.time()
    for _ in range(100):
        plus_one_convert_back(large_digits.copy())
    convert_time = time.time() - start_time
    
    print(f"Main approach: {main_time:.6f} seconds")
    print(f"Convert approach: {convert_time:.6f} seconds")
    
    # Edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],                  # Empty array
        [0],                 # Single zero
        [1],                 # Single one
        [9],                 # Single nine
        [1, 0, 0, 0],        # 1000
        [9, 9, 9, 9],        # 9999
    ]
    
    for case in edge_cases:
        result = plus_one(case.copy())
        print(f"{case} -> {result}")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Start from the rightmost digit")
    print("2. If digit < 9, increment and return")
    print("3. If digit = 9, set to 0 and continue")
    print("4. If all digits were 9, add new digit 1 at the beginning")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example = [9, 9, 9]
    print(f"Original: {example}")
    
    for i in range(len(example) - 1, -1, -1):
        if example[i] < 9:
            example[i] += 1
            print(f"Step {len(example) - 1 - i}: {example}")
            break
        else:
            example[i] = 0
            print(f"Step {len(example) - 1 - i}: {example}")
    
    if all(d == 0 for d in example):
        example = [1] + example
        print(f"Final: {example}")
    
    print(f"Result: {example}")
