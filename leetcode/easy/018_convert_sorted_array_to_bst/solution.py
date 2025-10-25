"""
Problem 18: Convert Sorted Array to Binary Search Tree
Difficulty: Easy

Given an integer array nums where the elements are sorted in ascending order, 
convert it to a height-balanced binary search tree.

Time Complexity: O(n)
Space Complexity: O(log n) - recursion stack
"""

class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"TreeNode({self.val})"


def sorted_array_to_bst(nums):
    """
    Convert sorted array to height-balanced BST.
    
    Args:
        nums: Sorted array of integers
        
    Returns:
        TreeNode: Root of the BST
    """
    if not nums:
        return None
    
    # Find the middle element
    mid = len(nums) // 2
    
    # Create root node
    root = TreeNode(nums[mid])
    
    # Recursively build left and right subtrees
    root.left = sorted_array_to_bst(nums[:mid])
    root.right = sorted_array_to_bst(nums[mid + 1:])
    
    return root


def sorted_array_to_bst_optimized(nums):
    """
    Convert sorted array to BST with optimized space usage.
    
    Args:
        nums: Sorted array of integers
        
    Returns:
        TreeNode: Root of the BST
    """
    def build_bst(left, right):
        if left > right:
            return None
        
        mid = (left + right) // 2
        root = TreeNode(nums[mid])
        root.left = build_bst(left, mid - 1)
        root.right = build_bst(mid + 1, right)
        
        return root
    
    return build_bst(0, len(nums) - 1)


def sorted_array_to_bst_verbose(nums):
    """
    Convert sorted array to BST with detailed step-by-step explanation.
    
    Args:
        nums: Sorted array of integers
        
    Returns:
        TreeNode: Root of the BST
    """
    def build_bst_verbose(left, right, depth=0):
        indent = "  " * depth
        print(f"{indent}build_bst({left}, {right})")
        
        if left > right:
            print(f"{indent}  -> None (empty range)")
            return None
        
        mid = (left + right) // 2
        print(f"{indent}  -> mid = {mid}, nums[{mid}] = {nums[mid]}")
        
        root = TreeNode(nums[mid])
        print(f"{indent}  -> Creating node with value {nums[mid]}")
        
        print(f"{indent}  -> Building left subtree: nums[{left}:{mid}]")
        root.left = build_bst_verbose(left, mid - 1, depth + 1)
        
        print(f"{indent}  -> Building right subtree: nums[{mid + 1}:{right + 1}]")
        root.right = build_bst_verbose(mid + 1, right, depth + 1)
        
        return root
    
    return build_bst_verbose(0, len(nums) - 1)


def sorted_array_to_bst_iterative(nums):
    """
    Convert sorted array to BST using iterative approach.
    
    Args:
        nums: Sorted array of integers
        
    Returns:
        TreeNode: Root of the BST
    """
    if not nums:
        return None
    
    # Stack to store ranges and their corresponding parent nodes
    stack = [(0, len(nums) - 1, None, None)]  # (left, right, parent, is_left)
    root = None
    
    while stack:
        left, right, parent, is_left = stack.pop()
        
        if left > right:
            continue
        
        mid = (left + right) // 2
        node = TreeNode(nums[mid])
        
        if parent is None:
            root = node
        elif is_left:
            parent.left = node
        else:
            parent.right = node
        
        # Add right and left subtrees to stack
        stack.append((mid + 1, right, node, False))
        stack.append((left, mid - 1, node, True))
    
    return root


def sorted_array_to_bst_with_balance_check(nums):
    """
    Convert sorted array to BST and verify it's height-balanced.
    
    Args:
        nums: Sorted array of integers
        
    Returns:
        tuple: (root, is_balanced, height)
    """
    def build_bst(left, right):
        if left > right:
            return None
        
        mid = (left + right) // 2
        root = TreeNode(nums[mid])
        root.left = build_bst(left, mid - 1)
        root.right = build_bst(mid + 1, right)
        
        return root
    
    def is_balanced(root):
        def check_balance(node):
            if not node:
                return True, 0
            
            left_balanced, left_height = check_balance(node.left)
            right_balanced, right_height = check_balance(node.right)
            
            is_balanced = left_balanced and right_balanced and abs(left_height - right_height) <= 1
            height = max(left_height, right_height) + 1
            
            return is_balanced, height
        
        return check_balance(root)
    
    root = build_bst(0, len(nums) - 1)
    is_balanced, height = is_balanced(root)
    
    return root, is_balanced, height


def sorted_array_to_bst_with_stats(nums):
    """
    Convert sorted array to BST and return statistics.
    
    Args:
        nums: Sorted array of integers
        
    Returns:
        dict: Statistics about the BST
    """
    def build_bst(left, right):
        if left > right:
            return None
        
        mid = (left + right) // 2
        root = TreeNode(nums[mid])
        root.left = build_bst(left, mid - 1)
        root.right = build_bst(mid + 1, right)
        
        return root
    
    def get_stats(root):
        if not root:
            return {
                'height': 0,
                'node_count': 0,
                'leaf_count': 0,
                'internal_count': 0
            }
        
        left_stats = get_stats(root.left)
        right_stats = get_stats(root.right)
        
        height = max(left_stats['height'], right_stats['height']) + 1
        node_count = left_stats['node_count'] + right_stats['node_count'] + 1
        leaf_count = left_stats['leaf_count'] + right_stats['leaf_count']
        internal_count = left_stats['internal_count'] + right_stats['internal_count']
        
        # If this is a leaf node
        if not root.left and not root.right:
            leaf_count += 1
        else:
            internal_count += 1
        
        return {
            'height': height,
            'node_count': node_count,
            'leaf_count': leaf_count,
            'internal_count': internal_count
        }
    
    root = build_bst(0, len(nums) - 1)
    stats = get_stats(root)
    
    return {
        'root': root,
        'stats': stats
    }


def sorted_array_to_bst_with_traversals(nums):
    """
    Convert sorted array to BST and return different traversals.
    
    Args:
        nums: Sorted array of integers
        
    Returns:
        dict: Different traversals of the BST
    """
    def build_bst(left, right):
        if left > right:
            return None
        
        mid = (left + right) // 2
        root = TreeNode(nums[mid])
        root.left = build_bst(left, mid - 1)
        root.right = build_bst(mid + 1, right)
        
        return root
    
    def inorder_traversal(root):
        if not root:
            return []
        return inorder_traversal(root.left) + [root.val] + inorder_traversal(root.right)
    
    def preorder_traversal(root):
        if not root:
            return []
        return [root.val] + preorder_traversal(root.left) + preorder_traversal(root.right)
    
    def postorder_traversal(root):
        if not root:
            return []
        return postorder_traversal(root.left) + postorder_traversal(root.right) + [root.val]
    
    def level_order_traversal(root):
        if not root:
            return []
        
        result = []
        queue = [root]
        
        while queue:
            level_size = len(queue)
            level = []
            
            for _ in range(level_size):
                node = queue.pop(0)
                level.append(node.val)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(level)
        
        return result
    
    root = build_bst(0, len(nums) - 1)
    
    return {
        'root': root,
        'inorder': inorder_traversal(root),
        'preorder': preorder_traversal(root),
        'postorder': postorder_traversal(root),
        'level_order': level_order_traversal(root)
    }


def print_tree(root, level=0, prefix="Root: "):
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
                print_tree(root.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            if root.right:
                print_tree(root.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")


# Test cases
if __name__ == "__main__":
    test_cases = [
        [-10, -3, 0, 5, 9],
        [1, 3],
        [1, 2, 3, 4, 5],
        [1],
        [1, 2],
        [1, 2, 3, 4, 5, 6, 7],
        [],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    ]
    
    for i, nums in enumerate(test_cases, 1):
        print(f"Test case {i}: {nums}")
        
        if not nums:
            print("Empty array -> None")
            continue
        
        # Test different approaches
        root1 = sorted_array_to_bst(nums)
        root2 = sorted_array_to_bst_optimized(nums)
        root3 = sorted_array_to_bst_iterative(nums)
        
        print(f"Recursive approach: {root1.val if root1 else None}")
        print(f"Optimized approach: {root2.val if root2 else None}")
        print(f"Iterative approach: {root3.val if root3 else None}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            sorted_array_to_bst_verbose(nums)
        
        # Test balance check
        root, is_balanced, height = sorted_array_to_bst_with_balance_check(nums)
        print(f"Is balanced: {is_balanced}, Height: {height}")
        
        # Test statistics
        result = sorted_array_to_bst_with_stats(nums)
        stats = result['stats']
        print(f"Stats: {stats}")
        
        # Test traversals
        traversals = sorted_array_to_bst_with_traversals(nums)
        print(f"Inorder: {traversals['inorder']}")
        print(f"Preorder: {traversals['preorder']}")
        print(f"Postorder: {traversals['postorder']}")
        print(f"Level order: {traversals['level_order']}")
        
        # Print tree structure
        print("\nTree structure:")
        print_tree(root)
        
        print("-" * 50)
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large test case
    large_nums = sorted([random.randint(1, 1000) for _ in range(1000)])
    
    # Test recursive approach
    start_time = time.time()
    for _ in range(100):
        sorted_array_to_bst(large_nums)
    recursive_time = time.time() - start_time
    
    # Test optimized approach
    start_time = time.time()
    for _ in range(100):
        sorted_array_to_bst_optimized(large_nums)
    optimized_time = time.time() - start_time
    
    # Test iterative approach
    start_time = time.time()
    for _ in range(100):
        sorted_array_to_bst_iterative(large_nums)
    iterative_time = time.time() - start_time
    
    print(f"Recursive: {recursive_time:.6f} seconds")
    print(f"Optimized: {optimized_time:.6f} seconds")
    print(f"Iterative: {iterative_time:.6f} seconds")
    
    # Edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],                    # Empty array
        [1],                   # Single element
        [1, 2],                # Two elements
        [1, 2, 3],             # Three elements
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Ten elements
    ]
    
    for case in edge_cases:
        if case:
            root = sorted_array_to_bst(case)
            print(f"Array: {case} -> Root: {root.val if root else None}")
        else:
            print("Empty array -> None")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Find the middle element of the array")
    print("2. Create a node with that element as the root")
    print("3. Recursively build the left subtree with elements before the middle")
    print("4. Recursively build the right subtree with elements after the middle")
    print("5. This ensures the tree is height-balanced")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example = [1, 2, 3, 4, 5]
    print(f"Array: {example}")
    
    def build_step_by_step(left, right, depth=0):
        indent = "  " * depth
        print(f"{indent}Range: [{left}, {right}]")
        
        if left > right:
            print(f"{indent}-> None")
            return None
        
        mid = (left + right) // 2
        print(f"{indent}-> Mid: {mid}, Value: {example[mid]}")
        
        root = TreeNode(example[mid])
        print(f"{indent}-> Creating node: {root.val}")
        
        print(f"{indent}-> Left subtree: [{left}, {mid-1}]")
        root.left = build_step_by_step(left, mid - 1, depth + 1)
        
        print(f"{indent}-> Right subtree: [{mid+1}, {right}]")
        root.right = build_step_by_step(mid + 1, right, depth + 1)
        
        return root
    
    root = build_step_by_step(0, len(example) - 1)
    print(f"\nFinal tree structure:")
    print_tree(root)
