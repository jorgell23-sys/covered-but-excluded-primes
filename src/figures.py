#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds docs/figures/*.svg from the real data.  Standard library only.

    python src/figures.py

SVG and not PNG so the pictures can be checked against the numbers: verify.py
regenerates them and compares, and a figure that drifts from the data fails the
build.  Every generator returns a string, so nothing is written twice.
"""
from __future__ import annotations

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from excluded import (arrow, certificate, cycle_through, digraph,  # noqa: E402
                      has_root, sieve)

random.seed(20260906)
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "figures")

STYLE = """<style>
  :root{--ink:#16202b;--soft:#5a6a7a;--line:#c3ced9;--bg:#ffffff;
        --good:#1d7a53;--bad:#b3402a;--mid:#2f6ea8}
  @media (prefers-color-scheme: dark){
   :root{--ink:#e6edf4;--soft:#9fb0c0;--line:#3d4a58;--bg:#0f1720;
         --good:#4fbf8b;--bad:#e0755c;--mid:#67a6dd}}
  text{font-family:ui-sans-serif,system-ui,Segoe UI,Helvetica,Arial,sans-serif}
  .t{fill:var(--ink)} .s{fill:var(--soft)} .ln{stroke:var(--line);fill:none}
</style>"""


def _svg(w, h, body, title):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'width="100%%" role="img" aria-label="%s">%s\n<rect width="%d" '
            'height="%d" fill="var(--bg)"/>\n%s\n</svg>\n'
            % (w, h, title, STYLE, w, h, body))


# ---------------------------------------------------------------------------
def fig_disjoint():
    """The two sets that never meet: who can cover 3, and who is covered."""
    P = [p for p in sieve(120) if p > 3]
    covered = [p for p in P if p % 6 == 1]
    pointers = [p for p in P if p % 3 == 2]
    w, h = 720, 330
    b = ['<text x="20" y="30" class="t" font-size="17" font-weight="600">'
         'f(q^e) = q^2e - q^e + 1 : the prime 3 is covered and divides nothing'
         '</text>']
    b.append('<text x="20" y="58" class="s" font-size="13">'
             'primes that CAN point at 3 (q = 2 mod 3)</text>')
    x = 20
    for p in pointers[:14]:
        b.append('<rect x="%d" y="70" width="40" height="28" rx="6" '
                 'fill="none" stroke="var(--bad)"/>'
                 '<text x="%d" y="89" class="t" font-size="13" '
                 'text-anchor="middle">%d</text>' % (x, x + 20, p))
        x += 46
    b.append('<text x="20" y="132" class="s" font-size="13">'
             'primes that are themselves covered (p = 1 mod 6)</text>')
    x = 20
    for p in covered[:14]:
        b.append('<rect x="%d" y="144" width="40" height="28" rx="6" '
                 'fill="none" stroke="var(--good)"/>'
                 '<text x="%d" y="163" class="t" font-size="13" '
                 'text-anchor="middle">%d</text>' % (x, x + 20, p))
        x += 46
    b.append('<line x1="20" y1="200" x2="700" y2="200" class="ln" '
             'stroke-dasharray="4 4"/>')
    b.append('<text x="20" y="228" class="t" font-size="14">'
             'The two rows share no prime. Every arrow into 3 starts in the '
             'top row,</text>')
    b.append('<text x="20" y="250" class="t" font-size="14">'
             'and no number of S(f) may contain a prime from the top row.'
             '</text>')
    b.append('<text x="20" y="286" class="s" font-size="13">'
             'so 3 has arrows coming in, and still divides no element of '
             'S(f) = { n : rad(n) | f(n) }.</text>')
    b.append('<text x="20" y="310" class="s" font-size="12">'
             '3 is the prime where x^2 - x + 1 = (x+1)^2 mod 3 has a repeated '
             'root: the ramified prime.</text>')
    return _svg(w, h, "\n".join(b), "The two disjoint sets of primes")


# ---------------------------------------------------------------------------
DENSITY_ROWS = [
    ("x+1", 0.0), ("Phi_3", 1 / 2), ("Phi_4", 1 / 2), ("Phi_6", 1 / 2),
    ("Phi_3Phi_4", 1 / 4), ("x^3-x-1  S_3", 1 / 3), ("x^4-x-1  S_4", 3 / 8),
    ("x^5-x-1  S_5", 11 / 30), ("x^3+x^2-2x-1  C_3", 2 / 3),
    ("Phi_5", 3 / 4), ("Phi_8", 3 / 4), ("C_5 of zeta_11", 4 / 5),
]
DENSITY_F = {
    "x+1": [1, 1], "Phi_3": [1, 1, 1], "Phi_4": [1, 0, 1], "Phi_6": [1, -1, 1],
    "Phi_3Phi_4": [1, 1, 2, 1, 1], "x^3-x-1  S_3": [1, 0, -1, -1],
    "x^4-x-1  S_4": [1, 0, 0, -1, -1], "x^5-x-1  S_5": [1, 0, 0, 0, -1, -1],
    "x^3+x^2-2x-1  C_3": [1, 1, -2, -1], "Phi_5": [1, 1, 1, 1, 1],
    "Phi_8": [1, 0, 0, 0, 1], "C_5 of zeta_11": [1, 1, -4, -3, 3, 1],
}


def fig_densities():
    """Predicted (Galois) against measured, one bar pair per F."""
    primes = sieve(30000)
    n = len(primes)
    rows = []
    for name, pred in DENSITY_ROWS:
        F = DENSITY_F[name]
        got = sum(1 for p in primes if not has_root(F, p)) / n
        rows.append((name, pred, got))
    w = 760
    top, row_h = 96, 34
    h = top + row_h * len(rows) + 46
    x0, bar_w = 250, 420
    b = ['<text x="20" y="30" class="t" font-size="17" font-weight="600">'
         'Density of primes that divide no element of S(f)</text>',
         '<text x="20" y="54" class="s" font-size="13">'
         'bar = predicted from the Galois group of F (fixed-point-free share); '
         'tick = measured over %d primes</text>' % n,
         '<text x="20" y="74" class="s" font-size="13">'
         'twelve different values, so 1/2 was a property of two functions and '
         'not of the problem</text>']
    y = top
    for name, pred, got in rows:
        b.append('<text x="20" y="%d" class="t" font-size="13">%s</text>'
                 % (y + 17, name))
        b.append('<rect x="%d" y="%d" width="%d" height="20" rx="4" '
                 'fill="none" class="ln"/>' % (x0, y + 3, bar_w))
        if pred > 0:
            b.append('<rect x="%d" y="%d" width="%.1f" height="20" rx="4" '
                     'fill="var(--mid)" opacity="0.45"/>'
                     % (x0, y + 3, bar_w * pred))
        tx = x0 + bar_w * got
        b.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" '
                 'stroke="var(--ink)" stroke-width="2"/>'
                 % (tx, y + 1, tx, y + 25))
        b.append('<text x="%d" y="%d" class="s" font-size="12">%.4f</text>'
                 % (x0 + bar_w + 12, y + 17, got))
        y += row_h
    b.append('<text x="%d" y="%d" class="s" font-size="12">0</text>'
             % (x0, h - 18))
    b.append('<text x="%d" y="%d" class="s" font-size="12">1</text>'
             % (x0 + bar_w - 6, h - 18))
    return _svg(w, h, "\n".join(b), "Predicted against measured densities")


# ---------------------------------------------------------------------------
def fig_certificate():
    """A cycle is a certificate: it IS a number of S(f), written out."""
    F = [1, -1, 1]
    primes = [p for p in sieve(3000) if has_root(F, p)]
    adj, _ = digraph(F, primes)
    cert = certificate(F, cycle_through(adj, 13))
    n = 1
    for q, e in cert:
        n *= q ** e
    w, h = 720, 260
    b = ['<text x="20" y="30" class="t" font-size="17" font-weight="600">'
         'A cycle is a certificate</text>',
         '<text x="20" y="56" class="s" font-size="13">'
         'each arrow says the next prime divides f of the previous prime '
         'power; a third party checks it with %d divisions</text>' % len(cert)]
    cx = [180, 500]
    for i, (q, e) in enumerate(cert[:2]):
        b.append('<circle cx="%d" cy="130" r="52" fill="none" '
                 'stroke="var(--mid)" stroke-width="2"/>' % cx[i])
        b.append('<text x="%d" y="126" class="t" font-size="20" '
                 'text-anchor="middle">%d^%d</text>' % (cx[i], q, e))
        b.append('<text x="%d" y="148" class="s" font-size="12" '
                 'text-anchor="middle">= %d</text>' % (cx[i], q ** e))
    b.append('<path d="M 236 108 Q 340 66 444 108" class="ln" '
             'stroke-width="2" marker-end="url(#a)"/>')
    b.append('<path d="M 444 152 Q 340 194 236 152" class="ln" '
             'stroke-width="2" marker-end="url(#a)"/>')
    b.append('<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" '
             'markerWidth="7" markerHeight="7" orient="auto">'
             '<path d="M 0 0 L 10 5 L 0 10 z" fill="var(--line)"/>'
             '</marker></defs>')
    b.append('<text x="340" y="60" class="s" font-size="12" '
             'text-anchor="middle">%d divides f(%d^%d)</text>'
             % (cert[1][0], cert[0][0], cert[0][1]))
    b.append('<text x="340" y="212" class="s" font-size="12" '
             'text-anchor="middle">%d divides f(%d^%d)</text>'
             % (cert[0][0], cert[1][0], cert[1][1]))
    b.append('<text x="20" y="244" class="t" font-size="14">'
             'so n = %d^%d . %d^%d = %d is in S(f)</text>'
             % (cert[0][0], cert[0][1], cert[1][0], cert[1][1], n))
    return _svg(w, h, "\n".join(b), "A cycle as a certificate")


FIGURES = {
    "disjoint.svg": fig_disjoint,
    "densities.svg": fig_densities,
    "certificate.svg": fig_certificate,
}


def build():
    """Returns {filename: svg text}.  Nothing is written by this function."""
    return {name: fn() for name, fn in sorted(FIGURES.items())}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, text in build().items():
        # No coordinate may fall off the canvas: a label placed relative to the
        # tallest bar lands outside it, and the picture cannot depend on which
        # datum happens to be the maximum.
        assert "-" not in text.split("viewBox")[1][:20], name
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print("wrote docs/figures/" + name)


if __name__ == "__main__":
    main()
