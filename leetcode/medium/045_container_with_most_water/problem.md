# Problem 45: Container With Most Water

## Difficulty: Medium

## Problem Statement

You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i`th line are `(i, 0)` and `(i, height[i])`.

Find two lines, which, together with the x-axis forms a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

## Examples

### Example 1:
```
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.
```

### Example 2:
```
Input: height = [1,1]
Output: 1
```

## Constraints

- `n == height.length`
- `2 <= n <= 10^5`
- `0 <= height[i] <= 10^4`

## Approach

### Two Pointers Technique

1. **Initialize Pointers**: Use two pointers at the start and end of the array.
2. **Calculate Area**: For each pair of lines, calculate the area of water that can be contained.
3. **Move Pointer**: Move the pointer pointing to the shorter line inward.
4. **Track Maximum**: Keep track of the maximum area found.

### Algorithm Steps

1. Initialize left pointer at 0 and right pointer at n-1
2. While left < right:
   - Calculate area = min(height[left], height[right]) * (right - left)
   - Update maximum area if current area is larger
   - Move the pointer pointing to the shorter line inward
3. Return maximum area

## Time Complexity

- **Time**: O(n) where n is the length of the array
- **Space**: O(1) for storing variables

## Space Complexity

- **Space**: O(1) - constant extra space

## Key Insights

- Use two pointers to efficiently find the maximum area
- Move the pointer pointing to the shorter line to potentially find larger areas
- The area is limited by the shorter of the two lines

## Solution Code

```python
def maxArea(height):
    """
    Find the maximum area of water that can be contained using two pointers.
    
    Args:
        height: List of integers representing heights
        
    Returns:
        int: Maximum area of water that can be contained
    """
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        # Calculate area with current two lines
        area = min(height[left], height[right]) * (right - left)
        max_area = max(max_area, area)
        
        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area
```

## Test Cases

### Test Case 1: Basic Example
```
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
```

### Test Case 2: Two Elements
```
Input: height = [1,1]
Output: 1
```

### Test Case 3: Increasing Heights
```
Input: height = [1,2,3,4,5]
Output: 6
```

### Test Case 4: Decreasing Heights
```
Input: height = [5,4,3,2,1]
Output: 6
```

### Test Case 5: Same Heights
```
Input: height = [3,3,3,3,3]
Output: 12
```

## Follow-up Questions

1. **What if we need to find the indices of the two lines?**
   - Track the indices along with the maximum area
   - Return the indices of the two lines that form the maximum area

2. **What if we need to find all pairs that form the maximum area?**
   - Collect all pairs that form the maximum area
   - Return list of all pairs with maximum area

3. **What if we need to find the area for a specific pair of lines?**
   - Calculate area for the given pair of indices
   - Return the area of water that can be contained

## Related Problems

- Trapping Rain Water
- Largest Rectangle in Histogram
- Maximum Product Subarray
- Two Sum
- 3Sum
