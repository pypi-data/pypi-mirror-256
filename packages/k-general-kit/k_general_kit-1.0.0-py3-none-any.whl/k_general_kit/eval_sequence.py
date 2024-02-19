import math
real = float|int

"""There we have functions to evaluate the sequence defined by : for n >= 5, Wn = (sin(W(n-1))+sin(W(n-2))+5)/(sqrt(n)-2), using recursion, from the worst to the best in terms of time complexity."""

def eval_suit_rec(n: int, w3: float, w4: float) -> float:
    """
    Computes the value of the sequence Wn for n >= 5 using the recurrence:
    Wn = (sin(W(n-1)) + sin(W(n-2)) + 5) / (sqrt(n) - 2), with W3=w3 and W4=w4.

    Args:
        n (int): The index of the value to compute in the sequence W.
        w3 (float): The value of the sequence W for n=3.
        w4 (float): The value of the sequence W for n=4.

    Returns:
        float: The value of the sequence W for the specified index n.

    Complexity:
        Time: O(2^n), where n is the index of the value to compute in the sequence W.
        Space: O(n), due to the recursion stack.

    Principle:
        The function uses recursion to compute the value of the sequence W for a given index n,
        using the previous two values W(n-1) and W(n-2).
        The computation is based on the recurrence formula Wn = (sin(W(n-1)) + sin(W(n-2)) + 5) / (sqrt(n) - 2).
        The base cases are when n is equal to 3 or 4, where the function returns the corresponding value of the sequence W.
    """
    if n == 3:
        return w3  # Base case for n=3
    if n == 4:
        return w4  # Base case for n=4
    return (math.sin(eval_suit_rec(n-2, w3, w4)) + math.sin(eval_suit_rec(n-1, w3, w4)) + 5) / (math.sqrt(n) - 2)

def eval_suit_rec2(n: int, w3: float, w4: float, S: list[float] = []) -> float:
    """
    Computes the value of the sequence Wn for n >= 5 using a recurrence formula and a list to store intermediate values.

    Args:
        n (int): The index of the value to compute in the sequence W.
        w3 (float): The value of the sequence W for n=3.
        w4 (float): The value of the sequence W for n=4.
        S (list[float]): A list to store the computed values of the sequence W for indices 3 to n-1.

    Returns:
        float: The value of the sequence W for the specified index n.

    Complexity:
        Time: O(n), where n is the index of the value to compute in the sequence W.
        Space: O(n), due to the storage of the computed values in the list.

    Principle:
        The function uses a list to store the computed values of the sequence W for indices 3 to n-1.
        If the list is not empty, the function returns the precomputed value for the specified index n.
        If the list is empty, the function initializes it with the values for indices 3 and 4.
        For each index i from 5 to n, the function computes the value of the sequence W using the recurrence formula
        Wn = (sin(W(n-1)) + sin(W(n-2)) + 5) / (sqrt(n) - 2).
        The function stores the computed value in the list and returns it.

        The time complexity of this function is O(n), because it computes the sequence W for the given index n
        by computing the previous values and storing them in the list. The space complexity is also O(n),
        because the list will contain n-2 elements.
    """
    l = len(S)
    if n == 4:
        if l == 0:
            S.extend([w3, w4])  # Initialize the list with values for indices 3 and 4
        return w4  # Return the value of the sequence W for index 4
    if n == 3:
        if l == 0:
            S.append(w3)  # Initialize the list with the value for index 3
        return w3  # Return the value of the sequence W for index 3
    if l >= n-2:
        return S[n-3]  # Return the precomputed value for the specified index n
    if l == n-3:
        w = (math.sin(S[n-4]) + math.sin(S[n-5]) + 5) / math.sqrt(n)  # Compute the value of the sequence W for index n
    else:
        w = (math.sin(eval_suit_rec2(n-1, w3, w4, S)) + math.sin(eval_suit_rec2(n-2, w3, w4, S)) + 5) / (math.sqrt(n) - 2)
    S.append(w)  # Store the computed value in the list
    return w  # Return the computed value

def eval_suit_rec3(n: int, w3: float, w4: float) -> float:
    """
    Calculates the nth term of the sequence Wn = (sin(W(n-1))+sin(W(n-2))+5)/(sqrt(n)-2) using recursion.
    
    Args:
    - n (int): The index of the term to calculate.
    - w3 (float): The value of W3.
    - w4 (float): The value of W4.
    
    Returns:
    - w (float): The value of Wn.
    
    Time complexity: O(n)
    Space complexity: O(1)
    
    The function uses a recursive approach, where it keeps track of the previous two terms of the sequence
    and calculates the current term based on them. It updates the previous two terms as it goes along,
    so it only needs constant space to keep track of them.
    """
    global prev2   # Use a global variable to keep track of the the term two terms ago
    if n == 4:
        prev2 = w3  # Initialize the term two terms ago which will start to be useful for n = 5
        return w4
    if n == 3:
        return w3   # Return the value of W3 for n = 3
    prev1 = eval_suit_rec3(n-1, w3, w4)   # Recursively calculate the value of W(n-1)
    w = (math.sin(prev1) + math.sin(prev2) + 5) / (math.sqrt(n) - 2)   # Calculate the value of Wn using the previous two terms
    prev2 = prev1   # Update the previous two terms for the next calculation
    return w   # Return the value of Wn

if __name__ == "__main__":
    import eval_sequence
    print(help(eval_sequence))