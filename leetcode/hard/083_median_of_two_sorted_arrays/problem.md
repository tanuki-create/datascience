# Problem 83: Median of Two Sorted Arrays

## Difficulty: Hard

## Problem Statement

Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.

The overall run time complexity should be `O(log (m+n))`.

## Examples

### Example 1:
```
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
```

### Example 2:
```
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
```

## Constraints

- `nums1.length == m`
- `nums2.length == n`
- `0 <= m <= 1000`
- `0 <= n <= 1000`
- `1 <= m + n <= 2000`
- `-10^6 <= nums1[i], nums2[i] <= 10^6`

## Approach

### Binary Search

1. **Ensure nums1 is smaller**: If nums1 is larger, swap the arrays.
2. **Binary Search**: Use binary search on the smaller array to find the correct partition.
3. **Partition Check**: For each partition, check if it's valid (left elements <= right elements).
4. **Calculate Median**: Once the correct partition is found, calculate the median.

### Algorithm Steps

1. Ensure nums1 is the smaller array
2. Use binary search on nums1 to find the correct partition
3. For each partition:
   - Calculate left and right parts of both arrays
   - Check if the partition is valid
   - If valid, calculate and return the median
   - If not, adjust the search range

## Time Complexity

- **Time**: O(log(min(m, n))) where m and n are the lengths of the arrays
- **Space**: O(1) for storing variables

## Space Complexity

- **Space**: O(1) - constant extra space

## Key Insights

- Use binary search on the smaller array
- Partition both arrays such that left elements <= right elements
- The median is the average of the maximum left element and minimum right element

## Solution Code

```python
def findMedianSortedArrays(nums1, nums2):
    """
    Find the median of two sorted arrays using binary search.
    
    Args:
        nums1: First sorted array
        nums2: Second sorted array
        
    Returns:
        float: Median of the two sorted arrays
    """
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    
    while left <= right:
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1
        
        # Handle edge cases
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]
        
        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]
        
        # Check if partition is correct
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found the correct partition
            if (m + n) % 2 == 0:
                return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
            else:
                return max(max_left1, max_left2)
        elif max_left1 > min_right2:
            # Move partition1 to the left
            right = partition1 - 1
        else:
            # Move partition1 to the right
            left = partition1 + 1
    
    return 0.0
```

## Test Cases

### Test Case 1: Basic Example
```
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
```

### Test Case 2: Even Length
```
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
```

### Test Case 3: Single Element
```
Input: nums1 = [1], nums2 = []
Output: 1.00000
```

### Test Case 4: Empty Arrays
```
Input: nums1 = [], nums2 = []
Output: 0.00000
```

### Test Case 5: Different Lengths
```
Input: nums1 = [1,2,3], nums2 = [4,5]
Output: 3.00000
```

## Follow-up Questions

1. **What if we need to find the kth smallest element?**
   - Modify the binary search to find the kth element
   - Use similar partitioning approach

2. **What if we need to find the median of k sorted arrays?**
   - Use divide and conquer approach
   - Merge arrays in pairs until one remains

3. **What if we need to find the median in O(1) space?**
   - Use the same approach but without extra space
   - Modify the existing arrays in-place

## Related Problems

- Find Kth Largest Element in an Array
- Merge Sorted Array
- Search in Rotated Sorted Array
- Find Minimum in Rotated Sorted Array
- Find Peak Element
