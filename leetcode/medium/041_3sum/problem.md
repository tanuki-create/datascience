# Problem 41: 3Sum

## Difficulty: Medium

## Problem Statement

Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

Notice that the solution set must not contain duplicate triplets.

## Examples

### Example 1:
```
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.
```

### Example 2:
```
Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.
```

### Example 3:
```
Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.
```

## Constraints

- `3 <= nums.length <= 3000`
- `-10^5 <= nums[i] <= 10^5`

## Approach

### Two Pointers Technique

1. **Sort Array**: First sort the array to enable two-pointer technique and avoid duplicates.
2. **Fix First Element**: For each element at position `i`, treat it as the first element of the triplet.
3. **Two Pointers**: Use two pointers (`left` and `right`) to find the remaining two elements.
4. **Skip Duplicates**: Skip duplicate elements to avoid duplicate triplets.
5. **Sum Check**: If the sum equals 0, add the triplet to the result.

### Algorithm Steps

1. Sort the input array
2. For each element at position `i`:
   - Skip if it's the same as the previous element (avoid duplicates)
   - Use two pointers: `left = i + 1`, `right = len(nums) - 1`
   - While `left < right`:
     - Calculate sum of three elements
     - If sum == 0, add triplet and skip duplicates
     - If sum < 0, move left pointer right
     - If sum > 0, move right pointer left
3. Return all unique triplets

## Time Complexity

- **Time**: O(n²) where n is the length of the array
- **Space**: O(1) excluding the output array

## Space Complexity

- **Space**: O(1) - constant extra space for pointers

## Key Insights

- Sorting enables the two-pointer technique
- Fixing one element reduces the problem to 2Sum
- Skip duplicates to avoid duplicate triplets
- Two-pointer technique is efficient for sorted arrays

## Solution Code

```python
def threeSum(nums):
    """
    Find all unique triplets that sum to zero using two-pointer technique.
    
    Args:
        nums: List of integers
        
    Returns:
        list: List of unique triplets that sum to zero
    """
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for the second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for the third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    
    return result
```

## Test Cases

### Test Case 1: Basic Example
```
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
```

### Test Case 2: No Solution
```
Input: nums = [0,1,1]
Output: []
```

### Test Case 3: Single Solution
```
Input: nums = [0,0,0]
Output: [[0,0,0]]
```

### Test Case 4: Multiple Solutions
```
Input: nums = [-2,0,1,1,2]
Output: [[-2,0,2],[-2,1,1]]
```

### Test Case 5: Edge Case
```
Input: nums = [0,0,0,0]
Output: [[0,0,0]]
```

## Follow-up Questions

1. **What if we need to find triplets that sum to a target value?**
   - Modify the sum check to compare with target
   - Use the same two-pointer technique

2. **What if we need to find quadruplets (4Sum)?**
   - Add another nested loop
   - Use similar approach with two pointers

3. **What if we need to find the closest sum to target?**
   - Track the closest sum found
   - Update when a closer sum is found

## Related Problems

- Two Sum
- 3Sum Closest
- 4Sum
- Two Sum II - Input Array Is Sorted
- 3Sum Smaller
