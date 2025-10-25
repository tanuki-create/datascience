# Problem 49: Valid Parentheses

## Difficulty: Medium

## Problem Statement

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:

1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

## Examples

### Example 1:
```
Input: s = "()"
Output: true
```

### Example 2:
```
Input: s = "()[]{}"
Output: true
```

### Example 3:
```
Input: s = "(]"
Output: false
```

### Example 4:
```
Input: s = "([)]"
Output: false
```

### Example 5:
```
Input: s = "{[]}"
Output: true
```

## Constraints

- `1 <= s.length <= 10^4`
- `s` consists of parentheses only `'()[]{}'`.

## Approach

### Stack Data Structure

1. **Initialize Stack**: Use a stack to keep track of opening brackets.
2. **Process Characters**: For each character in the string:
   - If it's an opening bracket, push it to the stack
   - If it's a closing bracket, check if it matches the top of the stack
3. **Validation**: The string is valid if the stack is empty at the end.

### Algorithm Steps

1. Create a stack and mapping of closing to opening brackets
2. For each character in the string:
   - If it's an opening bracket, push to stack
   - If it's a closing bracket:
     - If stack is empty or top doesn't match, return false
     - Otherwise, pop from stack
3. Return true if stack is empty, false otherwise

## Time Complexity

- **Time**: O(n) where n is the length of the string
- **Space**: O(n) for the stack in the worst case

## Space Complexity

- **Space**: O(n) - space for the stack

## Key Insights

- Use stack to track opening brackets
- Check if closing brackets match the most recent opening bracket
- Stack must be empty for valid parentheses

## Solution Code

```python
def isValid(s):
    """
    Check if the string has valid parentheses using stack.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        bool: True if parentheses are valid
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:  # Closing bracket
            if not stack or stack.pop() != mapping[char]:
                return False
        else:  # Opening bracket
            stack.append(char)
    
    return len(stack) == 0
```

## Test Cases

### Test Case 1: Basic Example
```
Input: s = "()"
Output: true
```

### Test Case 2: Multiple Types
```
Input: s = "()[]{}"
Output: true
```

### Test Case 3: Invalid
```
Input: s = "(]"
Output: false
```

### Test Case 4: Nested
```
Input: s = "([)]"
Output: false
```

### Test Case 5: Valid Nested
```
Input: s = "{[]}"
Output: true
```

## Follow-up Questions

1. **What if we need to find the minimum number of insertions to make it valid?**
   - Count unmatched opening and closing brackets
   - Return the sum of unmatched brackets

2. **What if we need to find the longest valid parentheses substring?**
   - Use dynamic programming or stack approach
   - Track the length of valid substrings

3. **What if we need to generate all valid parentheses combinations?**
   - Use backtracking to generate all combinations
   - Ensure each combination is valid

## Related Problems

- Generate Parentheses
- Longest Valid Parentheses
- Remove Invalid Parentheses
- Valid Parentheses
- Minimum Add to Make Parentheses Valid
