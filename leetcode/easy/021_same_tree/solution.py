"""
Problem 21: Same Tree
Difficulty: Easy

Given the roots of two binary trees p and q, write a function to check if they 
are the same or not.

Time Complexity: O(min(m, n)) where m and n are the number of nodes in the trees
Space Complexity: O(min(m, n)) for the recursion stack
"""

class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"TreeNode({self.val})"


def is_same_tree(p, q):
    """
    Check if two binary trees are the same using recursive approach.
    
    Args:
        p: Root of the first binary tree
        q: Root of the second binary tree
        
    Returns:
        bool: True if trees are the same, False otherwise
    """
    # Both trees are empty
    if not p and not q:
        return True
    
    # One tree is empty, the other is not
    if not p or not q:
        return False
    
    # Values are different
    if p.val != q.val:
        return False
    
    # Recursively check left and right subtrees
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)


def is_same_tree_iterative(p, q):
    """
    Check if two binary trees are the same using iterative approach.
    
    Args:
        p: Root of the first binary tree
        q: Root of the second binary tree
        
    Returns:
        bool: True if trees are the same, False otherwise
    """
    # Both trees are empty
    if not p and not q:
        return True
    
    # One tree is empty, the other is not
    if not p or not q:
        return False
    
    # Use stack to compare nodes
    stack = [(p, q)]
    
    while stack:
        node_p, node_q = stack.pop()
        
        # Both nodes are None
        if not node_p and not node_q:
            continue
        
        # One node is None, the other is not
        if not node_p or not node_q:
            return False
        
        # Values are different
        if node_p.val != node_q.val:
            return False
        
        # Add children to stack
        stack.append((node_p.left, node_q.left))
        stack.append((node_p.right, node_q.right))
    
    return True


def is_same_tree_verbose(p, q):
    """
    Check if two binary trees are the same with detailed step-by-step explanation.
    
    Args:
        p: Root of the first binary tree
        q: Root of the second binary tree
        
    Returns:
        bool: True if trees are the same, False otherwise
    """
    def compare_nodes(node_p, node_q, depth=0):
        indent = "  " * depth
        print(f"{indent}Comparing nodes: {node_p.val if node_p else None} vs {node_q.val if node_q else None}")
        
        # Both nodes are None
        if not node_p and not node_q:
            print(f"{indent}Both nodes are None -> True")
            return True
        
        # One node is None, the other is not
        if not node_p or not node_q:
            print(f"{indent}One node is None -> False")
            return False
        
        # Values are different
        if node_p.val != node_q.val:
            print(f"{indent}Values differ: {node_p.val} != {node_q.val} -> False")
            return False
        
        print(f"{indent}Values match: {node_p.val} == {node_q.val}")
        print(f"{indent}Checking left subtrees...")
        left_same = compare_nodes(node_p.left, node_q.left, depth + 1)
        print(f"{indent}Checking right subtrees...")
        right_same = compare_nodes(node_p.right, node_q.right, depth + 1)
        
        result = left_same and right_same
        print(f"{indent}Result: {result}")
        return result
    
    if not p and not q:
        print("Both trees are empty -> True")
        return True
    
    if not p or not q:
        print("One tree is empty, the other is not -> False")
        return False
    
    print(f"Comparing trees with roots: {p.val} vs {q.val}")
    return compare_nodes(p, q)


def is_same_tree_with_stats(p, q):
    """
    Check if two binary trees are the same and return statistics.
    
    Args:
        p: Root of the first binary tree
        q: Root of the second binary tree
        
    Returns:
        dict: Statistics about the comparison
    """
    comparisons = 0
    nodes_checked = 0
    
    def compare_with_stats(node_p, node_q):
        nonlocal comparisons, nodes_checked
        comparisons += 1
        nodes_checked += 1
        
        if not node_p and not node_q:
            return True
        
        if not node_p or not node_q:
            return False
        
        if node_p.val != node_q.val:
            return False
        
        return (compare_with_stats(node_p.left, node_q.left) and 
                compare_with_stats(node_p.right, node_q.right))
    
    is_same = compare_with_stats(p, q)
    
    return {
        'is_same': is_same,
        'comparisons': comparisons,
        'nodes_checked': nodes_checked
    }


def is_same_tree_with_paths(p, q):
    """
    Check if two binary trees are the same by comparing their paths.
    
    Args:
        p: Root of the first binary tree
        q: Root of the second binary tree
        
    Returns:
        bool: True if trees are the same, False otherwise
    """
    def get_paths(node, path, paths):
        if not node:
            paths.append(path + [None])
            return
        
        path.append(node.val)
        
        if not node.left and not node.right:
            paths.append(path.copy())
        else:
            get_paths(node.left, path, paths)
            get_paths(node.right, path, paths)
        
        path.pop()
    
    # Get paths from both trees
    paths_p = []
    get_paths(p, [], paths_p)
    
    paths_q = []
    get_paths(q, [], paths_q)
    
    return paths_p == paths_q


def is_same_tree_with_serialization(p, q):
    """
    Check if two binary trees are the same by serializing them.
    
    Args:
        p: Root of the first binary tree
        q: Root of the second binary tree
        
    Returns:
        bool: True if trees are the same, False otherwise
    """
    def serialize(node):
        if not node:
            return "null"
        return f"{node.val},{serialize(node.left)},{serialize(node.right)}"
    
    return serialize(p) == serialize(q)


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
        ([1, 2, 3], [1, 2, 3]),           # Same trees
        ([1, 2], [1, None, 2]),            # Different structures
        ([1, 2, 1], [1, 1, 2]),           # Different values
        ([1], [1]),                       # Single nodes
        ([], []),                         # Empty trees
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),  # Larger same trees
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 6]),  # Different values
    ]
    
    for i, (values_p, values_q) in enumerate(test_cases, 1):
        print(f"Test case {i}:")
        print(f"Tree p: {values_p}")
        print(f"Tree q: {values_q}")
        
        # Create trees from values
        p = create_tree_from_list(values_p)
        q = create_tree_from_list(values_q)
        
        # Test different approaches
        result_recursive = is_same_tree(p, q)
        result_iterative = is_same_tree_iterative(p, q)
        result_paths = is_same_tree_with_paths(p, q)
        result_serialization = is_same_tree_with_serialization(p, q)
        
        print(f"Recursive: {result_recursive}")
        print(f"Iterative: {result_iterative}")
        print(f"Paths: {result_paths}")
        print(f"Serialization: {result_serialization}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            is_same_tree_verbose(p, q)
        
        # Test with statistics
        stats = is_same_tree_with_stats(p, q)
        print(f"Statistics: {stats}")
        
        # Print tree structures
        print("\nTree p structure:")
        print_tree_structure(p)
        print("\nTree q structure:")
        print_tree_structure(q)
        
        print("-" * 50)
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        ([], []),                         # Both empty
        ([1], []),                        # One empty
        ([], [1]),                        # One empty
        ([1], [1]),                       # Single nodes
        ([1, 2], [1, 2]),                 # Two nodes
        ([1, 2, 3], [1, 2, 3]),           # Three nodes
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),  # Five nodes
    ]
    
    for case_p, case_q in edge_cases:
        p = create_tree_from_list(case_p)
        q = create_tree_from_list(case_q)
        result = is_same_tree(p, q)
        print(f"p: {case_p}, q: {case_q} -> Same: {result}")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large trees
    def create_large_tree(depth):
        """Create a large tree for testing."""
        if depth == 0:
            return None
        
        root = TreeNode(random.randint(1, 100))
        root.left = create_large_tree(depth - 1)
        root.right = create_large_tree(depth - 1)
        return root
    
    large_p = create_large_tree(10)
    large_q = create_large_tree(10)
    
    # Test recursive approach
    start_time = time.time()
    for _ in range(1000):
        is_same_tree(large_p, large_q)
    recursive_time = time.time() - start_time
    
    # Test iterative approach
    start_time = time.time()
    for _ in range(1000):
        is_same_tree_iterative(large_p, large_q)
    iterative_time = time.time() - start_time
    
    print(f"Recursive: {recursive_time:.6f} seconds")
    print(f"Iterative: {iterative_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Two trees are the same if:")
    print("   - Both are empty, OR")
    print("   - Both have the same root value, AND")
    print("   - Left subtrees are the same, AND")
    print("   - Right subtrees are the same")
    print("2. Recursively check each node and its children")
    print("3. Return True only if all conditions are met")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_p = [1, 2, 3]
    example_q = [1, 2, 3]
    p = create_tree_from_list(example_p)
    q = create_tree_from_list(example_q)
    
    print(f"Tree p: {example_p}")
    print(f"Tree q: {example_q}")
    print("Tree structures:")
    print("Tree p:")
    print_tree_structure(p)
    print("Tree q:")
    print_tree_structure(q)
    
    print("\nComparison steps:")
    print("1. Compare roots: 1 == 1 -> True")
    print("2. Compare left subtrees: 2 == 2 -> True")
    print("3. Compare right subtrees: 3 == 3 -> True")
    print("4. All comparisons return True -> Trees are the same")
    
    # Test with different tree shapes
    print("\nDifferent tree shapes:")
    
    # Skewed trees
    skewed_p = [1, 2, None, 3, None, 4, None]
    skewed_q = [1, 2, None, 3, None, 4, None]
    p_skewed = create_tree_from_list(skewed_p)
    q_skewed = create_tree_from_list(skewed_q)
    result_skewed = is_same_tree(p_skewed, q_skewed)
    print(f"Skewed trees: {skewed_p} vs {skewed_q} -> Same: {result_skewed}")
    
    # Complete binary trees
    complete_p = [1, 2, 3, 4, 5, 6, 7]
    complete_q = [1, 2, 3, 4, 5, 6, 7]
    p_complete = create_tree_from_list(complete_p)
    q_complete = create_tree_from_list(complete_q)
    result_complete = is_same_tree(p_complete, q_complete)
    print(f"Complete trees: {complete_p} vs {complete_q} -> Same: {result_complete}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for case_p, case_q in [(skewed_p, skewed_q), (complete_p, complete_q)]:
        p = create_tree_from_list(case_p)
        q = create_tree_from_list(case_q)
        stats = is_same_tree_with_stats(p, q)
        print(f"Trees: {case_p} vs {case_q}")
        print(f"  Same: {stats['is_same']}")
        print(f"  Comparisons: {stats['comparisons']}")
        print(f"  Nodes checked: {stats['nodes_checked']}")
        print()
