# Problem 35: Remove Element

## Difficulty: Easy

## Problem Statement

Given an integer array `nums` and an integer `val`, remove all occurrences of `val` in-place. The order of the elements may be changed. Then return the number of elements in `nums` which are not equal to `val`.

Do not allocate extra space for another array. You must do this by modifying the input array in-place with O(1) extra memory.

## Examples

### Example 1:
```
Input: nums = [3,2,2,3], val = 3
Output: 2, nums = [2,2,_,_]
Explanation: Your function should return k = 2, with the first two elements of nums being 2.
It does not matter what you leave beyond the returned k (hence they are underscores).
```

### Example 2:
```
Input: nums = [0,1,2,2,3,0,4,2], val = 2
Output: 5, nums = [0,1,4,0,3,_,_,_]
Explanation: Your function should return k = 5, with the first five elements of nums being 0, 1, 3, 0, and 4.
Note that the five elements can be returned in any order.
It does not matter what you leave beyond the returned k (hence they are underscores).
```

## Constraints

- `0 <= nums.length <= 100`
- `0 <= nums[i] <= 50`
- `0 <= val <= 100`

## Approach

### Two Pointers Technique

1. **Initialize Pointers**: Use two pointers - one for reading (`i`) and one for writing (`j`).
2. **Iterate Through Array**: For each element in the array:
   - If the element is not equal to `val`, copy it to position `j` and increment `j`
   - If the element equals `val`, skip it (don't copy)
3. **Return Count**: The value of `j` represents the number of elements not equal to `val`.

### Algorithm Steps

1. Initialize write pointer `j` to 0
2. For each element at position `i`:
   - If `nums[i] != val`, copy `nums[i]` to `nums[j]` and increment `j`
   - If `nums[i] == val`, skip the element
3. Return `j` as the count of remaining elements

## Time Complexity

- **Time**: O(n) where n is the length of the array
- **Space**: O(1) - constant extra space

## Space Complexity

- **Space**: O(1) - in-place modification with constant extra space

## Key Insights

- Use two pointers to efficiently remove elements in-place
- The write pointer tracks the next position to write a valid element
- The read pointer iterates through all elements
- Elements equal to `val` are skipped, not copied

## Solution Code

```python
def removeElement(nums, val):
    """
    Remove all occurrences of val in-place and return the new length.
    
    Args:
        nums: List of integers to modify
        val: Value to remove from the array
        
    Returns:
        int: Number of elements not equal to val
    """
    j = 0  # Write pointer
    
    for i in range(len(nums)):
        if nums[i] != val:
            nums[j] = nums[i]
            j += 1
    
    return j
```

## Test Cases

### Test Case 1: Basic Example
```
Input: nums = [3,2,2,3], val = 3
Output: 2, nums = [2,2,_,_]
```

### Test Case 2: Multiple Occurrences
```
Input: nums = [0,1,2,2,3,0,4,2], val = 2
Output: 5, nums = [0,1,4,0,3,_,_,_]
```

### Test Case 3: No Occurrences
```
Input: nums = [1,2,3,4], val = 5
Output: 4, nums = [1,2,3,4]
```

### Test Case 4: All Occurrences
```
Input: nums = [2,2,2,2], val = 2
Output: 0, nums = [_,_,_,_]
```

### Test Case 5: Single Element
```
Input: nums = [1], val = 1
Output: 0, nums = [_]
```

## Follow-up Questions

1. **What if we need to preserve the original order?**
   - Use a different approach with two passes
   - First pass: count non-val elements
   - Second pass: move elements to correct positions

2. **What if we need to remove multiple values?**
   - Use a set of values to remove
   - Check if element is in the set

3. **What if we need to remove elements based on a condition?**
   - Use a function to determine if element should be removed
   - Apply the same two-pointer technique

## Related Problems

- Remove Duplicates from Sorted Array
- Move Zeroes
- Remove Duplicates from Sorted Array II
- Remove Linked List Elements
- Remove Nth Node From End of List
