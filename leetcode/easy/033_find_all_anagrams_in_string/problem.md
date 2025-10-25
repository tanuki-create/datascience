# Problem 33: Find All Anagrams in String

## Difficulty: Easy

## Problem Statement

Given two strings `s` and `p`, return an array of all the start indices of `p`'s anagrams in `s`. You may return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

## Examples

### Example 1:
```
Input: s = "cbaebabacd", p = "abc"
Output: [0,6]
Explanation:
The substring with start index = 0 is "cba", which is an anagram of "abc".
The substring with start index = 6 is "bac", which is an anagram of "abc".
```

### Example 2:
```
Input: s = "abab", p = "ab"
Output: [0,1,2]
Explanation:
The substring with start index = 0 is "ab", which is an anagram of "ab".
The substring with start index = 1 is "ba", which is an anagram of "ab".
The substring with start index = 2 is "ab", which is an anagram of "ab".
```

## Constraints

- `1 <= s.length, p.length <= 3 * 10^4`
- `s` and `p` consist of lowercase English letters only.

## Approach

### Sliding Window with Character Count

1. **Count Characters in Pattern**: Create a frequency map for all characters in `p`.
2. **Sliding Window**: Use a sliding window of size `len(p)` to check each substring in `s`.
3. **Character Matching**: For each window, check if the character frequencies match the pattern.
4. **Result Collection**: If frequencies match, add the start index to the result.

### Algorithm Steps

1. Create frequency map for pattern `p`
2. Initialize sliding window pointers
3. For each position in `s`:
   - Check if current window matches pattern frequencies
   - If match found, add start index to result
   - Move window to next position
4. Return all start indices

## Time Complexity

- **Time**: O(n + m) where n is length of `s` and m is length of `p`
- **Space**: O(1) since we use fixed-size arrays for character counting

## Space Complexity

- **Space**: O(1) - constant space for character frequency arrays

## Key Insights

- Use sliding window technique to efficiently check all possible substrings
- Character frequency comparison is the key to identifying anagrams
- Fixed-size arrays (26 elements for lowercase letters) provide O(1) space complexity

## Solution Code

```python
def findAnagrams(s, p):
    """
    Find all anagrams of p in s using sliding window technique.
    
    Args:
        s: The main string to search in
        p: The pattern string to find anagrams of
        
    Returns:
        list: List of start indices where anagrams are found
    """
    if len(p) > len(s):
        return []
    
    # Count characters in pattern
    p_count = [0] * 26
    for char in p:
        p_count[ord(char) - ord('a')] += 1
    
    # Initialize sliding window
    window_count = [0] * 26
    window_size = len(p)
    
    # Initialize first window
    for i in range(window_size):
        window_count[ord(s[i]) - ord('a')] += 1
    
    result = []
    
    # Check first window
    if window_count == p_count:
        result.append(0)
    
    # Slide window through the rest of the string
    for i in range(window_size, len(s)):
        # Remove leftmost character
        window_count[ord(s[i - window_size]) - ord('a')] -= 1
        # Add new character
        window_count[ord(s[i]) - ord('a')] += 1
        
        # Check if current window matches pattern
        if window_count == p_count:
            result.append(i - window_size + 1)
    
    return result
```

## Test Cases

### Test Case 1: Basic Example
```
Input: s = "cbaebabacd", p = "abc"
Output: [0,6]
```

### Test Case 2: Multiple Anagrams
```
Input: s = "abab", p = "ab"
Output: [0,1,2]
```

### Test Case 3: No Anagrams
```
Input: s = "abcdef", p = "xyz"
Output: []
```

### Test Case 4: Single Character
```
Input: s = "aaaa", p = "a"
Output: [0,1,2,3]
```

### Test Case 5: Edge Case
```
Input: s = "a", p = "a"
Output: [0]
```

## Follow-up Questions

1. **What if the strings contain uppercase letters?**
   - Convert to lowercase before processing
   - Use 52-element array for both cases

2. **What if we need to find the longest anagram substring?**
   - Use sliding window with variable size
   - Track maximum length found

3. **What if we need to find anagrams of multiple patterns?**
   - Use a set of frequency maps
   - Check against all patterns for each window

## Related Problems

- Valid Anagram
- Group Anagrams
- Permutation in String
- Find All Duplicates in Array
- Sliding Window Maximum
