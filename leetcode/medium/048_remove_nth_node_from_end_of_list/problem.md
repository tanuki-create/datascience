# Problem 48: Remove Nth Node From End of List

## Difficulty: Medium

## Problem Statement

Given the head of a linked list, remove the nth node from the end of the list and return its head.

## Examples

### Example 1:
```
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
```

### Example 2:
```
Input: head = [1], n = 1
Output: []
```

### Example 3:
```
Input: head = [1,2], n = 1
Output: [1]
```

## Constraints

- The number of nodes in the list is `sz`.
- `1 <= sz <= 30`
- `0 <= Node.val <= 100`
- `1 <= n <= sz`

## Approach

### Two Pointers Technique

1. **Create Dummy Node**: Create a dummy node to handle edge cases.
2. **Two Pointers**: Use two pointers with a gap of n nodes.
3. **Move Pointers**: Move both pointers until the first pointer reaches the end.
4. **Remove Node**: Remove the nth node from the end.

### Algorithm Steps

1. Create a dummy node and point it to the head
2. Initialize two pointers: first and second
3. Move first pointer n steps ahead
4. Move both pointers until first reaches the end
5. Remove the node after second pointer
6. Return the head of the modified list

## Time Complexity

- **Time**: O(L) where L is the length of the linked list
- **Space**: O(1) for storing variables

## Space Complexity

- **Space**: O(1) - constant extra space

## Key Insights

- Use two pointers with a gap of n nodes
- Dummy node helps handle edge cases
- Move first pointer n steps ahead, then move both together

## Solution Code

```python
def removeNthFromEnd(head, n):
    """
    Remove the nth node from the end of the linked list.
    
    Args:
        head: Head of the linked list
        n: Position from the end to remove
        
    Returns:
        ListNode: Head of the modified linked list
    """
    # Create dummy node to handle edge cases
    dummy = ListNode(0)
    dummy.next = head
    
    # Initialize two pointers
    first = dummy
    second = dummy
    
    # Move first pointer n steps ahead
    for _ in range(n + 1):
        first = first.next
    
    # Move both pointers until first reaches the end
    while first:
        first = first.next
        second = second.next
    
    # Remove the node after second pointer
    second.next = second.next.next
    
    return dummy.next
```

## Test Cases

### Test Case 1: Basic Example
```
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
```

### Test Case 2: Single Node
```
Input: head = [1], n = 1
Output: []
```

### Test Case 3: Two Nodes
```
Input: head = [1,2], n = 1
Output: [1]
```

### Test Case 4: Remove First Node
```
Input: head = [1,2,3,4,5], n = 5
Output: [2,3,4,5]
```

### Test Case 5: Remove Last Node
```
Input: head = [1,2,3,4,5], n = 1
Output: [1,2,3,4]
```

## Follow-up Questions

1. **What if we need to remove multiple nodes?**
   - Use a loop to remove multiple nodes
   - Handle edge cases for each removal

2. **What if we need to remove nodes based on a condition?**
   - Check the condition for each node
   - Remove nodes that meet the condition

3. **What if we need to remove nodes in a specific range?**
   - Use two pointers to mark the range
   - Remove all nodes in the range

## Related Problems

- Remove Duplicates from Sorted List
- Remove Linked List Elements
- Delete Node in a Linked List
- Reverse Linked List
- Merge Two Sorted Lists
