from .likeness_mixin import LikenessMixin


def likeness(a: LikenessMixin, b: LikenessMixin) -> float:
    """
    Calculate the likeness between two objects of type LikenessMixin.

    :param a: The first object to compare.
    :type a: LikenessMixin
    :param b: The second object to compare.
    :type b: LikenessMixin
    :return: The likeness between the two objects, calculated by calling the `like` method of the first object with the second object as the argument.
    :rtype: float
    """
    return a.like(b)
