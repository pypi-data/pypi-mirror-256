from typing import Callable, ClassVar, Self

from numpy import array, prod


class LikenessMixin:
    """
    A mixin class that provides a method to calculate the likeness between two objects.

    :cvar _likeness_functions: A dictionary mapping attribute names to functions that calculate likeness.
    :vartype _likeness_functions: ClassVar[dict[str, Callable]]
    """

    _likeness_functions: ClassVar[dict[str, Callable]] = {}

    def __init__(self, *args, **kwargs):
        """
        Initialize the mixin, forwarding all unused arguments to the superclass.

        :param args: Positional arguments to be forwarded.
        :param kwargs: Keyword arguments to be forwarded.
        """
        super().__init__(*args, **kwargs)  # forwards all unused arguments

    def like(self, other: Self) -> float:
        """
        Calculate the likeness between this object and another.

        The likeness is calculated as the product of the likeness base and the likeness factors.
        The likeness base is 1 if there are likeness functions defined or if this object is equal to the other.
        The likeness factors are calculated by applying the likeness functions to corresponding attributes of the two objects.

        :param other: The other object to compare with.
        :type other: Self
        :return: The likeness between this object and the other.
        :rtype: float
        :raises ValueError: If a likeness function fails to apply.
        """
        likeness_base = float(bool(len(self._likeness_functions)) or self == other)

        factors = []
        for attribute, function in self._likeness_functions.items():
            try:
                a = getattr(self, attribute)
                b = getattr(other, attribute)
                factors.append(function(a, b))
            except Exception:  # noqa: PERF203
                raise ValueError(
                    f"Unable to calculate likeness: {attribute} comparison failed"
                )

        return prod(array([likeness_base, *factors]))
