# Problem 42: Group Anagrams

## Difficulty: Medium

## Problem Statement

Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

## Examples

### Example 1:
```
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
```

### Example 2:
```
Input: strs = [""]
Output: [[""]]
```

### Example 3:
```
Input: strs = ["a"]
Output: [["a"]]
```

## Constraints

- `1 <= strs.length <= 10^4`
- `0 <= strs[i].length <= 100`
- `strs[i]` consists of lowercase English letters only.

## Approach

### Hash Map with Sorted String Key

1. **Create Hash Map**: Use a hash map where the key is the sorted version of each string.
2. **Group Strings**: For each string, sort its characters and use as the key.
3. **Collect Groups**: All strings with the same sorted key are anagrams of each other.
4. **Return Result**: Return all groups as a list of lists.

### Algorithm Steps

1. Create an empty hash map
2. For each string in the input:
   - Sort the characters of the string
   - Use the sorted string as the key
   - Add the original string to the group for that key
3. Return all groups as a list of lists

## Time Complexity

- **Time**: O(n * m * log(m)) where n is the number of strings and m is the average length of strings
- **Space**: O(n * m) for storing all strings

## Space Complexity

- **Space**: O(n * m) - space for hash map and result

## Key Insights

- Anagrams have the same sorted character sequence
- Hash map with sorted string as key efficiently groups anagrams
- Sorting characters is the key to identifying anagrams

## Solution Code

```python
def groupAnagrams(strs):
    """
    Group anagrams together using hash map with sorted string as key.
    
    Args:
        strs: List of strings to group
        
    Returns:
        list: List of groups of anagrams
    """
    from collections import defaultdict
    
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Sort characters to create key
        sorted_str = ''.join(sorted(s))
        anagram_groups[sorted_str].append(s)
    
    return list(anagram_groups.values())
```

## Test Cases

### Test Case 1: Basic Example
```
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
```

### Test Case 2: Single Empty String
```
Input: strs = [""]
Output: [[""]]
```

### Test Case 3: Single Character
```
Input: strs = ["a"]
Output: [["a"]]
```

### Test Case 4: No Anagrams
```
Input: strs = ["abc","def","ghi"]
Output: [["abc"],["def"],["ghi"]]
```

### Test Case 5: All Anagrams
```
Input: strs = ["abc","bca","cab"]
Output: [["abc","bca","cab"]]
```

## Follow-up Questions

1. **What if we need to preserve the original order?**
   - Use OrderedDict or maintain insertion order
   - Track the order of first occurrence of each group

2. **What if we need to find the largest group?**
   - Track the size of each group
   - Return the group with maximum size

3. **What if we need to find groups of a specific size?**
   - Filter groups by size
   - Return only groups with the specified size

## Related Problems

- Valid Anagram
- Find All Anagrams in String
- Group Anagrams
- Anagrams
- Group Shifted Strings
