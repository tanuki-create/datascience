# Problem 84: Longest Valid Parentheses

## Difficulty: Hard

## Problem Statement

Given a string containing just the characters `'('` and `')'`, find the length of the longest valid (well-formed) parentheses substring.

## Examples

### Example 1:
```
Input: s = "(()"
Output: 2
Explanation: The longest valid parentheses substring is "()".
```

### Example 2:
```
Input: s = ")()())"
Output: 4
Explanation: The longest valid parentheses substring is "()()".
```

### Example 3:
```
Input: s = ""
Output: 0
```

## Constraints

- `0 <= s.length <= 3 * 10^4`
- `s[i]` is `'('`, or `')'`.

## Approach

### Dynamic Programming

1. **State Definition**: `dp[i]` represents the length of the longest valid parentheses ending at position `i`.
2. **State Transition**: 
   - If `s[i] == '('`, then `dp[i] = 0` (cannot form valid parentheses ending with '(')
   - If `s[i] == ')'`:
     - If `s[i-1] == '('`, then `dp[i] = dp[i-2] + 2`
     - If `s[i-1] == ')'` and `s[i-dp[i-1]-1] == '('`, then `dp[i] = dp[i-1] + dp[i-dp[i-1]-2] + 2`
3. **Base Case**: `dp[0] = 0`
4. **Result**: Maximum value in the dp array

### Algorithm Steps

1. Initialize dp array with zeros
2. For each position i:
   - If s[i] == '(', set dp[i] = 0
   - If s[i] == ')':
     - Check if it forms a valid pair with previous character
     - Update dp[i] accordingly
3. Return the maximum value in dp array

## Time Complexity

- **Time**: O(n) where n is the length of the string
- **Space**: O(n) for the dp array

## Space Complexity

- **Space**: O(n) - space for the dp array

## Key Insights

- Use dynamic programming to track the longest valid parentheses ending at each position
- Handle two cases: immediate pair and nested pair
- The result is the maximum value in the dp array

## Solution Code

```python
def longestValidParentheses(s):
    """
    Find the length of the longest valid parentheses substring using DP.
    
    Args:
        s: Input string containing parentheses
        
    Returns:
        int: Length of the longest valid parentheses substring
    """
    if not s:
        return 0
    
    n = len(s)
    dp = [0] * n
    max_length = 0
    
    for i in range(1, n):
        if s[i] == ')':
            if s[i-1] == '(':
                # Immediate pair
                dp[i] = (dp[i-2] if i >= 2 else 0) + 2
            elif i - dp[i-1] > 0 and s[i - dp[i-1] - 1] == '(':
                # Nested pair
                dp[i] = dp[i-1] + (dp[i - dp[i-1] - 2] if i - dp[i-1] >= 2 else 0) + 2
            
            max_length = max(max_length, dp[i])
    
    return max_length
```

## Test Cases

### Test Case 1: Basic Example
```
Input: s = "(()"
Output: 2
```

### Test Case 2: Multiple Pairs
```
Input: s = ")()())"
Output: 4
```

### Test Case 3: Empty String
```
Input: s = ""
Output: 0
```

### Test Case 4: No Valid Parentheses
```
Input: s = "((("
Output: 0
```

### Test Case 5: All Valid
```
Input: s = "()()"
Output: 4
```

## Follow-up Questions

1. **What if we need to find the actual longest valid parentheses substring?**
   - Track the start and end indices along with the length
   - Return the substring instead of just the length

2. **What if we need to find all valid parentheses substrings?**
   - Collect all valid substrings found
   - Return list of all valid substrings

3. **What if we need to find the number of valid parentheses substrings?**
   - Count the number of valid substrings instead of finding the longest
   - Return the count of valid substrings

## Related Problems

- Valid Parentheses
- Generate Parentheses
- Remove Invalid Parentheses
- Minimum Add to Make Parentheses Valid
- Check If a Parentheses String Can Be Valid
