# Escenarios de Análisis y Modelación ($G_0$, $G_1$, $G_2$)

Resumen técnico de la modelación matemática del laberinto (Integrante 1), la interfaz gráfica e integración (Integrante 3) y los tres escenarios comparativos manteniendo fijos `s` y `t`.

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

## 4. Interfaz e integración (Gabriel Gutiérrez)

La aplicación de escritorio usa Tkinter, ttk y Canvas. Un panel lateral organiza
los controles en tres pasos: definir el recorrido, editar pasillos y calcular.
Tres tarjetas resumen longitud mínima, rutas independientes y tamaño del corte.
Las pestañas inferiores separan el detalle de las rutas de la comparación.
El pasillo seleccionado tiene un halo azul; los botones se habilitan según esté
activo, bloqueado o disponible para agregar. Los vértices representan
intersecciones y las flechas indican el único sentido permitido de cada pasillo.
La entrada seleccionada se identifica en verde y la salida en naranja. Los
pasillos bloqueados permanecen visibles en gris discontinuo, pero quedan fuera
de todos los cálculos.

Los controles permiten seleccionar extremos distintos, bloquear/restablecer
pasillos existentes y agregar arcos. La validación se delega a `GrafoLaberinto`,
que rechaza lazos, duplicados (incluso si están bloqueados) y arcos recíprocos.
Los errores se presentan en un diálogo sin aplicar la modificación inválida.

El botón de cálculo invoca las funciones existentes `camino_minimo` y
`rutas_y_corte` sobre los mismos arcos activos. La interfaz no implementa BFS ni
flujo máximo. Las vistas separadas muestran la red completa, el camino mínimo
azul, las rutas independientes con colores y etiquetas R1/R2/R3, o el corte
mínimo rojo. Las rutas también se enumeran en texto. Tras modificar la red o
los extremos, se retiran los resultados anteriores hasta recalcular.

La pestaña «Comparar escenarios» calcula G0, G1 y G2 con los mismos extremos seleccionados.
Cada modificación se aplica a una nueva copia de G0. La tabla es una referencia:
las ediciones libres del usuario aparecen en el dibujo y en el resumen, pero no
redefinen sus tres filas. Al cargar un escenario se reemplaza la red editada.

## 5. Resultados y análisis de cambios

Para entrada `s` y salida `t`, la ejecución `python3 -m src.main --consola`
produce los siguientes certificados:

| Red | Rutas independientes devueltas | Corte mínimo devuelto |
|---|---|---|
| G0 | `s-B-F-t`; `s-A-D-G-t`; `s-C-E-H-t` | `{(s,A), (s,B), (s,C)}` |
| G1 | `s-B-F-t`; `s-A-D-G-t` | `{(F,t), (G,t)}` |
| G2 | `s-A-t`; `s-B-F-t`; `s-C-E-G-t` | `{(s,A), (s,B), (s,C)}` |

En G0 hay tres alternativas independientes y un recorrido mínimo de tres
arcos. Bloquear `H → t` en G1 mantiene ese recorrido mínimo, pero reduce las
rutas independientes de tres a dos: quedan solamente dos arcos activos que
entran a la salida. Esto muestra que conservar la distancia mínima no implica
conservar la misma redundancia.

Agregar `A → t` en G2 reduce la distancia mínima de tres a dos arcos. No aumenta
el número máximo de rutas independientes: siguen siendo tres, limitado por
los tres arcos que salen de `s`. La mejora de distancia y el aumento de
redundancia son propiedades diferentes.

Las pruebas verifican en los tres escenarios que las rutas respetan arcos
activos y direcciones, que no comparten arcos, que su cantidad coincide con el
tamaño del corte y que quitar el corte impide llegar a la salida. Al bloquear
`F → t`, `G → t` y `H → t`, el resumen es «Sin camino», con longitud `None`, cero
rutas y corte vacío.

## 6. Capturas para el informe y comprobación visual pendiente

Esta sesión de desarrollo no pudo conectarse a la pantalla (`DISPLAY=:0`),
por lo que no se generaron capturas ni se ejecutaron los dos tests gráficos.
Las pruebas de integración y el comando de consola sí se ejecutaron.

En una sesión gráfica, ejecutar `python3 -m src.main` y preparar estas capturas
con entrada `s` y salida `t`:

1. Cargar G0 y elegir «Rutas independientes»: mostrar las tres rutas y la tabla.
2. Cargar G1 y elegir «Corte mínimo»: mostrar `H → t` bloqueado y el corte de dos arcos.
3. Cargar G2 y elegir «Camino mínimo»: mostrar `s → A → t` y longitud dos.
4. Para demostrar el caso sin conexión, cargar G0, bloquear los tres arcos que
   llegan a `t` y recalcular: mostrar «Sin camino», cero rutas y corte vacío.

Guardar las imágenes como `docs/capturas/g0-rutas.png`, `g1-corte.png`,
`g2-camino.png` y `sin-conexion.png` e incorporarlas al informe con los análisis
anteriores. Esos archivos todavía no existen; no son resultados verificados
visualmente. Revisar también el redimensionamiento de la ventana, las flechas
de los arcos agregados y los mensajes de validación antes de la entrega.
