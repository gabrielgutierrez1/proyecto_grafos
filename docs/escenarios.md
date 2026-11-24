# Escenarios de Análisis y Modelación ($G_0$, $G_1$, $G_2$)

Resumen técnico de la modelación matemática del laberinto (Integrante 1) y los tres escenarios comparativos manteniendo fijos `s` y `t` (Secciones 4, 5 y 7 del informe; el análisis visual y capturas finales los completará el Integrante 3).

## 1. Red principal $G_0 = (V, E)$

- **Interpretación física:** cada vértice $v \in V$ representa una intersección o espacio del centro de almacenamiento; cada arco $(u, v) \in E$ representa un pasillo unidireccional de capacidad unitaria.
- **Vértices ($|V| = 10$):** `{"s", "A", "B", "C", "D", "E", "F", "G", "H", "t"}`
- **Arcos iniciales ($|E| = 18$):**
  - Desde `s`: `(s, A)`, `(s, B)`, `(s, C)`
  - Desde `A`: `(A, D)`, `(A, E)`
  - Desde `B`: `(B, D)`, `(B, E)`, `(B, F)`
  - Desde `C`: `(C, E)`, `(C, F)`
  - Desde `D` y `E`: `(D, G)`, `(D, H)`, `(E, G)`, `(E, H)`
  - Hacia `H` y `t`: `(F, H)`, `(F, t)`, `(G, t)`, `(H, t)`

## 2. Justificación algorítmica: BFS frente a DFS

- **Búsqueda por amplitud (BFS):** explora el grafo por capas de distancia usando una cola FIFO (`collections.deque`). Como cada pasillo aporta exactamente 1 arco sin pesos adicionales, el primer instante en que se descubre `t` garantiza minimizar la cantidad de arcos en tiempo $O(|V| + |E|)$.
- **Búsqueda en profundidad (DFS):** profundiza una rama antes de retroceder; sirve para alcanzabilidad en $O(|V| + |E|)$, pero la primera ruta que alcanza `t` puede contener más arcos que el óptimo (p. ej. `s -> A -> D -> G -> t` de longitud 4 frente a `s -> B -> F -> t` de longitud 3).

## 3. Tabla comparativa de referencia (Apéndice B)

> Las modificaciones $G_1$ y $G_2$ se evalúan **por separado** respecto a $G_0$.

| Configuración | Modificación sobre $G_0$ | Arcos activos | Camino mínimo (BFS) | $d_G(s, t)$ | $\lambda_G(s, t)$ | $|C_{\text{mín}}|$ |
|---|---|---:|---|---:|---:|---:|
| **$G_0$ (Original)** | Ninguna | 18 | `s -> B -> F -> t` | 3 | 3 | 3 |
| **$G_1$ (Bloqueo)** | Bloquear `(H, t)` | 17 | `s -> B -> F -> t` | 3 | 2 | 2 |
| **$G_2$ (Adición)** | Agregar `(A, t)` | 19 | `s -> A -> t` | 2 | 3 | 3 |
| **Sin conexión** | Bloquear corte de `s` o `t` | 15 | `Sin camino` (`None`) | Sin camino | 0 | 0 |
