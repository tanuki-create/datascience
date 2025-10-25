"""
Problem 20: Maximum Depth of Binary Tree
Difficulty: Easy

Given the root of a binary tree, return its maximum depth.
A binary tree's maximum depth is the number of nodes along the longest path 
from the root node down to the farthest leaf node.

Time Complexity: O(n)
Space Complexity: O(h) where h is the height of the tree
"""

class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"TreeNode({self.val})"


def max_depth(root):
    """
    Find the maximum depth of a binary tree using recursive approach.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        int: Maximum depth of the tree
    """
    if not root:
        return 0
    
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    
    return max(left_depth, right_depth) + 1


def max_depth_iterative(root):
    """
    Find the maximum depth using iterative approach with stack.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        int: Maximum depth of the tree
    """
    if not root:
        return 0
    
    stack = [(root, 1)]  # (node, depth)
    max_depth_found = 0
    
    while stack:
        node, depth = stack.pop()
        max_depth_found = max(max_depth_found, depth)
        
        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))
    
    return max_depth_found


def max_depth_level_order(root):
    """
    Find the maximum depth using level-order traversal.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        int: Maximum depth of the tree
    """
    if not root:
        return 0
    
    from collections import deque
    queue = deque([root])
    depth = 0
    
    while queue:
        level_size = len(queue)
        depth += 1
        
        for _ in range(level_size):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return depth


def max_depth_verbose(root):
    """
    Find the maximum depth with detailed step-by-step explanation.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        int: Maximum depth of the tree
    """
    def max_depth_helper(node, depth=0):
        if not node:
            print(f"  " * depth + f"Node is None, returning depth {depth}")
            return depth
        
        print(f"  " * depth + f"Processing node {node.val} at depth {depth}")
        
        left_depth = max_depth_helper(node.left, depth + 1)
        right_depth = max_depth_helper(node.right, depth + 1)
        
        max_depth_at_node = max(left_depth, right_depth)
        print(f"  " * depth + f"Max depth at node {node.val}: {max_depth_at_node}")
        
        return max_depth_at_node
    
    if not root:
        print("Empty tree, depth = 0")
        return 0
    
    print(f"Finding maximum depth of tree with root {root.val}")
    return max_depth_helper(root)


def max_depth_with_paths(root):
    """
    Find the maximum depth and return all paths to leaves.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        tuple: (max_depth, list_of_paths)
    """
    if not root:
        return 0, []
    
    def find_paths(node, path, all_paths):
        if not node:
            return
        
        path.append(node.val)
        
        if not node.left and not node.right:
            all_paths.append(path.copy())
        else:
            find_paths(node.left, path, all_paths)
            find_paths(node.right, path, all_paths)
        
        path.pop()
    
    all_paths = []
    find_paths(root, [], all_paths)
    
    max_depth_found = max(len(path) for path in all_paths) if all_paths else 0
    
    return max_depth_found, all_paths


def max_depth_with_stats(root):
    """
    Find the maximum depth and return detailed statistics.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Statistics about the tree
    """
    if not root:
        return {
            'max_depth': 0,
            'min_depth': 0,
            'node_count': 0,
            'leaf_count': 0,
            'internal_count': 0
        }
    
    def get_stats(node, depth=0):
        if not node:
            return {
                'max_depth': depth,
                'min_depth': depth,
                'node_count': 0,
                'leaf_count': 0,
                'internal_count': 0
            }
        
        left_stats = get_stats(node.left, depth + 1)
        right_stats = get_stats(node.right, depth + 1)
        
        max_depth = max(left_stats['max_depth'], right_stats['max_depth'])
        min_depth = min(left_stats['min_depth'], right_stats['min_depth'])
        node_count = left_stats['node_count'] + right_stats['node_count'] + 1
        leaf_count = left_stats['leaf_count'] + right_stats['leaf_count']
        internal_count = left_stats['internal_count'] + right_stats['internal_count']
        
        # If this is a leaf node
        if not node.left and not node.right:
            leaf_count += 1
        else:
            internal_count += 1
        
        return {
            'max_depth': max_depth,
            'min_depth': min_depth,
            'node_count': node_count,
            'leaf_count': leaf_count,
            'internal_count': internal_count
        }
    
    stats = get_stats(root)
    return stats


def max_depth_with_levels(root):
    """
    Find the maximum depth and return nodes at each level.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        tuple: (max_depth, dict_of_levels)
    """
    if not root:
        return 0, {}
    
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
    
    max_depth_found = max(levels.keys()) + 1 if levels else 0
    
    return max_depth_found, levels


def max_depth_with_balance_check(root):
    """
    Find the maximum depth and check if the tree is balanced.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        tuple: (max_depth, is_balanced)
    """
    def get_depth_and_balance(node):
        if not node:
            return 0, True
        
        left_depth, left_balanced = get_depth_and_balance(node.left)
        right_depth, right_balanced = get_depth_and_balance(node.right)
        
        depth = max(left_depth, right_depth) + 1
        is_balanced = (left_balanced and right_balanced and 
                      abs(left_depth - right_depth) <= 1)
        
        return depth, is_balanced
    
    if not root:
        return 0, True
    
    depth, is_balanced = get_depth_and_balance(root)
    return depth, is_balanced


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
        [3, 9, 20, None, None, 15, 7],  # Expected: 3
        [1, None, 2],                   # Expected: 2
        [],                             # Expected: 0
        [1],                            # Expected: 1
        [1, 2, 3, 4, 5, 6, 7],         # Expected: 3
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],  # Expected: 4
    ]
    
    for i, values in enumerate(test_cases, 1):
        print(f"Test case {i}: {values}")
        
        # Create tree from values
        root = create_tree_from_list(values)
        
        # Test different approaches
        result_recursive = max_depth(root)
        result_iterative = max_depth_iterative(root)
        result_level = max_depth_level_order(root)
        
        print(f"Recursive: {result_recursive}")
        print(f"Iterative: {result_iterative}")
        print(f"Level order: {result_level}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            max_depth_verbose(root)
        
        # Test with paths
        max_depth_found, paths = max_depth_with_paths(root)
        print(f"Max depth with paths: {max_depth_found}")
        print(f"Paths to leaves: {paths}")
        
        # Test with statistics
        stats = max_depth_with_stats(root)
        print(f"Statistics: {stats}")
        
        # Test with levels
        depth, levels = max_depth_with_levels(root)
        print(f"Levels: {levels}")
        
        # Test balance check
        depth, is_balanced = max_depth_with_balance_check(root)
        print(f"Depth: {depth}, Is balanced: {is_balanced}")
        
        # Print tree structure
        print("\nTree structure:")
        print_tree_structure(root)
        
        print("-" * 50)
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],                    # Empty tree
        [1],                   # Single node
        [1, 2],                # Two nodes
        [1, 2, 3],             # Three nodes
        [1, 2, 3, 4, 5, 6, 7], # Complete binary tree
        [1, 2, None, 3, None, 4, None],  # Skewed tree
    ]
    
    for case in edge_cases:
        if case:
            root = create_tree_from_list(case)
            result = max_depth(root)
            print(f"Tree: {case} -> Max depth: {result}")
        else:
            print("Empty tree -> Max depth: 0")
    
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
    
    large_root = create_large_tree(15)
    
    # Test recursive approach
    start_time = time.time()
    for _ in range(1000):
        max_depth(large_root)
    recursive_time = time.time() - start_time
    
    # Test iterative approach
    start_time = time.time()
    for _ in range(1000):
        max_depth_iterative(large_root)
    iterative_time = time.time() - start_time
    
    # Test level-order approach
    start_time = time.time()
    for _ in range(1000):
        max_depth_level_order(large_root)
    level_time = time.time() - start_time
    
    print(f"Recursive: {recursive_time:.6f} seconds")
    print(f"Iterative: {iterative_time:.6f} seconds")
    print(f"Level order: {level_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. If the tree is empty, depth is 0")
    print("2. If the tree has only a root, depth is 1")
    print("3. For any node, depth = max(left_depth, right_depth) + 1")
    print("4. Recursively calculate depth of left and right subtrees")
    print("5. Return the maximum depth found")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_values = [3, 9, 20, None, None, 15, 7]
    example_root = create_tree_from_list(example_values)
    print(f"Tree: {example_values}")
    print("Tree structure:")
    print_tree_structure(example_root)
    
    print("\nCalculating depth:")
    print("1. Root (3): depth = max(left_depth, right_depth) + 1")
    print("2. Left subtree (9): depth = max(0, 0) + 1 = 1")
    print("3. Right subtree (20): depth = max(left_depth, right_depth) + 1")
    print("4. Right-left (15): depth = max(0, 0) + 1 = 1")
    print("5. Right-right (7): depth = max(0, 0) + 1 = 1")
    print("6. Right subtree (20): depth = max(1, 1) + 1 = 2")
    print("7. Root (3): depth = max(1, 2) + 1 = 3")
    
    # Test with different tree shapes
    print("\nDifferent tree shapes:")
    
    # Skewed tree
    skewed_values = [1, 2, None, 3, None, 4, None]
    skewed_root = create_tree_from_list(skewed_values)
    skewed_depth = max_depth(skewed_root)
    print(f"Skewed tree: {skewed_values} -> Depth: {skewed_depth}")
    
    # Complete binary tree
    complete_values = [1, 2, 3, 4, 5, 6, 7]
    complete_root = create_tree_from_list(complete_values)
    complete_depth = max_depth(complete_root)
    print(f"Complete tree: {complete_values} -> Depth: {complete_depth}")
    
    # Test balance check
    print("\nBalance check:")
    for case in [skewed_values, complete_values]:
        root = create_tree_from_list(case)
        depth, is_balanced = max_depth_with_balance_check(root)
        print(f"Tree: {case} -> Depth: {depth}, Balanced: {is_balanced}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for case in [skewed_values, complete_values]:
        root = create_tree_from_list(case)
        stats = max_depth_with_stats(root)
        print(f"Tree: {case}")
        print(f"  Max depth: {stats['max_depth']}")
        print(f"  Min depth: {stats['min_depth']}")
        print(f"  Node count: {stats['node_count']}")
        print(f"  Leaf count: {stats['leaf_count']}")
        print(f"  Internal count: {stats['internal_count']}")
        print()
