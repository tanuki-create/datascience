"""
Problem 17: Merge Sorted Array
Difficulty: Easy

You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, 
and two integers m and n, representing the number of elements in nums1 and nums2 
respectively.

Time Complexity: O(m + n)
Space Complexity: O(1)
"""

def merge(nums1, m, nums2, n):
    """
    Merge nums2 into nums1 as one sorted array.
    
    Args:
        nums1: First sorted array with extra space
        m: Number of elements in nums1
        nums2: Second sorted array
        n: Number of elements in nums2
    """
    # Start from the end of both arrays
    i = m - 1  # Last element in nums1
    j = n - 1  # Last element in nums2
    k = m + n - 1  # Last position in nums1
    
    # Merge from the end
    while i >= 0 and j >= 0:
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
    
    # Copy remaining elements from nums2
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1
    
    # Note: We don't need to copy remaining elements from nums1
    # because they are already in the correct position


def merge_verbose(nums1, m, nums2, n):
    """
    Merge with detailed step-by-step explanation.
    
    Args:
        nums1: First sorted array with extra space
        m: Number of elements in nums1
        nums2: Second sorted array
        n: Number of elements in nums2
    """
    print(f"Initial nums1: {nums1}")
    print(f"Initial nums2: {nums2}")
    print(f"m = {m}, n = {n}")
    
    i = m - 1
    j = n - 1
    k = m + n - 1
    
    step = 1
    while i >= 0 and j >= 0:
        print(f"\nStep {step}:")
        print(f"i = {i}, j = {j}, k = {k}")
        print(f"nums1[i] = {nums1[i]}, nums2[j] = {nums2[j]}")
        
        if nums1[i] > nums2[j]:
            print(f"nums1[{i}] > nums2[{j}], so nums1[{k}] = nums1[{i}] = {nums1[i]}")
            nums1[k] = nums1[i]
            i -= 1
        else:
            print(f"nums1[{i}] <= nums2[{j}], so nums1[{k}] = nums2[{j}] = {nums2[j]}")
            nums1[k] = nums2[j]
            j -= 1
        
        k -= 1
        print(f"After step {step}: nums1 = {nums1}")
        step += 1
    
    # Copy remaining elements from nums2
    while j >= 0:
        print(f"\nStep {step}: Copy remaining nums2[{j}] = {nums2[j]}")
        nums1[k] = nums2[j]
        j -= 1
        k -= 1
        print(f"After step {step}: nums1 = {nums1}")
        step += 1
    
    print(f"\nFinal result: {nums1}")


def merge_using_extra_space(nums1, m, nums2, n):
    """
    Merge using extra space (not optimal but easier to understand).
    
    Args:
        nums1: First sorted array with extra space
        m: Number of elements in nums1
        nums2: Second sorted array
        n: Number of elements in nums2
    """
    # Create a copy of the first m elements of nums1
    nums1_copy = nums1[:m]
    
    i = j = k = 0
    
    # Merge the two arrays
    while i < m and j < n:
        if nums1_copy[i] <= nums2[j]:
            nums1[k] = nums1_copy[i]
            i += 1
        else:
            nums1[k] = nums2[j]
            j += 1
        k += 1
    
    # Copy remaining elements
    while i < m:
        nums1[k] = nums1_copy[i]
        i += 1
        k += 1
    
    while j < n:
        nums1[k] = nums2[j]
        j += 1
        k += 1


def merge_recursive(nums1, m, nums2, n):
    """
    Merge using recursive approach.
    
    Args:
        nums1: First sorted array with extra space
        m: Number of elements in nums1
        nums2: Second sorted array
        n: Number of elements in nums2
    """
    def merge_helper(i, j, k):
        if i < 0 and j < 0:
            return
        
        if i < 0:
            nums1[k] = nums2[j]
            merge_helper(i, j - 1, k - 1)
        elif j < 0:
            nums1[k] = nums1[i]
            merge_helper(i - 1, j, k - 1)
        else:
            if nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                merge_helper(i - 1, j, k - 1)
            else:
                nums1[k] = nums2[j]
                merge_helper(i, j - 1, k - 1)
    
    merge_helper(m - 1, n - 1, m + n - 1)


def merge_with_comparison_count(nums1, m, nums2, n):
    """
    Merge and count the number of comparisons made.
    
    Args:
        nums1: First sorted array with extra space
        m: Number of elements in nums1
        nums2: Second sorted array
        n: Number of elements in nums2
        
    Returns:
        int: Number of comparisons made
    """
    comparisons = 0
    i = m - 1
    j = n - 1
    k = m + n - 1
    
    while i >= 0 and j >= 0:
        comparisons += 1
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
    
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1
    
    return comparisons


def merge_three_arrays(nums1, m, nums2, n, nums3, p):
    """
    Merge three sorted arrays (bonus problem).
    
    Args:
        nums1: First sorted array
        m: Number of elements in nums1
        nums2: Second sorted array
        n: Number of elements in nums2
        nums3: Third sorted array
        p: Number of elements in nums3
        
    Returns:
        list: Merged sorted array
    """
    result = []
    i = j = k = 0
    
    while i < m and j < n and k < p:
        if nums1[i] <= nums2[j] and nums1[i] <= nums3[k]:
            result.append(nums1[i])
            i += 1
        elif nums2[j] <= nums1[i] and nums2[j] <= nums3[k]:
            result.append(nums2[j])
            j += 1
        else:
            result.append(nums3[k])
            k += 1
    
    # Handle remaining elements
    while i < m and j < n:
        if nums1[i] <= nums2[j]:
            result.append(nums1[i])
            i += 1
        else:
            result.append(nums2[j])
            j += 1
    
    while i < m and k < p:
        if nums1[i] <= nums3[k]:
            result.append(nums1[i])
            i += 1
        else:
            result.append(nums3[k])
            k += 1
    
    while j < n and k < p:
        if nums2[j] <= nums3[k]:
            result.append(nums2[j])
            j += 1
        else:
            result.append(nums3[k])
            k += 1
    
    # Copy remaining elements
    while i < m:
        result.append(nums1[i])
        i += 1
    
    while j < n:
        result.append(nums2[j])
        j += 1
    
    while k < p:
        result.append(nums3[k])
        k += 1
    
    return result


def merge_with_duplicates(nums1, m, nums2, n):
    """
    Merge arrays and remove duplicates (bonus problem).
    
    Args:
        nums1: First sorted array with extra space
        m: Number of elements in nums1
        nums2: Second sorted array
        n: Number of elements in nums2
        
    Returns:
        int: Length of merged array without duplicates
    """
    i = m - 1
    j = n - 1
    k = m + n - 1
    
    while i >= 0 and j >= 0:
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
    
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1
    
    # Remove duplicates
    write_index = 0
    for read_index in range(1, m + n):
        if nums1[read_index] != nums1[write_index]:
            write_index += 1
            nums1[write_index] = nums1[read_index]
    
    return write_index + 1


# Test cases
if __name__ == "__main__":
    test_cases = [
        ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3),  # Expected: [1, 2, 2, 3, 5, 6]
        ([1], 1, [], 0),                         # Expected: [1]
        ([0], 0, [1], 1),                       # Expected: [1]
        ([1, 2, 3, 0, 0], 3, [4, 5], 2),        # Expected: [1, 2, 3, 4, 5]
        ([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3),  # Expected: [1, 2, 3, 4, 5, 6]
    ]
    
    for i, (nums1, m, nums2, n) in enumerate(test_cases, 1):
        print(f"Test case {i}:")
        print(f"nums1: {nums1}, m: {m}")
        print(f"nums2: {nums2}, n: {n}")
        
        # Test different approaches
        nums1_copy1 = nums1.copy()
        merge(nums1_copy1, m, nums2, n)
        print(f"Main approach: {nums1_copy1}")
        
        nums1_copy2 = nums1.copy()
        merge_using_extra_space(nums1_copy2, m, nums2, n)
        print(f"Extra space: {nums1_copy2}")
        
        nums1_copy3 = nums1.copy()
        merge_recursive(nums1_copy3, m, nums2, n)
        print(f"Recursive: {nums1_copy3}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            nums1_verbose = nums1.copy()
            merge_verbose(nums1_verbose, m, nums2, n)
        
        print("-" * 50)
    
    # Test bonus problems
    print("\nBonus problems:")
    
    # Test three array merge
    three_array_tests = [
        ([1, 3, 5], 3, [2, 4, 6], 3, [7, 8, 9], 3),
        ([1, 2], 2, [3, 4], 2, [5, 6], 2),
    ]
    
    for nums1, m, nums2, n, nums3, p in three_array_tests:
        result = merge_three_arrays(nums1, m, nums2, n, nums3, p)
        print(f"Merge three arrays: {result}")
    
    # Test merge with duplicates
    duplicate_tests = [
        ([1, 2, 3, 0, 0], 3, [2, 3, 4], 3),
        ([1, 1, 2, 0, 0], 3, [1, 2, 2], 3),
    ]
    
    for nums1, m, nums2, n in duplicate_tests:
        nums1_copy = nums1.copy()
        length = merge_with_duplicates(nums1_copy, m, nums2, n)
        print(f"Merge with duplicates: {nums1_copy[:length]}")
    
    # Test comparison count
    print("\nComparison count:")
    comparison_tests = [
        ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3),
        ([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3),
    ]
    
    for nums1, m, nums2, n in comparison_tests:
        nums1_copy = nums1.copy()
        comparisons = merge_with_comparison_count(nums1_copy, m, nums2, n)
        print(f"Comparisons made: {comparisons}")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large test case
    m, n = 1000, 1000
    nums1_large = sorted([random.randint(1, 1000) for _ in range(m)]) + [0] * n
    nums2_large = sorted([random.randint(1, 1000) for _ in range(n)])
    
    # Test main approach
    start_time = time.time()
    for _ in range(100):
        nums1_copy = nums1_large.copy()
        merge(nums1_copy, m, nums2_large, n)
    main_time = time.time() - start_time
    
    # Test extra space approach
    start_time = time.time()
    for _ in range(100):
        nums1_copy = nums1_large.copy()
        merge_using_extra_space(nums1_copy, m, nums2_large, n)
    extra_time = time.time() - start_time
    
    print(f"Main approach: {main_time:.6f} seconds")
    print(f"Extra space: {extra_time:.6f} seconds")
    
    # Edge cases
    print("\nEdge cases:")
    edge_cases = [
        ([], 0, [], 0),                    # Both empty
        ([1], 1, [], 0),                   # Only nums1
        ([0], 0, [1], 1),                  # Only nums2
        ([1, 2], 2, [3, 4], 2),           # No overlap
        ([3, 4], 2, [1, 2], 2),           # nums2 all smaller
        ([1, 3], 2, [2, 4], 2),           # Interleaved
    ]
    
    for nums1, m, nums2, n in edge_cases:
        nums1_copy = nums1.copy()
        merge(nums1_copy, m, nums2, n)
        print(f"nums1: {nums1}, nums2: {nums2} -> {nums1_copy}")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Start from the end of both arrays")
    print("2. Compare elements and place the larger one at the end")
    print("3. Move the pointer of the array from which we took the element")
    print("4. Continue until one array is exhausted")
    print("5. Copy remaining elements from the other array")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_nums1 = [1, 2, 3, 0, 0, 0]
    example_nums2 = [2, 5, 6]
    example_m, example_n = 3, 3
    
    print(f"Initial: nums1 = {example_nums1}, nums2 = {example_nums2}")
    print(f"m = {example_m}, n = {example_n}")
    
    i, j, k = example_m - 1, example_n - 1, example_m + example_n - 1
    
    step = 1
    while i >= 0 and j >= 0:
        print(f"\nStep {step}: i={i}, j={j}, k={k}")
        print(f"nums1[{i}] = {example_nums1[i]}, nums2[{j}] = {example_nums2[j]}")
        
        if example_nums1[i] > example_nums2[j]:
            example_nums1[k] = example_nums1[i]
            i -= 1
            print(f"nums1[{i+1}] > nums2[{j}], so nums1[{k}] = nums1[{i+1}] = {example_nums1[k]}")
        else:
            example_nums1[k] = example_nums2[j]
            j -= 1
            print(f"nums1[{i}] <= nums2[{j+1}], so nums1[{k}] = nums2[{j+1}] = {example_nums1[k]}")
        
        k -= 1
        print(f"After step {step}: nums1 = {example_nums1}")
        step += 1
    
    print(f"\nFinal result: {example_nums1}")
