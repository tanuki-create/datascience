"""
Problem 22: Invert Binary Tree
Difficulty: Easy

Given the root of a binary tree, invert the tree, and return its root.

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


def invert_tree(root):
    """
    Invert a binary tree using recursive approach.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        TreeNode: Root of the inverted tree
    """
    if not root:
        return None
    
    # Invert left and right subtrees
    left_inverted = invert_tree(root.left)
    right_inverted = invert_tree(root.right)
    
    # Swap left and right children
    root.left = right_inverted
    root.right = left_inverted
    
    return root


def invert_tree_iterative(root):
    """
    Invert a binary tree using iterative approach with stack.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        TreeNode: Root of the inverted tree
    """
    if not root:
        return None
    
    stack = [root]
    
    while stack:
        node = stack.pop()
        
        # Swap left and right children
        node.left, node.right = node.right, node.left
        
        # Add children to stack
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    
    return root


def invert_tree_level_order(root):
    """
    Invert a binary tree using level-order traversal.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        TreeNode: Root of the inverted tree
    """
    if not root:
        return None
    
    from collections import deque
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        
        # Swap left and right children
        node.left, node.right = node.right, node.left
        
        # Add children to queue
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return root


def invert_tree_verbose(root):
    """
    Invert a binary tree with detailed step-by-step explanation.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        TreeNode: Root of the inverted tree
    """
    def invert_helper(node, depth=0):
        indent = "  " * depth
        if not node:
            print(f"{indent}Node is None, returning None")
            return None
        
        print(f"{indent}Inverting node {node.val}")
        print(f"{indent}Original: left={node.left.val if node.left else None}, right={node.right.val if node.right else None}")
        
        # Invert left and right subtrees
        print(f"{indent}Inverting left subtree...")
        left_inverted = invert_helper(node.left, depth + 1)
        print(f"{indent}Inverting right subtree...")
        right_inverted = invert_helper(node.right, depth + 1)
        
        # Swap left and right children
        node.left, node.right = right_inverted, left_inverted
        print(f"{indent}Swapped: left={node.left.val if node.left else None}, right={node.right.val if node.right else None}")
        
        return node
    
    if not root:
        print("Empty tree, returning None")
        return None
    
    print(f"Inverting tree with root {root.val}")
    return invert_helper(root)


def invert_tree_with_stats(root):
    """
    Invert a binary tree and return statistics.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Statistics about the inversion
    """
    if not root:
        return {
            'inverted': True,
            'nodes_processed': 0,
            'swaps_made': 0
        }
    
    nodes_processed = 0
    swaps_made = 0
    
    def invert_with_stats(node):
        nonlocal nodes_processed, swaps_made
        
        if not node:
            return None
        
        nodes_processed += 1
        
        # Invert subtrees
        left_inverted = invert_with_stats(node.left)
        right_inverted = invert_with_stats(node.right)
        
        # Swap children
        if node.left or node.right:
            swaps_made += 1
            node.left, node.right = right_inverted, left_inverted
        
        return node
    
    invert_with_stats(root)
    
    return {
        'inverted': True,
        'nodes_processed': nodes_processed,
        'swaps_made': swaps_made
    }


def invert_tree_with_comparison(original_root, inverted_root):
    """
    Compare original and inverted trees to verify correctness.
    
    Args:
        original_root: Root of the original tree
        inverted_root: Root of the inverted tree
        
    Returns:
        dict: Comparison results
    """
    def compare_trees(orig, inv):
        if not orig and not inv:
            return True
        if not orig or not inv:
            return False
        if orig.val != inv.val:
            return False
        
        # Check if left of original equals right of inverted
        # and right of original equals left of inverted
        return (compare_trees(orig.left, inv.right) and 
                compare_trees(orig.right, inv.left))
    
    def get_tree_values(node):
        if not node:
            return []
        return [node.val] + get_tree_values(node.left) + get_tree_values(node.right)
    
    is_correctly_inverted = compare_trees(original_root, inverted_root)
    original_values = get_tree_values(original_root)
    inverted_values = get_tree_values(inverted_root)
    
    return {
        'is_correctly_inverted': is_correctly_inverted,
        'original_values': original_values,
        'inverted_values': inverted_values,
        'values_match': sorted(original_values) == sorted(inverted_values)
    }


def invert_tree_multiple_times(root, times):
    """
    Invert a tree multiple times and return the result.
    
    Args:
        root: Root of the binary tree
        times: Number of times to invert
        
    Returns:
        TreeNode: Root of the tree after multiple inversions
    """
    current_root = root
    
    for i in range(times):
        current_root = invert_tree(current_root)
    
    return current_root


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


def get_tree_values_inorder(root):
    """
    Get values of the tree in inorder traversal.
    
    Args:
        root: Root of the tree
        
    Returns:
        list: Values in inorder traversal
    """
    if not root:
        return []
    
    return (get_tree_values_inorder(root.left) + 
            [root.val] + 
            get_tree_values_inorder(root.right))


# Test cases
if __name__ == "__main__":
    test_cases = [
        [4, 2, 7, 1, 3, 6, 9],  # Expected: [4, 7, 2, 9, 6, 3, 1]
        [2, 1, 3],              # Expected: [2, 3, 1]
        [],                     # Expected: []
        [1],                    # Expected: [1]
        [1, 2],                 # Expected: [1, None, 2]
        [1, 2, 3],              # Expected: [1, 3, 2]
        [1, 2, 3, 4, 5, 6, 7],  # Expected: [1, 3, 2, 7, 6, 5, 4]
    ]
    
    for i, values in enumerate(test_cases, 1):
        print(f"Test case {i}: {values}")
        
        # Create tree from values
        root = create_tree_from_list(values)
        
        # Test different approaches
        root_recursive = invert_tree(root)
        root_iterative = invert_tree_iterative(create_tree_from_list(values))
        root_level = invert_tree_level_order(create_tree_from_list(values))
        
        print(f"Recursive result: {get_tree_values_inorder(root_recursive)}")
        print(f"Iterative result: {get_tree_values_inorder(root_iterative)}")
        print(f"Level order result: {get_tree_values_inorder(root_level)}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            original_root = create_tree_from_list(values)
            invert_tree_verbose(original_root)
        
        # Test with statistics
        stats = invert_tree_with_stats(create_tree_from_list(values))
        print(f"Statistics: {stats}")
        
        # Test comparison
        original = create_tree_from_list(values)
        inverted = invert_tree(original)
        comparison = invert_tree_with_comparison(original, inverted)
        print(f"Comparison: {comparison}")
        
        # Print tree structures
        print("\nOriginal tree structure:")
        print_tree_structure(create_tree_from_list(values))
        print("\nInverted tree structure:")
        print_tree_structure(root_recursive)
        
        print("-" * 50)
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],                    # Empty tree
        [1],                   # Single node
        [1, 2],                # Two nodes
        [1, 2, 3],             # Three nodes
        [1, 2, 3, 4, 5, 6, 7], # Complete binary tree
    ]
    
    for case in edge_cases:
        root = create_tree_from_list(case)
        inverted = invert_tree(root)
        result = get_tree_values_inorder(inverted)
        print(f"Original: {case} -> Inverted: {result}")
    
    # Test multiple inversions
    print("\nMultiple inversions:")
    test_values = [1, 2, 3, 4, 5, 6, 7]
    root = create_tree_from_list(test_values)
    
    for times in range(5):
        inverted = invert_tree_multiple_times(root, times)
        result = get_tree_values_inorder(inverted)
        print(f"After {times} inversions: {result}")
    
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
        invert_tree(large_root)
    recursive_time = time.time() - start_time
    
    # Test iterative approach
    start_time = time.time()
    for _ in range(1000):
        invert_tree_iterative(large_root)
    iterative_time = time.time() - start_time
    
    # Test level-order approach
    start_time = time.time()
    for _ in range(1000):
        invert_tree_level_order(large_root)
    level_time = time.time() - start_time
    
    print(f"Recursive: {recursive_time:.6f} seconds")
    print(f"Iterative: {iterative_time:.6f} seconds")
    print(f"Level order: {level_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. For each node, swap its left and right children")
    print("2. Recursively invert the left and right subtrees")
    print("3. The result is a tree that is the mirror image of the original")
    print("4. All node values remain the same, only the structure changes")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_values = [4, 2, 7, 1, 3, 6, 9]
    root = create_tree_from_list(example_values)
    
    print(f"Original tree: {example_values}")
    print("Original tree structure:")
    print_tree_structure(root)
    
    print("\nInversion steps:")
    print("1. Start with root (4)")
    print("2. Swap left (2) and right (7) children")
    print("3. Invert left subtree (2)")
    print("4. Invert right subtree (7)")
    print("5. Continue recursively for all nodes")
    
    inverted = invert_tree(root)
    print("\nInverted tree structure:")
    print_tree_structure(inverted)
    
    # Test with different tree shapes
    print("\nDifferent tree shapes:")
    
    # Skewed tree
    skewed_values = [1, 2, None, 3, None, 4, None]
    skewed_root = create_tree_from_list(skewed_values)
    skewed_inverted = invert_tree(skewed_root)
    print(f"Skewed tree: {skewed_values}")
    print("Original:")
    print_tree_structure(create_tree_from_list(skewed_values))
    print("Inverted:")
    print_tree_structure(skewed_inverted)
    
    # Complete binary tree
    complete_values = [1, 2, 3, 4, 5, 6, 7]
    complete_root = create_tree_from_list(complete_values)
    complete_inverted = invert_tree(complete_root)
    print(f"\nComplete tree: {complete_values}")
    print("Original:")
    print_tree_structure(create_tree_from_list(complete_values))
    print("Inverted:")
    print_tree_structure(complete_inverted)
    
    # Test with statistics
    print("\nDetailed statistics:")
    for case in [skewed_values, complete_values]:
        root = create_tree_from_list(case)
        stats = invert_tree_with_stats(root)
        print(f"Tree: {case}")
        print(f"  Nodes processed: {stats['nodes_processed']}")
        print(f"  Swaps made: {stats['swaps_made']}")
        print()
