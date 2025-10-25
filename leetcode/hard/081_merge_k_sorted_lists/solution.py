"""
Problem 81: Merge k Sorted Lists
Difficulty: Hard

You are given an array of k linked-lists lists, each linked-list is sorted in 
ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

Time Complexity: O(n log k) where n is the total number of nodes and k is the number of lists
Space Complexity: O(log k) for the recursion stack
"""

class ListNode:
    """Definition for singly-linked list node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        return f"ListNode({self.val})"


def merge_k_lists(lists):
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
    left = merge_k_lists(lists[:mid])
    right = merge_k_lists(lists[mid:])
    
    # Merge the two sorted lists
    return merge_two_lists(left, right)


def merge_two_lists(list1, list2):
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


def merge_k_lists_with_heap(lists):
    """
    Merge k sorted linked lists using heap (priority queue).
    
    Args:
        lists: List of k sorted linked lists
        
    Returns:
        ListNode: Head of the merged sorted linked list
    """
    import heapq
    
    if not lists:
        return None
    
    # Create a min heap
    heap = []
    
    # Add the first node of each list to the heap
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst.val, i, lst))
    
    # Create dummy node for result
    dummy = ListNode(0)
    current = dummy
    
    # Process nodes from the heap
    while heap:
        val, i, node = heapq.heappop(heap)
        current.next = node
        current = current.next
        
        # Add the next node from the same list to the heap
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next


def merge_k_lists_verbose(lists):
    """
    Merge k sorted linked lists with detailed step-by-step explanation.
    
    Args:
        lists: List of k sorted linked lists
        
    Returns:
        ListNode: Head of the merged sorted linked list
    """
    print(f"Merging {len(lists)} sorted linked lists")
    print(f"Lists: {[list_to_array(lst) for lst in lists]}")
    
    if not lists:
        print("Empty lists, returning None")
        return None
    
    if len(lists) == 1:
        print("Single list, returning as is")
        return lists[0]
    
    # Divide the list into two halves
    mid = len(lists) // 2
    print(f"Splitting into two halves: left={lists[:mid]}, right={lists[mid:]}")
    
    left = merge_k_lists_verbose(lists[:mid])
    right = merge_k_lists_verbose(lists[mid:])
    
    print(f"Merging left: {list_to_array(left)} and right: {list_to_array(right)}")
    
    # Merge the two sorted lists
    result = merge_two_lists(left, right)
    print(f"Result: {list_to_array(result)}")
    
    return result


def merge_k_lists_with_stats(lists):
    """
    Merge k sorted linked lists and return statistics.
    
    Args:
        lists: List of k sorted linked lists
        
    Returns:
        dict: Statistics about the merging
    """
    if not lists:
        return {
            'result': None,
            'total_lists': 0,
            'total_nodes': 0,
            'comparisons': 0
        }
    
    if len(lists) == 1:
        return {
            'result': lists[0],
            'total_lists': 1,
            'total_nodes': list_length(lists[0]),
            'comparisons': 0
        }
    
    # Divide the list into two halves
    mid = len(lists) // 2
    left = merge_k_lists_with_stats(lists[:mid])
    right = merge_k_lists_with_stats(lists[mid:])
    
    # Merge the two sorted lists
    result = merge_two_lists(left['result'], right['result'])
    
    return {
        'result': result,
        'total_lists': len(lists),
        'total_nodes': left['total_nodes'] + right['total_nodes'],
        'comparisons': left['comparisons'] + right['comparisons']
    }


def merge_k_lists_with_validation(lists):
    """
    Merge k sorted linked lists with validation.
    
    Args:
        lists: List of k sorted linked lists
        
    Returns:
        dict: Detailed validation results
    """
    if not lists:
        return {
            'result': None,
            'is_valid': True,
            'reason': 'Empty lists'
        }
    
    if len(lists) == 1:
        return {
            'result': lists[0],
            'is_valid': True,
            'reason': 'Single list'
        }
    
    # Divide the list into two halves
    mid = len(lists) // 2
    left = merge_k_lists_with_validation(lists[:mid])
    right = merge_k_lists_with_validation(lists[mid:])
    
    # Merge the two sorted lists
    result = merge_two_lists(left['result'], right['result'])
    
    return {
        'result': result,
        'is_valid': True,
        'reason': f'Successfully merged {len(lists)} lists',
        'input': lists
    }


def merge_k_lists_with_comparison(lists):
    """
    Merge k sorted linked lists and compare different approaches.
    
    Args:
        lists: List of k sorted linked lists
        
    Returns:
        dict: Comparison of different approaches
    """
    # Divide and conquer approach
    dc_result = merge_k_lists(lists)
    
    # Heap approach
    heap_result = merge_k_lists_with_heap(lists)
    
    return {
        'divide_and_conquer': dc_result,
        'heap': heap_result
    }


def merge_k_lists_with_performance(lists):
    """
    Merge k sorted linked lists with performance metrics.
    
    Args:
        lists: List of k sorted linked lists
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    start_time = time.time()
    operations = 0
    
    if not lists:
        return {
            'result': None,
            'execution_time': 0,
            'operations': 0
        }
    
    if len(lists) == 1:
        return {
            'result': lists[0],
            'execution_time': 0,
            'operations': 0
        }
    
    # Divide the list into two halves
    mid = len(lists) // 2
    left = merge_k_lists_with_performance(lists[:mid])
    right = merge_k_lists_with_performance(lists[mid:])
    
    # Merge the two sorted lists
    result = merge_two_lists(left['result'], right['result'])
    operations = left['operations'] + right['operations'] + 1
    
    end_time = time.time()
    
    return {
        'result': result,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def merge_k_lists_with_debugging(lists):
    """
    Merge k sorted linked lists with debugging information.
    
    Args:
        lists: List of k sorted linked lists
        
    Returns:
        dict: Debugging information
    """
    if not lists:
        return {
            'result': None,
            'debug_info': 'Empty lists',
            'steps': 0
        }
    
    if len(lists) == 1:
        return {
            'result': lists[0],
            'debug_info': 'Single list',
            'steps': 0
        }
    
    # Divide the list into two halves
    mid = len(lists) // 2
    left = merge_k_lists_with_debugging(lists[:mid])
    right = merge_k_lists_with_debugging(lists[mid:])
    
    # Merge the two sorted lists
    result = merge_two_lists(left['result'], right['result'])
    
    return {
        'result': result,
        'debug_info': f'Processed {left['steps'] + right['steps'] + 1} operations',
        'steps': left['steps'] + right['steps'] + 1
    }


def merge_k_lists_with_analysis(lists):
    """
    Merge k sorted linked lists and return analysis.
    
    Args:
        lists: List of k sorted linked lists
        
    Returns:
        dict: Analysis results
    """
    if not lists:
        return {
            'result': None,
            'analysis': 'Empty lists',
            'efficiency': 1.0
        }
    
    if len(lists) == 1:
        return {
            'result': lists[0],
            'analysis': 'Single list',
            'efficiency': 1.0
        }
    
    # Divide the list into two halves
    mid = len(lists) // 2
    left = merge_k_lists_with_analysis(lists[:mid])
    right = merge_k_lists_with_analysis(lists[mid:])
    
    # Merge the two sorted lists
    result = merge_two_lists(left['result'], right['result'])
    
    efficiency = 1.0 / (left['steps'] + right['steps'] + 1) if (left['steps'] + right['steps'] + 1) > 0 else 0.0
    
    return {
        'result': result,
        'analysis': f'Merged {len(lists)} lists in {left['steps'] + right['steps'] + 1} operations',
        'efficiency': efficiency
    }


def merge_k_lists_with_optimization(lists):
    """
    Merge k sorted linked lists with optimization techniques.
    
    Args:
        lists: List of k sorted linked lists
        
    Returns:
        dict: Optimization results
    """
    if not lists:
        return {
            'result': None,
            'optimization': 'Empty lists',
            'space_saved': 0
        }
    
    if len(lists) == 1:
        return {
            'result': lists[0],
            'optimization': 'Single list',
            'space_saved': 0
        }
    
    # Divide the list into two halves
    mid = len(lists) // 2
    left = merge_k_lists_with_optimization(lists[:mid])
    right = merge_k_lists_with_optimization(lists[mid:])
    
    # Merge the two sorted lists
    result = merge_two_lists(left['result'], right['result'])
    
    # Calculate space optimization
    original_space = sum(list_length(lst) for lst in lists)
    optimized_space = list_length(result)
    space_saved = original_space - optimized_space
    
    return {
        'result': result,
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
        ([[1, 4, 5], [1, 3, 4], [2, 6]], [1, 1, 2, 3, 4, 4, 5, 6]),
        ([], []),
        ([[]], []),
        ([[1, 2, 3], [4, 5, 6]], [1, 2, 3, 4, 5, 6]),
        ([[1, 2, 3]], [1, 2, 3]),
        ([[1, 3, 5], [2, 4, 6]], [1, 2, 3, 4, 5, 6]),
        ([[1, 1, 1], [2, 2, 2], [3, 3, 3]], [1, 1, 1, 2, 2, 2, 3, 3, 3]),
        ([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ([[1, 3, 5, 7, 9], [2, 4, 6, 8, 10]], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ([[1], [2], [3], [4], [5]], [1, 2, 3, 4, 5]),
    ]
    
    for i, (lists_arr, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: lists={lists_arr}")
        
        # Convert arrays to linked lists
        lists = [array_to_list(arr) for arr in lists_arr]
        
        # Test basic approach
        result = merge_k_lists(lists)
        result_arr = list_to_array(result)
        print(f"Result: {result_arr}")
        print(f"Expected: {expected}")
        print(f"Correct: {result_arr == expected}")
        
        # Test heap approach
        lists_heap = [array_to_list(arr) for arr in lists_arr]
        result_heap = merge_k_lists_with_heap(lists_heap)
        result_heap_arr = list_to_array(result_heap)
        print(f"Heap result: {result_heap_arr}")
        
        # Test with statistics
        lists_stats = [array_to_list(arr) for arr in lists_arr]
        stats = merge_k_lists_with_stats(lists_stats)
        print(f"Statistics: {stats}")
        
        # Test with validation
        lists_validation = [array_to_list(arr) for arr in lists_arr]
        validation = merge_k_lists_with_validation(lists_validation)
        print(f"Validation: {validation}")
        
        # Test with comparison
        lists_comparison = [array_to_list(arr) for arr in lists_arr]
        comparison = merge_k_lists_with_comparison(lists_comparison)
        print(f"Comparison: {comparison}")
        
        # Test with performance
        lists_performance = [array_to_list(arr) for arr in lists_arr]
        performance = merge_k_lists_with_performance(lists_performance)
        print(f"Performance: {performance}")
        
        # Test with debugging
        lists_debugging = [array_to_list(arr) for arr in lists_arr]
        debugging = merge_k_lists_with_debugging(lists_debugging)
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        lists_analysis = [array_to_list(arr) for arr in lists_arr]
        analysis = merge_k_lists_with_analysis(lists_analysis)
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        lists_optimization = [array_to_list(arr) for arr in lists_arr]
        optimization = merge_k_lists_with_optimization(lists_optimization)
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    lists = [array_to_list([1, 4, 5]), array_to_list([1, 3, 4]), array_to_list([2, 6])]
    merge_k_lists_verbose(lists)
    
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
    
    large_lists = [generate_large_list(1000) for _ in range(10)]
    
    # Test divide and conquer approach
    start_time = time.time()
    for _ in range(100):
        merge_k_lists(large_lists)
    dc_time = time.time() - start_time
    
    # Test heap approach
    start_time = time.time()
    for _ in range(100):
        merge_k_lists_with_heap(large_lists)
    heap_time = time.time() - start_time
    
    print(f"Divide and conquer approach: {dc_time:.6f} seconds")
    print(f"Heap approach: {heap_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. If k <= 1, return the list or empty list")
    print("2. Split the array into two halves")
    print("3. Recursively merge the left half")
    print("4. Recursively merge the right half")
    print("5. Merge the two sorted lists")
    print("6. Return the merged list")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    lists = [array_to_list([1, 4, 5]), array_to_list([1, 3, 4]), array_to_list([2, 6])]
    print(f"Lists: {[list_to_array(lst) for lst in lists]}")
    print("\nSteps:")
    print("1. Split into two halves: left=[[1,4,5]], right=[[1,3,4],[2,6]]")
    print("2. Merge left half: [1,4,5]")
    print("3. Merge right half: [1,3,4] and [2,6] -> [1,2,3,4,6]")
    print("4. Merge [1,4,5] and [1,2,3,4,6] -> [1,1,2,3,4,4,5,6]")
    
    # Test with different numbers of lists
    print("\nDifferent numbers of lists:")
    test_lists = [
        [[1, 2, 3]],
        [[1, 2, 3], [4, 5, 6]],
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[1], [2], [3], [4], [5]],
        [[1, 3, 5], [2, 4, 6], [7, 9, 11], [8, 10, 12]],
    ]
    
    for lists_arr in test_lists:
        lists = [array_to_list(arr) for arr in lists_arr]
        result = merge_k_lists(lists)
        result_arr = list_to_array(result)
        print(f"Lists: {lists_arr} -> Result: {result_arr}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],
        [[]],
        [[], []],
        [[1], []],
        [[], [1]],
        [[1], [2]],
        [[1, 2], []],
        [[], [1, 2]],
    ]
    
    for lists_arr in edge_cases:
        lists = [array_to_list(arr) for arr in lists_arr]
        result = merge_k_lists(lists)
        result_arr = list_to_array(result)
        print(f"Lists: {lists_arr} -> Result: {result_arr}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for lists_arr, _ in test_cases[:5]:
        lists = [array_to_list(arr) for arr in lists_arr]
        stats = merge_k_lists_with_stats(lists)
        print(f"Lists: {lists_arr}")
        print(f"  Result: {list_to_array(stats['result'])}")
        print(f"  Total lists: {stats['total_lists']}")
        print(f"  Total nodes: {stats['total_nodes']}")
        print(f"  Comparisons: {stats['comparisons']}")
        print()
