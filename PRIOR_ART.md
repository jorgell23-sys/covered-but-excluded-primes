# Prior art — what was searched, where, when, and what was found

Searched on **2026-09-06**. Every negative below is reported together with a
**positive control**: a search of the same shape that *does* find something
known. A search that finds nothing is worth nothing unless it can be shown to
find something when there is something to find.

---

## 1. What is classical here, and is not claimed

Three pieces of this work are **not new** and are credited as such.

| piece | what it is | reference |
|---|---|---|
| the density rule (Theorem 2) | the density of primes for which a polynomial has a root equals the proportion of Galois elements with a fixed point | G. Frobenius, *Über Beziehungen zwischen den Primidealen eines algebraischen Körpers und den Substitutionen seiner Gruppe*, 1896. Modern accounts: B. Sury, *Resonance* **8**(12) (2003) 33–41; P. Stevenhagen and H. W. Lenstra, *Math. Intelligencer* **18** (1996) 26–37 |
| positive density of excluded primes for irreducible `F` of degree ≥ 2 | a transitive permutation group of degree > 1 contains a fixed-point-free element | C. Jordan, 1872 |
| polynomials with a root modulo every prime but no rational root | **intersective polynomials**, e.g. `(x²−2)(x²−3)(x²−6)` | standard; see the literature on intersective polynomials and Sárközy-type theorems |
| the object `S(σ) = { n : rad(n) \| σ(n) }` | studied under the name **prime-perfect / prime-abundant numbers** | P. Pollack and C. Pomerance, *Prime-perfect numbers*, INTEGERS **12A** (2012), Paper A14; OEIS A175200 |

What is **new** is the application: reading the primes that can divide an
element of `S(f)` off `F` alone (Theorem 1), the failure of the one-step
criterion (Theorem 3), the confinement of those failures to ramified primes
(Theorem 4), and the cycle characterisation with certificates (Theorem 5).

## 2. OEIS

Queried through the public JSON interface.

| query | result |
|---|---|
| `S(σ)` = 1, 6, 24, 28, 40, 54, 96, 120, 135, 216, … | **A175200**, *Numbers k such that rad(k) divides sigma(k)* — **POSITIVE CONTROL, passes** |
| `S(σ*)` = 6, 18, 20, 24, 45, 54, 60, 72, 90, 96, … | not in OEIS |
| `S(x³−x−1)` = 35, 85, 595, 935, 2345, 3325, 4165, … | not in OEIS |
| an invented sequence 6, 10, 15, 77, 1001, 90001, 7000003 | not in OEIS — **NEGATIVE CONTROL, passes** |

A175200 is also the external check of `verify.py [7]`: its 49 published terms
are recomputed from scratch and compared term by term.

## 3. Bibliographic databases

Six sources queried together: zbMATH Open, OpenAlex, Crossref, arXiv, Zenodo,
DataCite. Each query fixes **both halves** of the object with mandatory terms;
a single loose term matches any paper in the field and produces false positives.

| query | mandatory terms | result |
|---|---|---|
| prime perfect numbers radical sigma | `prime`, `perfect` | **found Pollack–Pomerance 2012** — POSITIVE CONTROL, passes |
| density of prime divisors of a polynomial Frobenius | `prime`, `divisors`, `polynomial` | found — POSITIVE CONTROL, passes |
| Frobenius density theorem fixed point Galois group | `Frobenius`, `density` | found |
| primes dividing elements of a set defined by radical divides a multiplicative function | `radical`, `multiplicative` | **not found** |
| covering digraph, prime divisors, arithmetic function, cycle | `covering`, `digraph`, `prime` | **not found** |
| an invented term | `hemispheric`, `cascade` | not found — NEGATIVE CONTROL, passes |

Web search was used in addition to confirm the classical status of the Frobenius
density theorem and of intersective polynomials; both are established and are
credited in §1 rather than claimed.

## 4. What the searches do and do not establish

They establish that the density rule and the intersective example are known, and
they are therefore presented as known. For Theorems 1, 3, 4 and 5 they establish
only that **nothing matching them appeared in what was consulted** — six
databases, OEIS, and web search, with the controls above showing the searches
were live and capable of finding known work. That is not a proof of novelty, and
it is not stated as one.

## 5. How to repeat the searches

The OEIS queries are `https://oeis.org/search?q=<terms>&fmt=json`. The database
queries used the public APIs of the six sources listed. The positive controls
are the first row of each table; if either fails when repeated, the negatives in
that table carry no weight.
