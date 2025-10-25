"""
Problem 24: Minimum Depth of Binary Tree
Difficulty: Easy

Given a binary tree, find its minimum depth.
The minimum depth is the number of nodes along the shortest path from the root 
node down to the nearest leaf node.

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


def min_depth(root):
    """
    Find the minimum depth of a binary tree using recursive approach.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        int: Minimum depth of the tree
    """
    if not root:
        return 0
    
    # If it's a leaf node, depth is 1
    if not root.left and not root.right:
        return 1
    
    # If one subtree is empty, return depth of the other subtree
    if not root.left:
        return min_depth(root.right) + 1
    if not root.right:
        return min_depth(root.left) + 1
    
    # Both subtrees exist, return minimum of both
    return min(min_depth(root.left), min_depth(root.right)) + 1


def min_depth_iterative(root):
    """
    Find the minimum depth using iterative approach with level-order traversal.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        int: Minimum depth of the tree
    """
    if not root:
        return 0
    
    from collections import deque
    queue = deque([(root, 1)])  # (node, depth)
    
    while queue:
        node, depth = queue.popleft()
        
        # If it's a leaf node, return its depth
        if not node.left and not node.right:
            return depth
        
        # Add children to queue
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    
    return 0


def min_depth_iterative_stack(root):
    """
    Find the minimum depth using iterative approach with stack.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        int: Minimum depth of the tree
    """
    if not root:
        return 0
    
    stack = [(root, 1)]  # (node, depth)
    min_depth_found = float('inf')
    
    while stack:
        node, depth = stack.pop()
        
        # If it's a leaf node, update minimum depth
        if not node.left and not node.right:
            min_depth_found = min(min_depth_found, depth)
        else:
            # Add children to stack
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))
    
    return min_depth_found if min_depth_found != float('inf') else 0


def min_depth_verbose(root):
    """
    Find the minimum depth with detailed step-by-step explanation.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        int: Minimum depth of the tree
    """
    def find_min_depth_helper(node, depth=0):
        indent = "  " * depth
        print(f"{indent}Processing node {node.val if node else None} at depth {depth}")
        
        if not node:
            print(f"{indent}Node is None, returning 0")
            return 0
        
        # If it's a leaf node, depth is 1
        if not node.left and not node.right:
            print(f"{indent}Leaf node {node.val}, returning depth 1")
            return 1
        
        # If one subtree is empty, return depth of the other subtree
        if not node.left:
            print(f"{indent}Left subtree is empty, checking right subtree")
            right_depth = find_min_depth_helper(node.right, depth + 1)
            print(f"{indent}Right subtree depth: {right_depth}, returning {right_depth + 1}")
            return right_depth + 1
        
        if not node.right:
            print(f"{indent}Right subtree is empty, checking left subtree")
            left_depth = find_min_depth_helper(node.left, depth + 1)
            print(f"{indent}Left subtree depth: {left_depth}, returning {left_depth + 1}")
            return left_depth + 1
        
        # Both subtrees exist, return minimum of both
        print(f"{indent}Both subtrees exist, checking both")
        left_depth = find_min_depth_helper(node.left, depth + 1)
        right_depth = find_min_depth_helper(node.right, depth + 1)
        min_depth_at_node = min(left_depth, right_depth) + 1
        print(f"{indent}Left depth: {left_depth}, Right depth: {right_depth}")
        print(f"{indent}Minimum depth at node {node.val}: {min_depth_at_node}")
        return min_depth_at_node
    
    if not root:
        print("Empty tree, depth = 0")
        return 0
    
    print(f"Finding minimum depth of tree with root {root.val}")
    return find_min_depth_helper(root)


def min_depth_with_paths(root):
    """
    Find the minimum depth and return all paths to leaves.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        tuple: (min_depth, list_of_paths)
    """
    if not root:
        return 0, []
    
    def find_paths(node, path, all_paths):
        if not node:
            return
        
        current_path = path + [node.val]
        
        if not node.left and not node.right:
            all_paths.append(current_path)
        else:
            find_paths(node.left, current_path, all_paths)
            find_paths(node.right, current_path, all_paths)
    
    all_paths = []
    find_paths(root, [], all_paths)
    
    min_depth_found = min(len(path) for path in all_paths) if all_paths else 0
    
    return min_depth_found, all_paths


def min_depth_with_stats(root):
    """
    Find the minimum depth and return detailed statistics.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Statistics about the tree
    """
    if not root:
        return {
            'min_depth': 0,
            'max_depth': 0,
            'node_count': 0,
            'leaf_count': 0,
            'paths_to_leaves': []
        }
    
    def get_stats(node, depth=0):
        if not node:
            return {
                'min_depth': float('inf'),
                'max_depth': 0,
                'node_count': 0,
                'leaf_count': 0,
                'paths_to_leaves': []
            }
        
        left_stats = get_stats(node.left, depth + 1)
        right_stats = get_stats(node.right, depth + 1)
        
        # If this is a leaf node
        if not node.left and not node.right:
            return {
                'min_depth': depth + 1,
                'max_depth': depth + 1,
                'node_count': 1,
                'leaf_count': 1,
                'paths_to_leaves': [[node.val]]
            }
        
        # Combine statistics from left and right subtrees
        min_depth = min(left_stats['min_depth'], right_stats['min_depth'])
        max_depth = max(left_stats['max_depth'], right_stats['max_depth'])
        node_count = left_stats['node_count'] + right_stats['node_count'] + 1
        leaf_count = left_stats['leaf_count'] + right_stats['leaf_count']
        
        # Combine paths
        paths = []
        for path in left_stats['paths_to_leaves']:
            paths.append([node.val] + path)
        for path in right_stats['paths_to_leaves']:
            paths.append([node.val] + path)
        
        return {
            'min_depth': min_depth,
            'max_depth': max_depth,
            'node_count': node_count,
            'leaf_count': leaf_count,
            'paths_to_leaves': paths
        }
    
    stats = get_stats(root)
    return stats


def min_depth_with_levels(root):
    """
    Find the minimum depth and return nodes at each level.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        tuple: (min_depth, dict_of_levels)
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
        
        # If it's a leaf node, we found the minimum depth
        if not node.left and not node.right:
            return level + 1, levels
        
        # Add children to queue
        if node.left:
            queue.append((node.left, level + 1))
        if node.right:
            queue.append((node.right, level + 1))
    
    return 0, levels


def min_depth_with_validation(root):
    """
    Find the minimum depth with validation and error checking.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Detailed validation results
    """
    if not root:
        return {
            'min_depth': 0,
            'is_valid': True,
            'reason': 'Empty tree',
            'paths_found': 0
        }
    
    def validate_and_find_depth(node, depth=0):
        if not node:
            return float('inf'), True, 0
        
        # If it's a leaf node, return depth 1
        if not node.left and not node.right:
            return depth + 1, True, 1
        
        # If one subtree is empty, return depth of the other subtree
        if not node.left:
            right_depth, is_valid, paths = validate_and_find_depth(node.right, depth + 1)
            return right_depth, is_valid, paths
        
        if not node.right:
            left_depth, is_valid, paths = validate_and_find_depth(node.left, depth + 1)
            return left_depth, is_valid, paths
        
        # Both subtrees exist, return minimum of both
        left_depth, left_valid, left_paths = validate_and_find_depth(node.left, depth + 1)
        right_depth, right_valid, right_paths = validate_and_find_depth(node.right, depth + 1)
        
        min_depth_at_node = min(left_depth, right_depth)
        is_valid = left_valid and right_valid
        total_paths = left_paths + right_paths
        
        return min_depth_at_node, is_valid, total_paths
    
    min_depth_found, is_valid, paths_found = validate_and_find_depth(root)
    
    return {
        'min_depth': min_depth_found if min_depth_found != float('inf') else 0,
        'is_valid': is_valid,
        'reason': f'Found {paths_found} path(s) to leaves' if is_valid else 'Invalid tree structure',
        'paths_found': paths_found
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
        [3, 9, 20, None, None, 15, 7],     # Expected: 2
        [2, None, 3, None, 4, None, 5, None, 6],  # Expected: 5
        [1],                               # Expected: 1
        [],                                # Expected: 0
        [1, 2],                            # Expected: 2
        [1, 2, 3],                         # Expected: 2
        [1, 2, 3, 4, 5, 6, 7],            # Expected: 3
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],  # Expected: 4
    ]
    
    for i, values in enumerate(test_cases, 1):
        print(f"Test case {i}: {values}")
        
        # Create tree from values
        root = create_tree_from_list(values)
        
        # Test different approaches
        result_recursive = min_depth(root)
        result_iterative = min_depth_iterative(root)
        result_stack = min_depth_iterative_stack(root)
        
        print(f"Recursive: {result_recursive}")
        print(f"Iterative (queue): {result_iterative}")
        print(f"Iterative (stack): {result_stack}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            min_depth_verbose(root)
        
        # Test with paths
        min_depth_found, paths = min_depth_with_paths(root)
        print(f"Min depth with paths: {min_depth_found}")
        print(f"Paths to leaves: {paths}")
        
        # Test with statistics
        stats = min_depth_with_stats(root)
        print(f"Statistics: {stats}")
        
        # Test with levels
        depth, levels = min_depth_with_levels(root)
        print(f"Levels: {levels}")
        
        # Test with validation
        validation = min_depth_with_validation(root)
        print(f"Validation: {validation}")
        
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
        root = create_tree_from_list(case)
        result = min_depth(root)
        print(f"Tree: {case} -> Min depth: {result}")
    
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
    
    # Test recursive approach
    start_time = time.time()
    for _ in range(1000):
        min_depth(large_root)
    recursive_time = time.time() - start_time
    
    # Test iterative approach
    start_time = time.time()
    for _ in range(1000):
        min_depth_iterative(large_root)
    iterative_time = time.time() - start_time
    
    # Test stack approach
    start_time = time.time()
    for _ in range(1000):
        min_depth_iterative_stack(large_root)
    stack_time = time.time() - start_time
    
    print(f"Recursive: {recursive_time:.6f} seconds")
    print(f"Iterative (queue): {iterative_time:.6f} seconds")
    print(f"Iterative (stack): {stack_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. If the tree is empty, depth is 0")
    print("2. If the tree has only a root, depth is 1")
    print("3. For any node, depth = min(left_depth, right_depth) + 1")
    print("4. If one subtree is empty, return depth of the other subtree")
    print("5. Recursively calculate depth of left and right subtrees")
    print("6. Return the minimum depth found")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_values = [3, 9, 20, None, None, 15, 7]
    root = create_tree_from_list(example_values)
    
    print(f"Tree: {example_values}")
    print("Tree structure:")
    print_tree_structure(root)
    
    print("\nCalculating minimum depth:")
    print("1. Root (3): depth = min(left_depth, right_depth) + 1")
    print("2. Left subtree (9): depth = min(0, 0) + 1 = 1 (leaf)")
    print("3. Right subtree (20): depth = min(left_depth, right_depth) + 1")
    print("4. Right-left (15): depth = min(0, 0) + 1 = 1 (leaf)")
    print("5. Right-right (7): depth = min(0, 0) + 1 = 1 (leaf)")
    print("6. Right subtree (20): depth = min(1, 1) + 1 = 2")
    print("7. Root (3): depth = min(1, 2) + 1 = 2")
    
    # Test with different tree shapes
    print("\nDifferent tree shapes:")
    
    # Skewed tree
    skewed_values = [1, 2, None, 3, None, 4, None]
    skewed_root = create_tree_from_list(skewed_values)
    skewed_depth = min_depth(skewed_root)
    print(f"Skewed tree: {skewed_values} -> Min depth: {skewed_depth}")
    
    # Complete binary tree
    complete_values = [1, 2, 3, 4, 5, 6, 7]
    complete_root = create_tree_from_list(complete_values)
    complete_depth = min_depth(complete_root)
    print(f"Complete tree: {complete_values} -> Min depth: {complete_depth}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for case in [skewed_values, complete_values]:
        root = create_tree_from_list(case)
        stats = min_depth_with_stats(root)
        print(f"Tree: {case}")
        print(f"  Min depth: {stats['min_depth']}")
        print(f"  Max depth: {stats['max_depth']}")
        print(f"  Node count: {stats['node_count']}")
        print(f"  Leaf count: {stats['leaf_count']}")
        print(f"  Paths to leaves: {stats['paths_to_leaves']}")
        print()
