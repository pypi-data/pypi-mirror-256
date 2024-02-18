def ignore(a: object, b: object) -> float:
    """
    Ignores the input parameters and returns 1. A helper function to use in LikenessMixin if you don't want a comparison to take place for a certain attribute.

    :param a: The first input parameter. This parameter is ignored.
    :type a: object
    :param b: The second input parameter. This parameter is ignored.
    :type b: object
    :return: The function always returns 1.
    :rtype: float
    """
    return 1
