"""
Problem 47: Letter Combinations of a Phone Number
Difficulty: Medium

Given a string containing digits from 2-9 inclusive, return all possible 
letter combinations that the number could represent. Return the answer in 
any order.

A mapping of digits to letters (just like on the telephone buttons) is given 
below. Note that 1 does not map to any letters.

Time Complexity: O(3^m * 4^n) where m is the number of digits with 3 letters and n is the number of digits with 4 letters
Space Complexity: O(3^m * 4^n) for storing all combinations
"""

def letter_combinations(digits):
    """
    Generate all possible letter combinations using backtracking.
    
    Args:
        digits: String of digits from 2-9
        
    Returns:
        list: List of all possible letter combinations
    """
    if not digits:
        return []
    
    # Mapping from digits to letters
    digit_to_letters = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    result = []
    
    def backtrack(index, current_combination):
        # Base case: if we've processed all digits
        if index == len(digits):
            result.append(current_combination)
            return
        
        # Get letters for current digit
        current_digit = digits[index]
        letters = digit_to_letters[current_digit]
        
        # Try each letter for current digit
        for letter in letters:
            backtrack(index + 1, current_combination + letter)
    
    backtrack(0, "")
    return result


def letter_combinations_optimized(digits):
    """
    Generate all possible letter combinations using optimized backtracking.
    
    Args:
        digits: String of digits from 2-9
        
    Returns:
        list: List of all possible letter combinations
    """
    if not digits:
        return []
    
    # Mapping from digits to letters
    digit_to_letters = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    result = []
    
    def backtrack(index, current_combination):
        # Base case: if we've processed all digits
        if index == len(digits):
            result.append(current_combination)
            return
        
        # Get letters for current digit
        current_digit = digits[index]
        letters = digit_to_letters[current_digit]
        
        # Try each letter for current digit
        for letter in letters:
            backtrack(index + 1, current_combination + letter)
    
    backtrack(0, "")
    return result


def letter_combinations_with_iterative(digits):
    """
    Generate all possible letter combinations using iterative approach.
    
    Args:
        digits: String of digits from 2-9
        
    Returns:
        list: List of all possible letter combinations
    """
    if not digits:
        return []
    
    # Mapping from digits to letters
    digit_to_letters = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    result = [""]
    
    for digit in digits:
        letters = digit_to_letters[digit]
        new_result = []
        
        for combination in result:
            for letter in letters:
                new_result.append(combination + letter)
        
        result = new_result
    
    return result


def letter_combinations_verbose(digits):
    """
    Generate all possible letter combinations with detailed step-by-step explanation.
    
    Args:
        digits: String of digits from 2-9
        
    Returns:
        list: List of all possible letter combinations
    """
    if not digits:
        print("Empty digits, returning []")
        return []
    
    print(f"Generating letter combinations for digits: '{digits}'")
    print(f"Number of digits: {len(digits)}")
    
    # Mapping from digits to letters
    digit_to_letters = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    print(f"Digit to letters mapping: {digit_to_letters}")
    
    result = []
    
    def backtrack(index, current_combination):
        print(f"\nStep {index + 1}: Processing digit '{digits[index]}' at index {index}")
        print(f"  Current combination: '{current_combination}'")
        
        # Base case: if we've processed all digits
        if index == len(digits):
            print(f"  Base case reached, adding combination: '{current_combination}'")
            result.append(current_combination)
            return
        
        # Get letters for current digit
        current_digit = digits[index]
        letters = digit_to_letters[current_digit]
        print(f"  Letters for digit '{current_digit}': '{letters}'")
        
        # Try each letter for current digit
        for i, letter in enumerate(letters):
            print(f"    Trying letter '{letter}' (option {i + 1}/{len(letters)})")
            new_combination = current_combination + letter
            print(f"    New combination: '{new_combination}'")
            backtrack(index + 1, new_combination)
    
    backtrack(0, "")
    print(f"\nFinal result: {result}")
    return result


def letter_combinations_with_stats(digits):
    """
    Generate all possible letter combinations and return statistics.
    
    Args:
        digits: String of digits from 2-9
        
    Returns:
        dict: Statistics about the generation
    """
    if not digits:
        return {
            'combinations': [],
            'total_combinations': 0,
            'digits_processed': 0,
            'letters_per_digit': []
        }
    
    # Mapping from digits to letters
    digit_to_letters = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    result = []
    letters_per_digit = []
    
    def backtrack(index, current_combination):
        # Base case: if we've processed all digits
        if index == len(digits):
            result.append(current_combination)
            return
        
        # Get letters for current digit
        current_digit = digits[index]
        letters = digit_to_letters[current_digit]
        letters_per_digit.append(len(letters))
        
        # Try each letter for current digit
        for letter in letters:
            backtrack(index + 1, current_combination + letter)
    
    backtrack(0, "")
    
    return {
        'combinations': result,
        'total_combinations': len(result),
        'digits_processed': len(digits),
        'letters_per_digit': letters_per_digit
    }


def letter_combinations_with_validation(digits):
    """
    Generate all possible letter combinations with validation.
    
    Args:
        digits: String of digits from 2-9
        
    Returns:
        dict: Detailed validation results
    """
    if not digits:
        return {
            'combinations': [],
            'is_valid': True,
            'reason': 'Empty input',
            'input': digits
        }
    
    # Check if all digits are valid
    valid_digits = set('23456789')
    if not all(digit in valid_digits for digit in digits):
        return {
            'combinations': [],
            'is_valid': False,
            'reason': 'Invalid digits found',
            'input': digits
        }
    
    # Mapping from digits to letters
    digit_to_letters = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    result = []
    
    def backtrack(index, current_combination):
        # Base case: if we've processed all digits
        if index == len(digits):
            result.append(current_combination)
            return
        
        # Get letters for current digit
        current_digit = digits[index]
        letters = digit_to_letters[current_digit]
        
        # Try each letter for current digit
        for letter in letters:
            backtrack(index + 1, current_combination + letter)
    
    backtrack(0, "")
    
    return {
        'combinations': result,
        'is_valid': True,
        'reason': f'Generated {len(result)} combinations',
        'input': digits
    }


def letter_combinations_with_comparison(digits):
    """
    Generate all possible letter combinations and compare different approaches.
    
    Args:
        digits: String of digits from 2-9
        
    Returns:
        dict: Comparison of different approaches
    """
    # Backtracking approach
    backtracking_result = letter_combinations(digits)
    
    # Iterative approach
    iterative_result = letter_combinations_with_iterative(digits)
    
    return {
        'backtracking': backtracking_result,
        'iterative': iterative_result
    }


def letter_combinations_with_performance(digits):
    """
    Generate all possible letter combinations with performance metrics.
    
    Args:
        digits: String of digits from 2-9
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    start_time = time.time()
    operations = 0
    
    if not digits:
        return {
            'combinations': [],
            'execution_time': 0,
            'operations': 0
        }
    
    # Mapping from digits to letters
    digit_to_letters = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    result = []
    
    def backtrack(index, current_combination):
        nonlocal operations
        operations += 1
        
        # Base case: if we've processed all digits
        if index == len(digits):
            result.append(current_combination)
            return
        
        # Get letters for current digit
        current_digit = digits[index]
        letters = digit_to_letters[current_digit]
        
        # Try each letter for current digit
        for letter in letters:
            backtrack(index + 1, current_combination + letter)
    
    backtrack(0, "")
    end_time = time.time()
    
    return {
        'combinations': result,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def letter_combinations_with_debugging(digits):
    """
    Generate all possible letter combinations with debugging information.
    
    Args:
        digits: String of digits from 2-9
        
    Returns:
        dict: Debugging information
    """
    if not digits:
        return {
            'combinations': [],
            'debug_info': 'Empty input',
            'steps': 0
        }
    
    # Mapping from digits to letters
    digit_to_letters = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    result = []
    steps = 0
    
    def backtrack(index, current_combination):
        nonlocal steps
        steps += 1
        
        # Base case: if we've processed all digits
        if index == len(digits):
            result.append(current_combination)
            return
        
        # Get letters for current digit
        current_digit = digits[index]
        letters = digit_to_letters[current_digit]
        
        # Try each letter for current digit
        for letter in letters:
            backtrack(index + 1, current_combination + letter)
    
    backtrack(0, "")
    
    return {
        'combinations': result,
        'debug_info': f'Processed {steps} operations',
        'steps': steps
    }


def letter_combinations_with_analysis(digits):
    """
    Generate all possible letter combinations and return analysis.
    
    Args:
        digits: String of digits from 2-9
        
    Returns:
        dict: Analysis results
    """
    if not digits:
        return {
            'combinations': [],
            'analysis': 'Empty input',
            'efficiency': 'N/A'
        }
    
    # Mapping from digits to letters
    digit_to_letters = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    result = []
    total_operations = 0
    
    def backtrack(index, current_combination):
        nonlocal total_operations
        total_operations += 1
        
        # Base case: if we've processed all digits
        if index == len(digits):
            result.append(current_combination)
            return
        
        # Get letters for current digit
        current_digit = digits[index]
        letters = digit_to_letters[current_digit]
        
        # Try each letter for current digit
        for letter in letters:
            backtrack(index + 1, current_combination + letter)
    
    backtrack(0, "")
    
    efficiency = len(result) / total_operations if total_operations > 0 else 0.0
    
    return {
        'combinations': result,
        'analysis': f'Generated {len(result)} combinations in {total_operations} operations',
        'efficiency': efficiency
    }


def letter_combinations_with_optimization(digits):
    """
    Generate all possible letter combinations with optimization techniques.
    
    Args:
        digits: String of digits from 2-9
        
    Returns:
        dict: Optimization results
    """
    if not digits:
        return {
            'combinations': [],
            'optimization': 'Empty input',
            'space_saved': 0
        }
    
    # Mapping from digits to letters
    digit_to_letters = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    result = []
    
    def backtrack(index, current_combination):
        # Base case: if we've processed all digits
        if index == len(digits):
            result.append(current_combination)
            return
        
        # Get letters for current digit
        current_digit = digits[index]
        letters = digit_to_letters[current_digit]
        
        # Try each letter for current digit
        for letter in letters:
            backtrack(index + 1, current_combination + letter)
    
    backtrack(0, "")
    
    # Calculate space optimization
    original_space = len(digits) * 4  # Assuming 4 bytes per character
    optimized_space = len(result) * len(result[0]) if result else 0
    space_saved = original_space - optimized_space
    
    return {
        'combinations': result,
        'optimization': f'Space saved: {space_saved} bytes',
        'space_saved': space_saved
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        ("23", ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]),
        ("", []),
        ("2", ["a", "b", "c"]),
        ("9", ["w", "x", "y", "z"]),
        ("234", ["adg", "adh", "adi", "aeg", "aeh", "aei", "afg", "afh", "afi", "bdg", "bdh", "bdi", "beg", "beh", "bei", "bfg", "bfh", "bfi", "cdg", "cdh", "cdi", "ceg", "ceh", "cei", "cfg", "cfh", "cfi"]),
    ]
    
    for i, (digits, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: digits='{digits}'")
        
        # Test basic approach
        result = letter_combinations(digits)
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = letter_combinations_optimized(digits)
        print(f"Optimized result: {result_opt}")
        
        # Test iterative approach
        result_iter = letter_combinations_with_iterative(digits)
        print(f"Iterative result: {result_iter}")
        
        # Test with statistics
        stats = letter_combinations_with_stats(digits)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = letter_combinations_with_validation(digits)
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = letter_combinations_with_comparison(digits)
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = letter_combinations_with_performance(digits)
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = letter_combinations_with_debugging(digits)
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        analysis = letter_combinations_with_analysis(digits)
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        optimization = letter_combinations_with_optimization(digits)
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    letter_combinations_verbose("23")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    
    # Test backtracking approach
    start_time = time.time()
    for _ in range(1000):
        letter_combinations("23")
    backtracking_time = time.time() - start_time
    
    # Test iterative approach
    start_time = time.time()
    for _ in range(1000):
        letter_combinations_with_iterative("23")
    iterative_time = time.time() - start_time
    
    print(f"Backtracking approach: {backtracking_time:.6f} seconds")
    print(f"Iterative approach: {iterative_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Create mapping from digits to letters")
    print("2. If digits is empty, return empty list")
    print("3. Use backtracking to generate combinations:")
    print("   - Base case: if index equals length of digits, add current combination")
    print("   - For each letter corresponding to current digit:")
    print("     - Add letter to current combination")
    print("     - Recurse with next digit")
    print("     - Remove letter from current combination (backtrack)")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    digits = "23"
    print(f"Digits: {digits}")
    print("\nSteps:")
    print("1. Start with empty combination: ''")
    print("2. Process digit '2' with letters 'abc':")
    print("   - Try 'a': combination = 'a'")
    print("   - Try 'b': combination = 'b'")
    print("   - Try 'c': combination = 'c'")
    print("3. Process digit '3' with letters 'def':")
    print("   - For 'a': try 'd', 'e', 'f' -> 'ad', 'ae', 'af'")
    print("   - For 'b': try 'd', 'e', 'f' -> 'bd', 'be', 'bf'")
    print("   - For 'c': try 'd', 'e', 'f' -> 'cd', 'ce', 'cf'")
    print("Final result: ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']")
    
    # Test with different digit patterns
    print("\nDifferent digit patterns:")
    test_digits = ["2", "23", "234", "2345", "9", "79", "23456789"]
    
    for digits in test_digits:
        result = letter_combinations(digits)
        print(f"Digits: '{digits}' -> {len(result)} combinations")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        "",
        "2",
        "9",
        "23",
        "234",
        "2345",
    ]
    
    for digits in edge_cases:
        result = letter_combinations(digits)
        print(f"Digits: '{digits}' -> {len(result)} combinations: {result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for digits, _ in test_cases[:5]:
        stats = letter_combinations_with_stats(digits)
        print(f"Digits: '{digits}'")
        print(f"  Combinations: {stats['combinations']}")
        print(f"  Total combinations: {stats['total_combinations']}")
        print(f"  Digits processed: {stats['digits_processed']}")
        print(f"  Letters per digit: {stats['letters_per_digit']}")
        print()
