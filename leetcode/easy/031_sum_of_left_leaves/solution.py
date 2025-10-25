"""
Problem 31: Sum of Left Leaves
Difficulty: Easy

Given the root of a binary tree, return the sum of all left leaves.
A leaf is a node with no children. A left leaf is a leaf that is the left child of another node.

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


def sum_of_left_leaves(root):
    """
    Find the sum of all left leaves using recursive approach.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        int: Sum of all left leaves
    """
    if not root:
        return 0
    
    def is_leaf(node):
        return node and not node.left and not node.right
    
    def sum_left_leaves_helper(node, is_left_child):
        if not node:
            return 0
        
        # If it's a left leaf, return its value
        if is_leaf(node) and is_left_child:
            return node.val
        
        # Recursively sum left and right subtrees
        return (sum_left_leaves_helper(node.left, True) + 
                sum_left_leaves_helper(node.right, False))
    
    return sum_left_leaves_helper(root, False)


def sum_of_left_leaves_iterative(root):
    """
    Find the sum of all left leaves using iterative approach.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        int: Sum of all left leaves
    """
    if not root:
        return 0
    
    from collections import deque
    queue = deque([(root, False)])  # (node, is_left_child)
    total_sum = 0
    
    while queue:
        node, is_left_child = queue.popleft()
        
        # If it's a left leaf, add its value
        if node.left is None and node.right is None and is_left_child:
            total_sum += node.val
        
        # Add children to queue
        if node.left:
            queue.append((node.left, True))
        if node.right:
            queue.append((node.right, False))
    
    return total_sum


def sum_of_left_leaves_verbose(root):
    """
    Find the sum of all left leaves with detailed step-by-step explanation.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        int: Sum of all left leaves
    """
    if not root:
        print("Empty tree, returning 0")
        return 0
    
    def is_leaf(node):
        return node and not node.left and not node.right
    
    def sum_helper(node, is_left_child, depth=0):
        indent = "  " * depth
        print(f"{indent}Processing node {node.val if node else None}")
        print(f"{indent}Is left child: {is_left_child}")
        
        if not node:
            print(f"{indent}Node is None, returning 0")
            return 0
        
        # If it's a left leaf, return its value
        if is_leaf(node) and is_left_child:
            print(f"{indent}Found left leaf with value {node.val}")
            return node.val
        
        print(f"{indent}Not a left leaf, checking children...")
        left_sum = sum_helper(node.left, True, depth + 1)
        right_sum = sum_helper(node.right, False, depth + 1)
        
        total = left_sum + right_sum
        print(f"{indent}Sum at node {node.val}: {total}")
        return total
    
    print(f"Finding sum of left leaves in tree with root {root.val}")
    return sum_helper(root, False)


def sum_of_left_leaves_with_stats(root):
    """
    Find the sum of all left leaves and return statistics.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Statistics about the tree
    """
    if not root:
        return {
            'sum': 0,
            'left_leaves': [],
            'total_leaves': 0,
            'left_leaf_count': 0
        }
    
    left_leaves = []
    total_leaves = 0
    
    def is_leaf(node):
        return node and not node.left and not node.right
    
    def sum_helper(node, is_left_child):
        nonlocal total_leaves
        
        if not node:
            return 0
        
        # If it's a leaf, count it
        if is_leaf(node):
            total_leaves += 1
            if is_left_child:
                left_leaves.append(node.val)
                return node.val
        
        # Recursively sum left and right subtrees
        return (sum_helper(node.left, True) + 
                sum_helper(node.right, False))
    
    total_sum = sum_helper(root, False)
    
    return {
        'sum': total_sum,
        'left_leaves': left_leaves,
        'total_leaves': total_leaves,
        'left_leaf_count': len(left_leaves)
    }


def sum_of_left_leaves_with_validation(root):
    """
    Find the sum of all left leaves with validation.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Detailed validation results
    """
    if not root:
        return {
            'sum': 0,
            'is_valid': True,
            'reason': 'Empty tree',
            'left_leaves': []
        }
    
    left_leaves = []
    
    def is_leaf(node):
        return node and not node.left and not node.right
    
    def sum_helper(node, is_left_child):
        if not node:
            return 0
        
        # If it's a left leaf, add to list and return its value
        if is_leaf(node) and is_left_child:
            left_leaves.append(node.val)
            return node.val
        
        # Recursively sum left and right subtrees
        return (sum_helper(node.left, True) + 
                sum_helper(node.right, False))
    
    total_sum = sum_helper(root, False)
    
    return {
        'sum': total_sum,
        'is_valid': True,
        'reason': f'Found {len(left_leaves)} left leaves with sum {total_sum}',
        'left_leaves': left_leaves
    }


def sum_of_left_leaves_with_paths(root):
    """
    Find the sum of all left leaves and return paths to them.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Sum with paths to left leaves
    """
    if not root:
        return {
            'sum': 0,
            'left_leaves': [],
            'paths': []
        }
    
    left_leaves = []
    paths = []
    
    def is_leaf(node):
        return node and not node.left and not node.right
    
    def sum_helper(node, is_left_child, path):
        if not node:
            return 0
        
        current_path = path + [node.val]
        
        # If it's a left leaf, add to lists and return its value
        if is_leaf(node) and is_left_child:
            left_leaves.append(node.val)
            paths.append(current_path)
            return node.val
        
        # Recursively sum left and right subtrees
        return (sum_helper(node.left, True, current_path) + 
                sum_helper(node.right, False, current_path))
    
    total_sum = sum_helper(root, False, [])
    
    return {
        'sum': total_sum,
        'left_leaves': left_leaves,
        'paths': paths
    }


def sum_of_left_leaves_with_levels(root):
    """
    Find the sum of all left leaves and return nodes by level.
    
    Args:
        root: Root of the binary tree
        
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


def sum_of_left_leaves_with_comparison(root):
    """
    Find the sum of all left leaves and compare with other approaches.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Comparison of different approaches
    """
    if not root:
        return {
            'recursive': 0,
            'iterative': 0
        }
    
    recursive_sum = sum_of_left_leaves(root)
    iterative_sum = sum_of_left_leaves_iterative(root)
    
    return {
        'recursive': recursive_sum,
        'iterative': iterative_sum
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
        [3, 9, 20, None, None, 15, 7],  # Expected: 24
        [1],                            # Expected: 0
        [1, 2, 3, 4, 5],               # Expected: 4
        [1, 2, 3],                     # Expected: 2
        [1, 2, 3, 4, 5, 6, 7],         # Expected: 4
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],  # Expected: 8
    ]
    
    for i, values in enumerate(test_cases, 1):
        print(f"Test case {i}: {values}")
        
        # Create tree from values
        root = create_tree_from_list(values)
        
        # Test different approaches
        result_recursive = sum_of_left_leaves(root)
        result_iterative = sum_of_left_leaves_iterative(root)
        
        print(f"Recursive: {result_recursive}")
        print(f"Iterative: {result_iterative}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            sum_of_left_leaves_verbose(root)
        
        # Test with statistics
        stats = sum_of_left_leaves_with_stats(root)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = sum_of_left_leaves_with_validation(root)
        print(f"Validation: {validation}")
        
        # Test with paths
        paths = sum_of_left_leaves_with_paths(root)
        print(f"Paths: {paths}")
        
        # Test with levels
        levels = sum_of_left_leaves_with_levels(root)
        print(f"Levels: {levels}")
        
        # Test with comparison
        comparison = sum_of_left_leaves_with_comparison(root)
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
        [1, 2],                # Two nodes
        [1, 2, 3],             # Three nodes
        [1, 2, 3, 4, 5, 6, 7], # Complete binary tree
        [1, 2, None, 3, None, 4, None],  # Skewed tree
    ]
    
    for case in edge_cases:
        root = create_tree_from_list(case)
        result = sum_of_left_leaves(root)
        print(f"Tree: {case} -> Sum of left leaves: {result}")
    
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
        sum_of_left_leaves(large_root)
    recursive_time = time.time() - start_time
    
    # Test iterative approach
    start_time = time.time()
    for _ in range(1000):
        sum_of_left_leaves_iterative(large_root)
    iterative_time = time.time() - start_time
    
    print(f"Recursive: {recursive_time:.6f} seconds")
    print(f"Iterative: {iterative_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. A left leaf is a leaf node that is the left child of another node")
    print("2. We need to identify left leaves and sum their values")
    print("3. Use recursive traversal with a flag to track if current node is left child")
    print("4. If a node is a leaf and is a left child, add its value to the sum")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_values = [3, 9, 20, None, None, 15, 7]
    root = create_tree_from_list(example_values)
    
    print(f"Tree: {example_values}")
    print("Tree structure:")
    print_tree_structure(root)
    
    print("\nLeft leaves identification:")
    print("1. Node 9: is left child of 3, is leaf -> left leaf")
    print("2. Node 15: is left child of 20, is leaf -> left leaf")
    print("3. Node 7: is right child of 20, is leaf -> not left leaf")
    print("4. Sum: 9 + 15 = 24")
    
    # Test with different tree shapes
    print("\nDifferent tree shapes:")
    
    # Skewed tree
    skewed_values = [1, 2, None, 3, None, 4, None]
    skewed_root = create_tree_from_list(skewed_values)
    skewed_result = sum_of_left_leaves(skewed_root)
    print(f"Skewed tree: {skewed_values} -> Sum: {skewed_result}")
    
    # Complete binary tree
    complete_values = [1, 2, 3, 4, 5, 6, 7]
    complete_root = create_tree_from_list(complete_values)
    complete_result = sum_of_left_leaves(complete_root)
    print(f"Complete tree: {complete_values} -> Sum: {complete_result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for case in [skewed_values, complete_values]:
        root = create_tree_from_list(case)
        stats = sum_of_left_leaves_with_stats(root)
        print(f"Tree: {case}")
        print(f"  Sum: {stats['sum']}")
        print(f"  Left leaves: {stats['left_leaves']}")
        print(f"  Total leaves: {stats['total_leaves']}")
        print(f"  Left leaf count: {stats['left_leaf_count']}")
        print()
