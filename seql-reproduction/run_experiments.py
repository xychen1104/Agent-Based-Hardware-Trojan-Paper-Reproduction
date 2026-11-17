"""Generate deterministic CSV results for the paper's abstract model."""

import csv
from fractions import Fraction
from itertools import product
from pathlib import Path

from seql import ScanLock


def analyze(width, style, inversion):
    zero = (0,) * width
    rows = []
    for key in product((0, 1), repeat=2 * width):
        model = ScanLock(key[::2], key[1::2], inversion, style == "SeqL")
        captured = model.capture(zero)
        observed = model.unload(captured)
        if observed != model.predicted_scan_error():
            raise AssertionError("Clocked shift disagrees with scan-path parity.")
        rows.append(("".join(map(str, key)), observed == zero,
                     model.functional_q(captured) == zero))
    return rows


def write_csv(path, headings, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(headings)
        writer.writerows(rows)


def main():
    output = Path("results")
    output.mkdir(exist_ok=True)
    table = analyze(2, "SeqL", (0, 0))
    assert {key for key, scan, _ in table if scan} == {"0000", "0011", "1101", "1110"}
    assert {key for key, _, functional in table if functional} == {"0000", "0001", "0100", "0101"}
    write_csv(output / "table_i.csv", ["fi1_sq1_fi0_sq0", "scan_correct", "functional_correct"], table)

    summary = []
    for width in range(1, 9):
        for style in ("SeqL", "EFF"):
            rows = analyze(width, style, (0,) * width)
            scanned = sum(scan for _, scan, _ in rows)
            functional = sum(functional for _, _, functional in rows)
            both = sum(scan and ok for _, scan, ok in rows)
            assert scanned == functional == 2 ** width
            if style == "SeqL":
                assert both == 1
            summary.append((width, style, len(rows), scanned, functional, both,
                            str(Fraction(scanned - both, scanned))))
    write_csv(output / "scaling.csv",
              ["cells", "style", "assignments", "scan_correct", "functional_correct",
               "both_correct", "scan_correct_but_functionally_wrong_fraction"], summary)

    # Exercise both gate polarities and all capture words for a three-cell chain.
    checked = 0
    for inversion in product((0, 1), repeat=3):
        for key in product((0, 1), repeat=6):
            for isolated in (True, False):
                model = ScanLock(key[::2], key[1::2], inversion, isolated)
                for word in product((0, 1), repeat=3):
                    captured = model.capture(word)
                    scan_expected = tuple(bit ^ mask for bit, mask in
                                          zip(word, model.predicted_scan_error()))
                    assert model.unload(captured) == scan_expected
                    assert tuple(a ^ b for a, b in zip(word, model.functional_q(captured))) == (
                        model.functional_q(model.capture((0, 0, 0))))
                    checked += 1
    print("PASS Table I: 16 assignments, 4 scan-correct, 4 functional-correct, 1 both")
    print("PASS SeqL scaling: 1 common assignment out of 2^n scan-correct assignments (n=1..8)")
    print(f"PASS {checked} three-cell mode, polarity, key, and capture-word checks")


if __name__ == "__main__":
    main()
