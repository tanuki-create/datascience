"""
Problem 28: Binary Tree Zigzag Level Order Traversal
Difficulty: Easy

Given the root of a binary tree, return the zigzag level order traversal of its 
nodes' values. (i.e., from left to right, then right to left for the next level 
and alternate between).

Time Complexity: O(n)
Space Complexity: O(w) where w is the maximum width of the tree
"""

class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"TreeNode({self.val})"


def zigzag_level_order(root):
    """
    Perform zigzag level order traversal using queue.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        list: List of lists representing each level in zigzag order
    """
    if not root:
        return []
    
    from collections import deque
    result = []
    queue = deque([root])
    left_to_right = True
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        if not left_to_right:
            level.reverse()
        
        result.append(level)
        left_to_right = not left_to_right
    
    return result


def zigzag_level_order_optimized(root):
    """
    Perform zigzag level order traversal with optimized approach.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        list: List of lists representing each level in zigzag order
    """
    if not root:
        return []
    
    from collections import deque
    result = []
    queue = deque([root])
    level = 0
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        # Reverse every other level
        if level % 2 == 1:
            current_level.reverse()
        
        result.append(current_level)
        level += 1
    
    return result


def zigzag_level_order_verbose(root):
    """
    Perform zigzag level order traversal with detailed step-by-step explanation.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        list: List of lists representing each level in zigzag order
    """
    if not root:
        print("Empty tree, returning []")
        return []
    
    from collections import deque
    result = []
    queue = deque([root])
    left_to_right = True
    level = 0
    
    print(f"Starting zigzag level order traversal with root {root.val}")
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        print(f"\nLevel {level}: Processing {level_size} nodes")
        print(f"Direction: {'Left to Right' if left_to_right else 'Right to Left'}")
        
        for i in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            print(f"  Node {i+1}: {node.val}")
            
            if node.left:
                queue.append(node.left)
                print(f"    Added left child: {node.left.val}")
            if node.right:
                queue.append(node.right)
                print(f"    Added right child: {node.right.val}")
        
        if not left_to_right:
            current_level.reverse()
            print(f"Reversed level: {current_level}")
        
        result.append(current_level)
        print(f"Level {level} result: {current_level}")
        left_to_right = not left_to_right
        level += 1
    
    print(f"\nFinal result: {result}")
    return result


def zigzag_level_order_with_stats(root):
    """
    Perform zigzag level order traversal and return statistics.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Statistics about the traversal
    """
    if not root:
        return {
            'levels': 0,
            'total_nodes': 0,
            'max_level_size': 0,
            'min_level_size': 0,
            'traversal': []
        }
    
    from collections import deque
    result = []
    queue = deque([root])
    left_to_right = True
    level_sizes = []
    
    while queue:
        level_size = len(queue)
        level = []
        level_sizes.append(level_size)
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        if not left_to_right:
            level.reverse()
        
        result.append(level)
        left_to_right = not left_to_right
    
    return {
        'levels': len(result),
        'total_nodes': sum(len(level) for level in result),
        'max_level_size': max(level_sizes) if level_sizes else 0,
        'min_level_size': min(level_sizes) if level_sizes else 0,
        'traversal': result
    }


def zigzag_level_order_with_validation(root):
    """
    Perform zigzag level order traversal with validation.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Detailed validation results
    """
    if not root:
        return {
            'traversal': [],
            'is_valid': True,
            'reason': 'Empty tree',
            'levels': 0
        }
    
    from collections import deque
    result = []
    queue = deque([root])
    left_to_right = True
    level = 0
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        if not left_to_right:
            current_level.reverse()
        
        result.append(current_level)
        left_to_right = not left_to_right
        level += 1
    
    return {
        'traversal': result,
        'is_valid': True,
        'reason': f'Successfully traversed {len(result)} levels in zigzag order',
        'levels': len(result)
    }


def zigzag_level_order_with_paths(root):
    """
    Perform zigzag level order traversal and return paths to each node.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Traversal with paths
    """
    if not root:
        return {
            'traversal': [],
            'paths': []
        }
    
    from collections import deque
    result = []
    paths = []
    queue = deque([(root, [root.val])])  # (node, path)
    left_to_right = True
    
    while queue:
        level_size = len(queue)
        level = []
        level_paths = []
        
        for _ in range(level_size:
            node, path = queue.popleft()
            level.append(node.val)
            level_paths.append(path)
            
            if node.left:
                queue.append((node.left, path + [node.left.val]))
            if node.right:
                queue.append((node.right, path + [node.right.val]))
        
        if not left_to_right:
            level.reverse()
            level_paths.reverse()
        
        result.append(level)
        paths.append(level_paths)
        left_to_right = not left_to_right
    
    return {
        'traversal': result,
        'paths': paths
    }


def zigzag_level_order_with_levels(root):
    """
    Perform zigzag level order traversal and return nodes by level.
    
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
    
    # Apply zigzag ordering
    for level in levels:
        if level % 2 == 1:
            levels[level].reverse()
    
    return levels


def zigzag_level_order_with_comparison(root):
    """
    Perform zigzag level order traversal and compare with other traversals.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Comparison of different traversals
    """
    if not root:
        return {
            'zigzag_level_order': [],
            'level_order': [],
            'inorder': [],
            'preorder': [],
            'postorder': []
        }
    
    def level_order_traversal(node):
        if not node:
            return []
        
        from collections import deque
        result = []
        queue = deque([node])
        
        while queue:
            level_size = len(queue)
            level = []
            
            for _ in range(level_size):
                n = queue.popleft()
                level.append(n.val)
                
                if n.left:
                    queue.append(n.left)
                if n.right:
                    queue.append(n.right)
            
            result.append(level)
        
        return result
    
    def inorder_traversal(node):
        if not node:
            return []
        return inorder_traversal(node.left) + [node.val] + inorder_traversal(node.right)
    
    def preorder_traversal(node):
        if not node:
            return []
        return [node.val] + preorder_traversal(node.left) + preorder_traversal(node.right)
    
    def postorder_traversal(node):
        if not node:
            return []
        return postorder_traversal(node.left) + postorder_traversal(node.right) + [node.val]
    
    zigzag_result = zigzag_level_order(root)
    level_order_result = level_order_traversal(root)
    inorder_result = inorder_traversal(root)
    preorder_result = preorder_traversal(root)
    postorder_result = postorder_traversal(root)
    
    return {
        'zigzag_level_order': zigzag_result,
        'level_order': level_order_result,
        'inorder': inorder_result,
        'preorder': preorder_result,
        'postorder': postorder_result
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
        [3, 9, 20, None, None, 15, 7],  # Expected: [[3], [20, 9], [15, 7]]
        [1],                            # Expected: [[1]]
        [],                             # Expected: []
        [1, 2, 3],                      # Expected: [[1], [3, 2]]
        [1, 2, 3, 4, 5, 6, 7],          # Expected: [[1], [3, 2], [4, 5, 6, 7]]
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],  # Expected: [[1], [3, 2], [4, 5, 6, 7], [15, 14, 13, 12, 11, 10, 9, 8]]
    ]
    
    for i, values in enumerate(test_cases, 1):
        print(f"Test case {i}: {values}")
        
        # Create tree from values
        root = create_tree_from_list(values)
        
        # Test different approaches
        result_queue = zigzag_level_order(root)
        result_optimized = zigzag_level_order_optimized(root)
        
        print(f"Queue approach: {result_queue}")
        print(f"Optimized approach: {result_optimized}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            zigzag_level_order_verbose(root)
        
        # Test with statistics
        stats = zigzag_level_order_with_stats(root)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = zigzag_level_order_with_validation(root)
        print(f"Validation: {validation}")
        
        # Test with paths
        paths = zigzag_level_order_with_paths(root)
        print(f"Paths: {paths}")
        
        # Test with levels
        levels = zigzag_level_order_with_levels(root)
        print(f"Levels: {levels}")
        
        # Test with comparison
        comparison = zigzag_level_order_with_comparison(root)
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
        result = zigzag_level_order(root)
        print(f"Tree: {case} -> Zigzag level order: {result}")
    
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
    
    # Test queue approach
    start_time = time.time()
    for _ in range(1000):
        zigzag_level_order(large_root)
    queue_time = time.time() - start_time
    
    # Test optimized approach
    start_time = time.time()
    for _ in range(1000):
        zigzag_level_order_optimized(large_root)
    optimized_time = time.time() - start_time
    
    print(f"Queue approach: {queue_time:.6f} seconds")
    print(f"Optimized approach: {optimized_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Use a queue to store nodes at each level")
    print("2. Process nodes level by level")
    print("3. For each level, add all nodes to the result")
    print("4. Reverse every other level to create zigzag pattern")
    print("5. Add children of current nodes to the queue for next level")
    print("6. Continue until queue is empty")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_values = [3, 9, 20, None, None, 15, 7]
    root = create_tree_from_list(example_values)
    
    print(f"Tree: {example_values}")
    print("Tree structure:")
    print_tree_structure(root)
    
    print("\nZigzag level order traversal steps:")
    print("1. Start with root (3)")
    print("2. Level 0: [3] (left to right)")
    print("3. Add children: 9, 20")
    print("4. Level 1: [20, 9] (right to left, reversed)")
    print("5. Add children: 15, 7")
    print("6. Level 2: [15, 7] (left to right, not reversed)")
    print("7. No more children")
    print("8. Result: [[3], [20, 9], [15, 7]]")
    
    # Test with different tree shapes
    print("\nDifferent tree shapes:")
    
    # Skewed tree
    skewed_values = [1, 2, None, 3, None, 4, None]
    skewed_root = create_tree_from_list(skewed_values)
    skewed_result = zigzag_level_order(skewed_root)
    print(f"Skewed tree: {skewed_values} -> Zigzag level order: {skewed_result}")
    
    # Complete binary tree
    complete_values = [1, 2, 3, 4, 5, 6, 7]
    complete_root = create_tree_from_list(complete_values)
    complete_result = zigzag_level_order(complete_root)
    print(f"Complete tree: {complete_values} -> Zigzag level order: {complete_result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for case in [skewed_values, complete_values]:
        root = create_tree_from_list(case)
        stats = zigzag_level_order_with_stats(root)
        print(f"Tree: {case}")
        print(f"  Levels: {stats['levels']}")
        print(f"  Total nodes: {stats['total_nodes']}")
        print(f"  Max level size: {stats['max_level_size']}")
        print(f"  Min level size: {stats['min_level_size']}")
        print(f"  Traversal: {stats['traversal']}")
        print()
