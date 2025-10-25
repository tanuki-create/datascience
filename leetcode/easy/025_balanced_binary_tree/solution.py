"""
Problem 25: Balanced Binary Tree
Difficulty: Easy

Given a binary tree, determine if it is height-balanced.
A height-balanced binary tree is defined as a binary tree in which the left and 
right subtrees of every node differ in height by no more than 1.

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


def is_balanced(root):
    """
    Check if a binary tree is height-balanced using recursive approach.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        bool: True if balanced, False otherwise
    """
    def get_height(node):
        if not node:
            return 0
        
        left_height = get_height(node.left)
        right_height = get_height(node.right)
        
        # If any subtree is unbalanced, return -1
        if left_height == -1 or right_height == -1:
            return -1
        
        # Check if current node is balanced
        if abs(left_height - right_height) > 1:
            return -1
        
        return max(left_height, right_height) + 1
    
    return get_height(root) != -1


def is_balanced_verbose(root):
    """
    Check if a binary tree is height-balanced with detailed step-by-step explanation.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        bool: True if balanced, False otherwise
    """
    def get_height_verbose(node, depth=0):
        indent = "  " * depth
        print(f"{indent}Checking node {node.val if node else None}")
        
        if not node:
            print(f"{indent}Node is None, height = 0")
            return 0
        
        print(f"{indent}Getting height of left subtree...")
        left_height = get_height_verbose(node.left, depth + 1)
        print(f"{indent}Getting height of right subtree...")
        right_height = get_height_verbose(node.right, depth + 1)
        
        print(f"{indent}Left height: {left_height}, Right height: {right_height}")
        
        # If any subtree is unbalanced, return -1
        if left_height == -1 or right_height == -1:
            print(f"{indent}Subtree is unbalanced, returning -1")
            return -1
        
        # Check if current node is balanced
        height_diff = abs(left_height - right_height)
        print(f"{indent}Height difference: {height_diff}")
        
        if height_diff > 1:
            print(f"{indent}Height difference > 1, tree is unbalanced")
            return -1
        
        current_height = max(left_height, right_height) + 1
        print(f"{indent}Current node height: {current_height}")
        return current_height
    
    if not root:
        print("Empty tree is balanced")
        return True
    
    print(f"Checking if tree with root {root.val} is balanced")
    height = get_height_verbose(root)
    is_balanced_result = height != -1
    print(f"Tree is balanced: {is_balanced_result}")
    return is_balanced_result


def is_balanced_with_stats(root):
    """
    Check if a binary tree is height-balanced and return statistics.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Statistics about the tree balance
    """
    if not root:
        return {
            'is_balanced': True,
            'height': 0,
            'nodes_checked': 0,
            'unbalanced_nodes': []
        }
    
    nodes_checked = 0
    unbalanced_nodes = []
    
    def get_height_with_stats(node, depth=0):
        nonlocal nodes_checked, unbalanced_nodes
        
        if not node:
            return 0
        
        nodes_checked += 1
        
        left_height = get_height_with_stats(node.left, depth + 1)
        right_height = get_height_with_stats(node.right, depth + 1)
        
        # If any subtree is unbalanced, return -1
        if left_height == -1 or right_height == -1:
            return -1
        
        # Check if current node is balanced
        if abs(left_height - right_height) > 1:
            unbalanced_nodes.append((node.val, depth, abs(left_height - right_height)))
            return -1
        
        return max(left_height, right_height) + 1
    
    height = get_height_with_stats(root)
    
    return {
        'is_balanced': height != -1,
        'height': height if height != -1 else 0,
        'nodes_checked': nodes_checked,
        'unbalanced_nodes': unbalanced_nodes
    }


def is_balanced_with_levels(root):
    """
    Check if a binary tree is height-balanced and return nodes by level.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        tuple: (is_balanced, dict_of_levels)
    """
    if not root:
        return True, {}
    
    from collections import deque
    queue = deque([(root, 0)])  # (node, level)
    levels = {}
    
    while queue:
        node, level = queue.popleft()
        
        if level not in levels:
            levels[level] = []
        levels[level].append(node.val)
        
        # Add children to queue
        if node.left:
            queue.append((node.left, level + 1))
        if node.right:
            queue.append((node.right, level + 1))
    
    # Check balance by comparing levels
    max_level = max(levels.keys()) if levels else 0
    is_balanced_result = True
    
    for level in levels:
        if level > 0:
            # Check if current level has too many nodes compared to previous level
            if len(levels[level]) > 2 * len(levels.get(level - 1, [])):
                is_balanced_result = False
                break
    
    return is_balanced_result, levels


def is_balanced_with_validation(root):
    """
    Check if a binary tree is height-balanced with validation.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Detailed validation results
    """
    if not root:
        return {
            'is_balanced': True,
            'height': 0,
            'reason': 'Empty tree is balanced',
            'unbalanced_nodes': []
        }
    
    unbalanced_nodes = []
    
    def get_height_with_validation(node, depth=0):
        if not node:
            return 0
        
        left_height = get_height_with_validation(node.left, depth + 1)
        right_height = get_height_with_validation(node.right, depth + 1)
        
        # If any subtree is unbalanced, return -1
        if left_height == -1 or right_height == -1:
            return -1
        
        # Check if current node is balanced
        height_diff = abs(left_height - right_height)
        if height_diff > 1:
            unbalanced_nodes.append({
                'node': node.val,
                'depth': depth,
                'left_height': left_height,
                'right_height': right_height,
                'height_diff': height_diff
            })
            return -1
        
        return max(left_height, right_height) + 1
    
    height = get_height_with_validation(root)
    
    return {
        'is_balanced': height != -1,
        'height': height if height != -1 else 0,
        'reason': f'Tree is balanced' if height != -1 else f'Tree is unbalanced at {len(unbalanced_nodes)} node(s)',
        'unbalanced_nodes': unbalanced_nodes
    }


def is_balanced_iterative(root):
    """
    Check if a binary tree is height-balanced using iterative approach.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        bool: True if balanced, False otherwise
    """
    if not root:
        return True
    
    # Use post-order traversal to check balance
    stack = []
    last_visited = None
    heights = {}
    
    while stack or root:
        if root:
            stack.append(root)
            root = root.left
        else:
            node = stack[-1]
            if node.right and node.right != last_visited:
                root = node.right
            else:
                # Process node
                left_height = heights.get(node.left, 0)
                right_height = heights.get(node.right, 0)
                
                if abs(left_height - right_height) > 1:
                    return False
                
                heights[node] = max(left_height, right_height) + 1
                last_visited = stack.pop()
    
    return True


def is_balanced_with_paths(root):
    """
    Check if a binary tree is height-balanced and return paths to leaves.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        tuple: (is_balanced, list_of_paths)
    """
    if not root:
        return True, []
    
    def get_paths(node, path, all_paths):
        if not node:
            return
        
        current_path = path + [node.val]
        
        if not node.left and not node.right:
            all_paths.append(current_path)
        else:
            get_paths(node.left, current_path, all_paths)
            get_paths(node.right, current_path, all_paths)
    
    all_paths = []
    get_paths(root, [], all_paths)
    
    # Check if all paths have similar lengths
    if not all_paths:
        return True, []
    
    path_lengths = [len(path) for path in all_paths]
    min_length = min(path_lengths)
    max_length = max(path_lengths)
    
    is_balanced_result = max_length - min_length <= 1
    
    return is_balanced_result, all_paths


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
        [3, 9, 20, None, None, 15, 7],     # Expected: True
        [1, 2, 2, 3, 3, None, None, 4, 4],  # Expected: False
        [],                               # Expected: True
        [1],                              # Expected: True
        [1, 2],                           # Expected: True
        [1, 2, 3],                        # Expected: True
        [1, 2, 3, 4, 5, 6, 7],           # Expected: True
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],  # Expected: True
    ]
    
    for i, values in enumerate(test_cases, 1):
        print(f"Test case {i}: {values}")
        
        # Create tree from values
        root = create_tree_from_list(values)
        
        # Test different approaches
        result_recursive = is_balanced(root)
        result_iterative = is_balanced_iterative(root)
        
        print(f"Recursive: {result_recursive}")
        print(f"Iterative: {result_iterative}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            is_balanced_verbose(root)
        
        # Test with statistics
        stats = is_balanced_with_stats(root)
        print(f"Statistics: {stats}")
        
        # Test with levels
        is_balanced_result, levels = is_balanced_with_levels(root)
        print(f"Levels: {levels}")
        
        # Test with validation
        validation = is_balanced_with_validation(root)
        print(f"Validation: {validation}")
        
        # Test with paths
        is_balanced_paths, paths = is_balanced_with_paths(root)
        print(f"Paths: {paths}")
        
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
        result = is_balanced(root)
        print(f"Tree: {case} -> Balanced: {result}")
    
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
        is_balanced(large_root)
    recursive_time = time.time() - start_time
    
    # Test iterative approach
    start_time = time.time()
    for _ in range(1000):
        is_balanced_iterative(large_root)
    iterative_time = time.time() - start_time
    
    print(f"Recursive: {recursive_time:.6f} seconds")
    print(f"Iterative: {iterative_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. A tree is height-balanced if:")
    print("   - The left and right subtrees differ in height by no more than 1")
    print("   - Both left and right subtrees are also height-balanced")
    print("2. Use post-order traversal to check balance from bottom up")
    print("3. Return -1 if any subtree is unbalanced")
    print("4. Return height if the tree is balanced")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_values = [3, 9, 20, None, None, 15, 7]
    root = create_tree_from_list(example_values)
    
    print(f"Tree: {example_values}")
    print("Tree structure:")
    print_tree_structure(root)
    
    print("\nBalance check steps:")
    print("1. Check leaf nodes (9, 15, 7): height = 1, balanced")
    print("2. Check node 20: left height = 1, right height = 1, difference = 0, balanced")
    print("3. Check root 3: left height = 1, right height = 2, difference = 1, balanced")
    print("4. All nodes are balanced -> Tree is balanced")
    
    # Test with different tree shapes
    print("\nDifferent tree shapes:")
    
    # Skewed tree
    skewed_values = [1, 2, None, 3, None, 4, None]
    skewed_root = create_tree_from_list(skewed_values)
    skewed_balanced = is_balanced(skewed_root)
    print(f"Skewed tree: {skewed_values} -> Balanced: {skewed_balanced}")
    
    # Complete binary tree
    complete_values = [1, 2, 3, 4, 5, 6, 7]
    complete_root = create_tree_from_list(complete_values)
    complete_balanced = is_balanced(complete_root)
    print(f"Complete tree: {complete_values} -> Balanced: {complete_balanced}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for case in [skewed_values, complete_values]:
        root = create_tree_from_list(case)
        stats = is_balanced_with_stats(root)
        print(f"Tree: {case}")
        print(f"  Balanced: {stats['is_balanced']}")
        print(f"  Height: {stats['height']}")
        print(f"  Nodes checked: {stats['nodes_checked']}")
        print(f"  Unbalanced nodes: {stats['unbalanced_nodes']}")
        print()
