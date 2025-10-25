# Problem 81: Merge k Sorted Lists

## Difficulty: Hard

## Problem Statement

You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

## Examples

### Example 1:
```
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted list:
1->1->2->3->4->4->5->6
```

### Example 2:
```
Input: lists = []
Output: []
```

### Example 3:
```
Input: lists = [[]]
Output: []
```

## Constraints

- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `lists[i]` is sorted in ascending order.
- The sum of `lists[i].length` won't exceed `10^4`.

## Approach

### Divide and Conquer

1. **Base Case**: If there are 0 or 1 lists, return the list or empty list.
2. **Divide**: Split the array of lists into two halves.
3. **Conquer**: Recursively merge the two halves.
4. **Combine**: Merge the two sorted lists from the recursive calls.

### Algorithm Steps

1. If k <= 1, return the list or empty list
2. Split the array into two halves
3. Recursively merge the left half
4. Recursively merge the right half
5. Merge the two sorted lists
6. Return the merged list

## Time Complexity

- **Time**: O(n log k) where n is the total number of nodes and k is the number of lists
- **Space**: O(log k) for the recursion stack

## Space Complexity

- **Space**: O(log k) - space for recursion stack

## Key Insights

- Use divide and conquer to reduce the problem size
- Merge two lists at a time recursively
- This approach is more efficient than merging one by one

## Solution Code

```python
def mergeKLists(lists):
    """
    Merge k sorted linked lists using divide and conquer.
    
    Args:
        lists: List of k sorted linked lists
        
    Returns:
        ListNode: Head of the merged sorted linked list
    """
    if not lists:
        return None
    
    if len(lists) == 1:
        return lists[0]
    
    # Divide the list into two halves
    mid = len(lists) // 2
    left = mergeKLists(lists[:mid])
    right = mergeKLists(lists[mid:])
    
    # Merge the two sorted lists
    return mergeTwoLists(left, right)

def mergeTwoLists(list1, list2):
    """Merge two sorted linked lists."""
    dummy = ListNode(0)
    current = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    
    current.next = list1 if list1 else list2
    return dummy.next
```

## Test Cases

### Test Case 1: Basic Example
```
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
```

### Test Case 2: Empty Input
```
Input: lists = []
Output: []
```

### Test Case 3: Single Empty List
```
Input: lists = [[]]
Output: []
```

### Test Case 4: Two Lists
```
Input: lists = [[1,2,3],[4,5,6]]
Output: [1,2,3,4,5,6]
```

### Test Case 5: Single List
```
Input: lists = [[1,2,3]]
Output: [1,2,3]
```

## Follow-up Questions

1. **What if we need to merge in-place?**
   - Modify the existing nodes instead of creating new ones
   - Use the same approach but modify pointers

2. **What if we need to merge with a specific order?**
   - Modify the comparison logic
   - Handle different sorting criteria

3. **What if we need to merge k lists with different priorities?**
   - Use a priority queue (heap) to always merge the smallest elements
   - This approach has O(n log k) time complexity

## Related Problems

- Merge Two Sorted Lists
- Merge Sorted Array
- Sort List
- Merge Two Binary Trees
- Merge Intervals
