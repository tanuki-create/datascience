"""
Problem 7: Valid Anagram
Difficulty: Easy

Given two strings s and t, return true if t is an anagram of s, and false otherwise.
An Anagram is a word or phrase formed by rearranging the letters of a different 
word or phrase, typically using all the original letters exactly once.

Time Complexity: O(n)
Space Complexity: O(1) - limited by alphabet size
"""

def is_anagram(s, t):
    """
    Check if two strings are anagrams using character counting.
    
    Args:
        s: First string
        t: Second string
        
    Returns:
        bool: True if anagrams, False otherwise
    """
    # Different lengths cannot be anagrams
    if len(s) != len(t):
        return False
    
    # Count characters in both strings
    char_count = {}
    
    # Count characters in s
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    
    # Subtract characters in t
    for char in t:
        if char not in char_count:
            return False
        char_count[char] -= 1
        if char_count[char] == 0:
            del char_count[char]
    
    # If all characters are matched, char_count should be empty
    return len(char_count) == 0


def is_anagram_sorting(s, t):
    """
    Check if two strings are anagrams using sorting.
    
    Args:
        s: First string
        t: Second string
        
    Returns:
        bool: True if anagrams, False otherwise
    """
    return sorted(s) == sorted(t)


def is_anagram_counter(s, t):
    """
    Check if two strings are anagrams using Counter from collections.
    
    Args:
        s: First string
        t: Second string
        
    Returns:
        bool: True if anagrams, False otherwise
    """
    from collections import Counter
    return Counter(s) == Counter(t)


def is_anagram_unicode(s, t):
    """
    Check if two strings are anagrams for Unicode characters.
    
    Args:
        s: First string
        t: Second string
        
    Returns:
        bool: True if anagrams, False otherwise
    """
    if len(s) != len(t):
        return False
    
    # Use a dictionary to handle Unicode characters
    char_count = {}
    
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    
    for char in t:
        if char not in char_count:
            return False
        char_count[char] -= 1
        if char_count[char] == 0:
            del char_count[char]
    
    return len(char_count) == 0


def is_anagram_case_insensitive(s, t):
    """
    Check if two strings are anagrams (case insensitive).
    
    Args:
        s: First string
        t: Second string
        
    Returns:
        bool: True if anagrams, False otherwise
    """
    return is_anagram(s.lower(), t.lower())


def find_anagrams_in_text(text, word):
    """
    Find all anagrams of a word in a given text.
    
    Args:
        text: The text to search in
        word: The word to find anagrams of
        
    Returns:
        list: List of anagram positions
    """
    if not text or not word:
        return []
    
    word_len = len(word)
    text_len = len(text)
    
    if word_len > text_len:
        return []
    
    # Get character count of the target word
    word_count = {}
    for char in word:
        word_count[char] = word_count.get(char, 0) + 1
    
    # Sliding window approach
    window_count = {}
    result = []
    
    # Initialize first window
    for i in range(word_len):
        char = text[i]
        window_count[char] = window_count.get(char, 0) + 1
    
    # Check if first window is an anagram
    if window_count == word_count:
        result.append(0)
    
    # Slide the window
    for i in range(word_len, text_len):
        # Remove leftmost character
        left_char = text[i - word_len]
        window_count[left_char] -= 1
        if window_count[left_char] == 0:
            del window_count[left_char]
        
        # Add new character
        new_char = text[i]
        window_count[new_char] = window_count.get(new_char, 0) + 1
        
        # Check if current window is an anagram
        if window_count == word_count:
            result.append(i - word_len + 1)
    
    return result


def group_anagrams(strs):
    """
    Group anagrams together (bonus problem).
    
    Args:
        strs: List of strings
        
    Returns:
        list: List of lists, each containing anagrams
    """
    from collections import defaultdict
    
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Use sorted string as key
        key = ''.join(sorted(s))
        anagram_groups[key].append(s)
    
    return list(anagram_groups.values())


# Test cases
if __name__ == "__main__":
    test_cases = [
        ("anagram", "nagaram"),  # True
        ("rat", "car"),          # False
        ("listen", "silent"),    # True
        ("a", "ab"),             # False
        ("", ""),                # True
        ("a", "a"),              # True
        ("ab", "ba"),            # True
        ("abc", "bca"),          # True
        ("hello", "world"),      # False
    ]
    
    for i, (s, t) in enumerate(test_cases, 1):
        print(f"Test case {i}: '{s}' and '{t}'")
        
        # Test different approaches
        result_counting = is_anagram(s, t)
        result_sorting = is_anagram_sorting(s, t)
        result_counter = is_anagram_counter(s, t)
        
        print(f"Character counting: {result_counting}")
        print(f"Sorting approach: {result_sorting}")
        print(f"Counter approach: {result_counter}")
        
        # Test Unicode support
        result_unicode = is_anagram_unicode(s, t)
        print(f"Unicode support: {result_unicode}")
        
        print("-" * 50)
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    
    # Large test case
    s_large = "abcdefghijklmnopqrstuvwxyz" * 1000
    t_large = "zyxwvutsrqponmlkjihgfedcba" * 1000
    
    # Test character counting
    start_time = time.time()
    for _ in range(100):
        is_anagram(s_large, t_large)
    counting_time = time.time() - start_time
    
    # Test sorting
    start_time = time.time()
    for _ in range(100):
        is_anagram_sorting(s_large, t_large)
    sorting_time = time.time() - start_time
    
    # Test Counter
    start_time = time.time()
    for _ in range(100):
        is_anagram_counter(s_large, t_large)
    counter_time = time.time() - start_time
    
    print(f"Character counting: {counting_time:.6f} seconds")
    print(f"Sorting approach: {sorting_time:.6f} seconds")
    print(f"Counter approach: {counter_time:.6f} seconds")
    
    # Test anagram finding
    print(f"\nAnagram finding in text:")
    text = "listen to the silent night, the stars are silent too"
    word = "silent"
    positions = find_anagrams_in_text(text, word)
    print(f"Text: '{text}'")
    print(f"Word: '{word}'")
    print(f"Anagram positions: {positions}")
    
    # Test anagram grouping
    print(f"\nAnagram grouping:")
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    groups = group_anagrams(words)
    print(f"Words: {words}")
    print(f"Groups: {groups}")
    
    # Unicode test
    print(f"\nUnicode test:")
    unicode_s = "café"
    unicode_t = "éfac"
    result = is_anagram_unicode(unicode_s, unicode_t)
    print(f"'{unicode_s}' and '{unicode_t}': {result}")
    
    # Case insensitive test
    print(f"\nCase insensitive test:")
    case_s = "Listen"
    case_t = "Silent"
    result = is_anagram_case_insensitive(case_s, case_t)
    print(f"'{case_s}' and '{case_t}': {result}")
