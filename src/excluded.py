#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Which primes divide an element of S(f) = { n : rad(n) | f(n) }.

Standard library only. No dependencies.

The setting.  f is multiplicative and *local*: p does not divide f(p^a) for any
a >= 1.  Then n is in S(f) exactly when every prime of n is divided by f(q^b)
for some *other* prime power q^b exactly dividing n.  Reading that as a digraph
on the primes of n -- an arrow q -> p when p | f(q^b) -- membership in S(f) says
every vertex has an incoming arrow.

We work with f of *polynomial type*: f(q^e) = F(q^e) for a fixed F in Z[x].
The condition F(0) = +-1 IS locality, since F(p^a) = F(0) mod p.

What this file computes:

  has_root(F, p)        the criterion: p has an incoming arrow in the global
                        digraph iff F has a root mod p
  root_orders(F, p)     the orders of those roots; the arrow q -> p exists iff
                        one of them divides ord_p(q)
  cycle_through(...)    a directed cycle, i.e. a *certificate* that p really
                        does divide an element of S(f)
  greatest_fixed_point  the primes that survive iterating "has an incoming
                        arrow from a surviving prime"
"""
from __future__ import annotations

import random

# ---------------------------------------------------------------------------
# Integers
# ---------------------------------------------------------------------------


def sieve(n):
    b = bytearray([1]) * (n + 1)
    b[0:2] = b"\0\0"
    for i in range(2, int(n ** 0.5) + 1):
        if b[i]:
            b[i * i::i] = bytearray(len(b[i * i::i]))
    return [i for i in range(n + 1) if b[i]]


def smallest_prime_factors(n):
    spf = list(range(n + 1))
    i = 2
    while i * i <= n:
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    return spf


def factor(n, spf=None):
    """[(p, a), ...] for n >= 2."""
    out = []
    if spf is not None and n < len(spf):
        while n > 1:
            p = spf[n]
            a = 0
            while n % p == 0:
                n //= p
                a += 1
            out.append((p, a))
        return out
    d = 2
    while d * d <= n:
        if n % d == 0:
            a = 0
            while n % d == 0:
                n //= d
                a += 1
            out.append((d, a))
        d += 1 if d == 2 else 2
    if n > 1:
        out.append((n, 1))
    return out


_ORDER_CACHE = {}


def prime_divisors(n):
    if n in _ORDER_CACHE:
        return _ORDER_CACHE[n]
    out = [p for p, _ in factor(n)]
    _ORDER_CACHE[n] = out
    return out


def mult_order(a, p):
    """ord_p(a), with p prime and p not dividing a."""
    a %= p
    if a == 0:
        return 0
    d = p - 1
    for q in prime_divisors(p - 1):
        while d % q == 0 and pow(a, d // q, p) == 1:
            d //= q
    return d


# ---------------------------------------------------------------------------
# Polynomials over F_p.  Coefficients run from HIGHEST to LOWEST degree.
# ---------------------------------------------------------------------------


def _norm(a, p):
    a = [c % p for c in a]
    i = 0
    while i < len(a) and a[i] == 0:
        i += 1
    return a[i:]


def _mul(a, b, p):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] = (r[i + j] + x * y) % p
    return _norm(r, p)


def _sub(a, b, p):
    n = max(len(a), len(b))
    a = [0] * (n - len(a)) + list(a)
    b = [0] * (n - len(b)) + list(b)
    return _norm([(x - y) % p for x, y in zip(a, b)], p)


def _divmod(a, b, p):
    """Quotient and remainder of a by b over F_p.

    The quotient coefficient is written at its POSITION rather than appended:
    a subtraction can drop the degree of the remainder by more than one, and
    the skipped positions are genuine zero coefficients of the quotient.
    Appending instead shifts the whole quotient and returns nonsense -- and it
    goes unnoticed, because gcd only ever looks at remainders.
    """
    a = _norm(a, p)
    b = _norm(b, p)
    if not b:
        raise ZeroDivisionError("division by the zero polynomial")
    if len(a) < len(b):
        return [], a
    inv = pow(b[0], p - 2, p)
    q = [0] * (len(a) - len(b) + 1)
    rem = a
    while rem and len(rem) >= len(b):
        shift = len(rem) - len(b)
        c = (rem[0] * inv) % p
        q[len(q) - 1 - shift] = c
        rem = _sub(rem, [(c * t) % p for t in b] + [0] * shift, p)
    return _norm(q, p), rem


def _gcd(a, b, p):
    a, b = _norm(a, p), _norm(b, p)
    while b:
        a, b = b, _divmod(a, b, p)[1]
    if a:
        inv = pow(a[0], p - 2, p)
        a = [(c * inv) % p for c in a]
    return a


def _powmod(base, e, m, p):
    r = [1]
    base = _divmod(base, m, p)[1]
    while e:
        if e & 1:
            r = _divmod(_mul(r, base, p), m, p)[1]
        base = _divmod(_mul(base, base, p), m, p)[1]
        e >>= 1
    return r


def _squarefree_part(f, p):
    n = len(f) - 1
    df = _norm([(n - i) * c % p for i, c in enumerate(f)][:-1], p)
    if not df:
        return f
    g = _gcd(f, df, p)
    if len(g) <= 1:
        return f
    return _divmod(f, g, p)[0]


def evaluate(F, x):
    v = 0
    for c in F:
        v = v * x + c
    return v


BRUTE_BELOW = 500


def roots(F, p, tries=80):
    """Every distinct root of F in F_p, sorted.

    For p above the brute-force threshold: x^p mod F by repeated squaring,
    gcd(x^p - x, F) -- whose roots are exactly the roots of F in F_p -- and
    Cantor-Zassenhaus to split it.
    """
    f = _norm(F, p)
    if not f:
        return list(range(p))
    if len(f) == 1:
        return []
    if p <= BRUTE_BELOW:
        return [a for a in range(p) if evaluate(f, a) % p == 0]
    g = _gcd(_sub(_powmod([1, 0], p, f, p), [1, 0], p), f, p)
    if len(g) <= 1:
        return []
    out = []
    _split(_squarefree_part(g, p), p, out, tries)
    return sorted(set(out))


def _split(g, p, out, tries):
    d = len(g) - 1
    if d <= 0:
        return
    if d == 1:
        out.append((-g[1] * pow(g[0], p - 2, p)) % p)
        return
    for _ in range(tries):
        a = random.randrange(p)
        h = _sub(_powmod([1, a], (p - 1) // 2, g, p), [1], p)
        f1 = _gcd(h, g, p)
        if 0 < len(f1) - 1 < d:
            _split(f1, p, out, tries)
            _split(_divmod(g, f1, p)[0], p, out, tries)
            return
    raise RuntimeError("Cantor-Zassenhaus failed on degree %d mod %d" % (d, p))


def has_root(F, p):
    """THE CRITERION: p has an incoming arrow in the digraph of f."""
    f = _norm(F, p)
    if not f:
        return True
    if len(f) == 1:
        return False
    if p <= BRUTE_BELOW:
        return any(evaluate(f, a) % p == 0 for a in range(p))
    return len(_gcd(_sub(_powmod([1, 0], p, f, p), [1, 0], p), f, p)) > 1


def count_roots(F, p):
    return len(roots(F, p))


# ---------------------------------------------------------------------------
# The global covering digraph
# ---------------------------------------------------------------------------


def root_orders(F, p, rs=None):
    """{ ord_p(r) : r a nonzero root of F mod p }.

    This is all that p contributes.  Because r^d = 1 iff ord_p(r) | d,

        q -> p   iff   some ord_p(r) divides ord_p(q)

    and the cyclotomic case falls out: every root of Phi_m mod p has order m,
    so the condition reads m | ord_p(q), and since ord_p(q) | p-1, m | p-1.
    """
    if rs is None:
        rs = roots(F, p)
    return set(mult_order(r, p) for r in rs if r)


def arrow(F, q, p, orders=None):
    """Is there an e >= 1 with p | F(q^e)?  No discrete logarithm needed."""
    if q == p or q % p == 0:
        return False
    if orders is None:
        orders = root_orders(F, p)
    if not orders:
        return False
    d = mult_order(q, p)
    return any(d % o == 0 for o in orders)


def exponent(F, q, p, rs=None):
    """The least e >= 1 with p | F(q^e), or None.  Only for exhibiting."""
    if q == p or q % p == 0:
        return None
    if rs is None:
        rs = roots(F, p)
    R = set(r for r in rs if r)
    if not R:
        return None
    v = q % p
    for e in range(1, mult_order(q, p) + 1):
        if v in R:
            return e
        v = (v * (q % p)) % p
    return None


def digraph(F, primes):
    """Adjacency lists of the covering digraph restricted to `primes`."""
    rs = {p: roots(F, p) for p in primes}
    orders = {p: root_orders(F, p, rs[p]) for p in primes}
    adj = {}
    for q in primes:
        adj[q] = [p for p in primes
                  if p != q and orders[p] and arrow(F, q, p, orders[p])]
    return adj, rs


def _sccs(adj):
    index, low, stack, onstack, out = {}, {}, [], set(), []
    counter = [0]
    for root in adj:
        if root in index:
            continue
        work = [(root, iter(adj[root]))]
        index[root] = low[root] = counter[0]
        counter[0] += 1
        stack.append(root)
        onstack.add(root)
        while work:
            v, it = work[-1]
            advanced = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter[0]
                    counter[0] += 1
                    stack.append(w)
                    onstack.add(w)
                    work.append((w, iter(adj[w])))
                    advanced = True
                    break
                if w in onstack:
                    low[v] = min(low[v], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    onstack.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                out.append(comp)
    return out


def on_a_cycle(adj):
    """Vertices lying on some directed cycle."""
    inside = set()
    for comp in _sccs(adj):
        if len(comp) > 1:
            inside |= set(comp)
        elif comp[0] in adj[comp[0]]:
            inside.add(comp[0])
    return inside


def cycle_through(adj, p):
    """A shortest directed cycle p -> ... -> p, as [p, ...], or None."""
    if p not in adj:
        return None
    parent, seen, front = {}, {p}, [p]
    while front:
        nxt = []
        for v in front:
            for w in adj[v]:
                if w == p:
                    path = [v]
                    while path[-1] != p:
                        path.append(parent[path[-1]])
                    path.reverse()
                    return path
                if w not in seen:
                    seen.add(w)
                    parent[w] = v
                    nxt.append(w)
        front = nxt
    return None


def certificate(F, cycle):
    """[(p_i, e_i)] with p_{i+1} | F(p_i^{e_i}); i.e. prod p_i^{e_i} is in S(f).

    Verified here with FULL integers, not modulo anything.  Raises if false.
    """
    k = len(cycle)
    out = []
    for i, q in enumerate(cycle):
        p = cycle[(i + 1) % k]
        e = exponent(F, q, p)
        if e is None:
            return None
        out.append((q, e))
    for i, (q, e) in enumerate(out):
        p = cycle[(i + 1) % k]
        if evaluate(F, q ** e) % p != 0:
            raise AssertionError("false certificate: %d does not divide F(%d^%d)"
                                 % (p, q, e))
    return out


def greatest_fixed_point(F, primes):
    """Iterate C -> { p in C : some q in C has q -> p } to its fixed point."""
    orders = {p: root_orders(F, p) for p in primes}
    C = [p for p in primes if orders[p]]
    while True:
        cur = set(C)
        nxt = [p for p in C
               if any(q != p and arrow(F, q, p, orders[p]) for q in cur)]
        if len(nxt) == len(C):
            return set(C)
        C = nxt


# ---------------------------------------------------------------------------
# S(f) computed as plain integers -- no digraph, no criterion
# ---------------------------------------------------------------------------


def S_of_f(f_value, N, spf=None):
    """Every n <= N with rad(n) | f(n), by factoring and multiplying out.

    `f_value(q, e)` returns f(q^e) as an integer.  n = 1 is included, matching
    the OEIS convention for A175200.
    """
    if spf is None:
        spf = smallest_prime_factors(N)
    out = [1]
    for n in range(2, N + 1):
        fac = factor(n, spf)
        prod = 1
        for q, a in fac:
            prod *= f_value(q, a)
        if all(prod % q == 0 for q, _ in fac):
            out.append(n)
    return out
