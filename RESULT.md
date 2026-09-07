# Covered but excluded primes — full statement

<!-- hallazgo:que -->
## What was found

For the multiplicative `f` with `f(q^e) = q^(2e) − q^e + 1`, the prime **3** has
incoming arrows in the covering digraph of `f` and yet divides **no** element of
`S(f) = { n : rad(n) | f(n) }`. An incoming arrow is necessary but not
sufficient.

<!-- hallazgo:enunciado -->
## The statements

`f` multiplicative with `f(q^e) = F(q^e)`, `F ∈ Z[x]`, `F(0) = ±1`.
`q → p` means `p | f(q^e)` for some `e ≥ 1`.
`D(f) = { p : p | n for some n ∈ S(f) }`.

> **Theorem 1.** `q → p` iff some `ord_p(r)` divides `ord_p(q)`, `r` over the
> roots of `F` mod `p`. Hence `p` has an incoming arrow iff `F` has a root
> mod `p`.
>
> **Theorem 2.** The density of primes with no incoming arrow equals the
> proportion of fixed-point-free elements of `Gal(F)` on the roots of `F`.
> *(Frobenius 1896, applied here; classical, not claimed.)*
>
> **Theorem 3.** For `F = x² − x + 1`, `3` has an incoming arrow and `3 ∉ D(f)`.
>
> **Theorem 4.** If `p` is unramified in the splitting field of `F` and `F` has
> a root mod `p`, then some prime `q` with a root of `F` mod `q` satisfies
> `q → p`. Hence `C₁ \ C_∞` consists of ramified primes only.
>
> **Theorem 5.** `{ p on a directed cycle of D_f } ⊆ D(f) ⊆ C_∞`, the left
> inclusion constructive with a finite certificate.

<!-- hallazgo:ejemplo -->
## The smallest case, worked

| | |
|---|---|
| `F mod 3` | `(x+1)²`, only root `2` |
| `ord_3(2)` | `2` |
| `q → 3` requires | `q ≡ 2 (mod 3)` |
| `p ≠ 3` covered iff | `p ≡ 1 (mod 6)` |
| primes `< 8000` with `q → 3` | **511** |
| of those, covered | **0** |
| `S(f)` below 400000 | `100009`, `175273`, `274939` |
| divisible by 3 | **0** |
| positive control on `q^e + 1` | **261** of **344** |

<!-- hallazgo:prueba -->
## Why it is true

Every `n ∈ S(f)` uses only primes covered *within `n`*. Mod 3, `x² − x + 1` is
`(x+1)²`, root `2` of order `2`, so `q → 3` forces `q ≡ 2 (mod 3)`; a covered
`p ≠ 3` needs `6 | p − 1`, so `p ≡ 1 (mod 3)`. Disjoint classes, so no covered
prime can cover 3, so 3 cannot occur in any `n ∈ S(f)`.

<!-- hallazgo:comprobar -->
## Check it

```bash
python verify.py
```

One `PASS`/`FAIL` per check, exit 1 on any failure. Check `[7]` is external: it
recomputes `{ n : rad(n) | σ(n) }` and matches the 49 terms published as OEIS
A175200.

<!-- hallazgo:nodice -->
## What this does not claim

- The density statement (Theorem 2) is **classical** — Frobenius 1896. Only its
  application to `S(f)` is new here.
- The equality `D(f) = C_∞` is **not proved**; it is measured with zero gaps
  over 310 polynomials × 168 primes and stated as a conjecture.
- Nothing is claimed about `|S(f)(x)|`. A hypothesis about it was declared,
  tested out of sample and **refuted** (§6).
- Theorem 4 bounds *where* failures can occur; it does not say which ramified
  primes actually fail. Of the 310 polynomials swept, 14 fail somewhere.
- Nothing here is claimed for `σ`, `σ₂` or `φ*`: those have no excluded primes.

---

## 1. Setting

`f` is multiplicative and **local**: `p ∤ f(p^a)` for every prime `p` and every
`a ≥ 1`. For such `f`,

    n ∈ S(f)   ⟺   for every p | n there is q | n, q ≠ p, with p | f(q^{v_q(n)})

so `n` becomes a digraph on its own primes, and membership says every vertex has
an incoming arrow.

We take `f(q^e) = F(q^e)` for a fixed `F ∈ Z[x]`. Since `F(p^a) ≡ F(0) (mod p)`,
locality is **exactly** `F(0) = ±1`; and then `0` is never a root mod `p`, so
"root" and "nonzero root" coincide.

Write `D_f` for the digraph on **all** primes, `C₁` for the primes with an
incoming arrow, and

    C_0 = all primes,   C_{i+1} = { p : q → p for some q ∈ C_i },   C_∞ = ⋂ C_i.

## 2. Theorem 1, with proof

**(a)** `p | F(q^e)` says `q^e` is a root of `F` mod `p`. The subgroup `⟨q⟩` of
`F_p^*` is cyclic of order `d = ord_p(q)`, and in a cyclic group that subgroup
is exactly `{ x : x^d = 1 }`; a root `r` lies in it iff `ord_p(r) | d`.

**(b)** If an arrow exists, `q^e mod p` is a nonzero root. Conversely if `r` is
a root, Dirichlet gives primes `q ≡ r (mod p)`, and `e = 1` works. ∎

**Cyclotomic case.** Every root of `Φ_m` mod `p` has order `m`, so (a) reads
`m | ord_p(q)`; and `ord_p(q) | p − 1` gives `m | p − 1`. Verified in
`verify.py [1c]` for `m = 3, 4, 5, 6, 8` over all primes below 3000, excluding
the primes dividing `m`, which are the ramified ones.

**Controls** (`verify.py [1]`, `[1b]`), on 13 polynomials over the 430 primes
below 3000:

| control | what it does | shares reasoning with the criterion? |
|---|---|---|
| exhaustive | scans **every** residue `a = 1 … p−1` for `F(a) ≡ 0` | no |
| constructive | exhibits a prime `q` and `e` with `p \| F(q^e)`, full integers | no |

Result: **0 discrepancies** in both, for all 13.

## 3. Theorem 2, and what is classical

By Theorem 1(b) the covered primes are those for which `F` has a root mod `p`.
The density of that set is the **Frobenius density theorem**: the density of
primes with a given decomposition type is the proportion of elements of the
Galois group with that cycle type, and "has a root" is "has a fixed point".

**This is classical and is not claimed here.** References: G. Frobenius (1896);
B. Sury, *Resonance* **8**(12) (2003) 33–41; P. Stevenhagen and H. W. Lenstra,
*Math. Intelligencer* **18** (1996) 26–37.

Measured over the 3245 primes below 30000 (`verify.py [2]`):

| `F` | group | predicted | measured |
|---|---|---|---|
| `x+1` | trivial | `0` | 0.00000 |
| `Φ₄ = x²+1` | `C₂` | `1/2` | 0.50324 |
| `Φ₃` | `C₂` | `1/2` | 0.50354 |
| `Φ₆ = x²−x+1` | `C₂` | `1/2` | 0.50354 |
| `x²−x−1` | `C₂` | `1/2` | 0.50354 |
| `Φ₃·Φ₄` | `C₂×C₂`, two orbits | `1/4` | 0.25085 |
| `x³−x−1` | `S₃` | `1/3` | 0.33559 |
| `x⁴−x−1` | `S₄` | `3/8` | 0.37935 |
| `x⁵−x−1` | `S₅` | `11/30` | 0.36364 |
| `x³+x²−2x−1` (periods of `ζ₇`) | `C₃` | `2/3` | 0.66872 |
| `Φ₅` | `C₄` | `3/4` | 0.75069 |
| `Φ₈ = x⁴+1` | `C₂×C₂` | `3/4` | 0.75439 |
| `x⁵+x⁴−4x³−3x²+3x+1` (periods of `ζ₁₁`) | `C₅` | `4/5` | 0.80031 |

Every row within `3 SE`. **Twelve distinct values**, three of which — `2/3`,
`4/5` and the `5/6` of the `ζ₁₃` periods — are not of the form `1 − 1/φ(m)`, so
no cyclotomic `Φ_m` produces them.

**A stronger form of the same check** (`verify.py [2b]`): not just the density
of "no root", but the density of **every** root count, against the fixed-point
distribution of the group.

| `F` | root count → predicted density | worst deviation |
|---|---|---|
| `x³−x−1` (`S₃`) | `0 → 1/3`, `1 → 1/2`, `3 → 1/6` | 0.65 SE |
| `x⁴−x−1` (`S₄`) | `0 → 3/8`, `1 → 1/3`, `2 → 1/4`, `4 → 1/24` | 1.42 SE |

**On the standard error.** The unit of evidence here is the prime: each prime
contributes one bit and the statistic is a proportion over primes, so the naive
binomial error is the right one. That is not so when the statistic ranges over
pairs or triples built from the same primes.

**Two corollaries.** By Jordan's theorem a transitive group of degree `> 1`
always contains a fixed-point-free element, so an **irreducible** `F` of degree
`≥ 2` always excludes a positive density of primes. And the density is always
`< 1`, since the identity fixes every root, so it is at most `1 − 1/|G|`.

**Zero density without a rational root is possible.** The classical intersective
polynomial `(x²−2)(x²−3)(x²−6)` has `F(0) = −36` and breaks locality; its
reciprocal `(2x²−1)(3x²−1)(6x²−1)` is local but loses the prime 3. The exact
condition for `F = (a₁x²−1)(a₂x²−1)(a₁a₂x²−1)` is that `(a₂|p) = 1` at `p | a₁`
and `(a₁|p) = 1` at `p | a₂`; away from `a₁a₂` the three Legendre symbols
multiply to `1` and cannot all be `−1`. With `a₁ = 2`, `a₂ = 17` — where
`17 ≡ 1 (mod 8)` gives `(2|17) = 1` — the polynomial

    F(x) = (2x² − 1)(17x² − 1)(34x² − 1)

has `F(0) = −1`, **no rational root**, and **no excluded prime** among the 5133
primes below 50000.

## 4. Theorem 3, with two independent controls

The proof is in the front matter. Two controls, neither using the criterion.

**The mechanism, on the integers** (`verify.py [3]`). `q → 3` is decided by
computing `f(q^e)` as an integer and dividing; "`q` is covered" is decided by
scanning **every** residue class mod `q`.

| `f` | `P` | primes `q → P` | of those, covered |
|---|---|---|---|
| `q^(2e) − q^e + 1` | 3 | **511** | **0** |
| *control* `q^e + 1` | 3 | 511 | **511** |

**`S(f)` as plain integers** (`verify.py [3b]`), sieving every `n ≤ 400000`,
factoring, applying `f`, multiplying and dividing:

| `f` | `\|S(f)\|` above 1 | divisible by 3 |
|---|---|---|
| `q^(2e) − q^e + 1` | 3 | **0** |
| *control* `q^e + 1` | 343 | **261** |

The three elements are `100009 = 7²·13·157`, `175273 = 7⁴·73` and
`274939 = 7²·31·181`; their six distinct primes `7, 13, 31, 73, 157, 181` are
all `≡ 1 (mod 6)`, i.e. all covered.

## 5. Theorems 4 and 5

**Theorem 4.** Let `r` be a root of `F` mod `p`; every prime `q ≡ r (mod p)`
satisfies `q → p`. Since `p` is unramified in the splitting field `L`, the field
`L ∩ Q(ζ_p)` is abelian, ramified only at `p` because it sits inside `Q(ζ_p)`,
and unramified at `p` because it sits inside `L`; being unramified everywhere it
is `Q` by Minkowski. Hence
`Gal(L·Q(ζ_p)/Q) = Gal(L/Q) × Gal(Q(ζ_p)/Q)`, and Chebotarev gives infinitely
many primes `q` with Frobenius `(1, r)`: they split completely in `L`, so `F`
has all its roots mod `q` and `q` is covered, and `q ≡ r (mod p)`. ∎

Iterating, such a `p` survives every step, so `C₁ \ C_∞` contains only primes
ramified in `L`, i.e. primes where `F mod p` has a repeated root — finitely many
for each `F`.

**Measured** (`verify.py [4]`), sweeping the 310 monic `F` of degrees 2 to 4
with coefficients in `[−2,2]` and `F(0) = ±1`, against the 168 primes below
1000:

| | |
|---|---|
| polynomials losing at least one prime to the iteration | **14** |
| covered-but-excluded primes found | **14** |
| of those, **unramified** | **0** |

**Theorem 5.** If `p₁ → p₂ → … → p_k → p₁` is a directed cycle, each vertex uses
a single outgoing arrow, so its exponent solves a single congruence and always
exists; `n = ∏ p_i^{e_i}` then has every vertex covered, so `n ∈ S(f)`.
Conversely, if `p | n ∈ S(f)` then `p` has an incoming arrow from another prime
of `n`, which has its own, and so on; every prime of `n` survives every step of
the iteration, so it lies in `C_∞`. ∎

The left inclusion is constructive. `verify.py [6]` writes one out: `13 → 19`
and `19 → 13` for `F = x² − x + 1`, giving

    n = 13³ · 19² = 793117,   19 | f(13³) = 4824613,   13 | f(19²) = 129961

which a reader checks with two divisions.

**The two bounds met everywhere they were compared** (`verify.py [5]`): over the
same 310 polynomials and 168 primes, `C_∞` equals the set of primes on a cycle,
with **zero** gaps. That is the evidence for `D(f) = C_∞`, and it is a
measurement.

What is missing for a proof: Theorem 4 produces a covered `q` with `q → p`, but
closing the cycle needs `p → q`, and the out-neighbours of `p` are the prime
divisors of the values `F(p^e)`, which cannot be prescribed in a congruence
class. That is the same obstacle as asking for primitive prime divisors of a
sequence like `2^k − 1` inside an arithmetic progression.

## 6. A hypothesis of our own that failed

`Φ₃` and `Φ₆` have essentially the **same** covered set — the primes `≡ 1 (mod
6)`, excluded density 0.511 for both — and yet `|S(Φ₃)| = 95` against
`|S(Φ₆)| = 3` below 400000. That suggested:

> **H.** What governs `|S(f)(x)|` is the **arrow density** of the digraph, not
> the density of covered vertices.

It fits the pair that produced it — 0.7531 against 0.4903 — which is why that
pair cannot test it. Out of sample, on eight functions that did not form it:

| predictor | Spearman with `\|S(f)\|` |
|---|---|
| arrow density | **+0.238** |
| excluded density | **−0.467** |

The arrow density is the **weaker** of the two. And with `n = 8` the 5 % critical
value of Spearman is `0.738`, so **neither is distinguishable from noise**. The
hypothesis is refuted and the counting question is left open. The counterexample
is in the same table: the cyclic cubic has arrow density 0.7546 and
`|S(f)| = 3`.

## 7. Functions that are not of polynomial type

`σ`, `σ₂` and `φ*` are not `F(q^e)` — their degree depends on `e`. Over the 78
primes below 400, computing `f(q^e)` as an integer: all three have **zero**
forbidden arrows, every prime is covered and lies on a cycle, so `D(f)` is all
of the primes. `σ**` has 109 forbidden arrows and still covers every prime.

If `f` is **not** local, i.e. `F(0) ≠ ±1`, loops appear: `p | f(p^a)` exactly
when `p | F(0)`, and such primes are in `D(f)` by themselves. Theorem 1(b) then
holds verbatim reading "root" without excluding `0`.

## 8. Reproducing

```bash
python verify.py            # every claim above, seconds, no dependencies
python src/figures.py       # regenerates docs/figures/*.svg from the data
```
