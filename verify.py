#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifies every claim in RESULT.md. Standard library only.

    python verify.py

Prints PASS/FAIL per check and exits 1 if anything fails.

Check [7] is EXTERNAL: it recomputes S(sigma) from scratch and compares it with
the terms published in OEIS A175200, so that "trust me" becomes "run it
yourself".
"""
from __future__ import annotations

import os
import random
import re
import sys
from itertools import product

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from excluded import (S_of_f, arrow, certificate, cycle_through,   # noqa: E402
                      digraph, evaluate, greatest_fixed_point, has_root,
                      mult_order, on_a_cycle, roots, root_orders, sieve,
                      smallest_prime_factors, _gcd, _norm)

random.seed(20260906)
ROOT = os.path.dirname(os.path.abspath(__file__))
FAILURES = []


def check(ok, label, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label +
          (("  -- " + detail) if detail else ""))
    if not ok:
        FAILURES.append(label)


# ---------------------------------------------------------------------------
# The catalogue.  Every F has F(0) = +-1, which is exactly locality.
# The predicted density is the proportion of elements of Gal(F) with NO fixed
# point on the roots (Frobenius, 1896).
# ---------------------------------------------------------------------------
CATALOGUE = [
    ("x+1            (sigma*)",   [1, 1],                 0.0),
    ("x^2+1          (Phi_4)",    [1, 0, 1],              1 / 2),
    ("x^2+x+1        (Phi_3)",    [1, 1, 1],              1 / 2),
    ("x^2-x+1        (Phi_6)",    [1, -1, 1],             1 / 2),
    ("x^4+x^3+x^2+x+1 (Phi_5)",   [1, 1, 1, 1, 1],        3 / 4),
    ("x^4+1          (Phi_8)",    [1, 0, 0, 0, 1],        3 / 4),
    ("x^4+x^3+2x^2+x+1 (Phi_3Phi_4)", [1, 1, 2, 1, 1],    1 / 4),
    ("x^3-x-1        (S_3)",      [1, 0, -1, -1],         1 / 3),
    ("x^3+x^2-2x-1   (C_3)",      [1, 1, -2, -1],         2 / 3),
    ("x^5+x^4-4x^3-3x^2+3x+1 (C_5)", [1, 1, -4, -3, 3, 1], 4 / 5),
    ("x^4-x-1        (S_4)",      [1, 0, 0, -1, -1],      3 / 8),
    ("x^5-x-1        (S_5)",      [1, 0, 0, 0, -1, -1],   11 / 30),
    ("x^2-x-1",                   [1, -1, -1],            1 / 2),
]

PHI6 = [1, -1, 1]


def phi6(q, e):
    return q ** (2 * e) - q ** e + 1


def sigma_star(q, e):
    return q ** e + 1


def sigma(q, e):
    return (q ** (e + 1) - 1) // (q - 1)


#: Published terms of OEIS A175200, "Numbers k such that rad(k) divides
#: sigma(k)".  Copied from the entry; recomputed from scratch in check [7].
A175200 = [1, 6, 24, 28, 40, 54, 96, 120, 135, 216, 224, 234, 270, 360, 384,
           486, 496, 540, 588, 600, 640, 672, 864, 891, 936, 1000, 1080, 1350,
           1372, 1521, 1536, 1638, 1782, 1792, 1920, 1944, 2016, 2160, 2176,
           3000, 3240, 3375, 3402, 3456, 3564, 3724, 3744, 3780, 4320]

N_INTEGERS = 400000
PRIMES_SMALL = sieve(3000)
PRIMES_DENS = sieve(30000)


# ---------------------------------------------------------------------------
# [0] The front page, checked before the mathematics
# ---------------------------------------------------------------------------
PARTS = ("hallazgo:que", "hallazgo:enunciado", "hallazgo:ejemplo",
         "hallazgo:prueba", "hallazgo:comprobar", "hallazgo:nodice")
HISTORY_FIRST = re.compile(
    r"(what changed in version|qu[eé] cambi[oó] en la versi[oó]n|"
    r"version \d|versi[oó]n \d|release \d)", re.I)
METHOD_LESSON = re.compile(
    r"(la regla que sale|the rule that comes out|the rule this leaves|"
    r"lo que esto ense[nñ]a|what this teaches|la lecci[oó]n|the lesson)", re.I)


def front_page():
    print("[0] The front page: what was found, before anything else")
    for rel in ("README.md", "README.es.md", "RESULT.md"):
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            check(False, rel + " is missing")
            continue
        text = open(path, encoding="utf-8").read()
        pos = [text.find("<!-- %s -->" % a) for a in PARTS]
        if min(pos) < 0:
            check(False, rel + ": missing parts",
                  str([a for a, i in zip(PARTS, pos) if i < 0]))
            continue
        problems = []
        if pos != sorted(pos):
            problems.append("the six parts are out of order")
        head = text[:pos[0]]
        if len(head.splitlines()) > 12:
            problems.append("the finding starts on line %d"
                            % (len(head.splitlines()) + 1))
        m = HISTORY_FIRST.search(head)
        if m:
            problems.append("version history before the finding: %r" % m.group(0))
        if len(re.findall(r"\d[\d.,]{2,}", text[pos[2]:pos[3]])) < 3:
            problems.append("the example carries no numbers")
        if "```" not in text[pos[4]:pos[5]]:
            problems.append("the check carries no runnable command")
        if "POR LLENAR" in text:
            problems.append("the skeleton is still unfilled")
        m = METHOD_LESSON.search(text)
        if m:
            problems.append("a lesson about method: %r" % m.group(0))
        check(not problems, rel + ": six parts, in order, at the top",
              "; ".join(problems))


# ---------------------------------------------------------------------------
def main():
    front_page()

    # --- [1] the criterion ------------------------------------------------
    print()
    print("[1] The criterion: p has an incoming arrow  <=>  F has a root mod p")
    for name, F, _d in CATALOGUE:
        bad = [p for p in PRIMES_SMALL
               if has_root(F, p) != any(evaluate(F, a) % p == 0
                                        for a in range(1, p))]
        check(not bad, "%-40s exhaustive over every residue class" % name,
              "" if not bad else "differs at %s" % bad[:4])

    print()
    print("[1b] Every prime the criterion calls covered gets an explicit witness")
    for name, F, _d in CATALOGUE:
        missing = []
        for p in PRIMES_SMALL:
            if not has_root(F, p):
                continue
            found = None
            for r in roots(F, p):
                if r == 0:
                    continue
                cand = r if r > 1 else r + p
                while cand < r + 400 * p:
                    if cand != p and _is_prime(cand):
                        found = (cand, 1)
                        break
                    cand += p
                if found:
                    break
            if not found or evaluate(F, found[0] ** found[1]) % p != 0:
                missing.append(p)
        check(not missing, "%-40s a prime q and e with p | F(q^e)" % name,
              "" if not missing else "no witness for %s" % missing[:4])

    print()
    print("[1c] Theorem 31 is the cyclotomic case: covered  <=>  m | p-1")
    for m, F in ((3, [1, 1, 1]), (4, [1, 0, 1]), (5, [1, 1, 1, 1, 1]),
                 (6, [1, -1, 1]), (8, [1, 0, 0, 0, 1])):
        # p | m is the RAMIFIED case and the rule is not about it: mod 2,
        # Phi_4 = (x+1)^2 has the root 1 although 4 does not divide 2-1.
        bad = [p for p in PRIMES_SMALL
               if m % p and has_root(F, p) != ((p - 1) % m == 0)]
        check(not bad, "Phi_%d: covered exactly when %d | p-1 (p not dividing %d)"
              % (m, m, m), "" if not bad else str(bad[:4]))

    # --- [2] the density --------------------------------------------------
    print()
    print("[2] The density of uncovered primes is the proportion of "
          "fixed-point-free elements of Gal(F)")
    n = len(PRIMES_DENS)
    for name, F, pred in CATALOGUE:
        got = sum(1 for p in PRIMES_DENS if not has_root(F, p)) / n
        se = (pred * (1 - pred) / n) ** 0.5
        ok = abs(got - pred) <= max(3 * se, 1.5 / n)
        check(ok, "%-40s predicted %.5f" % (name, pred),
              "measured %.5f over %d primes" % (got, n))

    print()
    print("[2b] Stronger: the WHOLE distribution of the number of roots")
    for name, F, expected in (
            ("x^3-x-1 (S_3)", [1, 0, -1, -1], {0: 1 / 3, 1: 1 / 2, 3: 1 / 6}),
            ("x^4-x-1 (S_4)", [1, 0, 0, -1, -1],
             {0: 3 / 8, 1: 1 / 3, 2: 1 / 4, 4: 1 / 24})):
        tally = {}
        for p in PRIMES_DENS:
            k = len(roots(F, p))
            tally[k] = tally.get(k, 0) + 1
        worst, where = 0.0, None
        for k, pr in expected.items():
            got = tally.get(k, 0) / n
            se = max((pr * (1 - pr) / n) ** 0.5, 1e-9)
            if abs(got - pr) / se > worst:
                worst, where = abs(got - pr) / se, (k, got, pr)
        check(worst <= 3.0, "%-16s every root-count density matches" % name,
              "worst: %d roots, %.5f vs %.5f (%.2f SE)"
              % (where[0], where[1], where[2], worst))

    # --- [3] the finding --------------------------------------------------
    print()
    print("[3] Phi_6 and the prime 3: covered, and it divides nothing in S(f)")
    check(sorted(roots(PHI6, 3)) == [2], "the only root of x^2-x+1 mod 3 is 2")
    check(mult_order(2, 3) == 2, "that root has order 2 mod 3")
    check(has_root(PHI6, 3), "so 3 IS covered by the criterion")

    into3 = [q for q in sieve(8000) if q != 3 and arrow(PHI6, q, 3)]
    also_cov = [q for q in into3 if has_root(PHI6, q)]
    check(len(into3) > 400 and not also_cov,
          "of the %d primes with an arrow into 3, none is itself covered"
          % len(into3), "covered ones: %s" % also_cov[:5])
    check(all(q % 3 == 2 for q in into3),
          "every prime pointing at 3 is 2 mod 3")
    check(all(p % 6 == 1 for p in PRIMES_SMALL
              if p not in (2, 3) and has_root(PHI6, p)),
          "every covered prime other than 3 is 1 mod 6 -- the two sets are "
          "disjoint")

    print()
    print("[3b] The same thing on the integers, with a positive control")
    spf = smallest_prime_factors(N_INTEGERS)
    s_phi6 = S_of_f(phi6, N_INTEGERS, spf)
    s_star = S_of_f(sigma_star, N_INTEGERS, spf)
    bad = [n for n in s_phi6 if n % 3 == 0]
    good = [n for n in s_star if n % 3 == 0]
    check(len(s_phi6) > 1 and not bad,
          "S(Phi_6) up to %d: %d elements above 1, none divisible by 3"
          % (N_INTEGERS, len(s_phi6) - 1), "elements: %s" % s_phi6[1:])
    check(len(good) > 50,
          "POSITIVE CONTROL: the same search on sigma* finds %d elements "
          "divisible by 3" % len(good), "of %d" % len(s_star))
    covered_primes = set()
    for n in s_phi6[1:]:
        for p, _ in _fac(n, spf):
            covered_primes.add(p)
    check(all(has_root(PHI6, p) for p in covered_primes),
          "every prime appearing in S(Phi_6) is covered",
          "primes: %s" % sorted(covered_primes))

    # --- [4] the failures live on ramified primes -------------------------
    print()
    print("[4] Where the one-step criterion can fail: only at ramified primes")
    sweep = _sweep_polynomials()
    lost_total, unramified_lost, with_loss = 0, [], 0
    small = sieve(1000)
    for F in sweep:
        C1 = [p for p in small if has_root(F, p)]
        if not C1:
            continue
        Cinf = greatest_fixed_point(F, C1)
        lost = [p for p in C1 if p not in Cinf]
        if lost:
            with_loss += 1
        for p in lost:
            lost_total += 1
            if _squarefree_mod(F, p):
                unramified_lost.append((F, p))
    check(lost_total > 0,
          "the sweep of %d polynomials finds %d covered-but-excluded primes "
          "in %d of them" % (len(sweep), lost_total, with_loss))
    check(not unramified_lost,
          "every one of them is ramified, i.e. F mod p has a repeated root",
          "unramified: %s" % unramified_lost[:3])

    # --- [5] cycles: the two bounds meet ----------------------------------
    print()
    print("[5] The lower bound (cycles) meets the upper bound (fixed point)")
    gaps = 0
    for F in sweep:
        C1 = [p for p in small if has_root(F, p)]
        if not C1:
            continue
        adj, _ = digraph(F, C1)
        gaps += len(greatest_fixed_point(F, C1) - on_a_cycle(adj))
    check(gaps == 0,
          "no gap between the two bounds over %d polynomials x %d primes"
          % (len(sweep), len(small)), "gaps: %d" % gaps)

    print()
    print("[5b] Certificates, verified with full integers")
    for name, F, _d in CATALOGUE[:8]:
        C1 = [p for p in PRIMES_SMALL if has_root(F, p)]
        adj, _ = digraph(F, C1)
        cyc = on_a_cycle(adj)
        issued = 0
        for p in sorted(cyc):
            cert = certificate(F, cycle_through(adj, p))   # raises if false
            if cert:
                issued += 1
        check(issued == len(cyc) and issued > 0,
              "%-40s %d certificates, each a real n in S(f)" % (name, issued))

    # --- [6] a certificate spelled out ------------------------------------
    print()
    print("[6] One certificate, written out")
    C1 = [p for p in PRIMES_SMALL if has_root(PHI6, p)]
    adj, _ = digraph(PHI6, C1)
    cert = certificate(PHI6, cycle_through(adj, 13))
    n = 1
    for q, e in cert:
        n *= q ** e
    ok = all(phi6(q, e) % cert[(i + 1) % len(cert)][0] == 0
             for i, (q, e) in enumerate(cert))
    check(ok and 13 in [q for q, _ in cert],
          "13 lies on the cycle " + " -> ".join("%d^%d" % t for t in cert),
          "n = %d" % n)

    # --- [7] EXTERNAL control ---------------------------------------------
    print()
    print("[7] EXTERNAL control -- OEIS A175200, published independently")
    mine = S_of_f(sigma, A175200[-1], smallest_prime_factors(A175200[-1]))
    check(mine == A175200,
          "recomputing { n : rad(n) | sigma(n) } reproduces the %d published "
          "terms" % len(A175200),
          "" if mine == A175200 else "got %s" % mine[:12])

    # --- [8] the numbers printed on docs/ ---------------------------------
    print()
    print("[8] The live numbers on docs/ are the ones computed here")
    expected = {
        "into3": str(len(into3)),
        "into3_covered": "0",
        "s_phi6": str(len(s_phi6) - 1),
        "s_phi6_with3": "0",
        "control_sigmastar": str(len(good)),
        "phi6_smallest": str(s_phi6[1]),
        "densities": "12",
        "sweep_lost": str(lost_total),
    }
    for rel in ("docs/index.html", "docs/es/index.html"):
        path = os.path.join(ROOT, *rel.split("/"))
        if not os.path.exists(path):
            check(False, rel + " is missing")
            continue
        html = open(path, encoding="utf-8").read()
        facts = dict(re.findall(r'data-fact="([a-z_0-9]+)">([^<]+)<', html))
        wrong = [k for k, v in expected.items()
                 if facts.get(k, "").replace(",", "").replace(".", "") != v]
        absent = [k for k in expected if k not in facts]
        check(not wrong and not absent,
              "%s: %d live numbers agree" % (rel, len(expected)),
              (("wrong: %s " % wrong) if wrong else "") +
              (("missing: %s" % absent) if absent else ""))

    # --- [9] the figures still match the data -----------------------------
    print()
    print("[9] Every figure equals what its generator produces from today's data")
    try:
        sys.path.insert(0, os.path.join(ROOT, "src"))
        import figures                                      # noqa: E402
        built = figures.build()
    except Exception as err:                                # pragma: no cover
        check(False, "src/figures.py runs", repr(err))
        built = {}
    for name, text in built.items():
        path = os.path.join(ROOT, "docs", "figures", name)
        if not os.path.exists(path):
            check(False, "docs/figures/" + name + " is missing")
            continue
        on_disk = open(path, encoding="utf-8").read()
        check(on_disk == text, "docs/figures/" + name + " matches its generator",
              "" if on_disk == text else "regenerate with: python src/figures.py")

    # --- [10] section 6 of RESULT.md: the hypothesis that failed -----------
    print()
    print("[10] Section 6: the densities are recomputed and the rank "
          "correlations follow from the table")
    path = os.path.join(ROOT, "data", "counting.txt")
    if not os.path.exists(path):
        check(False, "data/counting.txt is missing",
              "regenerate with: python src/counting.py")
    else:
        import counting                                    # noqa: E402
        table, wrong = [], []
        for line in open(path, encoding="utf-8"):
            if line.startswith("#") or not line.strip():
                continue
            name, excl, arr, size, formed = line.rstrip("\n").split("\t")
            table.append((name, float(excl), float(arr), int(size),
                          formed == "yes"))
        by_name = {n: (F, f, formed) for n, F, f, formed in counting.FUNCTIONS}
        for name, excl, arr, _size, formed in table:
            F = by_name[name][0]
            got_e, got_a = counting.densities(F)
            if abs(got_e - excl) > 5e-4 or abs(got_a - arr) > 5e-4:
                wrong.append((name, got_e, excl, got_a, arr))
        check(len(table) == len(counting.FUNCTIONS) and not wrong,
              "every density in data/counting.txt is reproduced right now",
              "" if not wrong else "differs: %s" % wrong[:2])

        out = [(a, s) for _n, _e, a, s, formed in table if not formed]
        exc = [(e, s) for _n, e, _a, s, formed in table if not formed]
        r_arrow = counting.spearman([a for a, _ in out], [s for _, s in out])
        r_excl = counting.spearman([e for e, _ in exc], [s for _, s in exc])
        check(abs(r_arrow - 0.238) < 0.001 and abs(r_excl + 0.467) < 0.001,
              "out of sample: arrow %+.3f, excluded %+.3f -- the hypothesis "
              "that arrows govern |S(f)| is REFUTED" % (r_arrow, r_excl))
        check(abs(r_arrow) < 0.738 and abs(r_excl) < 0.738,
              "and neither reaches the 5%% critical value 0.738 at n = %d, so "
              "the counting question stays open" % len(out))
        sizes = {n: s for n, _e, _a, s, _f in table}
        check(sizes.get("Phi_3") == 95 and sizes.get("Phi_6") == 3,
              "the pair that formed the hypothesis: |S(Phi_3)| = 95 against "
              "|S(Phi_6)| = 3, with the same covered set")

    print()
    if FAILURES:
        print("FAILED %d:" % len(FAILURES))
        for f in FAILURES:
            print("  -", f)
        return 1
    print("ALL CHECKS PASS")
    return 0


# ---------------------------------------------------------------------------
def _is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _fac(n, spf):
    out = []
    while n > 1:
        p = spf[n]
        a = 0
        while n % p == 0:
            n //= p
            a += 1
        out.append((p, a))
    return out


def _squarefree_mod(F, p):
    """True when F mod p has no repeated root: p is UNRAMIFIED for F."""
    f = _norm(F, p)
    if len(f) < len(F):
        return False                       # p divides the leading coefficient
    if len(f) <= 1:
        return False
    d = len(f) - 1
    df = _norm([(d - i) * c % p for i, c in enumerate(f)][:-1], p)
    if not df:
        return False
    return len(_gcd(f, df, p)) <= 1


def _sweep_polynomials():
    """Monic F with F(0) = +-1, degrees 2..4, coefficients in [-2, 2]."""
    out, seen = [], set()
    for g in range(2, 5):
        for mid in product(*[range(-2, 3)] * (g - 1)):
            for c0 in (1, -1):
                F = tuple([1] + list(mid) + [c0])
                if F not in seen:
                    seen.add(F)
                    out.append(list(F))
    return out


if __name__ == "__main__":
    sys.exit(main())
