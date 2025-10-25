"""
Problem 48: Remove Nth Node From End of List
Difficulty: Medium

Given the head of a linked list, remove the nth node from the end of the list 
and return its head.

Time Complexity: O(L) where L is the length of the linked list
Space Complexity: O(1) for storing variables
"""

class ListNode:
    """Definition for singly-linked list node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        return f"ListNode({self.val})"


def remove_nth_from_end(head, n):
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


def remove_nth_from_end_optimized(head, n):
    """
    Remove the nth node from the end using optimized approach.
    
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


def remove_nth_from_end_with_two_passes(head, n):
    """
    Remove the nth node from the end using two-pass approach.
    
    Args:
        head: Head of the linked list
        n: Position from the end to remove
        
    Returns:
        ListNode: Head of the modified linked list
    """
    # First pass: count the total number of nodes
    count = 0
    current = head
    while current:
        count += 1
        current = current.next
    
    # Calculate the position from the beginning
    position = count - n
    
    # Handle edge case: remove the first node
    if position == 0:
        return head.next
    
    # Second pass: find and remove the node
    current = head
    for _ in range(position - 1):
        current = current.next
    
    current.next = current.next.next
    
    return head


def remove_nth_from_end_verbose(head, n):
    """
    Remove the nth node from the end with detailed step-by-step explanation.
    
    Args:
        head: Head of the linked list
        n: Position from the end to remove
        
    Returns:
        ListNode: Head of the modified linked list
    """
    print(f"Removing {n}th node from the end of the linked list")
    print(f"Original list: {list_to_array(head)}")
    
    # Create dummy node to handle edge cases
    dummy = ListNode(0)
    dummy.next = head
    print(f"Created dummy node: {dummy.val}")
    
    # Initialize two pointers
    first = dummy
    second = dummy
    print(f"Initialized pointers: first={first.val}, second={second.val}")
    
    # Move first pointer n steps ahead
    print(f"Moving first pointer {n + 1} steps ahead...")
    for i in range(n + 1):
        first = first.next
        print(f"  Step {i + 1}: first = {first.val if first else None}")
    
    # Move both pointers until first reaches the end
    print("Moving both pointers until first reaches the end...")
    step = 1
    while first:
        first = first.next
        second = second.next
        print(f"  Step {step}: first = {first.val if first else None}, second = {second.val}")
        step += 1
    
    # Remove the node after second pointer
    print(f"Removing node after second pointer: {second.next.val if second.next else None}")
    second.next = second.next.next
    
    result = dummy.next
    print(f"Final result: {list_to_array(result)}")
    return result


def remove_nth_from_end_with_stats(head, n):
    """
    Remove the nth node from the end and return statistics.
    
    Args:
        head: Head of the linked list
        n: Position from the end to remove
        
    Returns:
        dict: Statistics about the operation
    """
    # Create dummy node to handle edge cases
    dummy = ListNode(0)
    dummy.next = head
    
    # Initialize two pointers
    first = dummy
    second = dummy
    
    # Move first pointer n steps ahead
    steps = 0
    for _ in range(n + 1):
        first = first.next
        steps += 1
    
    # Move both pointers until first reaches the end
    while first:
        first = first.next
        second = second.next
        steps += 1
    
    # Remove the node after second pointer
    second.next = second.next.next
    
    return {
        'result': dummy.next,
        'total_steps': steps,
        'n': n,
        'list_length': steps - n
    }


def remove_nth_from_end_with_validation(head, n):
    """
    Remove the nth node from the end with validation.
    
    Args:
        head: Head of the linked list
        n: Position from the end to remove
        
    Returns:
        dict: Detailed validation results
    """
    if not head:
        return {
            'result': None,
            'is_valid': False,
            'reason': 'Empty list'
        }
    
    if n <= 0:
        return {
            'result': head,
            'is_valid': False,
            'reason': f'Invalid n: {n} <= 0'
        }
    
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
    
    return {
        'result': dummy.next,
        'is_valid': True,
        'reason': f'Successfully removed {n}th node from the end',
        'input': head,
        'n': n
    }


def remove_nth_from_end_with_comparison(head, n):
    """
    Remove the nth node from the end and compare different approaches.
    
    Args:
        head: Head of the linked list
        n: Position from the end to remove
        
    Returns:
        dict: Comparison of different approaches
    """
    # Two-pointer approach
    two_pointer_result = remove_nth_from_end(head, n)
    
    # Two-pass approach
    two_pass_result = remove_nth_from_end_with_two_passes(head, n)
    
    return {
        'two_pointer': two_pointer_result,
        'two_pass': two_pass_result
    }


def remove_nth_from_end_with_performance(head, n):
    """
    Remove the nth node from the end with performance metrics.
    
    Args:
        head: Head of the linked list
        n: Position from the end to remove
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    start_time = time.time()
    operations = 0
    
    # Create dummy node to handle edge cases
    dummy = ListNode(0)
    dummy.next = head
    
    # Initialize two pointers
    first = dummy
    second = dummy
    
    # Move first pointer n steps ahead
    for _ in range(n + 1):
        first = first.next
        operations += 1
    
    # Move both pointers until first reaches the end
    while first:
        first = first.next
        second = second.next
        operations += 1
    
    # Remove the node after second pointer
    second.next = second.next.next
    operations += 1
    
    end_time = time.time()
    
    return {
        'result': dummy.next,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def remove_nth_from_end_with_debugging(head, n):
    """
    Remove the nth node from the end with debugging information.
    
    Args:
        head: Head of the linked list
        n: Position from the end to remove
        
    Returns:
        dict: Debugging information
    """
    if not head:
        return {
            'result': None,
            'debug_info': 'Empty list',
            'steps': 0
        }
    
    # Create dummy node to handle edge cases
    dummy = ListNode(0)
    dummy.next = head
    
    # Initialize two pointers
    first = dummy
    second = dummy
    
    # Move first pointer n steps ahead
    steps = 0
    for _ in range(n + 1):
        first = first.next
        steps += 1
    
    # Move both pointers until first reaches the end
    while first:
        first = first.next
        second = second.next
        steps += 1
    
    # Remove the node after second pointer
    second.next = second.next.next
    steps += 1
    
    return {
        'result': dummy.next,
        'debug_info': f'Processed {steps} operations',
        'steps': steps
    }


def remove_nth_from_end_with_analysis(head, n):
    """
    Remove the nth node from the end and return analysis.
    
    Args:
        head: Head of the linked list
        n: Position from the end to remove
        
    Returns:
        dict: Analysis results
    """
    if not head:
        return {
            'result': None,
            'analysis': 'Empty list',
            'efficiency': 'N/A'
        }
    
    # Create dummy node to handle edge cases
    dummy = ListNode(0)
    dummy.next = head
    
    # Initialize two pointers
    first = dummy
    second = dummy
    
    # Move first pointer n steps ahead
    total_operations = 0
    for _ in range(n + 1):
        first = first.next
        total_operations += 1
    
    # Move both pointers until first reaches the end
    while first:
        first = first.next
        second = second.next
        total_operations += 1
    
    # Remove the node after second pointer
    second.next = second.next.next
    total_operations += 1
    
    efficiency = 1.0 / total_operations if total_operations > 0 else 0.0
    
    return {
        'result': dummy.next,
        'analysis': f'Removed {n}th node from the end in {total_operations} operations',
        'efficiency': efficiency
    }


def remove_nth_from_end_with_optimization(head, n):
    """
    Remove the nth node from the end with optimization techniques.
    
    Args:
        head: Head of the linked list
        n: Position from the end to remove
        
    Returns:
        dict: Optimization results
    """
    if not head:
        return {
            'result': None,
            'optimization': 'Empty list',
            'space_saved': 0
        }
    
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
    
    # Calculate space optimization
    original_space = 1  # One node removed
    optimized_space = 0  # No extra space used
    space_saved = original_space - optimized_space
    
    return {
        'result': dummy.next,
        'optimization': f'Space saved: {space_saved} nodes',
        'space_saved': space_saved
    }


def list_to_array(head):
    """Convert linked list to array for display."""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


def array_to_list(arr):
    """Convert array to linked list."""
    if not arr:
        return None
    
    head = ListNode(arr[0])
    current = head
    
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    
    return head


# Test cases
if __name__ == "__main__":
    test_cases = [
        ([1, 2, 3, 4, 5], 2, [1, 2, 3, 5]),
        ([1], 1, []),
        ([1, 2], 1, [1]),
        ([1, 2, 3, 4, 5], 5, [2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], 1, [1, 2, 3, 4]),
        ([], 1, []),
        ([1, 2], 2, [2]),
        ([1, 2, 3], 1, [1, 2]),
        ([1, 2, 3], 2, [1, 3]),
        ([1, 2, 3], 3, [2, 3]),
    ]
    
    for i, (arr, n, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: arr={arr}, n={n}")
        
        # Test basic approach
        head = array_to_list(arr)
        result = remove_nth_from_end(head, n)
        result_arr = list_to_array(result)
        print(f"Result: {result_arr}")
        print(f"Expected: {expected}")
        print(f"Correct: {result_arr == expected}")
        
        # Test optimized approach
        head_opt = array_to_list(arr)
        result_opt = remove_nth_from_end_optimized(head_opt, n)
        result_opt_arr = list_to_array(result_opt)
        print(f"Optimized result: {result_opt_arr}")
        
        # Test two-pass approach
        head_two_pass = array_to_list(arr)
        result_two_pass = remove_nth_from_end_with_two_passes(head_two_pass, n)
        result_two_pass_arr = list_to_array(result_two_pass)
        print(f"Two-pass result: {result_two_pass_arr}")
        
        # Test with statistics
        head_stats = array_to_list(arr)
        stats = remove_nth_from_end_with_stats(head_stats, n)
        print(f"Statistics: {stats}")
        
        # Test with validation
        head_validation = array_to_list(arr)
        validation = remove_nth_from_end_with_validation(head_validation, n)
        print(f"Validation: {validation}")
        
        # Test with comparison
        head_comparison = array_to_list(arr)
        comparison = remove_nth_from_end_with_comparison(head_comparison, n)
        print(f"Comparison: {comparison}")
        
        # Test with performance
        head_performance = array_to_list(arr)
        performance = remove_nth_from_end_with_performance(head_performance, n)
        print(f"Performance: {performance}")
        
        # Test with debugging
        head_debugging = array_to_list(arr)
        debugging = remove_nth_from_end_with_debugging(head_debugging, n)
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        head_analysis = array_to_list(arr)
        analysis = remove_nth_from_end_with_analysis(head_analysis, n)
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        head_optimization = array_to_list(arr)
        optimization = remove_nth_from_end_with_optimization(head_optimization, n)
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    head = array_to_list([1, 2, 3, 4, 5])
    remove_nth_from_end_verbose(head, 2)
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    
    # Generate large linked list for testing
    def generate_large_list(length):
        """Generate a large linked list for testing."""
        head = ListNode(1)
        current = head
        for i in range(2, length + 1):
            current.next = ListNode(i)
            current = current.next
        return head
    
    large_head = generate_large_list(10000)
    n = 5000
    
    # Test two-pointer approach
    start_time = time.time()
    for _ in range(100):
        remove_nth_from_end(large_head, n)
    two_pointer_time = time.time() - start_time
    
    # Test two-pass approach
    start_time = time.time()
    for _ in range(100):
        remove_nth_from_end_with_two_passes(large_head, n)
    two_pass_time = time.time() - start_time
    
    print(f"Two-pointer approach: {two_pointer_time:.6f} seconds")
    print(f"Two-pass approach: {two_pass_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Create dummy node to handle edge cases")
    print("2. Initialize two pointers: first and second")
    print("3. Move first pointer n steps ahead")
    print("4. Move both pointers until first reaches the end")
    print("5. Remove the node after second pointer")
    print("6. Return the head of the modified list")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    head = array_to_list([1, 2, 3, 4, 5])
    n = 2
    print(f"List: {list_to_array(head)}")
    print(f"Remove {n}th node from the end")
    print("\nSteps:")
    print("1. Create dummy node: 0 -> 1 -> 2 -> 3 -> 4 -> 5")
    print("2. Move first pointer 3 steps ahead: first = 4")
    print("3. Move both pointers until first reaches end:")
    print("   - first = 5, second = 1")
    print("   - first = None, second = 2")
    print("4. Remove node after second: 2 -> 5")
    print("5. Result: 1 -> 2 -> 3 -> 5")
    
    # Test with different values of n
    print("\nDifferent values of n:")
    test_list = [1, 2, 3, 4, 5]
    for n in range(1, len(test_list) + 1):
        head = array_to_list(test_list)
        result = remove_nth_from_end(head, n)
        result_arr = list_to_array(result)
        print(f"n={n}: {test_list} -> {result_arr}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        ([], 1),
        ([1], 1),
        ([1, 2], 1),
        ([1, 2], 2),
        ([1, 2, 3], 1),
        ([1, 2, 3], 2),
        ([1, 2, 3], 3),
    ]
    
    for arr, n in edge_cases:
        head = array_to_list(arr)
        result = remove_nth_from_end(head, n)
        result_arr = list_to_array(result)
        print(f"List: {arr}, n={n} -> {result_arr}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for arr, n, _ in test_cases[:5]:
        head = array_to_list(arr)
        stats = remove_nth_from_end_with_stats(head, n)
        print(f"List: {arr}, n={n}")
        print(f"  Result: {list_to_array(stats['result'])}")
        print(f"  Total steps: {stats['total_steps']}")
        print(f"  n: {stats['n']}")
        print(f"  List length: {stats['list_length']}")
        print()
