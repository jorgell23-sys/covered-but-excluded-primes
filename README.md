# Covered but excluded primes

<!-- hallazgo:que -->
## What was found

For the multiplicative function `f` given on prime powers by
`f(q^e) = q^(2e) − q^e + 1`, the prime **3** has incoming arrows in the covering
digraph of `f` and nevertheless **divides no element at all** of
`S(f) = { n : rad(n) | f(n) }`. Having an incoming arrow is therefore
*necessary* but **not sufficient** for a prime to divide an element of `S(f)`.

<!-- hallazgo:enunciado -->
## The statements

Throughout, `f` is multiplicative with `f(q^e) = F(q^e)` for a fixed `F ∈ Z[x]`
with `F(0) = ±1` — which is exactly the condition `p ∤ f(p^a)`. Write `q → p`
when `p | f(q^e)` for some `e ≥ 1`.

> **Theorem 1 (criterion).** `q → p` holds iff some `ord_p(r)` divides
> `ord_p(q)`, with `r` running over the roots of `F` mod `p`. Consequently
> **`p` has an incoming arrow iff `F` has a root mod `p`.**

> **Theorem 2 (density).** The density of primes with no incoming arrow is the
> proportion of elements of `Gal(F)` acting on the roots of `F` with **no fixed
> point**. *This is the Frobenius density theorem (1896) applied to this
> object; the density statement is classical and is not claimed here.*

> **Theorem 3 (one step is not enough).** For `F = x² − x + 1`, the prime `3`
> has an incoming arrow and divides no element of `S(f)`.

> **Theorem 4 (where failures can live).** If `p` is unramified in the
> splitting field of `F` and `F` has a root mod `p`, then some prime `q` that
> itself has a root of `F` mod `q` satisfies `q → p`. Hence every failure of
> the kind in Theorem 3 occurs at a prime where `F mod p` has a repeated root —
> finitely many for each `F`.

<!-- hallazgo:ejemplo -->
## The smallest case, worked

`F = x² − x + 1`, i.e. `f(q^e) = q^(2e) − q^e + 1`.

| | |
|---|---|
| `F mod 3` | `x² − x + 1 ≡ (x+1)²`, whose only root is `2` |
| `ord_3(2)` | `2`, since `2 · 2 = 4 ≡ 1` |
| so `q → 3` requires | `2 \| ord_3(q)`, i.e. `q ≡ 2 (mod 3)` |
| `p ≠ 3` has a root of `F` iff | `6 \| p − 1`, i.e. `p ≡ 1 (mod 6)` |
| primes below 8000 with `q → 3` | **511** |
| of those, how many are covered | **0** |
| `S(f)` below 400000 | `100009 = 7²·13·157`, `175273 = 7⁴·73`, `274939 = 7²·31·181` |
| how many are divisible by 3 | **0** |
| positive control, same search on `f(q^e) = q^e + 1` | **261** elements divisible by 3, out of 344 |

<!-- hallazgo:prueba -->
## Why it is true

A number `n ∈ S(f)` is built only from primes that are themselves covered
*inside `n`*: every vertex of its digraph needs an incoming arrow from another
prime of `n`. Modulo 3 the polynomial `x² − x + 1` becomes `(x+1)²`, whose root
`2` has order `2`, so by Theorem 1 an arrow `q → 3` forces `q ≡ 2 (mod 3)`. But
a prime `p ≠ 3` has a root of `F` only when `6 | p − 1`, hence `p ≡ 1 (mod 3)`.
The two classes are disjoint, so every prime that could cover 3 is itself
uncovered and cannot appear in `n`. Therefore `3 ∤ n` for every `n ∈ S(f)`.

<!-- hallazgo:comprobar -->
## Check it yourself

No dependencies, standard library only:

```bash
git clone https://github.com/jorgell23-sys/covered-but-excluded-primes
cd covered-but-excluded-primes
python verify.py
```

It prints one `PASS`/`FAIL` line per check — **77** of them — and exits
non-zero if any fails.
Check `[3]` is the theorem above, `[4]` is the ramification bound over a sweep
of 310 polynomials, and check `[7]` is **external**: it recomputes
`{ n : rad(n) | σ(n) }` from scratch and compares it against the 49 terms
published independently as OEIS A175200.

<!-- hallazgo:nodice -->
## What this does not claim

- It does **not** claim the density statement of Theorem 2 as new. That is
  Frobenius (1896); what is new here is applying it to `S(f)` and reading the
  excluded primes off `F` alone.
- It does **not** prove that the two bounds in
  `{p on a cycle} ⊆ D(f) ⊆ C_∞` always coincide. They coincided in every case
  measured — 310 polynomials against the 168 primes below 1000, with zero gaps
  — but that is a measurement, recorded as a conjecture.
- It says **nothing** about how many elements `S(f)` has below `x`. A
  hypothesis about that was declared, tested out of sample and **refuted**; see
  RESULT.md.
- `σ`, `σ₂` and `φ*` have **no** excluded primes at all; the phenomenon needs a
  function whose profile forbids arrows.

---

## What is in here

| file | what it is |
|---|---|
| `RESULT.md` | the full statement, proofs, tables and limits |
| `PRIOR_ART.md` | what was searched, where, when, and the positive controls |
| `verify.py` | every claim, re-checked in seconds, no dependencies |
| `src/excluded.py` | the criterion, the digraph, the cycles, the certificates |
| `src/figures.py` | the figures, generated from the data |
| `data/` | the generated tables |
| `docs/` | an explanation from scratch, for a reader new to the subject |

The explanation for non-specialists is at
<https://jorgell23-sys.github.io/covered-but-excluded-primes/>
(and in Spanish at `/es/`).

## Citing

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22565634.svg)](https://doi.org/10.5281/zenodo.22565634)

> Ellena Godoy, Jorge (2026). *Covered but excluded primes: which primes divide
> an element of { n : rad(n) | f(n) }*. Zenodo. https://doi.org/10.5281/zenodo.22565634

The DOI above is the **concept** DOI and always resolves to the latest version.


## Author

**Jorge Ellena Godoy** — <jorgell23@gmail.com>

System design and research direction are the author's. The mathematical results
were produced by an automated system (Claude, Anthropic) under that direction.
All computations were verified by two independent implementations and
cross-checked against published work. The author is responsible for the
correctness of everything published here.

## Licence

MIT for the code, CC BY 4.0 for text and data. See `LICENSE`.
