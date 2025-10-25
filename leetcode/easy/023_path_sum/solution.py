"""
Problem 23: Path Sum
Difficulty: Easy

Given the root of a binary tree and an integer targetSum, return true if the tree 
has a root-to-leaf path such that adding up all the values along the path equals targetSum.

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


def has_path_sum(root, target_sum):
    """
    Check if there exists a root-to-leaf path with the given sum.
    
    Args:
        root: Root of the binary tree
        target_sum: Target sum to find
        
    Returns:
        bool: True if path exists, False otherwise
    """
    if not root:
        return False
    
    # If it's a leaf node, check if the value equals target sum
    if not root.left and not root.right:
        return root.val == target_sum
    
    # Recursively check left and right subtrees
    remaining_sum = target_sum - root.val
    return (has_path_sum(root.left, remaining_sum) or 
            has_path_sum(root.right, remaining_sum))


def has_path_sum_iterative(root, target_sum):
    """
    Check if there exists a root-to-leaf path with the given sum using iterative approach.
    
    Args:
        root: Root of the binary tree
        target_sum: Target sum to find
        
    Returns:
        bool: True if path exists, False otherwise
    """
    if not root:
        return False
    
    # Stack to store (node, remaining_sum)
    stack = [(root, target_sum)]
    
    while stack:
        node, remaining_sum = stack.pop()
        
        # If it's a leaf node, check if the value equals remaining sum
        if not node.left and not node.right:
            if node.val == remaining_sum:
                return True
        else:
            # Add children to stack with updated remaining sum
            if node.left:
                stack.append((node.left, remaining_sum - node.val))
            if node.right:
                stack.append((node.right, remaining_sum - node.val))
    
    return False


def has_path_sum_verbose(root, target_sum):
    """
    Check if there exists a root-to-leaf path with detailed step-by-step explanation.
    
    Args:
        root: Root of the binary tree
        target_sum: Target sum to find
        
    Returns:
        bool: True if path exists, False otherwise
    """
    def check_path(node, remaining_sum, path, depth=0):
        indent = "  " * depth
        print(f"{indent}Checking node {node.val if node else None} with remaining sum {remaining_sum}")
        
        if not node:
            print(f"{indent}Node is None -> False")
            return False
        
        current_path = path + [node.val]
        print(f"{indent}Current path: {current_path}")
        
        # If it's a leaf node, check if the value equals remaining sum
        if not node.left and not node.right:
            if node.val == remaining_sum:
                print(f"{indent}Leaf node {node.val} equals remaining sum {remaining_sum} -> True")
                print(f"{indent}Found path: {current_path}")
                return True
            else:
                print(f"{indent}Leaf node {node.val} does not equal remaining sum {remaining_sum} -> False")
                return False
        
        # Recursively check left and right subtrees
        new_remaining_sum = remaining_sum - node.val
        print(f"{indent}New remaining sum: {new_remaining_sum}")
        
        print(f"{indent}Checking left subtree...")
        left_result = check_path(node.left, new_remaining_sum, current_path, depth + 1)
        print(f"{indent}Checking right subtree...")
        right_result = check_path(node.right, new_remaining_sum, current_path, depth + 1)
        
        result = left_result or right_result
        print(f"{indent}Result: {result}")
        return result
    
    if not root:
        print("Empty tree -> False")
        return False
    
    print(f"Checking if tree has path with sum {target_sum}")
    return check_path(root, target_sum, [])


def has_path_sum_with_paths(root, target_sum):
    """
    Check if there exists a root-to-leaf path and return all such paths.
    
    Args:
        root: Root of the binary tree
        target_sum: Target sum to find
        
    Returns:
        tuple: (has_path, list_of_paths)
    """
    if not root:
        return False, []
    
    def find_paths(node, remaining_sum, path, all_paths):
        if not node:
            return
        
        current_path = path + [node.val]
        
        # If it's a leaf node, check if the value equals remaining sum
        if not node.left and not node.right:
            if node.val == remaining_sum:
                all_paths.append(current_path)
        else:
            # Recursively check left and right subtrees
            new_remaining_sum = remaining_sum - node.val
            find_paths(node.left, new_remaining_sum, current_path, all_paths)
            find_paths(node.right, new_remaining_sum, current_path, all_paths)
    
    all_paths = []
    find_paths(root, target_sum, [], all_paths)
    
    return len(all_paths) > 0, all_paths


def has_path_sum_with_stats(root, target_sum):
    """
    Check if there exists a root-to-leaf path and return statistics.
    
    Args:
        root: Root of the binary tree
        target_sum: Target sum to find
        
    Returns:
        dict: Statistics about the path search
    """
    if not root:
        return {
            'has_path': False,
            'paths_found': 0,
            'nodes_checked': 0,
            'leaf_nodes_checked': 0
        }
    
    paths_found = 0
    nodes_checked = 0
    leaf_nodes_checked = 0
    
    def search_with_stats(node, remaining_sum, path):
        nonlocal paths_found, nodes_checked, leaf_nodes_checked
        
        if not node:
            return
        
        nodes_checked += 1
        current_path = path + [node.val]
        
        # If it's a leaf node, check if the value equals remaining sum
        if not node.left and not node.right:
            leaf_nodes_checked += 1
            if node.val == remaining_sum:
                paths_found += 1
        else:
            # Recursively check left and right subtrees
            new_remaining_sum = remaining_sum - node.val
            search_with_stats(node.left, new_remaining_sum, current_path)
            search_with_stats(node.right, new_remaining_sum, current_path)
    
    search_with_stats(root, target_sum, [])
    
    return {
        'has_path': paths_found > 0,
        'paths_found': paths_found,
        'nodes_checked': nodes_checked,
        'leaf_nodes_checked': leaf_nodes_checked
    }


def has_path_sum_with_levels(root, target_sum):
    """
    Check if there exists a root-to-leaf path and return paths by level.
    
    Args:
        root: Root of the binary tree
        target_sum: Target sum to find
        
    Returns:
        dict: Paths organized by level
    """
    if not root:
        return {}
    
    from collections import deque
    queue = deque([(root, target_sum, [root.val], 0)])  # (node, remaining_sum, path, level)
    paths_by_level = {}
    
    while queue:
        node, remaining_sum, path, level = queue.popleft()
        
        if level not in paths_by_level:
            paths_by_level[level] = []
        
        # If it's a leaf node, check if the value equals remaining sum
        if not node.left and not node.right:
            if node.val == remaining_sum:
                paths_by_level[level].append(path)
        else:
            # Add children to queue
            new_remaining_sum = remaining_sum - node.val
            if node.left:
                queue.append((node.left, new_remaining_sum, path + [node.left.val], level + 1))
            if node.right:
                queue.append((node.right, new_remaining_sum, path + [node.right.val], level + 1))
    
    return paths_by_level


def has_path_sum_with_validation(root, target_sum):
    """
    Check if there exists a root-to-leaf path with validation.
    
    Args:
        root: Root of the binary tree
        target_sum: Target sum to find
        
    Returns:
        dict: Detailed validation results
    """
    if not root:
        return {
            'has_path': False,
            'reason': 'Empty tree',
            'paths_found': 0,
            'valid_paths': []
        }
    
    def find_valid_paths(node, remaining_sum, path, valid_paths):
        if not node:
            return
        
        current_path = path + [node.val]
        
        # If it's a leaf node, check if the value equals remaining sum
        if not node.left and not node.right:
            if node.val == remaining_sum:
                valid_paths.append(current_path)
        else:
            # Recursively check left and right subtrees
            new_remaining_sum = remaining_sum - node.val
            find_valid_paths(node.left, new_remaining_sum, current_path, valid_paths)
            find_valid_paths(node.right, new_remaining_sum, current_path, valid_paths)
    
    valid_paths = []
    find_valid_paths(root, target_sum, [], valid_paths)
    
    return {
        'has_path': len(valid_paths) > 0,
        'reason': f'Found {len(valid_paths)} path(s) with sum {target_sum}' if valid_paths else f'No paths found with sum {target_sum}',
        'paths_found': len(valid_paths),
        'valid_paths': valid_paths
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
        ([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22),  # Expected: True
        ([1, 2, 3], 5),                                              # Expected: False
        ([], 0),                                                     # Expected: False
        ([1], 1),                                                    # Expected: True
        ([1, 2], 3),                                                 # Expected: True
        ([1, 2, 3], 4),                                              # Expected: True
        ([1, 2, 3], 6),                                              # Expected: True
        ([1, 2, 3], 7),                                              # Expected: False
    ]
    
    for i, (values, target_sum) in enumerate(test_cases, 1):
        print(f"Test case {i}: {values}, target_sum = {target_sum}")
        
        # Create tree from values
        root = create_tree_from_list(values)
        
        # Test different approaches
        result_recursive = has_path_sum(root, target_sum)
        result_iterative = has_path_sum_iterative(root, target_sum)
        
        print(f"Recursive: {result_recursive}")
        print(f"Iterative: {result_iterative}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            has_path_sum_verbose(root, target_sum)
        
        # Test with paths
        has_path, paths = has_path_sum_with_paths(root, target_sum)
        print(f"Has path: {has_path}")
        print(f"Paths found: {paths}")
        
        # Test with statistics
        stats = has_path_sum_with_stats(root, target_sum)
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = has_path_sum_with_validation(root, target_sum)
        print(f"Validation: {validation}")
        
        # Print tree structure
        print("\nTree structure:")
        print_tree_structure(root)
        
        print("-" * 50)
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        ([], 0),                    # Empty tree
        ([1], 1),                   # Single node, correct sum
        ([1], 2),                   # Single node, incorrect sum
        ([1, 2], 3),                # Two nodes, correct sum
        ([1, 2], 4),                # Two nodes, incorrect sum
        ([1, 2, 3], 4),             # Three nodes, correct sum
        ([1, 2, 3], 7),             # Three nodes, incorrect sum
    ]
    
    for case_values, case_sum in edge_cases:
        root = create_tree_from_list(case_values)
        result = has_path_sum(root, case_sum)
        print(f"Tree: {case_values}, target_sum: {case_sum} -> Has path: {result}")
    
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
    large_target = 1000
    
    # Test recursive approach
    start_time = time.time()
    for _ in range(1000):
        has_path_sum(large_root, large_target)
    recursive_time = time.time() - start_time
    
    # Test iterative approach
    start_time = time.time()
    for _ in range(1000):
        has_path_sum_iterative(large_root, large_target)
    iterative_time = time.time() - start_time
    
    print(f"Recursive: {recursive_time:.6f} seconds")
    print(f"Iterative: {iterative_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Start from the root with the target sum")
    print("2. For each node, subtract its value from the remaining sum")
    print("3. If it's a leaf node, check if the remaining sum equals the node's value")
    print("4. If not a leaf, recursively check left and right subtrees")
    print("5. Return True if any path from root to leaf has the target sum")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_values = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]
    example_target = 22
    root = create_tree_from_list(example_values)
    
    print(f"Tree: {example_values}")
    print(f"Target sum: {example_target}")
    print("Tree structure:")
    print_tree_structure(root)
    
    print("\nPath search steps:")
    print("1. Start at root (5) with target sum 22")
    print("2. Remaining sum: 22 - 5 = 17")
    print("3. Check left subtree (4) with remaining sum 17")
    print("4. Remaining sum: 17 - 4 = 13")
    print("5. Check left subtree (11) with remaining sum 13")
    print("6. Remaining sum: 13 - 11 = 2")
    print("7. Check left subtree (11) - this is a leaf")
    print("8. Check if leaf value (11) equals remaining sum (2) -> No")
    print("9. Check right subtree (2) with remaining sum 2")
    print("10. This is a leaf with value 2, which equals remaining sum 2 -> Found path!")
    print("11. Path: 5 -> 4 -> 11 -> 2, sum = 5 + 4 + 11 + 2 = 22")
    
    # Test with different tree shapes
    print("\nDifferent tree shapes:")
    
    # Skewed tree
    skewed_values = [1, 2, None, 3, None, 4, None]
    skewed_root = create_tree_from_list(skewed_values)
    skewed_target = 10
    skewed_result = has_path_sum(skewed_root, skewed_target)
    print(f"Skewed tree: {skewed_values}, target: {skewed_target} -> Has path: {skewed_result}")
    
    # Complete binary tree
    complete_values = [1, 2, 3, 4, 5, 6, 7]
    complete_root = create_tree_from_list(complete_values)
    complete_target = 7
    complete_result = has_path_sum(complete_root, complete_target)
    print(f"Complete tree: {complete_values}, target: {complete_target} -> Has path: {complete_result}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for case_values, case_target in [(skewed_values, skewed_target), (complete_values, complete_target)]:
        root = create_tree_from_list(case_values)
        stats = has_path_sum_with_stats(root, case_target)
        print(f"Tree: {case_values}, target: {case_target}")
        print(f"  Has path: {stats['has_path']}")
        print(f"  Paths found: {stats['paths_found']}")
        print(f"  Nodes checked: {stats['nodes_checked']}")
        print(f"  Leaf nodes checked: {stats['leaf_nodes_checked']}")
        print()
