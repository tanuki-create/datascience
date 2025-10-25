"""
Problem 26: Convert Sorted List to Binary Search Tree
Difficulty: Easy

Given the head of a singly linked list where elements are sorted in ascending order, 
convert it to a height-balanced binary search tree.

Time Complexity: O(n)
Space Complexity: O(log n) for the recursion stack
"""

class ListNode:
    """Definition for singly-linked list node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        return f"ListNode({self.val})"


class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"TreeNode({self.val})"


def sorted_list_to_bst(head):
    """
    Convert sorted linked list to height-balanced BST.
    
    Args:
        head: Head of the sorted linked list
        
    Returns:
        TreeNode: Root of the BST
    """
    if not head:
        return None
    
    # Find the middle node
    slow = fast = head
    prev = None
    
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    
    # Create root node
    root = TreeNode(slow.val)
    
    # Split the list
    if prev:
        prev.next = None
        root.left = sorted_list_to_bst(head)
    
    root.right = sorted_list_to_bst(slow.next)
    
    return root


def sorted_list_to_bst_optimized(head):
    """
    Convert sorted linked list to BST with optimized approach.
    
    Args:
        head: Head of the sorted linked list
        
    Returns:
        TreeNode: Root of the BST
    """
    def get_list_length(node):
        length = 0
        while node:
            length += 1
            node = node.next
        return length
    
    def build_bst(left, right):
        nonlocal head
        
        if left > right:
            return None
        
        mid = (left + right) // 2
        
        # Build left subtree
        left_subtree = build_bst(left, mid - 1)
        
        # Create root node
        root = TreeNode(head.val)
        head = head.next
        
        # Build right subtree
        root.right = build_bst(mid + 1, right)
        root.left = left_subtree
        
        return root
    
    length = get_list_length(head)
    return build_bst(0, length - 1)


def sorted_list_to_bst_verbose(head):
    """
    Convert sorted linked list to BST with detailed step-by-step explanation.
    
    Args:
        head: Head of the sorted linked list
        
    Returns:
        TreeNode: Root of the BST
    """
    def convert_verbose(node, depth=0):
        indent = "  " * depth
        print(f"{indent}Converting list starting with {node.val if node else None}")
        
        if not node:
            print(f"{indent}Empty list -> None")
            return None
        
        # Find the middle node
        slow = fast = node
        prev = None
        
        print(f"{indent}Finding middle node...")
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        
        print(f"{indent}Middle node: {slow.val}")
        
        # Create root node
        root = TreeNode(slow.val)
        print(f"{indent}Created root node: {root.val}")
        
        # Split the list
        if prev:
            prev.next = None
            print(f"{indent}Splitting list, left part starts with {node.val}")
            root.left = convert_verbose(node, depth + 1)
        else:
            print(f"{indent}No left part")
            root.left = None
        
        print(f"{indent}Right part starts with {slow.next.val if slow.next else None}")
        root.right = convert_verbose(slow.next, depth + 1)
        
        return root
    
    if not head:
        print("Empty list -> None")
        return None
    
    print(f"Converting sorted list to BST")
    return convert_verbose(head)


def sorted_list_to_bst_with_stats(head):
    """
    Convert sorted linked list to BST and return statistics.
    
    Args:
        head: Head of the sorted linked list
        
    Returns:
        dict: Statistics about the conversion
    """
    if not head:
        return {
            'converted': True,
            'nodes_processed': 0,
            'height': 0,
            'is_balanced': True
        }
    
    nodes_processed = 0
    
    def convert_with_stats(node):
        nonlocal nodes_processed
        
        if not node:
            return None
        
        nodes_processed += 1
        
        # Find the middle node
        slow = fast = node
        prev = None
        
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        
        # Create root node
        root = TreeNode(slow.val)
        
        # Split the list
        if prev:
            prev.next = None
            root.left = convert_with_stats(node)
        
        root.right = convert_with_stats(slow.next)
        
        return root
    
    def get_height(node):
        if not node:
            return 0
        
        left_height = get_height(node.left)
        right_height = get_height(node.right)
        
        return max(left_height, right_height) + 1
    
    def is_balanced(node):
        if not node:
            return True
        
        left_height = get_height(node.left)
        right_height = get_height(node.right)
        
        if abs(left_height - right_height) > 1:
            return False
        
        return is_balanced(node.left) and is_balanced(node.right)
    
    root = convert_with_stats(head)
    height = get_height(root)
    is_balanced_result = is_balanced(root)
    
    return {
        'converted': True,
        'nodes_processed': nodes_processed,
        'height': height,
        'is_balanced': is_balanced_result
    }


def sorted_list_to_bst_with_validation(head):
    """
    Convert sorted linked list to BST with validation.
    
    Args:
        head: Head of the sorted linked list
        
    Returns:
        dict: Detailed validation results
    """
    if not head:
        return {
            'converted': True,
            'root': None,
            'is_valid_bst': True,
            'is_balanced': True,
            'height': 0
        }
    
    def convert_with_validation(node):
        if not node:
            return None
        
        # Find the middle node
        slow = fast = node
        prev = None
        
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        
        # Create root node
        root = TreeNode(slow.val)
        
        # Split the list
        if prev:
            prev.next = None
            root.left = convert_with_validation(node)
        
        root.right = convert_with_validation(slow.next)
        
        return root
    
    def is_valid_bst(node, min_val=float('-inf'), max_val=float('inf')):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (is_valid_bst(node.left, min_val, node.val) and 
                is_valid_bst(node.right, node.val, max_val))
    
    def get_height(node):
        if not node:
            return 0
        
        left_height = get_height(node.left)
        right_height = get_height(node.right)
        
        return max(left_height, right_height) + 1
    
    def is_balanced(node):
        if not node:
            return True
        
        left_height = get_height(node.left)
        right_height = get_height(node.right)
        
        if abs(left_height - right_height) > 1:
            return False
        
        return is_balanced(node.left) and is_balanced(node.right)
    
    root = convert_with_validation(head)
    is_valid = is_valid_bst(root)
    is_balanced_result = is_balanced(root)
    height = get_height(root)
    
    return {
        'converted': True,
        'root': root,
        'is_valid_bst': is_valid,
        'is_balanced': is_balanced_result,
        'height': height
    }


def sorted_list_to_bst_with_traversals(head):
    """
    Convert sorted linked list to BST and return different traversals.
    
    Args:
        head: Head of the sorted linked list
        
    Returns:
        dict: Different traversals of the BST
    """
    def convert_to_bst(node):
        if not node:
            return None
        
        # Find the middle node
        slow = fast = node
        prev = None
        
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        
        # Create root node
        root = TreeNode(slow.val)
        
        # Split the list
        if prev:
            prev.next = None
            root.left = convert_to_bst(node)
        
        root.right = convert_to_bst(slow.next)
        
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
        
        from collections import deque
        result = []
        queue = deque([root])
        
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
            
            result.append(level)
        
        return result
    
    root = convert_to_bst(head)
    
    return {
        'root': root,
        'inorder': inorder_traversal(root),
        'preorder': preorder_traversal(root),
        'postorder': postorder_traversal(root),
        'level_order': level_order_traversal(root)
    }


def create_list_from_values(values):
    """
    Create a linked list from a list of values.
    
    Args:
        values: List of values to create the linked list
        
    Returns:
        ListNode: Head of the linked list
    """
    if not values:
        return None
    
    head = ListNode(values[0])
    current = head
    
    for i in range(1, len(values)):
        current.next = ListNode(values[i])
        current = current.next
    
    return head


def print_list(head):
    """
    Print the linked list.
    
    Args:
        head: Head of the linked list
    """
    values = []
    current = head
    
    while current:
        values.append(current.val)
        current = current.next
    
    print(f"Linked list: {values}")


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
        [-10, -3, 0, 5, 9],  # Expected: [0, -3, 9, -10, null, 5]
        [],                   # Expected: []
        [0],                  # Expected: [0]
        [1, 2, 3],            # Expected: [2, 1, 3]
        [1, 2, 3, 4, 5],      # Expected: [3, 1, 4, null, 2, null, 5]
        [1, 2, 3, 4, 5, 6, 7], # Expected: [4, 2, 6, 1, 3, 5, 7]
    ]
    
    for i, values in enumerate(test_cases, 1):
        print(f"Test case {i}: {values}")
        
        # Create linked list from values
        head = create_list_from_values(values)
        
        # Test different approaches
        root1 = sorted_list_to_bst(head)
        root2 = sorted_list_to_bst_optimized(create_list_from_values(values))
        
        print(f"Recursive approach: {root1.val if root1 else None}")
        print(f"Optimized approach: {root2.val if root2 else None}")
        
        # Test verbose output for first case
        if i == 1:
            print("\nVerbose output:")
            sorted_list_to_bst_verbose(create_list_from_values(values))
        
        # Test with statistics
        stats = sorted_list_to_bst_with_stats(create_list_from_values(values))
        print(f"Statistics: {stats}")
        
        # Test with validation
        validation = sorted_list_to_bst_with_validation(create_list_from_values(values))
        print(f"Validation: {validation}")
        
        # Test with traversals
        traversals = sorted_list_to_bst_with_traversals(create_list_from_values(values))
        print(f"Inorder: {traversals['inorder']}")
        print(f"Preorder: {traversals['preorder']}")
        print(f"Postorder: {traversals['postorder']}")
        print(f"Level order: {traversals['level_order']}")
        
        # Print tree structure
        print("\nTree structure:")
        print_tree_structure(root1)
        
        print("-" * 50)
    
    # Test edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],                    # Empty list
        [1],                   # Single node
        [1, 2],                # Two nodes
        [1, 2, 3],             # Three nodes
        [1, 2, 3, 4, 5, 6, 7], # Seven nodes
    ]
    
    for case in edge_cases:
        head = create_list_from_values(case)
        root = sorted_list_to_bst(head)
        result = root.val if root else None
        print(f"List: {case} -> Root: {result}")
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large test case
    large_values = sorted([random.randint(1, 1000) for _ in range(1000)])
    large_head = create_list_from_values(large_values)
    
    # Test recursive approach
    start_time = time.time()
    for _ in range(100):
        sorted_list_to_bst(large_head)
    recursive_time = time.time() - start_time
    
    # Test optimized approach
    start_time = time.time()
    for _ in range(100):
        sorted_list_to_bst_optimized(large_head)
    optimized_time = time.time() - start_time
    
    print(f"Recursive: {recursive_time:.6f} seconds")
    print(f"Optimized: {optimized_time:.6f} seconds")
    
    # Algorithm explanation
    print("\nAlgorithm explanation:")
    print("1. Find the middle node of the linked list")
    print("2. Create a root node with the middle value")
    print("3. Split the list into left and right parts")
    print("4. Recursively build left and right subtrees")
    print("5. This ensures the tree is height-balanced")
    
    # Step-by-step example
    print("\nStep-by-step example:")
    example_values = [-10, -3, 0, 5, 9]
    head = create_list_from_values(example_values)
    
    print(f"List: {example_values}")
    print_list(head)
    
    print("\nConversion steps:")
    print("1. Find middle node: 0")
    print("2. Create root: 0")
    print("3. Split list: left = [-10, -3], right = [5, 9]")
    print("4. Build left subtree from [-10, -3]")
    print("5. Build right subtree from [5, 9]")
    print("6. Result: balanced BST with root 0")
    
    # Test with different list sizes
    print("\nDifferent list sizes:")
    for size in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        values = list(range(1, size + 1))
        head = create_list_from_values(values)
        root = sorted_list_to_bst(head)
        height = 0
        if root:
            def get_height(node):
                if not node:
                    return 0
                return max(get_height(node.left), get_height(node.right)) + 1
            height = get_height(root)
        print(f"Size {size}: {values} -> Height: {height}")
    
    # Test with statistics
    print("\nDetailed statistics:")
    for case in [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]:
        head = create_list_from_values(case)
        stats = sorted_list_to_bst_with_stats(head)
        print(f"List: {case}")
        print(f"  Nodes processed: {stats['nodes_processed']}")
        print(f"  Height: {stats['height']}")
        print(f"  Is balanced: {stats['is_balanced']}")
        print()
