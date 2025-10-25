# Problem 85: Edit Distance

## Difficulty: Hard

## Problem Statement

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

## Constraints

- `0 <= word1.length, word2.length <= 500`
- `word1` and `word2` consist of only lowercase English letters.

## Approach

### Dynamic Programming

1. **State Definition**: `dp[i][j]` represents the minimum number of operations to convert `word1[0:i]` to `word2[0:j]`.
2. **State Transition**: 
   - If `word1[i-1] == word2[j-1]`, then `dp[i][j] = dp[i-1][j-1]` (no operation needed)
   - Otherwise, `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])` (insert, delete, or replace)
3. **Base Case**: `dp[0][j] = j` and `dp[i][0] = i`
4. **Result**: `dp[m][n]` where m and n are the lengths of word1 and word2

### Algorithm Steps

1. Create a 2D dp array of size (m+1) x (n+1)
2. Initialize base cases
3. Fill the dp array using the state transition
4. Return dp[m][n]

## Time Complexity

- **Time**: O(m * n) where m and n are the lengths of the strings
- **Space**: O(m * n) for the dp array

## Space Complexity

- **Space**: O(m * n) - space for the dp array

## Key Insights

- Use dynamic programming to solve the problem optimally
- The state transition handles all three operations (insert, delete, replace)
- The base cases handle empty strings

## Solution Code

```python
def minDistance(word1, word2):
    """
    Find the minimum number of operations to convert word1 to word2 using DP.
    
    Args:
        word1: First string
        word2: Second string
        
    Returns:
        int: Minimum number of operations
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill the dp array
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    return dp[m][n]
```

## Test Cases

### Test Case 1: Basic Example
```
Input: word1 = "horse", word2 = "ros"
Output: 3
```

### Test Case 2: Complex Example
```
Input: word1 = "intention", word2 = "execution"
Output: 5
```

### Test Case 3: Same Strings
```
Input: word1 = "abc", word2 = "abc"
Output: 0
```

### Test Case 4: Empty Strings
```
Input: word1 = "", word2 = ""
Output: 0
```

### Test Case 5: One Empty String
```
Input: word1 = "abc", word2 = ""
Output: 3
```

## Follow-up Questions

1. **What if we need to find the actual sequence of operations?**
   - Track the operations along with the minimum distance
   - Return the sequence of operations

2. **What if we need to find the minimum distance with different costs for operations?**
   - Modify the state transition to use different costs
   - Return the minimum cost

3. **What if we need to find the minimum distance for multiple strings?**
   - Use a different approach for multiple strings
   - Consider all possible combinations

## Related Problems

- Longest Common Subsequence
- Longest Common Substring
- Minimum Path Sum
- Unique Paths
- Climbing Stairs
