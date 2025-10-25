"""
Problem 4: Best Time to Buy and Sell Stock
Difficulty: Easy

You are given an array prices where prices[i] is the price of a given stock on the ith day.
You want to maximize your profit by choosing a single day to buy one stock and choosing 
a different day in the future to sell that stock.

Time Complexity: O(n)
Space Complexity: O(1)
"""

def max_profit(prices):
    """
    Find maximum profit from buying and selling stock once.
    
    Args:
        prices: List of stock prices
        
    Returns:
        int: Maximum profit achievable
    """
    if not prices or len(prices) < 2:
        return 0
    
    min_price = prices[0]
    max_profit = 0
    
    for price in prices[1:]:
        # Update minimum price seen so far
        min_price = min(min_price, price)
        # Calculate profit if we sell today
        profit = price - min_price
        # Update maximum profit
        max_profit = max(max_profit, profit)
    
    return max_profit


def max_profit_brute_force(prices):
    """
    Brute force approach - O(n²) time complexity.
    
    Args:
        prices: List of stock prices
        
    Returns:
        int: Maximum profit achievable
    """
    if not prices or len(prices) < 2:
        return 0
    
    max_profit = 0
    n = len(prices)
    
    # Try all possible buy and sell combinations
    for i in range(n):
        for j in range(i + 1, n):
            profit = prices[j] - prices[i]
            max_profit = max(max_profit, profit)
    
    return max_profit


def max_profit_with_dates(prices):
    """
    Find maximum profit and return the buy/sell dates.
    
    Args:
        prices: List of stock prices
        
    Returns:
        tuple: (max_profit, buy_day, sell_day)
    """
    if not prices or len(prices) < 2:
        return 0, 0, 0
    
    min_price = prices[0]
    min_price_day = 0
    max_profit = 0
    buy_day = sell_day = 0
    
    for i, price in enumerate(prices[1:], 1):
        if price < min_price:
            min_price = price
            min_price_day = i
        
        profit = price - min_price
        if profit > max_profit:
            max_profit = profit
            buy_day = min_price_day
            sell_day = i
    
    return max_profit, buy_day, sell_day


def max_profit_multiple_transactions(prices):
    """
    Find maximum profit with multiple transactions allowed.
    This is a follow-up problem.
    
    Args:
        prices: List of stock prices
        
    Returns:
        int: Maximum profit with multiple transactions
    """
    if not prices or len(prices) < 2:
        return 0
    
    profit = 0
    
    # Buy low, sell high - capture every profitable transaction
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
    
    return profit


# Test cases
if __name__ == "__main__":
    test_cases = [
        [7, 1, 5, 3, 6, 4],  # Expected: 5
        [7, 6, 4, 3, 1],      # Expected: 0
        [1, 2, 3, 4, 5],      # Expected: 4
        [5, 4, 3, 2, 1],      # Expected: 0
        [2, 4, 1],            # Expected: 2
        [1],                  # Expected: 0
        [1, 2],               # Expected: 1
    ]
    
    for i, prices in enumerate(test_cases, 1):
        print(f"Test case {i}: {prices}")
        
        # Single transaction
        result_single = max_profit(prices)
        print(f"Single transaction max profit: {result_single}")
        
        # With dates
        profit, buy_day, sell_day = max_profit_with_dates(prices)
        if profit > 0:
            print(f"Buy on day {buy_day} (price: {prices[buy_day]}), "
                  f"sell on day {sell_day} (price: {prices[sell_day]})")
        else:
            print("No profitable transaction possible")
        
        # Multiple transactions (follow-up)
        if len(prices) > 1:
            result_multiple = max_profit_multiple_transactions(prices)
            print(f"Multiple transactions max profit: {result_multiple}")
        
        print("-" * 50)
    
    # Performance comparison
    print("\nPerformance comparison:")
    import time
    import random
    
    # Generate large test case
    large_prices = [random.randint(1, 1000) for _ in range(10000)]
    
    # Test optimized approach
    start_time = time.time()
    for _ in range(100):
        max_profit(large_prices)
    optimized_time = time.time() - start_time
    
    # Test brute force approach
    start_time = time.time()
    for _ in range(10):  # Reduced iterations due to O(n²) complexity
        max_profit_brute_force(large_prices)
    brute_time = time.time() - start_time
    
    print(f"Optimized approach: {optimized_time:.6f} seconds")
    print(f"Brute force approach: {brute_time:.6f} seconds")
    print(f"Optimized is {brute_time/optimized_time:.2f}x faster")
    
    # Edge cases
    print("\nEdge cases:")
    edge_cases = [
        [],           # Empty array
        [5],          # Single element
        [1, 1, 1, 1], # All same prices
        [1, 5, 1, 5], # Multiple peaks and valleys
    ]
    
    for case in edge_cases:
        result = max_profit(case)
        print(f"Prices: {case} -> Max profit: {result}")
