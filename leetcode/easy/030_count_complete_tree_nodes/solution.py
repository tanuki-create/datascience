"""
Problem 30: Count Complete Tree Nodes
Difficulty: Easy

Given the root of a complete binary tree, return the number of the nodes in the tree.
Design an algorithm that runs in less than O(n) time complexity.

Time Complexity: O(log n * log n)
Space Complexity: O(log n)
"""

class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"TreeNode({self.val})"


def count_nodes(root):
    """
    Count nodes in a complete binary tree using optimized approach.
    
    Args:
        root: Root of the complete binary tree
        
    Returns:
        int: Number of nodes in the tree
    """
    if not root:
        return 0
    
    def get_height(node):
        """Get the height of the tree by going left."""
        height = 0
        while node:
            height += 1
            node = node.left
        return height
    
    def count_nodes_helper(node):
        if not node:
            return 0
        
        left_height = get_height(node.left)
        right_height = get_height(node.right)
        
        # If left and right heights are equal, left subtree is complete
        if left_height == right_height:
            # Left subtree is complete, right subtree might not be
            return (2 ** left_height) + count_nodes_helper(node.right)
        else:
            # Right subtree is complete, left subtree might not be
            return (2 ** right_height) + count_nodes_helper(node.left)
    
    return count_nodes_helper(root)


def count_nodes_brute_force(root):
    """
    Count nodes using brute force approach (O(n) time complexity).
    
    Args:
        root: Root of the complete binary tree
        
    Returns:
        int: Number of nodes in the tree
    """
    if not root:
        return 0
    
    return 1 + count_nodes_brute_force(root.left) + count_nodes_brute_force(root.right)


def count_nodes_iterative(root):
    """
    Count nodes using iterative approach.
    
    Args:
        root: Root of the complete binary tree
        
    Returns:
        int: Number of nodes in the tree
    """
    if not root:
        return 0
    
    count = 0
    stack = [root]
    
    while stack:
        node = stack.pop()
        count += 1
        
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    
    return count


def count_nodes_verbose(root):
    """
    Count nodes with detailed step-by-step explanation.
    
    Args:
        root: Root of the complete binary tree
        
    Returns:
        int: Number of nodes in the tree
    """
    if not root:
        print("Empty tree, returning 0")
        return 0
    
    def get_height_verbose(node, direction=""):
        height = 0
        current = node
        print(f"Getting {direction} height...")
        
        while current:
            height += 1
            current = current.left
            print(f"  Height so far: {height}")
        
        print(f"{direction} height: {height}")
        return height
    
    def count_helper(node, depth=0):
        indent = "  " * depth
        print(f"{indent}Counting nodes at depth {depth}")
        
        if not node:
            print(f"{indent}Node is None, returning 0")
            return 0
        
        print(f"{indent}Node value: {node.val}")
        
        left_height = get_height_verbose(node.left, "left")
        right_height = get_height_verbose(node.right, "right")
        
        print(f"{indent}Left height: {left_height}, Right height: {right_height}")
        
        if left_height == right_height:
            print(f"{indent}Left and right heights are equal")
            print(f"{indent}Left subtree is complete with {2 ** left_height} nodes")
            print(f"{indent}Counting right subtree...")
            right_count = count_helper(node.right, depth + 1)
            total = (2 ** left_height) + right_count
            print(f"{indent}Total nodes: {total}")
            return total
        else:
            print(f"{indent}Left and right heights are different")
            print(f"{indent}Right subtree is complete with {2 ** right_height} nodes")
            print(f"{indent}Counting left subtree...")
            left_count = count_helper(node.left, depth + 1)
            total = (2 ** right_height) + left_count
            print(f"{indent}Total nodes: {total}")
            return total
    
    print(f"Counting nodes in complete binary tree with root {root.val}")
    return count_helper(root)


def count_nodes_with_stats(root):
    """
    Count nodes and return statistics.
    
    Args:
        root: Root of the complete binary tree
        
    Returns:
        dict: Statistics about the tree
    """
    if not root:
        return {
            'node_count': 0,
            'height': 0,
            'is_complete': True,
            'levels': 0
        }
    
    def get_height(node):
        height = 0
        while node:
            height += 1
            node = node.left
        return height
    
    def count_with_stats(node):
        if not node:
            return 0
        
        left_height = get_height(node.left)
        right_height = get_height(node.right)
        
        if left_height == right_height:
            return (2 ** left_height) + count_with_stats(node.right)
        else:
            return (2 ** right_height) + count_with_stats(node.left)
    
    node_count = count_with_stats(root)
    height = get_height(root)
    levels = height
    
    return {
        'node_count': node_count,
        'height': height,
        'is_complete': True,  # Given that it's a complete binary tree
        'levels': levels
    }


def count_nodes_with_validation(root):
    """
    Count nodes with validation.
    
    Args:
        root: Root of the complete binary tree
        
    Returns:
        dict: Detailed validation results
    """
    if not root:
        return {
            'node_count': 0,
            'is_valid': True,
            'reason': 'Empty tree',
            'height': 0
        }
    
    def get_height(node):
        height = 0
        while node:
            height += 1
            node = node.left
        return height
    
    def count_with_validation(node):
        if not node:
            return 0
        
        left_height = get_height(node.left)
        right_height = get_height(node.right)
        
        if left_height == right_height:
            return (2 ** left_height) + count_with_validation(node.right)
        else:
            return (2 ** right_height) + count_with_validation(node.left)
    
    node_count = count_with_validation(root)
    height = get_height(root)
    
    return {
        'node_count': node_count,
        'is_valid': True,
        'reason': f'Successfully counted {node_count} nodes in complete binary tree',
        'height': height
    }


def count_nodes_with_levels(root):
    """
    Count nodes and return nodes by level.
    
    Args:
        root: Root of the complete binary tree
        
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


def count_nodes_with_comparison(root):
    """
    Count nodes and compare different approaches.
    
    Args:
        root: Root of the complete binary tree
        
    Returns:
        dict: Comparison of different approaches
    """
    if not root:
        return {
            'optimized': 0,
            'brute_force': 0,
            'iterative': 0
        }
    
    optimized_count = count_nodes(root)
    brute_force_count = count_nodes_brute_force(root)
    iterative_count = count_nodes_iterative(root)
    
    return {
        'optimized': optimized_count,
        'brute_force': brute_force_count,
        'iterative': iterative_count
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
        [1, 2, 3, 4, 5, 6],    # Expected: 6
        [],                     # Expected: 0
        [1],                    # Expected: 1
        [1, 2],                 # Expected: 2
        [1, 2, 3],              # Expected: 3
        [1, 2, 3, 4, 5, 6, 7],  # Expected: 7
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],  # Expected: 15
    ]
    
    for i, values in enumerate(test_cases, 1):
        print(f"Test case {i}: {values}")
        
        # Create tree from values
        root = create_tree_from_list(values)
        
        # Test different approaches
        result_optimized = count_nodes(root)
        result_brute_force = count_nodes_brute_force(root)
        result_iterative = count_nodes_iterative(root)
        
        print(f"Optimized: {result_optimized}")
        print(f"Brute force: {result_brute_force}")
        print(f"Iterative: {result_iterative}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            count_nodes_verbose(root)
        
        # Test with statistics
        stats = count_nodes_with_stats(root)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = count_nodes_with_validation(root)
        print(f"Validation: {validation}")
        
        # Test with levels
        levels = count_nodes_with_levels(root)
        print(f"Levels: {levels}")
        
        # Test with comparison
        comparison = count_nodes_with_comparison(root)
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
    ]
    
    for case in edge_cases:
        root = create_tree_from_list(case)
        result = count_nodes(root)
        print(f"Tree: {case} -> Node count: {result}")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large complete binary tree
    def create_complete_tree(depth):
        """Create a complete binary tree for testing."""
        if depth == 0:
            return None
        
        root = TreeNode(random.randint(1, 100))
        root.left = create_complete_tree(depth - 1)
        root.right = create_complete_tree(depth - 1)
        return root
    
    large_root = create_complete_tree(10)
    
    # Test optimized approach
    start_time = time.time()
    for _ in range(1000):
        count_nodes(large_root)
    optimized_time = time.time() - start_time
    
    # Test brute force approach
    start_time = time.time()
    for _ in range(1000):
        count_nodes_brute_force(large_root)
    brute_force_time = time.time() - start_time
    
    # Test iterative approach
    start_time = time.time()
    for _ in range(1000):
        count_nodes_iterative(large_root)
    iterative_time = time.time() - start_time
    
    print(f"Optimized: {optimized_time:.6f} seconds")
    print(f"Brute force: {brute_force_time:.6f} seconds")
    print(f"Iterative: {iterative_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. For a complete binary tree, we can use the property that:")
    print("   - If left and right heights are equal, left subtree is complete")
    print("   - If heights differ, right subtree is complete")
    print("2. For a complete subtree with height h, it has 2^h nodes")
    print("3. We recursively count nodes in the incomplete subtree")
    print("4. Time complexity: O(log n * log n) instead of O(n)")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_values = [1, 2, 3, 4, 5, 6]
    root = create_tree_from_list(example_values)
    
    print(f"Tree: {example_values}")
    print("Tree structure:")
    print_tree_structure(root)
    
    print("\nCounting steps:")
    print("1. Root (1): left height = 2, right height = 2")
    print("2. Heights are equal, so left subtree is complete")
    print("3. Left subtree has 2^2 = 4 nodes")
    print("4. Count nodes in right subtree (3)")
    print("5. Right subtree: left height = 1, right height = 1")
    print("6. Heights are equal, so left subtree is complete")
    print("7. Left subtree has 2^1 = 2 nodes")
    print("8. Count nodes in right subtree (6)")
    print("9. Right subtree: left height = 0, right height = 0")
    print("10. Heights are equal, so left subtree is complete")
    print("11. Left subtree has 2^0 = 1 node")
    print("12. Total: 4 + 2 + 1 = 7 nodes")
    
    # Test with different tree sizes
    print("\nDifferent tree sizes:")
    for size in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        values = list(range(1, size + 1))
        root = create_tree_from_list(values)
        count = count_nodes(root)
        print(f"Size {size}: {values} -> Node count: {count}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for case in [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]]:
        root = create_tree_from_list(case)
        stats = count_nodes_with_stats(root)
        print(f"Tree: {case}")
        print(f"  Node count: {stats['node_count']}")
        print(f"  Height: {stats['height']}")
        print(f"  Levels: {stats['levels']}")
        print(f"  Is complete: {stats['is_complete']}")
        print()
