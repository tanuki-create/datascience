# Problem 34: Permutation in String

## Difficulty: Easy

## Problem Statement

Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, or `false` otherwise.

In other words, return `true` if one of the first string's permutations is the substring of the second string.

## Examples

### Example 1:
```
Input: s1 = "ab", s2 = "eidbaooo"
Output: true
Explanation: s2 contains one permutation of s1 ("ba").
```

### Example 2:
```
Input: s1 = "ab", s2 = "eidboaoo"
Output: false
```

## Constraints

- `1 <= s1.length, s2.length <= 10^4`
- `s1` and `s2` consist of lowercase English letters only.

## Approach

### Sliding Window with Character Count

1. **Count Characters in s1**: Create a frequency map for all characters in `s1`.
2. **Sliding Window**: Use a sliding window of size `len(s1)` to check each substring in `s2`.
3. **Character Matching**: For each window, check if the character frequencies match `s1`.
4. **Early Return**: If a match is found, return `true` immediately.

### Algorithm Steps

1. Create frequency map for string `s1`
2. Initialize sliding window pointers
3. For each position in `s2`:
   - Check if current window matches `s1` frequencies
   - If match found, return `true`
   - Move window to next position
4. Return `false` if no match found

## Time Complexity

- **Time**: O(n + m) where n is length of `s2` and m is length of `s1`
- **Space**: O(1) since we use fixed-size arrays for character counting

## Space Complexity

- **Space**: O(1) - constant space for character frequency arrays

## Key Insights

- Use sliding window technique to efficiently check all possible substrings
- Character frequency comparison is the key to identifying permutations
- Fixed-size arrays (26 elements for lowercase letters) provide O(1) space complexity
- Early return optimization when match is found

## Solution Code

```python
def checkInclusion(s1, s2):
    """
    Check if s2 contains a permutation of s1 using sliding window technique.
    
    Args:
        s1: The string to find permutation of
        s2: The string to search in
        
    Returns:
        bool: True if s2 contains a permutation of s1
    """
    if len(s1) > len(s2):
        return False
    
    # Count characters in s1
    s1_count = [0] * 26
    for char in s1:
        s1_count[ord(char) - ord('a')] += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(s1)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s2[i]) - ord('a')] += 1
    
    # Check first window
    if window_count == s1_count:
        return True
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s2)):
        # Remove leftmost character
        window_count[ord(s2[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s2[i]) - ord('a')] += 1
        
        # Check if current window matches s1
        if window_count == s1_count:
            return True
    
    return False
```

## Test Cases

### Test Case 1: Basic Example
```
Input: s1 = "ab", s2 = "eidbaooo"
Output: true
```

### Test Case 2: No Permutation
```
Input: s1 = "ab", s2 = "eidboaoo"
Output: false
```

### Test Case 3: Single Character
```
Input: s1 = "a", s2 = "ab"
Output: true
```

### Test Case 4: Same String
```
Input: s1 = "ab", s2 = "ab"
Output: true
```

### Test Case 5: Edge Case
```
Input: s1 = "ab", s2 = "a"
Output: false
```

## Follow-up Questions

1. **What if the strings contain uppercase letters?**
   - Convert to lowercase before processing
   - Use 52-element array for both cases

2. **What if we need to find the longest permutation substring?**
   - Use sliding window with variable size
   - Track maximum length found

3. **What if we need to find all permutation substrings?**
   - Return list of start indices instead of boolean
   - Use similar approach but collect all matches

## Related Problems

- Find All Anagrams in String
- Valid Anagram
- Group Anagrams
- Sliding Window Maximum
- Longest Substring Without Repeating Characters
