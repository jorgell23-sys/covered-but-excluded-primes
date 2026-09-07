# Primos cubiertos y aun así excluidos

<!-- hallazgo:que -->
## Qué se encontró

Para la función multiplicativa `f` dada en potencias de primo por
`f(q^e) = q^(2e) − q^e + 1`, el primo **3** tiene flechas entrantes en el
digrafo de cubrimiento de `f` y sin embargo **no divide a ningún elemento** de
`S(f) = { n : rad(n) | f(n) }`. Tener flecha entrante es entonces
*necesario* pero **no suficiente** para que un primo divida a un elemento de
`S(f)`.

<!-- hallazgo:enunciado -->
## Los enunciados

En todo lo que sigue `f` es multiplicativa con `f(q^e) = F(q^e)` para un
`F ∈ Z[x]` fijo con `F(0) = ±1` — que es exactamente la condición
`p ∤ f(p^a)`. Se escribe `q → p` cuando `p | f(q^e)` para algún `e ≥ 1`.

> **Teorema 1 (criterio).** `q → p` vale si y sólo si algún `ord_p(r)` divide a
> `ord_p(q)`, con `r` recorriendo las raíces de `F` módulo `p`. En
> consecuencia, **`p` tiene flecha entrante si y sólo si `F` tiene una raíz
> módulo `p`.**

> **Teorema 2 (densidad).** La densidad de los primos sin flecha entrante es la
> proporción de elementos de `Gal(F)` actuando sobre las raíces de `F` **sin
> punto fijo**. *Esto es el teorema de densidad de Frobenius (1896) aplicado a
> este objeto; el enunciado de densidad es clásico y no se reclama acá.*

> **Teorema 3 (un paso no alcanza).** Para `F = x² − x + 1`, el primo `3` tiene
> flecha entrante y no divide a ningún elemento de `S(f)`.

> **Teorema 4 (dónde pueden vivir los fallos).** Si `p` no ramifica en el cuerpo
> de descomposición de `F` y `F` tiene raíz módulo `p`, entonces existe un primo
> `q` que a su vez tiene raíz de `F` módulo `q` y cumple `q → p`. Por lo tanto
> todo fallo como el del Teorema 3 ocurre en un primo donde `F mod p` tiene una
> raíz repetida — finitos para cada `F`.

<!-- hallazgo:ejemplo -->
## El caso más chico, hecho

`F = x² − x + 1`, o sea `f(q^e) = q^(2e) − q^e + 1`.

| | |
|---|---|
| `F mod 3` | `x² − x + 1 ≡ (x+1)²`, cuya única raíz es `2` |
| `ord_3(2)` | `2`, porque `2 · 2 = 4 ≡ 1` |
| entonces `q → 3` exige | `2 \| ord_3(q)`, o sea `q ≡ 2 (mod 3)` |
| `p ≠ 3` tiene raíz de `F` si y sólo si | `6 \| p − 1`, o sea `p ≡ 1 (mod 6)` |
| primos bajo 8000 con `q → 3` | **511** |
| de ésos, cuántos están cubiertos | **0** |
| `S(f)` bajo 400000 | `100009 = 7²·13·157`, `175273 = 7⁴·73`, `274939 = 7²·31·181` |
| cuántos son divisibles por 3 | **0** |
| control positivo, la misma búsqueda sobre `f(q^e) = q^e + 1` | **261** elementos divisibles por 3, de 344 |

<!-- hallazgo:prueba -->
## Por qué es cierto

Un `n ∈ S(f)` se arma sólo con primos que estén ellos mismos cubiertos *dentro
de `n`*: cada vértice de su digrafo necesita una flecha entrante desde otro
primo de `n`. Módulo 3 el polinomio `x² − x + 1` se vuelve `(x+1)²`, cuya raíz
`2` tiene orden `2`, así que por el Teorema 1 una flecha `q → 3` obliga
`q ≡ 2 (mod 3)`. Pero un primo `p ≠ 3` tiene raíz de `F` sólo cuando
`6 | p − 1`, y entonces `p ≡ 1 (mod 3)`. Las dos clases son disjuntas, así que
todo primo que podría cubrir al 3 está él mismo sin cubrir y no puede aparecer
en `n`. Por lo tanto `3 ∤ n` para todo `n ∈ S(f)`.

<!-- hallazgo:comprobar -->
## Comprobalo vos

Sin dependencias, sólo biblioteca estándar:

```bash
git clone https://github.com/jorgell23-sys/covered-but-excluded-primes
cd covered-but-excluded-primes
python verify.py
```

Imprime una línea `PASS`/`FAIL` por control —son **77**— y sale con código
distinto de cero si algo falla. El control `[3]` es el teorema de arriba, el `[4]` es la cota de
ramificación sobre un barrido de 310 polinomios, y el `[7]` es **externo**:
recalcula `{ n : rad(n) | σ(n) }` desde cero y lo compara contra los 49 términos
publicados de manera independiente como OEIS A175200.

<!-- hallazgo:nodice -->
## Lo que no dice

- **No** reclama como nuevo el enunciado de densidad del Teorema 2. Eso es
  Frobenius (1896); lo nuevo acá es aplicarlo a `S(f)` y leer los primos
  excluidos de `F` sola.
- **No** demuestra que las dos cotas de `{p en un ciclo} ⊆ D(f) ⊆ C_∞`
  coincidan siempre. Coincidieron en todos los casos medidos — 310 polinomios
  contra los 168 primos por debajo de 1000, sin una sola brecha — pero eso es
  una medición y queda registrada como conjetura.
- **No** dice nada sobre cuántos elementos tiene `S(f)` por debajo de `x`. Se
  declaró una hipótesis sobre eso, se probó fuera de muestra y quedó
  **refutada**; está en `RESULT.md`.
- `σ`, `σ₂` y `φ*` **no** tienen ningún primo excluido; el fenómeno necesita una
  función cuyo perfil prohíba flechas.

---

## Qué hay acá adentro

| archivo | qué es |
|---|---|
| `RESULT.md` | el enunciado completo, las pruebas, las tablas y los límites |
| `PRIOR_ART.md` | qué se buscó, dónde, cuándo, y los controles positivos |
| `verify.py` | cada afirmación, recomprobada en segundos, sin dependencias |
| `src/excluded.py` | el criterio, el digrafo, los ciclos y los certificados |
| `src/figures.py` | las figuras, generadas desde los datos |
| `data/` | las tablas generadas |
| `docs/` | una explicación desde cero, para quien no conoce el tema |

La explicación para no iniciados está en
<https://jorgell23-sys.github.io/covered-but-excluded-primes/es/>.

## Autor

**Jorge Ellena Godoy** — <jorgell23@gmail.com>

El diseño del sistema y la dirección de la investigación son del autor. Los
resultados matemáticos los produjo un sistema automatizado (Claude, Anthropic)
bajo esa dirección. Todos los cálculos fueron verificados por dos
implementaciones independientes y cruzados contra trabajo publicado. El autor es
responsable de la corrección de todo lo publicado acá.

## Licencia

MIT para el código, CC BY 4.0 para texto y datos. Ver `LICENSE`.
