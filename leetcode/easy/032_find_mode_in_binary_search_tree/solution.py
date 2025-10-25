"""
Problem 32: Find Mode in Binary Search Tree
Difficulty: Easy

Given the root of a binary search tree (BST) with duplicates, return all the 
mode(s) (i.e., the most frequently occurred element) in it.

Time Complexity: O(n)
Space Complexity: O(n)
"""

class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"TreeNode({self.val})"


def find_mode(root):
    """
    Find all modes in a binary search tree.
    
    Args:
        root: Root of the binary search tree
        
    Returns:
        list: List of all modes
    """
    if not root:
        return []
    
    # Count frequencies using inorder traversal
    frequencies = {}
    
    def inorder_traversal(node):
        if not node:
            return
        
        inorder_traversal(node.left)
        frequencies[node.val] = frequencies.get(node.val, 0) + 1
        inorder_traversal(node.right)
    
    inorder_traversal(root)
    
    # Find maximum frequency
    max_frequency = max(frequencies.values())
    
    # Return all values with maximum frequency
    return [val for val, freq in frequencies.items() if freq == max_frequency]


def find_mode_optimized(root):
    """
    Find all modes using optimized approach without extra space.
    
    Args:
        root: Root of the binary search tree
        
    Returns:
        list: List of all modes
    """
    if not root:
        return []
    
    modes = []
    current_val = None
    current_count = 0
    max_count = 0
    
    def inorder_traversal(node):
        nonlocal current_val, current_count, max_count, modes
        
        if not node:
            return
        
        inorder_traversal(node.left)
        
        # Update current value and count
        if node.val == current_val:
            current_count += 1
        else:
            current_val = node.val
            current_count = 1
        
        # Update modes based on current count
        if current_count > max_count:
            max_count = current_count
            modes = [current_val]
        elif current_count == max_count:
            modes.append(current_val)
        
        inorder_traversal(node.right)
    
    inorder_traversal(root)
    return modes


def find_mode_verbose(root):
    """
    Find all modes with detailed step-by-step explanation.
    
    Args:
        root: Root of the binary search tree
        
    Returns:
        list: List of all modes
    """
    if not root:
        print("Empty tree, returning []")
        return []
    
    frequencies = {}
    
    def inorder_traversal_verbose(node, depth=0):
        indent = "  " * depth
        print(f"{indent}Processing node {node.val if node else None}")
        
        if not node:
            print(f"{indent}Node is None, returning")
            return
        
        print(f"{indent}Traversing left subtree...")
        inorder_traversal_verbose(node.left, depth + 1)
        
        print(f"{indent}Processing value {node.val}")
        frequencies[node.val] = frequencies.get(node.val, 0) + 1
        print(f"{indent}Frequency of {node.val}: {frequencies[node.val]}")
        
        print(f"{indent}Traversing right subtree...")
        inorder_traversal_verbose(node.right, depth + 1)
    
    print(f"Finding modes in BST with root {root.val}")
    inorder_traversal_verbose(root)
    
    print(f"\nFrequencies: {frequencies}")
    max_frequency = max(frequencies.values())
    print(f"Maximum frequency: {max_frequency}")
    
    modes = [val for val, freq in frequencies.items() if freq == max_frequency]
    print(f"Modes: {modes}")
    
    return modes


def find_mode_with_stats(root):
    """
    Find all modes and return statistics.
    
    Args:
        root: Root of the binary search tree
        
    Returns:
        dict: Statistics about the tree
    """
    if not root:
        return {
            'modes': [],
            'frequencies': {},
            'max_frequency': 0,
            'total_nodes': 0,
            'unique_values': 0
        }
    
    frequencies = {}
    total_nodes = 0
    
    def inorder_traversal(node):
        nonlocal total_nodes
        
        if not node:
            return
        
        inorder_traversal(node.left)
        frequencies[node.val] = frequencies.get(node.val, 0) + 1
        total_nodes += 1
        inorder_traversal(node.right)
    
    inorder_traversal(root)
    
    max_frequency = max(frequencies.values())
    modes = [val for val, freq in frequencies.items() if freq == max_frequency]
    
    return {
        'modes': modes,
        'frequencies': frequencies,
        'max_frequency': max_frequency,
        'total_nodes': total_nodes,
        'unique_values': len(frequencies)
    }


def find_mode_with_validation(root):
    """
    Find all modes with validation.
    
    Args:
        root: Root of the binary search tree
        
    Returns:
        dict: Detailed validation results
    """
    if not root:
        return {
            'modes': [],
            'is_valid': True,
            'reason': 'Empty tree',
            'frequencies': {}
        }
    
    frequencies = {}
    
    def inorder_traversal(node):
        if not node:
            return
        
        inorder_traversal(node.left)
        frequencies[node.val] = frequencies.get(node.val, 0) + 1
        inorder_traversal(node.right)
    
    inorder_traversal(root)
    
    max_frequency = max(frequencies.values())
    modes = [val for val, freq in frequencies.items() if freq == max_frequency]
    
    return {
        'modes': modes,
        'is_valid': True,
        'reason': f'Found {len(modes)} mode(s) with frequency {max_frequency}',
        'frequencies': frequencies
    }


def find_mode_with_paths(root):
    """
    Find all modes and return paths to them.
    
    Args:
        root: Root of the binary search tree
        
    Returns:
        dict: Modes with paths
    """
    if not root:
        return {
            'modes': [],
            'paths': []
        }
    
    frequencies = {}
    paths = {}
    
    def inorder_traversal(node, path):
        if not node:
            return
        
        current_path = path + [node.val]
        
        inorder_traversal(node.left, current_path)
        
        frequencies[node.val] = frequencies.get(node.val, 0) + 1
        if node.val not in paths:
            paths[node.val] = []
        paths[node.val].append(current_path)
        
        inorder_traversal(node.right, current_path)
    
    inorder_traversal(root, [])
    
    max_frequency = max(frequencies.values())
    modes = [val for val, freq in frequencies.items() if freq == max_frequency]
    
    return {
        'modes': modes,
        'paths': {mode: paths[mode] for mode in modes}
    }


def find_mode_with_levels(root):
    """
    Find all modes and return nodes by level.
    
    Args:
        root: Root of the binary search tree
        
    Returns:
        dict: Nodes organized by level
    """
    if not root:
        return {}
    
    from collections import deque
    queue = deque([(root, 0)])  # (node, level)
    levels = {}
    
    while queue:
        node, level = queue.popleft()
        
        if level not in levels:
            levels[level] = []
        levels[level].append(node.val)
        
        if node.left:
            queue.append((node.left, level + 1))
        if node.right:
            queue.append((node.right, level + 1))
    
    return levels


def find_mode_with_comparison(root):
    """
    Find all modes and compare with other approaches.
    
    Args:
        root: Root of the binary search tree
        
    Returns:
        dict: Comparison of different approaches
    """
    if not root:
        return {
            'hash_map': [],
            'optimized': []
        }
    
    # Hash map approach
    frequencies = {}
    
    def inorder_traversal(node):
        if not node:
            return
        
        inorder_traversal(node.left)
        frequencies[node.val] = frequencies.get(node.val, 0) + 1
        inorder_traversal(node.right)
    
    inorder_traversal(root)
    max_frequency = max(frequencies.values())
    hash_map_modes = [val for val, freq in frequencies.items() if freq == max_frequency]
    
    # Optimized approach
    optimized_modes = find_mode_optimized(root)
    
    return {
        'hash_map': hash_map_modes,
        'optimized': optimized_modes
    }


def create_tree_from_list(values):
    """
    Create a binary tree from a list of values.
    
    Args:
        values: List of values to create the tree
        
    Returns:
        TreeNode: Root of the created tree
    """
    if not values:
        return None
    
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    
    while queue and i < len(values):
        node = queue.pop(0)
        
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    
    return root


def print_tree_structure(root, level=0, prefix="Root: "):
    """
    Print the tree structure.
    
    Args:
        root: Root of the tree
        level: Current level
        prefix: Prefix for the current node
    """
    if root is not None:
        print(" " * (level * 4) + prefix + str(root.val))
        if root.left is not None or root.right is not None:
            if root.left:
                print_tree_structure(root.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            if root.right:
                print_tree_structure(root.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")


# Test cases
if __name__ == "__main__":
    test_cases = [
        [1, None, 2, 2],       # Expected: [2]
        [0],                  # Expected: [0]
        [1, 1, 2],            # Expected: [1, 2]
        [1, 2, 3, 2, 3, 3],  # Expected: [3]
        [1, 1, 1, 2, 2, 2],  # Expected: [1, 2]
        [1, 2, 3, 4, 5, 6, 7],  # Expected: [1, 2, 3, 4, 5, 6, 7]
    ]
    
    for i, values in enumerate(test_cases, 1):
        print(f"Test case {i}: {values}")
        
        # Create tree from values
        root = create_tree_from_list(values)
        
        # Test different approaches
        result_hash_map = find_mode(root)
        result_optimized = find_mode_optimized(root)
        
        print(f"Hash map approach: {result_hash_map}")
        print(f"Optimized approach: {result_optimized}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            find_mode_verbose(root)
        
        # Test with statistics
        stats = find_mode_with_stats(root)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = find_mode_with_validation(root)
        print(f"Validation: {validation}")
        
        # Test with paths
        paths = find_mode_with_paths(root)
        print(f"Paths: {paths}")
        
        # Test with levels
        levels = find_mode_with_levels(root)
        print(f"Levels: {levels}")
        
        # Test with comparison
        comparison = find_mode_with_comparison(root)
        print(f"Comparison: {comparison}")
        
        # Print tree structure
        print("\nTree structure:")
        print_tree_structure(root)
        
        print("-" * 50)
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],                    # Empty tree
        [1],                   # Single node
        [1, 1],                # Two same nodes
        [1, 2],                # Two different nodes
        [1, 1, 1],            # Three same nodes
        [1, 2, 3],             # Three different nodes
    ]
    
    for case in edge_cases:
        root = create_tree_from_list(case)
        result = find_mode(root)
        print(f"Tree: {case} -> Modes: {result}")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large tree
    def create_large_tree(depth):
        """Create a large tree for testing."""
        if depth == 0:
            return None
        
        root = TreeNode(random.randint(1, 100))
        root.left = create_large_tree(depth - 1)
        root.right = create_large_tree(depth - 1)
        return root
    
    large_root = create_large_tree(10)
    
    # Test hash map approach
    start_time = time.time()
    for _ in range(1000):
        find_mode(large_root)
    hash_map_time = time.time() - start_time
    
    # Test optimized approach
    start_time = time.time()
    for _ in range(1000):
        find_mode_optimized(large_root)
    optimized_time = time.time() - start_time
    
    print(f"Hash map approach: {hash_map_time:.6f} seconds")
    print(f"Optimized approach: {optimized_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Use inorder traversal to visit nodes in sorted order")
    print("2. Count frequency of each value")
    print("3. Find the maximum frequency")
    print("4. Return all values with maximum frequency")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_values = [1, None, 2, 2]
    root = create_tree_from_list(example_values)
    
    print(f"Tree: {example_values}")
    print("Tree structure:")
    print_tree_structure(root)
    
    print("\nMode finding steps:")
    print("1. Inorder traversal: 1, 2, 2")
    print("2. Count frequencies: {1: 1, 2: 2}")
    print("3. Maximum frequency: 2")
    print("4. Values with frequency 2: [2]")
    print("5. Modes: [2]")
    
    # Test with different tree shapes
    print("\nDifferent tree shapes:")
    
    # Skewed tree
    skewed_values = [1, 2, None, 3, None, 4, None]
    skewed_root = create_tree_from_list(skewed_values)
    skewed_result = find_mode(skewed_root)
    print(f"Skewed tree: {skewed_values} -> Modes: {skewed_result}")
    
    # Complete binary tree
    complete_values = [1, 2, 3, 4, 5, 6, 7]
    complete_root = create_tree_from_list(complete_values)
    complete_result = find_mode(complete_root)
    print(f"Complete tree: {complete_values} -> Modes: {complete_result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for case in [skewed_values, complete_values]:
        root = create_tree_from_list(case)
        stats = find_mode_with_stats(root)
        print(f"Tree: {case}")
        print(f"  Modes: {stats['modes']}")
        print(f"  Frequencies: {stats['frequencies']}")
        print(f"  Max frequency: {stats['max_frequency']}")
        print(f"  Total nodes: {stats['total_nodes']}")
        print(f"  Unique values: {stats['unique_values']}")
        print()
