# Problem 89: Edit Distance

## Description

Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`.

You have the following three operations permitted on a word:

1. Insert a character
2. Delete a character
3. Replace a character

## Examples

### Example 1:
```
Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation: 
horse -> rorse (replace 'h' with 'r')
rorse -> rose (remove 'r')
rose -> ros (remove 'e')
```

### Example 2:
```
Input: word1 = "intention", word2 = "execution"
Output: 5
Explanation: 
intention -> inention (remove 't')
inention -> enention (replace 'i' with 'e')
enention -> exention (replace 'n' with 'x')
exention -> exection (replace 'n' with 'c')
exection -> execution (insert 'u')
```

### Example 3:
```
Input: word1 = "abc", word2 = "abc"
Output: 0
Explanation: No operations needed.
```

### Example 4:
```
Input: word1 = "", word2 = ""
Output: 0
Explanation: Both strings are empty.
```

### Example 5:
```
Input: word1 = "abc", word2 = ""
Output: 3
Explanation: Remove all characters from word1.
```

### Example 6:
```
Input: word1 = "", word2 = "abc"
Output: 3
Explanation: Insert all characters to word1.
```

## Constraints

- 0 <= word1.length, word2.length <= 500
- word1 and word2 consist of only lowercase English letters.

## Follow-up

Can you solve it in O(m * n) time complexity and O(m * n) space complexity?

## Hints

1. Think about the state transition in dynamic programming.
2. Consider what happens when characters match vs when they don't match.
3. The base cases are when one string is empty.
4. You can optimize space complexity to O(min(m, n)).

## Solution Approach

### Approach 1: Dynamic Programming (2D Array)

1. **State Definition**: `dp[i][j]` represents the minimum number of operations to convert the first `i` characters of `word1` to the first `j` characters of `word2`.

2. **Base Cases**:
   - `dp[i][0] = i` (delete all characters from word1)
   - `dp[0][j] = j` (insert all characters to word1)

3. **State Transition**:
   - If `word1[i-1] == word2[j-1]`: `dp[i][j] = dp[i-1][j-1]` (no operation needed)
   - If `word1[i-1] != word2[j-1]`: `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`
     - `dp[i-1][j]`: delete character from word1
     - `dp[i][j-1]`: insert character to word1
     - `dp[i-1][j-1]`: replace character in word1

4. **Time Complexity**: O(m * n)
5. **Space Complexity**: O(m * n)

### Approach 2: Space-Optimized Dynamic Programming

1. **Space Optimization**: Use only two rows instead of the full 2D array.
2. **Time Complexity**: O(m * n)
3. **Space Complexity**: O(min(m, n))

## Algorithm Steps

1. Initialize a 2D DP array of size (m+1) x (n+1)
2. Set base cases: dp[i][0] = i and dp[0][j] = j
3. Fill the DP table using the state transition
4. Return dp[m][n]

## Edge Cases

1. Both strings are empty
2. One string is empty
3. Both strings are identical
4. One string is a substring of the other
5. Strings have no common characters

## Test Cases

```python
# Test case 1: Basic example
word1 = "horse"
word2 = "ros"
# Expected output: 3

# Test case 2: Longer strings
word1 = "intention"
word2 = "execution"
# Expected output: 5

# Test case 3: Identical strings
word1 = "abc"
word2 = "abc"
# Expected output: 0

# Test case 4: Empty strings
word1 = ""
word2 = ""
# Expected output: 0

# Test case 5: One empty string
word1 = "abc"
word2 = ""
# Expected output: 3

# Test case 6: One empty string
word1 = ""
word2 = "abc"
# Expected output: 3

# Test case 7: No common characters
word1 = "abc"
word2 = "def"
# Expected output: 3

# Test case 8: One character difference
word1 = "abc"
word2 = "ab"
# Expected output: 1

# Test case 9: One character difference
word1 = "ab"
word2 = "abc"
# Expected output: 1

# Test case 10: Single characters
word1 = "a"
word2 = "b"
# Expected output: 1
```

## Complexity Analysis

- **Time Complexity**: O(m * n) where m and n are the lengths of the strings
- **Space Complexity**: O(m * n) for the standard approach, O(min(m, n)) for the optimized approach

## Related Problems

- [LeetCode 72: Edit Distance](https://leetcode.com/problems/edit-distance/)
- [LeetCode 583: Delete Operation for Two Strings](https://leetcode.com/problems/delete-operation-for-two-strings/)
- [LeetCode 712: Minimum ASCII Delete Sum for Two Strings](https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/)

## Tags

- Dynamic Programming
- String
- Edit Distance
- Levenshtein Distance
- String Matching
- Algorithm
- Hard
