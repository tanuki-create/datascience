# Problem 46: 3Sum Closest

## Difficulty: Medium

## Problem Statement

Given an integer array `nums` of length `n` and an integer `target`, find three integers in `nums` such that the sum is closest to `target`. Return the sum of the three integers.

You may assume that each input would have exactly one solution.

## Examples

### Example 1:
```
Input: nums = [-1,2,1,-4], target = 1
Output: 2
Explanation: The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).
```

### Example 2:
```
Input: nums = [0,0,0], target = 1
Output: 0
```

## Constraints

- `3 <= nums.length <= 1000`
- `-1000 <= nums[i] <= 1000`
- `-10^4 <= target <= 10^4`

## Approach

### Two Pointers Technique

1. **Sort Array**: First sort the array to enable two-pointer technique.
2. **Fix First Element**: For each element at position `i`, treat it as the first element of the triplet.
3. **Two Pointers**: Use two pointers (`left` and `right`) to find the remaining two elements.
4. **Track Closest**: Keep track of the sum closest to the target.

### Algorithm Steps

1. Sort the input array
2. Initialize closest sum to a large value
3. For each element at position `i`:
   - Use two pointers: `left = i + 1`, `right = len(nums) - 1`
   - While `left < right`:
     - Calculate sum of three elements
     - If sum is closer to target, update closest sum
     - If sum < target, move left pointer right
     - If sum > target, move right pointer left
4. Return closest sum

## Time Complexity

- **Time**: O(n²) where n is the length of the array
- **Space**: O(1) excluding the output

## Space Complexity

- **Space**: O(1) - constant extra space for pointers

## Key Insights

- Sorting enables the two-pointer technique
- Fixing one element reduces the problem to 2Sum
- Track the closest sum instead of exact matches
- Two-pointer technique is efficient for sorted arrays

## Solution Code

```python
def threeSumClosest(nums, target):
    """
    Find three integers whose sum is closest to target using two-pointer technique.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        int: Sum of three integers closest to target
    """
    nums.sort()
    closest_sum = float('inf')
    
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            # Update closest sum if current is closer to target
            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum
            
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                return current_sum  # Exact match found
    
    return closest_sum
```

## Test Cases

### Test Case 1: Basic Example
```
Input: nums = [-1,2,1,-4], target = 1
Output: 2
```

### Test Case 2: Exact Match
```
Input: nums = [0,0,0], target = 1
Output: 0
```

### Test Case 3: Negative Target
```
Input: nums = [1,1,1,0], target = -100
Output: 2
```

### Test Case 4: Large Target
```
Input: nums = [1,1,1,0], target = 100
Output: 3
```

### Test Case 5: Edge Case
```
Input: nums = [1,1,1,0], target = 1
Output: 2
```

## Follow-up Questions

1. **What if we need to find the indices of the three integers?**
   - Track the indices along with the closest sum
   - Return the indices of the three integers that form the closest sum

2. **What if we need to find all triplets with the closest sum?**
   - Collect all triplets that form the closest sum
   - Return list of all triplets with closest sum

3. **What if we need to find the closest sum within a tolerance?**
   - Check if the closest sum is within the tolerance
   - Return the closest sum only if it's within tolerance

## Related Problems

- 3Sum
- Two Sum
- 3Sum Smaller
- 4Sum
- Two Sum II - Input Array Is Sorted
