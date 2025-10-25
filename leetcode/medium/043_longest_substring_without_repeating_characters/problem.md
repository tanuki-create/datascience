# Problem 43: Longest Substring Without Repeating Characters

## Difficulty: Medium

## Problem Statement

Given a string `s`, find the length of the longest substring without repeating characters.

## Examples

### Example 1:
```
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
```

### Example 2:
```
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
```

### Example 3:
```
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
```

## Constraints

- `0 <= s.length <= 5 * 10^4`
- `s` consists of English letters, digits, symbols and spaces.

## Approach

### Sliding Window with Hash Set

1. **Initialize Variables**: Use two pointers (`left` and `right`) and a hash set to track characters.
2. **Expand Window**: Move the right pointer and add characters to the set.
3. **Contract Window**: When a duplicate is found, move the left pointer until the duplicate is removed.
4. **Track Maximum**: Keep track of the maximum length found.

### Algorithm Steps

1. Initialize left pointer, right pointer, and hash set
2. For each character at right pointer:
   - If character is not in set, add it and move right pointer
   - If character is in set, remove characters from left until duplicate is removed
   - Update maximum length
3. Return maximum length

## Time Complexity

- **Time**: O(n) where n is the length of the string
- **Space**: O(min(m, n)) where m is the size of the character set

## Space Complexity

- **Space**: O(min(m, n)) - space for hash set

## Key Insights

- Use sliding window technique to efficiently find longest substring
- Hash set provides O(1) lookup for character checking
- Two pointers maintain the window boundaries

## Solution Code

```python
def lengthOfLongestSubstring(s):
    """
    Find the length of the longest substring without repeating characters.
    
    Args:
        s: Input string
        
    Returns:
        int: Length of the longest substring without repeating characters
    """
    if not s:
        return 0
    
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # If character is already in set, remove characters from left
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character to set
        char_set.add(s[right])
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

## Test Cases

### Test Case 1: Basic Example
```
Input: s = "abcabcbb"
Output: 3
```

### Test Case 2: Single Character
```
Input: s = "bbbbb"
Output: 1
```

### Test Case 3: Mixed Characters
```
Input: s = "pwwkew"
Output: 3
```

### Test Case 4: Empty String
```
Input: s = ""
Output: 0
```

### Test Case 5: Single Character
```
Input: s = "a"
Output: 1
```

## Follow-up Questions

1. **What if we need to return the actual substring?**
   - Track the start and end indices of the longest substring
   - Return the substring instead of just the length

2. **What if we need to find all longest substrings?**
   - Track all substrings with maximum length
   - Return list of all longest substrings

3. **What if we need to find the longest substring with at most k distinct characters?**
   - Use sliding window with character count
   - Maintain count of distinct characters

## Related Problems

- Longest Substring with At Most Two Distinct Characters
- Longest Substring with At Most K Distinct Characters
- Longest Substring with At Most K Distinct Characters
- Longest Substring with At Most K Distinct Characters
- Longest Substring with At Most K Distinct Characters
