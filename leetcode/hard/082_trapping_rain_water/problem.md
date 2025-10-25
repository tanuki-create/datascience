# Problem 82: Trapping Rain Water

## Difficulty: Hard

## Problem Statement

Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

## Examples

### Example 1:
```
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.
```

### Example 2:
```
Input: height = [4,2,0,3,2,5]
Output: 9
```

## Constraints

- `n == height.length`
- `1 <= n <= 2 * 10^4`
- `0 <= height[i] <= 10^5`

## Approach

### Two Pointers Technique

1. **Initialize Pointers**: Use two pointers at the start and end of the array.
2. **Track Maximums**: Keep track of the maximum height seen from left and right.
3. **Calculate Water**: For each position, the water trapped is the minimum of left and right maximums minus the current height.
4. **Move Pointers**: Move the pointer pointing to the smaller maximum.

### Algorithm Steps

1. Initialize left pointer, right pointer, left max, and right max
2. While left < right:
   - If left max < right max:
     - Move left pointer
     - Update left max
     - Add water trapped at left position
   - Else:
     - Move right pointer
     - Update right max
     - Add water trapped at right position
3. Return total water trapped

## Time Complexity

- **Time**: O(n) where n is the length of the array
- **Space**: O(1) for storing variables

## Space Complexity

- **Space**: O(1) - constant extra space

## Key Insights

- Use two pointers to efficiently calculate trapped water
- Water trapped at each position depends on the minimum of left and right maximums
- Move the pointer pointing to the smaller maximum

## Solution Code

```python
def trap(height):
    """
    Calculate trapped rainwater using two-pointer technique.
    
    Args:
        height: List of heights
        
    Returns:
        int: Total amount of water trapped
    """
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += max(0, left_max - height[left])
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += max(0, right_max - height[right])
    
    return water
```

## Test Cases

### Test Case 1: Basic Example
```
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
```

### Test Case 2: Simple Case
```
Input: height = [4,2,0,3,2,5]
Output: 9
```

### Test Case 3: No Water
```
Input: height = [1,2,3,4,5]
Output: 0
```

### Test Case 4: Single Bar
```
Input: height = [5]
Output: 0
```

### Test Case 5: Empty Array
```
Input: height = []
Output: 0
```

## Follow-up Questions

1. **What if we need to find the positions where water is trapped?**
   - Track the positions along with the water amount
   - Return list of positions and water amounts

2. **What if we need to find the maximum water that can be trapped?**
   - Use the same approach but track the maximum
   - Return the maximum water trapped

3. **What if we need to find the water trapped in a specific range?**
   - Modify the algorithm to work within a range
   - Return water trapped in the specified range

## Related Problems

- Container With Most Water
- Largest Rectangle in Histogram
- Maximum Product Subarray
- Two Sum
- 3Sum
