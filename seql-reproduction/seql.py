"""Defensive behavioral model of the SeqL FI/SQ split and EFF comparator."""

from dataclasses import dataclass
from itertools import accumulate
from operator import xor


@dataclass(frozen=True)
class ScanLock:
    """Bits are indexed from scan-out towards scan-in."""

    fi: tuple[int, ...]
    sq: tuple[int, ...]
    inversion: tuple[int, ...]
    isolated: bool = True

    def __post_init__(self):
        if not len(self.fi) == len(self.sq) == len(self.inversion) or not self.fi:
            raise ValueError("FI, SQ and inversion must have the same positive width.")
        if set(self.fi + self.sq + self.inversion) - {0, 1}:
            raise ValueError("Key and inversion values must be binary.")

    @property
    def scan_masks(self):
        return tuple(sq ^ inv for sq, inv in zip(self.sq, self.inversion))

    def capture(self, functional_inputs):
        """Return the stored bits after a functional capture."""
        return tuple(bit ^ key for bit, key in zip(functional_inputs, self.fi))

    def functional_q(self, captured):
        if self.isolated:
            return captured
        return tuple(bit ^ mask for bit, mask in zip(captured, self.scan_masks))

    def unload(self, captured):
        """Evaluate n test-shift cycles from the supplied captured state."""
        q = captured
        output = []
        for _ in q:
            scan_q = tuple(bit ^ mask for bit, mask in zip(q, self.scan_masks))
            output.append(scan_q[0])
            q = scan_q[1:] + (0,)
        return tuple(output)

    def predicted_scan_error(self):
        return tuple(fi ^ parity for fi, parity in
                     zip(self.fi, accumulate(self.scan_masks, xor)))
