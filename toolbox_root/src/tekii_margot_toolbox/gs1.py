"""GS1"""

from typing import Literal
import re

__all__ = ["GTIN", "GLN"]


class _Base:  # pylint: disable=R0903
    def __init__(self, digits, re_) -> None:
        match = re_.match(digits)
        if match:
            self.digits = match[1]
            self.parity = match[2]
        else:
            raise ValueError

    def verify(self) -> Literal[True]:
        """Check parity and raise ValueError"""
        sum_: int = 0
        parity: int = 0
        current: int = len(self.digits) - 1
        while current >= 0:
            k: int = 1 if parity % 2 else 3
            sum_ += k * int(self.digits[current])
            current -= 1
            parity += 1
        multiple = sum_ + ((10 - (sum_ % 10)) if (sum_ % 10) else 0)
        calculated = multiple - sum_

        if int(self.parity) != calculated:
            raise ValueError

        return True


class GTIN(_Base):
    """GS1 GTIN"""

    RE = re.compile(r"^(\d?\d{12})(\d)$")

    def __init__(self, digits) -> None:
        super().__init__(digits, GTIN.RE)

    def __str__(self):
        return (self.digits + self.parity).zfill(14)


class GLN(_Base):
    """GS1 GTIN"""

    RE = re.compile(r"^(\d{12})(\d)$")

    def __init__(self, digits) -> None:
        super().__init__(digits, GLN.RE)

    def __str__(self):
        return self.digits + self.parity
