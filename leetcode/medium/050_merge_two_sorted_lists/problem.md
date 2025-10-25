# Problem 50: Merge Two Sorted Lists

## Difficulty: Medium

## Problem Statement

You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists in a one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

## Examples

### Example 1:
```
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]
```

### Example 2:
```
Input: list1 = [], list2 = []
Output: []
```

### Example 3:
```
Input: list1 = [], list2 = [0]
Output: [0]
```

## Constraints

- The number of nodes in both lists is in the range `[0, 50]`.
- `-100 <= Node.val <= 100`
- Both `list1` and `list2` are sorted in non-decreasing order.

## Approach

### Two Pointers Technique

1. **Create Dummy Node**: Create a dummy node to simplify the merging process.
2. **Compare Nodes**: Compare the values of the current nodes in both lists.
3. **Link Nodes**: Link the smaller node to the result and move the pointer.
4. **Handle Remaining**: Link any remaining nodes from the non-empty list.

### Algorithm Steps

1. Create a dummy node and a current pointer
2. While both lists are not empty:
   - Compare the values of the current nodes
   - Link the smaller node to the result
   - Move the pointer of the list with the smaller node
3. Link any remaining nodes from the non-empty list
4. Return the head of the merged list

## Time Complexity

- **Time**: O(n + m) where n and m are the lengths of the two lists
- **Space**: O(1) for storing variables

## Space Complexity

- **Space**: O(1) - constant extra space

## Key Insights

- Use dummy node to simplify the merging process
- Compare nodes and link the smaller one
- Handle remaining nodes after one list is exhausted

## Solution Code

```python
def mergeTwoLists(list1, list2):
    """
    Merge two sorted linked lists into one sorted list.
    
    Args:
        list1: Head of the first sorted linked list
        list2: Head of the second sorted linked list
        
    Returns:
        ListNode: Head of the merged sorted linked list
    """
    # Create dummy node to simplify merging
    dummy = ListNode(0)
    current = dummy
    
    # Compare nodes and link the smaller one
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    
    # Link any remaining nodes
    current.next = list1 if list1 else list2
    
    return dummy.next
```

## Test Cases

### Test Case 1: Basic Example
```
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]
```

### Test Case 2: Empty Lists
```
Input: list1 = [], list2 = []
Output: []
```

### Test Case 3: One Empty List
```
Input: list1 = [], list2 = [0]
Output: [0]
```

### Test Case 4: Different Lengths
```
Input: list1 = [1,2,3], list2 = [4,5]
Output: [1,2,3,4,5]
```

### Test Case 5: Single Nodes
```
Input: list1 = [1], list2 = [2]
Output: [1,2]
```

## Follow-up Questions

1. **What if we need to merge k sorted lists?**
   - Use divide and conquer approach
   - Merge lists in pairs until one list remains

2. **What if we need to merge in-place?**
   - Modify the existing nodes instead of creating new ones
   - Use the same approach but modify pointers

3. **What if we need to merge with a specific order?**
   - Modify the comparison logic
   - Handle different sorting criteria

## Related Problems

- Merge k Sorted Lists
- Merge Sorted Array
- Sort List
- Merge Two Binary Trees
- Merge Intervals
