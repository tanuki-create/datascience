# Problem 44: Longest Palindromic Substring

## Difficulty: Medium

## Problem Statement

Given a string `s`, return the longest palindromic substring in `s`.

## Examples

### Example 1:
```
Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.
```

### Example 2:
```
Input: s = "cbbd"
Output: "bb"
```

### Example 3:
```
Input: s = "a"
Output: "a"
```

## Constraints

- `1 <= s.length <= 1000`
- `s` consist of only digits and English letters.

## Approach

### Expand Around Centers

1. **Check All Centers**: For each possible center of a palindrome, expand outward.
2. **Handle Odd and Even Lengths**: Check both odd-length (center at character) and even-length (center between characters) palindromes.
3. **Track Longest**: Keep track of the longest palindrome found.

### Algorithm Steps

1. For each position in the string:
   - Check odd-length palindromes (center at character)
   - Check even-length palindromes (center between characters)
   - Update longest palindrome if current is longer
2. Return the longest palindrome found

## Time Complexity

- **Time**: O(n²) where n is the length of the string
- **Space**: O(1) for storing the result

## Space Complexity

- **Space**: O(1) - constant extra space

## Key Insights

- Check all possible centers for palindromes
- Handle both odd and even length palindromes
- Expand around centers to find longest palindrome

## Solution Code

```python
def longestPalindrome(s):
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
```

## Test Cases

### Test Case 1: Basic Example
```
Input: s = "babad"
Output: "bab"
```

### Test Case 2: Even Length
```
Input: s = "cbbd"
Output: "bb"
```

### Test Case 3: Single Character
```
Input: s = "a"
Output: "a"
```

### Test Case 4: No Palindrome
```
Input: s = "abc"
Output: "a"
```

### Test Case 5: Long Palindrome
```
Input: s = "racecar"
Output: "racecar"
```

## Follow-up Questions

1. **What if we need to find all palindromic substrings?**
   - Modify to collect all palindromes found
   - Return list of all palindromic substrings

2. **What if we need to find the number of palindromic substrings?**
   - Count palindromes instead of tracking longest
   - Return count of all palindromic substrings

3. **What if we need to find palindromes of a specific length?**
   - Filter palindromes by length
   - Return palindromes with specified length

## Related Problems

- Longest Palindromic Subsequence
- Palindromic Substrings
- Valid Palindrome
- Palindrome Number
- Shortest Palindrome
