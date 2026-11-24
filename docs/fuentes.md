# Fuentes Bibliográficas y Académicas

Referencias académicas utilizadas para fundamentar la modelación en grafos dirigidos, la comparación BFS frente a DFS, el teorema de Menger y el enfoque de flujo máximo–corte mínimo (listas para enlazar las citas pendientes en el informe LaTeX/PDF):

1. **Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022).** *Introduction to Algorithms* (4th ed.). MIT Press.
   - Cap. 20 (*Elementary Graph Algorithms*): representación por listas de adyacencia, complejidad $O(|V| + |E|)$, comparación entre BFS y DFS, y demostración de optimalidad de BFS en distancia por número de arcos.
   - Cap. 24 (*Maximum Flow*): redes de flujo, red residual, teorema de flujo máximo–corte mínimo y algoritmo de Ford–Fulkerson / Edmonds–Karp.

2. **Kleinberg, J., & Tardos, É. (2005).** *Algorithm Design*. Pearson / Addison-Wesley.
   - Cap. 3 (*Graphs*): recorridos BFS por capas y reconstrucción de caminos mediante árbol de búsqueda.
   - Cap. 7 (*Network Flow*, §7.1–7.6): capacidades enteras/unitarias, caminos disjuntos por arcos (*edge-disjoint paths*) en grafos dirigidos y extracción de rutas acíclicas.

3. **Bondy, J. A., & Murty, U. S. R. (2008).** *Graph Theory*. Springer (Graduate Texts in Mathematics, Vol. 244).
   - Definiciones formales de digrafos, caminos simples dirigidos, cortes $s\text{–}t$ y versión dirigida por arcos del teorema de Menger ($\lambda_G(s, t)$).

4. **Diestel, R. (2017).** *Graph Theory* (5th ed.). Springer.
   - Cap. 3 (*Connectivity*): conectividad por arcos y relación estructural entre familias de caminos independientes y cortes separadores mínimos.

5. **Edmonds, J., & Karp, R. M. (1972).** Theoretical improvements in algorithmic efficiency for network flow problems. *Journal of the ACM (JACM)*, 19(2), 248–264.
   - Selección de caminos aumentantes más cortos mediante BFS y cota polinomial $O(|V||E|^2)$.
