def discount(calculation: float) -> float:
    """
    Calculate the discounted value.

    :param calculation: The original value to be discounted.
    :type calculation: float
    :raises ValueError: If the calculation is less than 0.
    :return: The discounted value. It is the maximum of 1 minus the calculation and 0.
    :rtype: float
    """
    if calculation < 0:
        raise ValueError("Discount function must return a value below 1")
    return max(1 - calculation, 0)
