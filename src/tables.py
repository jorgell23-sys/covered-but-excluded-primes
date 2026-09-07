#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Writes data/*.txt.  Everything in data/ is produced here, never by hand.

    python src/tables.py
"""
from __future__ import annotations

import os
import random
import sys
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from excluded import (S_of_f, arrow, certificate, cycle_through,   # noqa: E402
                      digraph, evaluate, greatest_fixed_point, has_root,
                      mult_order, on_a_cycle, roots, sieve,
                      smallest_prime_factors, _gcd, _norm)

random.seed(20260906)
DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "data")

CATALOGUE = [
    ("x+1", [1, 1], "trivial", "0"),
    ("x^2+1 (Phi_4)", [1, 0, 1], "C_2", "1/2"),
    ("x^2+x+1 (Phi_3)", [1, 1, 1], "C_2", "1/2"),
    ("x^2-x+1 (Phi_6)", [1, -1, 1], "C_2", "1/2"),
    ("x^2-x-1", [1, -1, -1], "C_2", "1/2"),
    ("x^4+x^3+2x^2+x+1 (Phi_3 Phi_4)", [1, 1, 2, 1, 1], "C_2xC_2 two orbits", "1/4"),
    ("x^3-x-1", [1, 0, -1, -1], "S_3", "1/3"),
    ("x^4-x-1", [1, 0, 0, -1, -1], "S_4", "3/8"),
    ("x^5-x-1", [1, 0, 0, 0, -1, -1], "S_5", "11/30"),
    ("x^3+x^2-2x-1 (periods of zeta_7)", [1, 1, -2, -1], "C_3", "2/3"),
    ("x^4+x^3+x^2+x+1 (Phi_5)", [1, 1, 1, 1, 1], "C_4", "3/4"),
    ("x^4+1 (Phi_8)", [1, 0, 0, 0, 1], "C_2xC_2", "3/4"),
    ("x^5+x^4-4x^3-3x^2+3x+1 (periods of zeta_11)", [1, 1, -4, -3, 3, 1],
     "C_5", "4/5"),
]
PHI6 = [1, -1, 1]


def squarefree_mod(F, p):
    f = _norm(F, p)
    if len(f) < len(F) or len(f) <= 1:
        return False
    d = len(f) - 1
    df = _norm([(d - i) * c % p for i, c in enumerate(f)][:-1], p)
    if not df:
        return False
    return len(_gcd(f, df, p)) <= 1


def write(name, lines):
    path = os.path.join(DATA, name)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote data/" + name, "(%d lines)" % len(lines))


def main():
    os.makedirs(DATA, exist_ok=True)
    primes30k = sieve(30000)
    n = len(primes30k)

    rows = ["# Density of primes that divide no element of S(f), f(q^e)=F(q^e)",
            "# predicted = share of fixed-point-free elements of Gal(F)",
            "# measured over the %d primes below 30000" % n,
            "# F\tGalois group\tpredicted\tmeasured"]
    for name, F, grp, pred in CATALOGUE:
        got = sum(1 for p in primes30k if not has_root(F, p)) / n
        rows.append("%s\t%s\t%s\t%.6f" % (name, grp, pred, got))
    write("densities.txt", rows)

    rows = ["# f(q^e) = q^(2e) - q^e + 1.  Primes q < 8000 with an arrow q -> 3,",
            "# and whether q is itself covered (i.e. F has a root mod q).",
            "# q\tq mod 3\tq covered?"]
    into = [q for q in sieve(8000) if q != 3 and arrow(PHI6, q, 3)]
    for q in into:
        rows.append("%d\t%d\t%s" % (q, q % 3, "yes" if has_root(PHI6, q) else "no"))
    rows.append("# total %d, of which covered: %d"
                % (len(into), sum(1 for q in into if has_root(PHI6, q))))
    write("arrows_into_3.txt", rows)

    small = sieve(3000)
    C1 = [p for p in small if has_root(PHI6, p)]
    adj, _ = digraph(PHI6, C1)
    cyc = on_a_cycle(adj)
    rows = ["# f(q^e) = q^(2e) - q^e + 1.  For every covered prime below 3000,",
            "# a directed cycle, i.e. an explicit n in S(f).",
            "# p\tcertificate (prime^exponent, ...)\tn has how many digits"]
    for p in sorted(C1):
        if p not in cyc:
            rows.append("%d\tNO CYCLE - covered but excluded\t-" % p)
            continue
        cert = certificate(PHI6, cycle_through(adj, p))
        m = 1
        for q, e in cert:
            m *= q ** e
        rows.append("%d\t%s\t%d"
                    % (p, " ".join("%d^%d" % t for t in cert), len(str(m))))
    write("certificates_phi6.txt", rows)

    rows = ["# Sweep: monic F of degree 2..4, coefficients in [-2,2], F(0)=+-1,",
            "# against the primes below 1000.  Lists every prime that has an",
            "# incoming arrow but survives no further iteration.",
            "# F\tlost prime\tF mod p squarefree? (unramified)"]
    seen, lost_total = set(), 0
    for g in range(2, 5):
        for mid in product(*[range(-2, 3)] * (g - 1)):
            for c0 in (1, -1):
                F = [1] + list(mid) + [c0]
                if tuple(F) in seen:
                    continue
                seen.add(tuple(F))
                C = [p for p in sieve(1000) if has_root(F, p)]
                if not C:
                    continue
                inf = greatest_fixed_point(F, C)
                for p in [p for p in C if p not in inf]:
                    lost_total += 1
                    rows.append("%s\t%d\t%s"
                                % (F, p, "YES (unramified!)"
                                   if squarefree_mod(F, p) else "no (ramified)"))
    rows.append("# %d polynomials swept, %d covered-but-excluded primes"
                % (len(seen), lost_total))
    write("covered_but_excluded.txt", rows)

    spf = smallest_prime_factors(400000)
    s6 = S_of_f(lambda q, e: q ** (2 * e) - q ** e + 1, 400000, spf)
    ss = S_of_f(lambda q, e: q ** e + 1, 400000, spf)
    rows = ["# S(f) up to 400000, computed as plain integers: factor n, apply f,",
            "# multiply, divide.  No digraph, no criterion.  n = 1 included.",
            "f(q^e) = q^(2e) - q^e + 1 : %s" % s6,
            "  divisible by 3: %d" % sum(1 for x in s6 if x % 3 == 0),
            "POSITIVE CONTROL  f(q^e) = q^e + 1 : %d elements" % len(ss),
            "  divisible by 3: %d" % sum(1 for x in ss if x % 3 == 0),
            "  first twenty: %s" % ss[:20]]
    write("s_of_f_integers.txt", rows)


if __name__ == "__main__":
    main()
