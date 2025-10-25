"""
Problem 13: Longest Common Prefix
Difficulty: Easy

Write a function to find the longest common prefix string amongst an array of strings.
If there is no common prefix, return an empty string "".

Time Complexity: O(S) where S is the sum of all characters in all strings
Space Complexity: O(1)
"""

def longest_common_prefix(strs):
    """
    Find the longest common prefix using vertical scanning.
    
    Args:
        strs: List of strings
        
    Returns:
        str: Longest common prefix
    """
    if not strs:
        return ""
    
    if len(strs) == 1:
        return strs[0]
    
    # Start with the first string as reference
    prefix = strs[0]
    
    for i in range(1, len(strs)):
        # Find the common prefix between current prefix and current string
        while not strs[i].startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    
    return prefix


def longest_common_prefix_horizontal(strs):
    """
    Find the longest common prefix using horizontal scanning.
    
    Args:
        strs: List of strings
        
    Returns:
        str: Longest common prefix
    """
    if not strs:
        return ""
    
    if len(strs) == 1:
        return strs[0]
    
    # Start with the first string
    prefix = strs[0]
    
    for i in range(1, len(strs)):
        # Find common prefix between prefix and current string
        j = 0
        while j < len(prefix) and j < len(strs[i]) and prefix[j] == strs[i][j]:
            j += 1
        
        prefix = prefix[:j]
        if not prefix:
            return ""
    
    return prefix


def longest_common_prefix_vertical(strs):
    """
    Find the longest common prefix using vertical scanning.
    
    Args:
        strs: List of strings
        
    Returns:
        str: Longest common prefix
    """
    if not strs:
        return ""
    
    if len(strs) == 1:
        return strs[0]
    
    # Find the minimum length string
    min_len = min(len(s) for s in strs)
    
    for i in range(min_len):
        char = strs[0][i]
        for j in range(1, len(strs)):
            if strs[j][i] != char:
                return strs[0][:i]
    
    return strs[0][:min_len]


def longest_common_prefix_binary_search(strs):
    """
    Find the longest common prefix using binary search.
    
    Args:
        strs: List of strings
        
    Returns:
        str: Longest common prefix
    """
    if not strs:
        return ""
    
    if len(strs) == 1:
        return strs[0]
    
    def is_common_prefix(length):
        """Check if the first 'length' characters form a common prefix."""
        prefix = strs[0][:length]
        for i in range(1, len(strs)):
            if not strs[i].startswith(prefix):
                return False
        return True
    
    # Find the minimum length
    min_len = min(len(s) for s in strs)
    
    # Binary search for the longest common prefix
    left, right = 0, min_len
    
    while left < right:
        mid = (left + right + 1) // 2
        if is_common_prefix(mid):
            left = mid
        else:
            right = mid - 1
    
    return strs[0][:left]


def longest_common_prefix_divide_conquer(strs):
    """
    Find the longest common prefix using divide and conquer.
    
    Args:
        strs: List of strings
        
    Returns:
        str: Longest common prefix
    """
    if not strs:
        return ""
    
    if len(strs) == 1:
        return strs[0]
    
    def lcp_two_strings(s1, s2):
        """Find common prefix between two strings."""
        i = 0
        while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
            i += 1
        return s1[:i]
    
    def lcp_divide_conquer(left, right):
        """Divide and conquer approach."""
        if left == right:
            return strs[left]
        
        mid = (left + right) // 2
        left_lcp = lcp_divide_conquer(left, mid)
        right_lcp = lcp_divide_conquer(mid + 1, right)
        
        return lcp_two_strings(left_lcp, right_lcp)
    
    return lcp_divide_conquer(0, len(strs) - 1)


def longest_common_prefix_trie(strs):
    """
    Find the longest common prefix using trie (bonus approach).
    
    Args:
        strs: List of strings
        
    Returns:
        str: Longest common prefix
    """
    if not strs:
        return ""
    
    if len(strs) == 1:
        return strs[0]
    
    # Build trie
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.is_end = False
            self.count = 0
    
    root = TrieNode()
    
    # Insert all strings into trie
    for s in strs:
        node = root
        for char in s:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += 1
        node.is_end = True
    
    # Find the longest common prefix
    prefix = []
    node = root
    
    while len(node.children) == 1 and not node.is_end:
        char = list(node.children.keys())[0]
        child = node.children[char]
        
        # Check if all strings have this character
        if child.count == len(strs):
            prefix.append(char)
            node = child
        else:
            break
    
    return ''.join(prefix)


def find_common_suffix(strs):
    """
    Find the longest common suffix (bonus problem).
    
    Args:
        strs: List of strings
        
    Returns:
        str: Longest common suffix
    """
    if not strs:
        return ""
    
    if len(strs) == 1:
        return strs[0]
    
    # Start with the first string
    suffix = strs[0]
    
    for i in range(1, len(strs)):
        # Find common suffix
        j = 0
        while j < len(suffix) and j < len(strs[i]) and suffix[-(j+1)] == strs[i][-(j+1)]:
            j += 1
        
        suffix = suffix[-j:] if j > 0 else ""
        if not suffix:
            return ""
    
    return suffix


def find_common_substring(strs):
    """
    Find the longest common substring (bonus problem).
    
    Args:
        strs: List of strings
        
    Returns:
        str: Longest common substring
    """
    if not strs:
        return ""
    
    if len(strs) == 1:
        return strs[0]
    
    # Find the shortest string
    shortest = min(strs, key=len)
    max_len = len(shortest)
    longest_substring = ""
    
    # Try all possible substrings of the shortest string
    for i in range(max_len):
        for j in range(i + 1, max_len + 1):
            substring = shortest[i:j]
            
            # Check if this substring exists in all strings
            if all(substring in s for s in strs):
                if len(substring) > len(longest_substring):
                    longest_substring = substring
    
    return longest_substring


# Test cases
if __name__ == "__main__":
    test_cases = [
        ["flower", "flow", "flight"],  # "fl"
        ["dog", "racecar", "car"],     # ""
        ["", "abc", "def"],            # ""
        ["abc", "abc", "abc"],         # "abc"
        ["a"],                         # "a"
        ["ab", "a"],                   # "a"
        ["a", "ab"],                   # "a"
        ["", ""],                      # ""
        ["abc", "ab", "a"],            # "a"
        ["abc", "def", "ghi"],         # ""
    ]
    
    for i, strs in enumerate(test_cases, 1):
        print(f"Test case {i}: {strs}")
        
        # Test different approaches
        result_vertical = longest_common_prefix(strs)
        result_horizontal = longest_common_prefix_horizontal(strs)
        result_vertical_scan = longest_common_prefix_vertical(strs)
        result_binary = longest_common_prefix_binary_search(strs)
        result_divide = longest_common_prefix_divide_conquer(strs)
        result_trie = longest_common_prefix_trie(strs)
        
        print(f"Vertical: '{result_vertical}'")
        print(f"Horizontal: '{result_horizontal}'")
        print(f"Vertical scan: '{result_vertical_scan}'")
        print(f"Binary search: '{result_binary}'")
        print(f"Divide & conquer: '{result_divide}'")
        print(f"Trie: '{result_trie}'")
        
        print("-" * 50)
    
    # Test bonus problems
    print("\nBonus problems:")
    
    # Test common suffix
    suffix_tests = [
        ["flower", "power", "tower"],  # "wer"
        ["abc", "def", "ghi"],         # ""
        ["abc", "bc", "c"],            # "c"
    ]
    
    for strs in suffix_tests:
        suffix = find_common_suffix(strs)
        print(f"Common suffix of {strs}: '{suffix}'")
    
    # Test common substring
    substring_tests = [
        ["abcdef", "defghi", "ghijkl"],  # "def"
        ["abc", "def", "ghi"],           # ""
        ["abc", "bcd", "cde"],           # "bc"
    ]
    
    for strs in substring_tests:
        substring = find_common_substring(strs)
        print(f"Common substring of {strs}: '{substring}'")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    import string
    
    # Generate large test case
    def generate_random_string(length):
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    large_strs = [generate_random_string(100) for _ in range(100)]
    # Add a common prefix
    common_prefix = "common_prefix_"
    large_strs = [common_prefix + s for s in large_strs]
    
    # Test vertical approach
    start_time = time.time()
    for _ in range(100):
        longest_common_prefix(large_strs)
    vertical_time = time.time() - start_time
    
    # Test horizontal approach
    start_time = time.time()
    for _ in range(100):
        longest_common_prefix_horizontal(large_strs)
    horizontal_time = time.time() - start_time
    
    # Test binary search approach
    start_time = time.time()
    for _ in range(100):
        longest_common_prefix_binary_search(large_strs)
    binary_time = time.time() - start_time
    
    print(f"Vertical: {vertical_time:.6f} seconds")
    print(f"Horizontal: {horizontal_time:.6f} seconds")
    print(f"Binary search: {binary_time:.6f} seconds")
    
    # Edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],                    # Empty list
        [""],                  # Single empty string
        ["", ""],              # Multiple empty strings
        ["a", "a", "a"],       # All same strings
        ["a", "b", "c"],       # No common prefix
        ["ab", "abc", "abcd"], # Common prefix
    ]
    
    for case in edge_cases:
        result = longest_common_prefix(case)
        print(f"{case} -> '{result}'")
    
    # String analysis
    print("\nString analysis:")
    analysis_strs = ["flower", "flow", "flight"]
    print(f"Strings: {analysis_strs}")
    
    # Character by character analysis
    min_len = min(len(s) for s in analysis_strs)
    for i in range(min_len):
        chars = [s[i] for s in analysis_strs]
        print(f"Position {i}: {chars} -> All same: {len(set(chars)) == 1}")
    
    # Common prefix properties
    print("\nCommon prefix properties:")
    print("1. Common prefix is always a prefix of the shortest string")
    print("2. If all strings are the same, the common prefix is the entire string")
    print("3. If there's an empty string, the common prefix is empty")
    print("4. Common prefix is transitive: if A and B share prefix P, and B and C share prefix P, then A, B, C all share prefix P")
