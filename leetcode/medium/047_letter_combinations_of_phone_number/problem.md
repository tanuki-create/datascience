# Problem 47: Letter Combinations of a Phone Number

## Difficulty: Medium

## Problem Statement

Given a string containing digits from `2-9` inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.

A mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.

## Examples

### Example 1:
```
Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

### Example 2:
```
Input: digits = ""
Output: []
```

### Example 3:
```
Input: digits = "2"
Output: ["a","b","c"]
```

## Constraints

- `0 <= digits.length <= 4`
- `digits[i]` is a digit in the range `['2', '9']`.

## Approach

### Backtracking

1. **Create Mapping**: Create a mapping from digits to letters.
2. **Backtracking**: Use backtracking to generate all possible combinations.
3. **Base Case**: When we've processed all digits, add the current combination to the result.
4. **Recursive Case**: For each letter corresponding to the current digit, add it to the current combination and recurse.

### Algorithm Steps

1. Create mapping from digits to letters
2. If digits is empty, return empty list
3. Use backtracking to generate combinations:
   - Base case: if index equals length of digits, add current combination
   - For each letter corresponding to current digit:
     - Add letter to current combination
     - Recurse with next digit
     - Remove letter from current combination (backtrack)

## Time Complexity

- **Time**: O(3^m * 4^n) where m is the number of digits with 3 letters and n is the number of digits with 4 letters
- **Space**: O(3^m * 4^n) for storing all combinations

## Space Complexity

- **Space**: O(3^m * 4^n) - space for all combinations

## Key Insights

- Use backtracking to generate all possible combinations
- Handle empty input case
- Use recursive approach to build combinations incrementally

## Solution Code

```python
def letterCombinations(digits):
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
```

## Test Cases

### Test Case 1: Basic Example
```
Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

### Test Case 2: Empty Input
```
Input: digits = ""
Output: []
```

### Test Case 3: Single Digit
```
Input: digits = "2"
Output: ["a","b","c"]
```

### Test Case 4: Multiple Digits
```
Input: digits = "234"
Output: ["adg","adh","adi","aeg","aeh","aei","afg","afh","afi","bdg","bdh","bdi","beg","beh","bei","bfg","bfh","bfi","cdg","cdh","cdi","ceg","ceh","cei","cfg","cfh","cfi"]
```

### Test Case 5: Edge Case
```
Input: digits = "9"
Output: ["w","x","y","z"]
```

## Follow-up Questions

1. **What if we need to find combinations of a specific length?**
   - Filter combinations by length
   - Return only combinations with specified length

2. **What if we need to find combinations that form valid words?**
   - Check combinations against a dictionary
   - Return only combinations that form valid words

3. **What if we need to find combinations with a specific pattern?**
   - Use regex or pattern matching
   - Return only combinations that match the pattern

## Related Problems

- Generate Parentheses
- Permutations
- Combinations
- Subsets
- Word Search
