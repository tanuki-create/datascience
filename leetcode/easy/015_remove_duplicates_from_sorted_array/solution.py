"""
Problem 15: Remove Duplicates from Sorted Array
Difficulty: Easy

Given an integer array nums sorted in non-decreasing order, remove the duplicates 
in-place such that each unique element appears only once. The relative order of 
the elements should be kept the same.

Time Complexity: O(n)
Space Complexity: O(1)
"""

def remove_duplicates(nums):
    """
    Remove duplicates from sorted array in-place.
    
    Args:
        nums: Sorted array with duplicates
        
    Returns:
        int: Length of array after removing duplicates
    """
    if not nums:
        return 0
    
    # Two pointers approach
    write_index = 1
    
    for read_index in range(1, len(nums)):
        # If current element is different from previous
        if nums[read_index] != nums[read_index - 1]:
            nums[write_index] = nums[read_index]
            write_index += 1
    
    return write_index


def remove_duplicates_verbose(nums):
    """
    Remove duplicates with detailed step-by-step explanation.
    
    Args:
        nums: Sorted array with duplicates
        
    Returns:
        int: Length of array after removing duplicates
    """
    if not nums:
        return 0
    
    print(f"Original array: {nums}")
    
    write_index = 1
    
    for read_index in range(1, len(nums)):
        print(f"Read index: {read_index}, Value: {nums[read_index]}")
        print(f"Previous value: {nums[read_index - 1]}")
        
        if nums[read_index] != nums[read_index - 1]:
            print(f"Unique element found, writing to index {write_index}")
            nums[write_index] = nums[read_index]
            write_index += 1
        else:
            print("Duplicate found, skipping")
        
        print(f"Array so far: {nums[:write_index]}")
        print("-" * 30)
    
    print(f"Final result: {nums[:write_index]}")
    return write_index


def remove_duplicates_using_set(nums):
    """
    Remove duplicates using set (creates new array - not in-place).
    
    Args:
        nums: Sorted array with duplicates
        
    Returns:
        int: Length of array after removing duplicates
    """
    if not nums:
        return 0
    
    # Convert to set to remove duplicates, then back to list
    unique_elements = list(set(nums))
    unique_elements.sort()  # Maintain sorted order
    
    # Update the original array
    for i in range(len(unique_elements)):
        nums[i] = unique_elements[i]
    
    return len(unique_elements)


def remove_duplicates_manual(nums):
    """
    Remove duplicates manually without using any built-in functions.
    
    Args:
        nums: Sorted array with duplicates
        
    Returns:
        int: Length of array after removing duplicates
    """
    if not nums:
        return 0
    
    # Count unique elements
    unique_count = 1
    for i in range(1, len(nums)):
        if nums[i] != nums[i - 1]:
            unique_count += 1
    
    # Remove duplicates
    write_index = 1
    for read_index in range(1, len(nums)):
        if nums[read_index] != nums[read_index - 1]:
            nums[write_index] = nums[read_index]
            write_index += 1
    
    return unique_count


def remove_duplicates_with_count(nums):
    """
    Remove duplicates and return both length and count of each unique element.
    
    Args:
        nums: Sorted array with duplicates
        
    Returns:
        tuple: (length, count_dict)
    """
    if not nums:
        return 0, {}
    
    # Count occurrences
    count_dict = {}
    for num in nums:
        count_dict[num] = count_dict.get(num, 0) + 1
    
    # Remove duplicates
    write_index = 1
    for read_index in range(1, len(nums)):
        if nums[read_index] != nums[read_index - 1]:
            nums[write_index] = nums[read_index]
            write_index += 1
    
    return write_index, count_dict


def remove_duplicates_at_most_k(nums, k):
    """
    Remove duplicates allowing at most k occurrences of each element.
    
    Args:
        nums: Sorted array with duplicates
        k: Maximum number of occurrences allowed
        
    Returns:
        int: Length of array after removing duplicates
    """
    if not nums:
        return 0
    
    write_index = 0
    count = 1
    
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            count += 1
        else:
            count = 1
        
        if count <= k:
            nums[write_index] = nums[i]
            write_index += 1
    
    return write_index


def remove_duplicates_unsorted(nums):
    """
    Remove duplicates from unsorted array (bonus problem).
    
    Args:
        nums: Unsorted array with duplicates
        
    Returns:
        int: Length of array after removing duplicates
    """
    if not nums:
        return 0
    
    # Use set to track seen elements
    seen = set()
    write_index = 0
    
    for read_index in range(len(nums)):
        if nums[read_index] not in seen:
            seen.add(nums[read_index])
            nums[write_index] = nums[read_index]
            write_index += 1
    
    return write_index


def find_duplicates_in_sorted_array(nums):
    """
    Find all duplicate elements in a sorted array.
    
    Args:
        nums: Sorted array
        
    Returns:
        list: List of duplicate elements
    """
    if not nums:
        return []
    
    duplicates = []
    i = 0
    
    while i < len(nums):
        # Count consecutive occurrences
        count = 1
        j = i + 1
        while j < len(nums) and nums[j] == nums[i]:
            count += 1
            j += 1
        
        # If count > 1, it's a duplicate
        if count > 1:
            duplicates.append(nums[i])
        
        i = j
    
    return duplicates


# Test cases
if __name__ == "__main__":
    test_cases = [
        [1, 1, 2],                    # Expected: 2
        [0, 0, 1, 1, 1, 2, 2, 3, 3, 4], # Expected: 5
        [1, 2, 3, 4, 5],              # Expected: 5
        [1, 1, 1, 1, 1],              # Expected: 1
        [1],                          # Expected: 1
        [],                           # Expected: 0
        [1, 2, 2, 3, 3, 3, 4, 4, 4, 4], # Expected: 4
    ]
    
    for i, nums in enumerate(test_cases, 1):
        print(f"Test case {i}: {nums}")
        
        # Create a copy for testing
        nums_copy = nums.copy()
        
        # Test different approaches
        result_main = remove_duplicates(nums_copy)
        print(f"Main approach: {result_main}")
        print(f"Array after: {nums_copy[:result_main]}")
        
        # Test with verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            nums_verbose = nums.copy()
            remove_duplicates_verbose(nums_verbose)
        
        print("-" * 50)
    
    # Test bonus problems
    print("\nBonus problems:")
    
    # Test remove duplicates allowing at most k occurrences
    k_tests = [
        ([1, 1, 1, 2, 2, 3], 1),      # Allow 1 occurrence
        ([1, 1, 1, 2, 2, 3], 2),      # Allow 2 occurrences
        ([1, 1, 1, 2, 2, 3], 3),      # Allow 3 occurrences
    ]
    
    for nums, k in k_tests:
        nums_copy = nums.copy()
        result = remove_duplicates_at_most_k(nums_copy, k)
        print(f"Allow {k} occurrences: {nums} -> {result}, {nums_copy[:result]}")
    
    # Test find duplicates
    duplicate_tests = [
        [1, 1, 2, 2, 3, 4, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 1, 1, 2, 2, 3],
    ]
    
    for nums in duplicate_tests:
        duplicates = find_duplicates_in_sorted_array(nums)
        print(f"Duplicates in {nums}: {duplicates}")
    
    # Test unsorted array
    print("\nUnsorted array test:")
    unsorted_nums = [3, 1, 2, 1, 3, 2, 4]
    print(f"Original: {unsorted_nums}")
    result = remove_duplicates_unsorted(unsorted_nums)
    print(f"After removing duplicates: {unsorted_nums[:result]}")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large test case
    large_nums = sorted([random.randint(1, 100) for _ in range(10000)])
    
    # Test main approach
    start_time = time.time()
    for _ in range(100):
        nums_copy = large_nums.copy()
        remove_duplicates(nums_copy)
    main_time = time.time() - start_time
    
    # Test set approach
    start_time = time.time()
    for _ in range(100):
        nums_copy = large_nums.copy()
        remove_duplicates_using_set(nums_copy)
    set_time = time.time() - start_time
    
    print(f"Main approach: {main_time:.6f} seconds")
    print(f"Set approach: {set_time:.6f} seconds")
    
    # Edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],                    # Empty array
        [1],                   # Single element
        [1, 1],                # Two same elements
        [1, 2],                # Two different elements
        [1, 1, 1, 1, 1],       # All same elements
        [1, 2, 3, 4, 5],       # No duplicates
    ]
    
    for case in edge_cases:
        nums_copy = case.copy()
        result = remove_duplicates(nums_copy)
        print(f"{case} -> {result}, {nums_copy[:result]}")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Use two pointers: read_index and write_index")
    print("2. read_index scans the array")
    print("3. write_index points to where the next unique element should be written")
    print("4. When we find a unique element, write it to write_index and increment")
    print("5. The final write_index is the length of the unique array")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example = [1, 1, 2, 2, 3, 3, 3, 4]
    print(f"Original: {example}")
    
    write_index = 1
    for read_index in range(1, len(example)):
        if example[read_index] != example[read_index - 1]:
            example[write_index] = example[read_index]
            write_index += 1
        print(f"Step {read_index}: {example[:write_index]}")
    
    print(f"Final result: {example[:write_index]}")
    print(f"Length: {write_index}")
