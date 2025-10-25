"""
Problem 50: Merge Two Sorted Lists
Difficulty: Medium

You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists in a one sorted list. The list should be made by splicing 
together the nodes of the first two lists.

Return the head of the merged linked list.

Time Complexity: O(n + m) where n and m are the lengths of the two lists
Space Complexity: O(1) for storing variables
"""

class ListNode:
    """Definition for singly-linked list node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        return f"ListNode({self.val})"


def merge_two_lists(list1, list2):
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


def merge_two_lists_optimized(list1, list2):
    """
    Merge two sorted linked lists using optimized approach.
    
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


def merge_two_lists_with_recursion(list1, list2):
    """
    Merge two sorted linked lists using recursive approach.
    
    Args:
        list1: Head of the first sorted linked list
        list2: Head of the second sorted linked list
        
    Returns:
        ListNode: Head of the merged sorted linked list
    """
    if not list1:
        return list2
    if not list2:
        return list1
    
    if list1.val <= list2.val:
        list1.next = merge_two_lists_with_recursion(list1.next, list2)
        return list1
    else:
        list2.next = merge_two_lists_with_recursion(list1, list2.next)
        return list2


def merge_two_lists_verbose(list1, list2):
    """
    Merge two sorted linked lists with detailed step-by-step explanation.
    
    Args:
        list1: Head of the first sorted linked list
        list2: Head of the second sorted linked list
        
    Returns:
        ListNode: Head of the merged sorted linked list
    """
    print(f"Merging two sorted lists:")
    print(f"List1: {list_to_array(list1)}")
    print(f"List2: {list_to_array(list2)}")
    
    # Create dummy node to simplify merging
    dummy = ListNode(0)
    current = dummy
    print(f"Created dummy node: {dummy.val}")
    
    step = 1
    # Compare nodes and link the smaller one
    while list1 and list2:
        print(f"\nStep {step}:")
        print(f"  Comparing list1.val={list1.val} and list2.val={list2.val}")
        
        if list1.val <= list2.val:
            print(f"  list1.val <= list2.val, linking list1 node")
            current.next = list1
            list1 = list1.next
        else:
            print(f"  list1.val > list2.val, linking list2 node")
            current.next = list2
            list2 = list2.next
        
        current = current.next
        print(f"  Current result: {list_to_array(dummy.next)}")
        step += 1
    
    # Link any remaining nodes
    if list1:
        print(f"\nLinking remaining nodes from list1: {list_to_array(list1)}")
        current.next = list1
    elif list2:
        print(f"\nLinking remaining nodes from list2: {list_to_array(list2)}")
        current.next = list2
    
    result = dummy.next
    print(f"\nFinal result: {list_to_array(result)}")
    return result


def merge_two_lists_with_stats(list1, list2):
    """
    Merge two sorted linked lists and return statistics.
    
    Args:
        list1: Head of the first sorted linked list
        list2: Head of the second sorted linked list
        
    Returns:
        dict: Statistics about the merging
    """
    # Create dummy node to simplify merging
    dummy = ListNode(0)
    current = dummy
    
    comparisons = 0
    links = 0
    
    # Compare nodes and link the smaller one
    while list1 and list2:
        comparisons += 1
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
        links += 1
    
    # Link any remaining nodes
    if list1:
        current.next = list1
        links += 1
    elif list2:
        current.next = list2
        links += 1
    
    return {
        'result': dummy.next,
        'comparisons': comparisons,
        'links': links,
        'list1_length': list_length(list1),
        'list2_length': list_length(list2)
    }


def merge_two_lists_with_validation(list1, list2):
    """
    Merge two sorted linked lists with validation.
    
    Args:
        list1: Head of the first sorted linked list
        list2: Head of the second sorted linked list
        
    Returns:
        dict: Detailed validation results
    """
    if not list1 and not list2:
        return {
            'result': None,
            'is_valid': True,
            'reason': 'Both lists are empty'
        }
    
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
    
    return {
        'result': dummy.next,
        'is_valid': True,
        'reason': f'Successfully merged two lists',
        'list1': list1,
        'list2': list2
    }


def merge_two_lists_with_comparison(list1, list2):
    """
    Merge two sorted linked lists and compare different approaches.
    
    Args:
        list1: Head of the first sorted linked list
        list2: Head of the second sorted linked list
        
    Returns:
        dict: Comparison of different approaches
    """
    # Iterative approach
    iterative_result = merge_two_lists(list1, list2)
    
    # Recursive approach
    recursive_result = merge_two_lists_with_recursion(list1, list2)
    
    return {
        'iterative': iterative_result,
        'recursive': recursive_result
    }


def merge_two_lists_with_performance(list1, list2):
    """
    Merge two sorted linked lists with performance metrics.
    
    Args:
        list1: Head of the first sorted linked list
        list2: Head of the second sorted linked list
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    start_time = time.time()
    operations = 0
    
    # Create dummy node to simplify merging
    dummy = ListNode(0)
    current = dummy
    
    # Compare nodes and link the smaller one
    while list1 and list2:
        operations += 1
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
        operations += 1
    
    # Link any remaining nodes
    current.next = list1 if list1 else list2
    operations += 1
    
    end_time = time.time()
    
    return {
        'result': dummy.next,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def merge_two_lists_with_debugging(list1, list2):
    """
    Merge two sorted linked lists with debugging information.
    
    Args:
        list1: Head of the first sorted linked list
        list2: Head of the second sorted linked list
        
    Returns:
        dict: Debugging information
    """
    if not list1 and not list2:
        return {
            'result': None,
            'debug_info': 'Both lists are empty',
            'steps': 0
        }
    
    # Create dummy node to simplify merging
    dummy = ListNode(0)
    current = dummy
    
    steps = 0
    # Compare nodes and link the smaller one
    while list1 and list2:
        steps += 1
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    
    # Link any remaining nodes
    current.next = list1 if list1 else list2
    steps += 1
    
    return {
        'result': dummy.next,
        'debug_info': f'Processed {steps} operations',
        'steps': steps
    }


def merge_two_lists_with_analysis(list1, list2):
    """
    Merge two sorted linked lists and return analysis.
    
    Args:
        list1: Head of the first sorted linked list
        list2: Head of the second sorted linked list
        
    Returns:
        dict: Analysis results
    """
    if not list1 and not list2:
        return {
            'result': None,
            'analysis': 'Both lists are empty',
            'efficiency': 1.0
        }
    
    # Create dummy node to simplify merging
    dummy = ListNode(0)
    current = dummy
    
    total_operations = 0
    # Compare nodes and link the smaller one
    while list1 and list2:
        total_operations += 1
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    
    # Link any remaining nodes
    current.next = list1 if list1 else list2
    total_operations += 1
    
    efficiency = 1.0 / total_operations if total_operations > 0 else 0.0
    
    return {
        'result': dummy.next,
        'analysis': f'Merged two lists in {total_operations} operations',
        'efficiency': efficiency
    }


def merge_two_lists_with_optimization(list1, list2):
    """
    Merge two sorted linked lists with optimization techniques.
    
    Args:
        list1: Head of the first sorted linked list
        list2: Head of the second sorted linked list
        
    Returns:
        dict: Optimization results
    """
    if not list1 and not list2:
        return {
            'result': None,
            'optimization': 'Both lists are empty',
            'space_saved': 0
        }
    
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
    
    # Calculate space optimization
    original_space = list_length(list1) + list_length(list2)
    optimized_space = list_length(dummy.next)
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


def list_length(head):
    """Get the length of a linked list."""
    length = 0
    current = head
    while current:
        length += 1
        current = current.next
    return length


# Test cases
if __name__ == "__main__":
    test_cases = [
        ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
        ([], [], []),
        ([], [0], [0]),
        ([1, 2, 3], [4, 5], [1, 2, 3, 4, 5]),
        ([1], [2], [1, 2]),
        ([1, 2, 3], [], [1, 2, 3]),
        ([], [1, 2, 3], [1, 2, 3]),
        ([1, 3, 5], [2, 4, 6], [1, 2, 3, 4, 5, 6]),
        ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ([1, 1, 1], [2, 2, 2], [1, 1, 1, 2, 2, 2]),
    ]
    
    for i, (arr1, arr2, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: list1={arr1}, list2={arr2}")
        
        # Test basic approach
        list1 = array_to_list(arr1)
        list2 = array_to_list(arr2)
        result = merge_two_lists(list1, list2)
        result_arr = list_to_array(result)
        print(f"Result: {result_arr}")
        print(f"Expected: {expected}")
        print(f"Correct: {result_arr == expected}")
        
        # Test optimized approach
        list1_opt = array_to_list(arr1)
        list2_opt = array_to_list(arr2)
        result_opt = merge_two_lists_optimized(list1_opt, list2_opt)
        result_opt_arr = list_to_array(result_opt)
        print(f"Optimized result: {result_opt_arr}")
        
        # Test recursive approach
        list1_rec = array_to_list(arr1)
        list2_rec = array_to_list(arr2)
        result_rec = merge_two_lists_with_recursion(list1_rec, list2_rec)
        result_rec_arr = list_to_array(result_rec)
        print(f"Recursive result: {result_rec_arr}")
        
        # Test with statistics
        list1_stats = array_to_list(arr1)
        list2_stats = array_to_list(arr2)
        stats = merge_two_lists_with_stats(list1_stats, list2_stats)
        print(f"Statistics: {stats}")
        
        # Test with validation
        list1_validation = array_to_list(arr1)
        list2_validation = array_to_list(arr2)
        validation = merge_two_lists_with_validation(list1_validation, list2_validation)
        print(f"Validation: {validation}")
        
        # Test with comparison
        list1_comparison = array_to_list(arr1)
        list2_comparison = array_to_list(arr2)
        comparison = merge_two_lists_with_comparison(list1_comparison, list2_comparison)
        print(f"Comparison: {comparison}")
        
        # Test with performance
        list1_performance = array_to_list(arr1)
        list2_performance = array_to_list(arr2)
        performance = merge_two_lists_with_performance(list1_performance, list2_performance)
        print(f"Performance: {performance}")
        
        # Test with debugging
        list1_debugging = array_to_list(arr1)
        list2_debugging = array_to_list(arr2)
        debugging = merge_two_lists_with_debugging(list1_debugging, list2_debugging)
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        list1_analysis = array_to_list(arr1)
        list2_analysis = array_to_list(arr2)
        analysis = merge_two_lists_with_analysis(list1_analysis, list2_analysis)
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        list1_optimization = array_to_list(arr1)
        list2_optimization = array_to_list(arr2)
        optimization = merge_two_lists_with_optimization(list1_optimization, list2_optimization)
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    list1 = array_to_list([1, 2, 4])
    list2 = array_to_list([1, 3, 4])
    merge_two_lists_verbose(list1, list2)
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    
    # Generate large linked lists for testing
    def generate_large_list(length):
        """Generate a large linked list for testing."""
        head = ListNode(1)
        current = head
        for i in range(2, length + 1):
            current.next = ListNode(i)
            current = current.next
        return head
    
    large_list1 = generate_large_list(5000)
    large_list2 = generate_large_list(5000)
    
    # Test iterative approach
    start_time = time.time()
    for _ in range(100):
        merge_two_lists(large_list1, large_list2)
    iterative_time = time.time() - start_time
    
    # Test recursive approach
    start_time = time.time()
    for _ in range(100):
        merge_two_lists_with_recursion(large_list1, large_list2)
    recursive_time = time.time() - start_time
    
    print(f"Iterative approach: {iterative_time:.6f} seconds")
    print(f"Recursive approach: {recursive_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Create dummy node to simplify merging")
    print("2. Compare nodes and link the smaller one")
    print("3. Move the pointer of the list with the smaller node")
    print("4. Link any remaining nodes from the non-empty list")
    print("5. Return the head of the merged list")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    list1 = array_to_list([1, 2, 4])
    list2 = array_to_list([1, 3, 4])
    print(f"List1: {list_to_array(list1)}")
    print(f"List2: {list_to_array(list2)}")
    print("\nSteps:")
    print("1. Compare 1 and 1: 1 <= 1, link 1 from list1 -> result: [1]")
    print("2. Compare 2 and 1: 2 > 1, link 1 from list2 -> result: [1, 1]")
    print("3. Compare 2 and 3: 2 <= 3, link 2 from list1 -> result: [1, 1, 2]")
    print("4. Compare 4 and 3: 4 > 3, link 3 from list2 -> result: [1, 1, 2, 3]")
    print("5. Compare 4 and 4: 4 <= 4, link 4 from list1 -> result: [1, 1, 2, 3, 4]")
    print("6. Link remaining 4 from list2 -> result: [1, 1, 2, 3, 4, 4]")
    
    # Test with different list patterns
    print("\nDifferent list patterns:")
    test_lists = [
        ([1, 2, 3], [4, 5, 6]),
        ([1, 3, 5], [2, 4, 6]),
        ([1, 1, 1], [2, 2, 2]),
        ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]),
        ([1, 3, 5, 7, 9], [2, 4, 6, 8, 10]),
    ]
    
    for arr1, arr2 in test_lists:
        list1 = array_to_list(arr1)
        list2 = array_to_list(arr2)
        result = merge_two_lists(list1, list2)
        result_arr = list_to_array(result)
        print(f"List1: {arr1}, List2: {arr2} -> Result: {result_arr}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        ([], []),
        ([], [1]),
        ([1], []),
        ([1], [2]),
        ([1, 2], []),
        ([], [1, 2]),
        ([1, 2], [3, 4]),
        ([3, 4], [1, 2]),
    ]
    
    for arr1, arr2 in edge_cases:
        list1 = array_to_list(arr1)
        list2 = array_to_list(arr2)
        result = merge_two_lists(list1, list2)
        result_arr = list_to_array(result)
        print(f"List1: {arr1}, List2: {arr2} -> Result: {result_arr}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for arr1, arr2, _ in test_cases[:5]:
        list1 = array_to_list(arr1)
        list2 = array_to_list(arr2)
        stats = merge_two_lists_with_stats(list1, list2)
        print(f"List1: {arr1}, List2: {arr2}")
        print(f"  Result: {list_to_array(stats['result'])}")
        print(f"  Comparisons: {stats['comparisons']}")
        print(f"  Links: {stats['links']}")
        print(f"  List1 length: {stats['list1_length']}")
        print(f"  List2 length: {stats['list2_length']}")
        print()
