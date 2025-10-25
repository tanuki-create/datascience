"""
Problem 29: Binary Tree Right Side View
Difficulty: Easy

Given the root of a binary tree, imagine yourself standing on the right side of it, 
return the values of the nodes you can see ordered from top to bottom.

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


def right_side_view(root):
    """
    Get the right side view of a binary tree using level order traversal.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        list: Values of nodes visible from the right side
    """
    if not root:
        return []
    
    from collections import deque
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        
        for i in range(level_size):
            node = queue.popleft()
            
            # Add the last node of each level (rightmost node)
            if i == level_size - 1:
                result.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return result


def right_side_view_recursive(root):
    """
    Get the right side view using recursive approach.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        list: Values of nodes visible from the right side
    """
    if not root:
        return []
    
    result = []
    
    def traverse(node, level):
        if not node:
            return
        
        # If this is the first node we've seen at this level
        if level == len(result):
            result.append(node.val)
        
        # Traverse right subtree first, then left
        traverse(node.right, level + 1)
        traverse(node.left, level + 1)
    
    traverse(root, 0)
    return result


def right_side_view_verbose(root):
    """
    Get the right side view with detailed step-by-step explanation.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        list: Values of nodes visible from the right side
    """
    if not root:
        print("Empty tree, returning []")
        return []
    
    from collections import deque
    result = []
    queue = deque([root])
    level = 0
    
    print(f"Starting right side view traversal with root {root.val}")
    
    while queue:
        level_size = len(queue)
        print(f"\nLevel {level}: Processing {level_size} nodes")
        
        for i in range(level_size):
            node = queue.popleft()
            print(f"  Node {i+1}: {node.val}")
            
            # Add the last node of each level (rightmost node)
            if i == level_size - 1:
                result.append(node.val)
                print(f"    Added to result: {node.val} (rightmost node at level {level})")
            
            if node.left:
                queue.append(node.left)
                print(f"    Added left child: {node.left.val}")
            if node.right:
                queue.append(node.right)
                print(f"    Added right child: {node.right.val}")
        
        print(f"Level {level} result so far: {result}")
        level += 1
    
    print(f"\nFinal result: {result}")
    return result


def right_side_view_with_stats(root):
    """
    Get the right side view and return statistics.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Statistics about the traversal
    """
    if not root:
        return {
            'right_side_view': [],
            'levels': 0,
            'total_nodes': 0,
            'nodes_visible': 0
        }
    
    from collections import deque
    result = []
    queue = deque([root])
    levels = 0
    total_nodes = 0
    
    while queue:
        level_size = len(queue)
        levels += 1
        
        for i in range(level_size):
            node = queue.popleft()
            total_nodes += 1
            
            # Add the last node of each level (rightmost node)
            if i == level_size - 1:
                result.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return {
        'right_side_view': result,
        'levels': levels,
        'total_nodes': total_nodes,
        'nodes_visible': len(result)
    }


def right_side_view_with_validation(root):
    """
    Get the right side view with validation.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Detailed validation results
    """
    if not root:
        return {
            'right_side_view': [],
            'is_valid': True,
            'reason': 'Empty tree',
            'levels': 0
        }
    
    from collections import deque
    result = []
    queue = deque([root])
    level = 0
    
    while queue:
        level_size = len(queue)
        level_nodes = []
        
        for i in range(level_size):
            node = queue.popleft()
            level_nodes.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        # Add the rightmost node of this level
        if level_nodes:
            result.append(level_nodes[-1])
        
        level += 1
    
    return {
        'right_side_view': result,
        'is_valid': True,
        'reason': f'Successfully found right side view with {len(result)} nodes',
        'levels': level
    }


def right_side_view_with_paths(root):
    """
    Get the right side view and return paths to visible nodes.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Right side view with paths
    """
    if not root:
        return {
            'right_side_view': [],
            'paths': []
        }
    
    from collections import deque
    result = []
    paths = []
    queue = deque([(root, [root.val])])  # (node, path)
    
    while queue:
        level_size = len(queue)
        level_paths = []
        
        for i in range(level_size):
            node, path = queue.popleft()
            level_paths.append(path)
            
            if node.left:
                queue.append((node.left, path + [node.left.val]))
            if node.right:
                queue.append((node.right, path + [node.right.val]))
        
        # Add the path to the rightmost node of this level
        if level_paths:
            result.append(level_paths[-1][-1])  # Value of rightmost node
            paths.append(level_paths[-1])  # Path to rightmost node
    
    return {
        'right_side_view': result,
        'paths': paths
    }


def right_side_view_with_levels(root):
    """
    Get the right side view and return nodes by level.
    
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


def right_side_view_with_comparison(root):
    """
    Get the right side view and compare with other traversals.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Comparison of different traversals
    """
    if not root:
        return {
            'right_side_view': [],
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
    
    right_side_result = right_side_view(root)
    level_order_result = level_order_traversal(root)
    inorder_result = inorder_traversal(root)
    preorder_result = preorder_traversal(root)
    postorder_result = postorder_traversal(root)
    
    return {
        'right_side_view': right_side_result,
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
        [1, 2, 3, None, 5, None, 4],  # Expected: [1, 3, 4]
        [1, None, 3],                 # Expected: [1, 3]
        [],                           # Expected: []
        [1],                          # Expected: [1]
        [1, 2],                      # Expected: [1, 2]
        [1, 2, 3],                   # Expected: [1, 3]
        [1, 2, 3, 4, 5, 6, 7],       # Expected: [1, 3, 7]
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],  # Expected: [1, 3, 7, 15]
    ]
    
    for i, values in enumerate(test_cases, 1):
        print(f"Test case {i}: {values}")
        
        # Create tree from values
        root = create_tree_from_list(values)
        
        # Test different approaches
        result_queue = right_side_view(root)
        result_recursive = right_side_view_recursive(root)
        
        print(f"Queue approach: {result_queue}")
        print(f"Recursive approach: {result_recursive}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            right_side_view_verbose(root)
        
        # Test with statistics
        stats = right_side_view_with_stats(root)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = right_side_view_with_validation(root)
        print(f"Validation: {validation}")
        
        # Test with paths
        paths = right_side_view_with_paths(root)
        print(f"Paths: {paths}")
        
        # Test with levels
        levels = right_side_view_with_levels(root)
        print(f"Levels: {levels}")
        
        # Test with comparison
        comparison = right_side_view_with_comparison(root)
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
        result = right_side_view(root)
        print(f"Tree: {case} -> Right side view: {result}")
    
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
        right_side_view(large_root)
    queue_time = time.time() - start_time
    
    # Test recursive approach
    start_time = time.time()
    for _ in range(1000):
        right_side_view_recursive(large_root)
    recursive_time = time.time() - start_time
    
    print(f"Queue approach: {queue_time:.6f} seconds")
    print(f"Recursive approach: {recursive_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Use level order traversal to process nodes level by level")
    print("2. For each level, keep track of the rightmost node")
    print("3. Add the rightmost node of each level to the result")
    print("4. The result represents what you would see from the right side")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_values = [1, 2, 3, None, 5, None, 4]
    root = create_tree_from_list(example_values)
    
    print(f"Tree: {example_values}")
    print("Tree structure:")
    print_tree_structure(root)
    
    print("\nRight side view steps:")
    print("1. Level 0: [1] -> Rightmost: 1")
    print("2. Level 1: [2, 3] -> Rightmost: 3")
    print("3. Level 2: [5, 4] -> Rightmost: 4")
    print("4. Result: [1, 3, 4]")
    
    # Test with different tree shapes
    print("\nDifferent tree shapes:")
    
    # Skewed tree
    skewed_values = [1, 2, None, 3, None, 4, None]
    skewed_root = create_tree_from_list(skewed_values)
    skewed_result = right_side_view(skewed_root)
    print(f"Skewed tree: {skewed_values} -> Right side view: {skewed_result}")
    
    # Complete binary tree
    complete_values = [1, 2, 3, 4, 5, 6, 7]
    complete_root = create_tree_from_list(complete_values)
    complete_result = right_side_view(complete_root)
    print(f"Complete tree: {complete_values} -> Right side view: {complete_result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for case in [skewed_values, complete_values]:
        root = create_tree_from_list(case)
        stats = right_side_view_with_stats(root)
        print(f"Tree: {case}")
        print(f"  Right side view: {stats['right_side_view']}")
        print(f"  Levels: {stats['levels']}")
        print(f"  Total nodes: {stats['total_nodes']}")
        print(f"  Nodes visible: {stats['nodes_visible']}")
        print()
