"""
Problem 42: Group Anagrams
Difficulty: Medium

Given an array of strings strs, group the anagrams together. You can return 
the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different 
word or phrase, typically using all the original letters exactly once.

Time Complexity: O(n * m * log(m)) where n is the number of strings and m is the average length of strings
Space Complexity: O(n * m) for storing all strings
"""

def group_anagrams(strs):
    """
    Group anagrams together using hash map with sorted string as key.
    
    Args:
        strs: List of strings to group
        
    Returns:
        list: List of groups of anagrams
    """
    from collections import defaultdict
    
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Sort characters to create key
        sorted_str = ''.join(sorted(s))
        anagram_groups[sorted_str].append(s)
    
    return list(anagram_groups.values())


def group_anagrams_optimized(strs):
    """
    Group anagrams using optimized approach with character counting.
    
    Args:
        strs: List of strings to group
        
    Returns:
        list: List of groups of anagrams
    """
    from collections import defaultdict
    
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Count characters instead of sorting
        char_count = [0] * 26
        for char in s:
            char_count[ord(char) - ord('a')] += 1
        
        # Use tuple as key
        key = tuple(char_count)
        anagram_groups[key].append(s)
    
    return list(anagram_groups.values())


def group_anagrams_with_hashmap(strs):
    """
    Group anagrams using hashmap with sorted string as key.
    
    Args:
        strs: List of strings to group
        
    Returns:
        list: List of groups of anagrams
    """
    anagram_groups = {}
    
    for s in strs:
        # Sort characters to create key
        sorted_str = ''.join(sorted(s))
        
        if sorted_str in anagram_groups:
            anagram_groups[sorted_str].append(s)
        else:
            anagram_groups[sorted_str] = [s]
    
    return list(anagram_groups.values())


def group_anagrams_verbose(strs):
    """
    Group anagrams with detailed step-by-step explanation.
    
    Args:
        strs: List of strings to group
        
    Returns:
        list: List of groups of anagrams
    """
    print(f"Grouping anagrams in {strs}")
    print(f"Number of strings: {len(strs)}")
    
    from collections import defaultdict
    
    anagram_groups = defaultdict(list)
    
    for i, s in enumerate(strs):
        print(f"\nStep {i + 1}: Processing '{s}'")
        
        # Sort characters to create key
        sorted_str = ''.join(sorted(s))
        print(f"  Sorted string: '{sorted_str}'")
        
        anagram_groups[sorted_str].append(s)
        print(f"  Added to group with key '{sorted_str}'")
        print(f"  Current groups: {dict(anagram_groups)}")
    
    result = list(anagram_groups.values())
    print(f"\nFinal result: {result}")
    
    return result


def group_anagrams_with_stats(strs):
    """
    Group anagrams and return statistics.
    
    Args:
        strs: List of strings to group
        
    Returns:
        dict: Statistics about the grouping
    """
    from collections import defaultdict
    
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Sort characters to create key
        sorted_str = ''.join(sorted(s))
        anagram_groups[sorted_str].append(s)
    
    result = list(anagram_groups.values())
    
    # Calculate statistics
    total_groups = len(result)
    total_strings = len(strs)
    group_sizes = [len(group) for group in result]
    max_group_size = max(group_sizes) if group_sizes else 0
    min_group_size = min(group_sizes) if group_sizes else 0
    avg_group_size = sum(group_sizes) / len(group_sizes) if group_sizes else 0
    
    return {
        'groups': result,
        'total_groups': total_groups,
        'total_strings': total_strings,
        'group_sizes': group_sizes,
        'max_group_size': max_group_size,
        'min_group_size': min_group_size,
        'avg_group_size': avg_group_size
    }


def group_anagrams_with_validation(strs):
    """
    Group anagrams with validation.
    
    Args:
        strs: List of strings to group
        
    Returns:
        dict: Detailed validation results
    """
    if not strs:
        return {
            'groups': [],
            'is_valid': False,
            'reason': 'Empty input'
        }
    
    from collections import defaultdict
    
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Sort characters to create key
        sorted_str = ''.join(sorted(s))
        anagram_groups[sorted_str].append(s)
    
    result = list(anagram_groups.values())
    
    return {
        'groups': result,
        'is_valid': True,
        'reason': f'Successfully grouped {len(strs)} strings into {len(result)} groups',
        'input': strs
    }


def group_anagrams_with_comparison(strs):
    """
    Group anagrams and compare different approaches.
    
    Args:
        strs: List of strings to group
        
    Returns:
        dict: Comparison of different approaches
    """
    # Sorting approach
    sorting_result = group_anagrams(strs.copy())
    
    # Character counting approach
    counting_result = group_anagrams_optimized(strs.copy())
    
    return {
        'sorting_approach': sorting_result,
        'counting_approach': counting_result
    }


def group_anagrams_with_performance(strs):
    """
    Group anagrams with performance metrics.
    
    Args:
        strs: List of strings to group
        
    Returns:
        dict: Performance metrics
    """
    import time
    
    start_time = time.time()
    operations = 0
    
    from collections import defaultdict
    
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Sort characters to create key
        sorted_str = ''.join(sorted(s))
        anagram_groups[sorted_str].append(s)
        operations += 1
    
    result = list(anagram_groups.values())
    end_time = time.time()
    
    return {
        'groups': result,
        'execution_time': end_time - start_time,
        'operations': operations
    }


def group_anagrams_with_debugging(strs):
    """
    Group anagrams with debugging information.
    
    Args:
        strs: List of strings to group
        
    Returns:
        dict: Debugging information
    """
    if not strs:
        return {
            'groups': [],
            'debug_info': 'Empty input',
            'steps': 0
        }
    
    from collections import defaultdict
    
    anagram_groups = defaultdict(list)
    steps = 0
    
    for s in strs:
        # Sort characters to create key
        sorted_str = ''.join(sorted(s))
        anagram_groups[sorted_str].append(s)
        steps += 1
    
    result = list(anagram_groups.values())
    
    return {
        'groups': result,
        'debug_info': f'Processed {steps} strings',
        'steps': steps
    }


def group_anagrams_with_analysis(strs):
    """
    Group anagrams and return analysis.
    
    Args:
        strs: List of strings to group
        
    Returns:
        dict: Analysis results
    """
    if not strs:
        return {
            'groups': [],
            'analysis': 'Empty input',
            'efficiency': 'N/A'
        }
    
    from collections import defaultdict
    
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Sort characters to create key
        sorted_str = ''.join(sorted(s))
        anagram_groups[sorted_str].append(s)
    
    result = list(anagram_groups.values())
    
    # Calculate efficiency
    total_strings = len(strs)
    total_groups = len(result)
    efficiency = total_groups / total_strings if total_strings > 0 else 0.0
    
    return {
        'groups': result,
        'analysis': f'Grouped {total_strings} strings into {total_groups} groups',
        'efficiency': efficiency
    }


def group_anagrams_with_optimization(strs):
    """
    Group anagrams with optimization techniques.
    
    Args:
        strs: List of strings to group
        
    Returns:
        dict: Optimization results
    """
    if not strs:
        return {
            'groups': [],
            'optimization': 'Empty input',
            'space_saved': 0
        }
    
    from collections import defaultdict
    
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Sort characters to create key
        sorted_str = ''.join(sorted(s))
        anagram_groups[sorted_str].append(s)
    
    result = list(anagram_groups.values())
    
    # Calculate space optimization
    original_space = sum(len(s) for s in strs)
    grouped_space = sum(len(group) for group in result)
    space_saved = original_space - grouped_space
    
    return {
        'groups': result,
        'optimization': f'Space saved: {space_saved} characters',
        'space_saved': space_saved
    }


# Test cases
if __name__ == "__main__":
    test_cases = [
        (["eat", "tea", "tan", "ate", "nat", "bat"], [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),
        ([""], [[""]]),
        (["a"], [["a"]]),
        (["abc", "def", "ghi"], [["abc"], ["def"], ["ghi"]]),
        (["abc", "bca", "cab"], [["abc", "bca", "cab"]]),
        ([], []),
        (["a", "a"], [["a", "a"]]),
        (["a", "b"], [["a"], ["b"]]),
        (["abc", "acb", "bac", "bca", "cab", "cba"], [["abc", "acb", "bac", "bca", "cab", "cba"]]),
        (["listen", "silent", "enlist"], [["listen", "silent", "enlist"]]),
    ]
    
    for i, (strs, expected) in enumerate(test_cases, 1):
        print(f"Test case {i}: strs={strs}")
        
        # Test basic approach
        result = group_anagrams(strs.copy())
        print(f"Result: {result}")
        print(f"Expected: {expected}")
        print(f"Correct: {result == expected}")
        
        # Test optimized approach
        result_opt = group_anagrams_optimized(strs.copy())
        print(f"Optimized result: {result_opt}")
        
        # Test hashmap approach
        result_hash = group_anagrams_with_hashmap(strs.copy())
        print(f"Hashmap result: {result_hash}")
        
        # Test with statistics
        stats = group_anagrams_with_stats(strs.copy())
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = group_anagrams_with_validation(strs.copy())
        print(f"Validation: {validation}")
        
        # Test with comparison
        comparison = group_anagrams_with_comparison(strs.copy())
        print(f"Comparison: {comparison}")
        
        # Test with performance
        performance = group_anagrams_with_performance(strs.copy())
        print(f"Performance: {performance}")
        
        # Test with debugging
        debugging = group_anagrams_with_debugging(strs.copy())
        print(f"Debugging: {debugging}")
        
        # Test with analysis
        analysis = group_anagrams_with_analysis(strs.copy())
        print(f"Analysis: {analysis}")
        
        # Test with optimization
        optimization = group_anagrams_with_optimization(strs.copy())
        print(f"Optimization: {optimization}")
        
        print("-" * 50)
    
    # Test verbose output for first case
    print("\nVerbose output for first test case:")
    group_anagrams_verbose(["eat", "tea", "tan", "ate", "nat", "bat"])
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    import string
    
    # Generate large list of strings for testing
    def generate_large_strings(length):
        """Generate a large list of strings for testing."""
        return [''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10))) for _ in range(length)]
    
    large_strs = generate_large_strings(1000)
    
    # Test sorting approach
    start_time = time.time()
    for _ in range(100):
        group_anagrams(large_strs.copy())
    sorting_time = time.time() - start_time
    
    # Test counting approach
    start_time = time.time()
    for _ in range(100):
        group_anagrams_optimized(large_strs.copy())
    counting_time = time.time() - start_time
    
    print(f"Sorting approach: {sorting_time:.6f} seconds")
    print(f"Counting approach: {counting_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Create a hash map where keys are sorted strings")
    print("2. For each string in the input:")
    print("   - Sort the characters of the string")
    print("   - Use the sorted string as the key")
    print("   - Add the original string to the group for that key")
    print("3. Return all groups as a list of lists")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(f"Input: {strs}")
    print("\nSteps:")
    for i, s in enumerate(strs):
        sorted_str = ''.join(sorted(s))
        print(f"  Step {i + 1}: '{s}' -> sorted: '{sorted_str}'")
    print("\nGrouping by sorted strings:")
    print("  'aet' -> ['eat', 'tea', 'ate']")
    print("  'ant' -> ['tan', 'nat']")
    print("  'abt' -> ['bat']")
    
    # Test with different string lengths
    print("\nDifferent string lengths:")
    test_strings = [
        ["a", "b", "c"],
        ["ab", "ba", "cd"],
        ["abc", "bca", "cab"],
        ["abcd", "dcba", "efgh"],
    ]
    
    for strs in test_strings:
        result = group_anagrams(strs.copy())
        print(f"Strings: {strs} -> Groups: {result}")
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],
        [""],
        ["a"],
        ["a", "a"],
        ["a", "b"],
        ["ab", "ba"],
        ["abc", "def"],
    ]
    
    for strs in edge_cases:
        result = group_anagrams(strs.copy())
        print(f"Strings: {strs} -> Groups: {result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for strs, _ in test_cases[:5]:
        stats = group_anagrams_with_stats(strs.copy())
        print(f"Strings: {strs}")
        print(f"  Groups: {stats['groups']}")
        print(f"  Total groups: {stats['total_groups']}")
        print(f"  Total strings: {stats['total_strings']}")
        print(f"  Group sizes: {stats['group_sizes']}")
        print(f"  Max group size: {stats['max_group_size']}")
        print(f"  Min group size: {stats['min_group_size']}")
        print(f"  Avg group size: {stats['avg_group_size']:.2f}")
        print()
