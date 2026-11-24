# Caso Independiente Resuelto Manualmente ($G_m$)

Caso pequeño distinto de la red principal utilizado para contrastar los resultados matemáticos manuales con las salidas del programa (Sección 8.1 del informe técnico).

## 1. Definición formal

- **Vértices ($|V_m| = 5$):** `V_m = {"s", "A", "B", "C", "t"}`
- **Arcos ($|E_m| = 7$):** `E_m = {("s", "A"), ("s", "B"), ("A", "C"), ("A", "t"), ("B", "C"), ("B", "t"), ("C", "t")}`

## 2. Resolución manual de referencia

| Indicador | Resultado manual | Justificación |
|---|---|---|
| **Camino mínimo** | `s -> A -> t` (o `s -> B -> t`), $d_{G_m}(s, t) = 2$ | No existe el arco directo `(s, t)`, por lo que ninguna ruta tiene longitud 1. Con orden canónico de vecinos (`A` antes que `B`), BFS reconstruye `s -> A -> t`. |
| **Rutas disjuntas por arcos** | $\lambda_{G_m}(s, t) = 2$: `s -> A -> t` y `s -> B -> t` | No comparten arcos y desde `s` solo salen 2 arcos, por lo que $\lambda_{G_m}(s, t) \le 2$. |
| **Corte mínimo** | $C_m = \{(\text{s}, \text{A}), (\text{s}, \text{B})\}$, $|C_m| = 2$ | Desconecta `s` de toda la red y coincide en cardinalidad con las 2 rutas independientes (certificado de optimalidad). |
