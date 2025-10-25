"""
Problem 19: Symmetric Tree
Difficulty: Easy

Given the root of a binary tree, check whether it is a mirror of itself 
(i.e., symmetric around its center).

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


def is_symmetric(root):
    """
    Check if a binary tree is symmetric using recursive approach.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        bool: True if symmetric, False otherwise
    """
    if not root:
        return True
    
    def is_mirror(left, right):
        if not left and not right:
            return True
        if not left or not right:
            return False
        return (left.val == right.val and 
                is_mirror(left.left, right.right) and 
                is_mirror(left.right, right.left))
    
    return is_mirror(root.left, root.right)


def is_symmetric_iterative(root):
    """
    Check if a binary tree is symmetric using iterative approach.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        bool: True if symmetric, False otherwise
    """
    if not root:
        return True
    
    # Use a queue to compare nodes in pairs
    from collections import deque
    queue = deque([(root.left, root.right)])
    
    while queue:
        left, right = queue.popleft()
        
        if not left and not right:
            continue
        if not left or not right:
            return False
        if left.val != right.val:
            return False
        
        # Add pairs of nodes to compare
        queue.append((left.left, right.right))
        queue.append((left.right, right.left))
    
    return True


def is_symmetric_iterative_stack(root):
    """
    Check if a binary tree is symmetric using stack-based iterative approach.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        bool: True if symmetric, False otherwise
    """
    if not root:
        return True
    
    stack = [(root.left, root.right)]
    
    while stack:
        left, right = stack.pop()
        
        if not left and not right:
            continue
        if not left or not right:
            return False
        if left.val != right.val:
            return False
        
        # Add pairs of nodes to compare
        stack.append((left.left, right.right))
        stack.append((left.right, right.left))
    
    return True


def is_symmetric_verbose(root):
    """
    Check if a binary tree is symmetric with detailed step-by-step explanation.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        bool: True if symmetric, False otherwise
    """
    if not root:
        return True
    
    def is_mirror_verbose(left, right, depth=0):
        indent = "  " * depth
        print(f"{indent}Comparing: {left.val if left else None} vs {right.val if right else None}")
        
        if not left and not right:
            print(f"{indent}Both None -> True")
            return True
        if not left or not right:
            print(f"{indent}One is None -> False")
            return False
        
        if left.val != right.val:
            print(f"{indent}Values differ: {left.val} != {right.val} -> False")
            return False
        
        print(f"{indent}Values match: {left.val} == {right.val}")
        print(f"{indent}Checking left.left vs right.right")
        left_result = is_mirror_verbose(left.left, right.right, depth + 1)
        print(f"{indent}Checking left.right vs right.left")
        right_result = is_mirror_verbose(left.right, right.left, depth + 1)
        
        result = left_result and right_result
        print(f"{indent}Result: {result}")
        return result
    
    return is_mirror_verbose(root.left, root.right)


def is_symmetric_with_paths(root):
    """
    Check if a binary tree is symmetric by comparing paths.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        bool: True if symmetric, False otherwise
    """
    if not root:
        return True
    
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
    
    # Get paths from left subtree
    left_paths = []
    get_paths(root.left, [], left_paths)
    
    # Get paths from right subtree
    right_paths = []
    get_paths(root.right, [], right_paths)
    
    # Reverse the right paths to check symmetry
    right_paths_reversed = [path[::-1] for path in right_paths]
    
    return left_paths == right_paths_reversed


def is_symmetric_with_level_order(root):
    """
    Check if a binary tree is symmetric using level-order traversal.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        bool: True if symmetric, False otherwise
    """
    if not root:
        return True
    
    from collections import deque
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val if node else None)
            
            if node:
                queue.append(node.left)
                queue.append(node.right)
        
        # Check if the level is symmetric
        left, right = 0, len(level) - 1
        while left < right:
            if level[left] != level[right]:
                return False
            left += 1
            right -= 1
    
    return True


def is_symmetric_with_validation(root):
    """
    Check if a binary tree is symmetric with validation and statistics.
    
    Args:
        root: Root of the binary tree
        
    Returns:
        dict: Detailed information about the symmetry check
    """
    if not root:
        return {
            'is_symmetric': True,
            'reason': 'Empty tree is symmetric',
            'comparisons': 0
        }
    
    comparisons = 0
    
    def is_mirror_with_stats(left, right):
        nonlocal comparisons
        comparisons += 1
        
        if not left and not right:
            return True
        if not left or not right:
            return False
        if left.val != right.val:
            return False
        
        return (is_mirror_with_stats(left.left, right.right) and 
                is_mirror_with_stats(left.right, right.left))
    
    is_symmetric = is_mirror_with_stats(root.left, root.right)
    
    return {
        'is_symmetric': is_symmetric,
        'reason': 'Tree is symmetric' if is_symmetric else 'Tree is not symmetric',
        'comparisons': comparisons
    }


def create_symmetric_tree(values):
    """
    Create a symmetric tree from a list of values.
    
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
        [1, 2, 2, 3, 4, 4, 3],        # Symmetric
        [1, 2, 2, None, 3, None, 3],   # Not symmetric
        [1],                           # Symmetric (single node)
        [1, 2, 2],                     # Symmetric
        [1, 2, 2, 3, 3, 3, 3],        # Symmetric
        [1, 2, 2, None, 3, 3, None],   # Symmetric
        [1, 2, 2, 3, None, None, 3],   # Symmetric
        [1, 2, 2, 3, 4, 4, 3, 5, 6, 6, 5],  # Symmetric
    ]
    
    for i, values in enumerate(test_cases, 1):
        print(f"Test case {i}: {values}")
        
        # Create tree from values
        root = create_symmetric_tree(values)
        
        # Test different approaches
        result_recursive = is_symmetric(root)
        result_iterative = is_symmetric_iterative(root)
        result_stack = is_symmetric_iterative_stack(root)
        result_level = is_symmetric_with_level_order(root)
        
        print(f"Recursive: {result_recursive}")
        print(f"Iterative (queue): {result_iterative}")
        print(f"Iterative (stack): {result_stack}")
        print(f"Level order: {result_level}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            is_symmetric_verbose(root)
        
        # Test with validation
        validation = is_symmetric_with_validation(root)
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
        [1, 2, 2],             # Three nodes
        [1, 2, 2, 3, 4, 4, 3], # Seven nodes
        [1, 2, 2, None, 3, None, 3],  # Asymmetric
    ]
    
    for case in edge_cases:
        if case:
            root = create_symmetric_tree(case)
            result = is_symmetric(root)
            print(f"Tree: {case} -> Symmetric: {result}")
        else:
            print("Empty tree -> Symmetric: True")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large symmetric tree
    def create_large_symmetric_tree(depth):
        """Create a large symmetric tree for testing."""
        if depth == 0:
            return None
        
        root = TreeNode(random.randint(1, 100))
        root.left = create_large_symmetric_tree(depth - 1)
        root.right = create_large_symmetric_tree(depth - 1)
        return root
    
    large_root = create_large_symmetric_tree(10)
    
    # Test recursive approach
    start_time = time.time()
    for _ in range(1000):
        is_symmetric(large_root)
    recursive_time = time.time() - start_time
    
    # Test iterative approach
    start_time = time.time()
    for _ in range(1000):
        is_symmetric_iterative(large_root)
    iterative_time = time.time() - start_time
    
    print(f"Recursive: {recursive_time:.6f} seconds")
    print(f"Iterative: {iterative_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. A tree is symmetric if its left and right subtrees are mirror images")
    print("2. Two trees are mirror images if:")
    print("   - Both are empty, OR")
    print("   - Both have the same root value, AND")
    print("   - Left subtree of first tree is mirror of right subtree of second tree, AND")
    print("   - Right subtree of first tree is mirror of left subtree of second tree")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_values = [1, 2, 2, 3, 4, 4, 3]
    example_root = create_symmetric_tree(example_values)
    print(f"Tree: {example_values}")
    print("Tree structure:")
    print_tree_structure(example_root)
    
    print("\nChecking symmetry:")
    print("1. Compare root.left (2) with root.right (2) -> True")
    print("2. Compare root.left.left (3) with root.right.right (3) -> True")
    print("3. Compare root.left.right (4) with root.right.left (4) -> True")
    print("4. All comparisons return True -> Tree is symmetric")
    
    # Test with paths
    print("\nPath-based approach:")
    paths_result = is_symmetric_with_paths(example_root)
    print(f"Path-based result: {paths_result}")
    
    # Test level-order approach
    print("\nLevel-order approach:")
    level_result = is_symmetric_with_level_order(example_root)
    print(f"Level-order result: {level_result}")
    
    # Test asymmetric tree
    print("\nAsymmetric tree example:")
    asymmetric_values = [1, 2, 2, None, 3, None, 3]
    asymmetric_root = create_symmetric_tree(asymmetric_values)
    print(f"Tree: {asymmetric_values}")
    print("Tree structure:")
    print_tree_structure(asymmetric_root)
    
    asymmetric_result = is_symmetric(asymmetric_root)
    print(f"Is symmetric: {asymmetric_result}")
    
    # Test with validation
    print("\nValidation for asymmetric tree:")
    validation = is_symmetric_with_validation(asymmetric_root)
    print(f"Validation: {validation}")
