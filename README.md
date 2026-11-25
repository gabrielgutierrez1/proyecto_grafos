# Proyecto 1 — Simulador interactivo de laberintos y rutas alternativas

**Asignatura:** INFO1158 — Teoría de Grafos  
**Equipo:** David Fernández, Ailyn Melillán y Gabriel Gutiérrez (3 estudiantes)  
**Presentación y entrega:** lunes 30 de noviembre de 2026  
**Entrega del informe PDF:** hasta las 15:00 (Educa)  
\

## 1. Objetivo

Desarrollar una aplicación interactiva que represente un laberinto como **grafo dirigido** y permita:

- Encontrar un camino desde la entrada `s` hasta la salida `t` con el **menor número de arcos**.
- Calcular el **máximo número de caminos dirigidos que no comparten arcos** y mostrar esos caminos.
- Identificar un **conjunto mínimo de arcos** cuyo bloqueo impida llegar desde `s` hasta `t`.
- Modificar la red desde la interfaz y comparar los resultados.

> Las rutas independientes **pueden compartir vértices, pero no arcos**. La longitud de un camino es su cantidad de arcos, no la distancia física.

## 2. Tecnologías definidas

- **Lenguaje:** Python 3.
- **Bibliotecas:** bibliotecas estándar de Python y, cuando sea necesario, bibliotecas de Python para la interfaz y la visualización de grafos. **Las bibliotecas concretas aún no están seleccionadas.**
- **Control de versiones:** Git y GitHub.
- **Documentación:** Markdown (`README.md`) e informe técnico en PDF.
- **Algoritmos:** implementación propia de los procedimientos seleccionados para camino mínimo, rutas independientes y corte mínimo.

**Restricción del enunciado:** no utilizar bibliotecas que realicen directamente los cálculos algorítmicos solicitados. Se permiten bibliotecas para representar el grafo y desarrollar la interfaz visual.

Las dependencias definitivas y el comando de ejecución se documentarán aquí cuando se implemente la aplicación.

## 3. Reparto de responsabilidades

### Integrante 1 — Modelación matemática y camino mínimo

**Responsable:** David Fernández

- [x] Definir el grafo inicial `G = (V, E)` con **10 a 12 vértices** y **14 a 20 arcos**.
- [x] Verificar que `s != t`, que ningún vértice esté aislado y que no existan lazos, arcos repetidos ni arcos recíprocos.
- [x] Asegurar que el grafo inicial tenga **al menos dos caminos dirigidos de `s` a `t` sin arcos compartidos**.
- [x] Documentar los conjuntos `V` y `E` y qué representan físicamente.
- [x] Implementar la estructura del grafo, sus arcos activos y la validación de modificaciones.
- [x] Investigar y comparar **BFS versus DFS** para buscar caminos dirigidos.
- [x] Justificar la estrategia seleccionada para obtener la menor cantidad de arcos.
- [x] Implementar BFS desde cero, reconstruyendo un camino mínimo mediante predecesores.
- [x] Manejar explícitamente el caso **sin camino** (no asignar longitud numérica).
- [x] Crear pruebas del caso normal, múltiples caminos mínimos y destino inalcanzable.
- [ ] Redactar las secciones del informe sobre modelación, BFS y comparación BFS/DFS, con fuentes.

**Archivos sugeridos:** `src/grafo.py`, `src/camino_minimo.py`, `tests/test_camino_minimo.py`.

### Integrante 2 — Rutas independientes y corte mínimo

**Responsable:** Ailyn Melillán

- [x] Investigar y comparar al menos **dos estrategias** para determinar el máximo número de caminos sin arcos compartidos (p. ej., búsqueda de caminos disjuntos y flujo máximo de capacidad unitaria).
- [x] Elegir y justificar el enfoque con fuentes académicas o técnicas.
- [x] Implementar desde cero el algoritmo de **flujo máximo con capacidad 1 por arco** (por ejemplo, Edmonds–Karp).
- [x] Reconstruir y devolver los caminos dirigidos que alcanzan el máximo; permitir vértices compartidos, pero no arcos.
- [x] Implementar la identificación de un **corte mínimo de arcos** a partir de la red residual.
- [x] Verificar que `cantidad de caminos independientes == cantidad de arcos del corte mínimo`.
- [x] Resolver correctamente el caso **sin conexión**: cero caminos independientes y corte vacío.
- [x] Preparar pruebas con rutas compartidas, pasillos bloqueados y red sin conexión.
- [x] Redactar las secciones del informe sobre comparación de algoritmos, flujo máximo y corte mínimo, con fuentes.

**Archivos sugeridos:** `src/rutas_independientes.py`, `src/corte_minimo.py`, `tests/test_flujo_corte.py`.

**Responsable:** Gabriel Gutiérrez

- [ ] Diseñar una interfaz que muestre **vértices, arcos y direcciones** (flechas).
- [ ] Permitir seleccionar `s` y `t` distintos mediante controles visuales.
- [ ] Incluir acciones para **bloquear y restablecer** un pasillo.
- [ ] Incluir una acción para **agregar un arco dirigido**, validando lazos, duplicados y arcos recíprocos.
- [ ] Incluir un botón para **calcular/recalcular** los resultados.
- [ ] Destacar visualmente y de manera distinguible: camino mínimo, caminos independientes y corte mínimo (por ejemplo, capas o modos de visualización).
- [ ] Mostrar en texto la longitud mínima (o «sin camino»), cantidad de rutas independientes y arcos del corte.
- [ ] Coordinar con los integrantes 1 y 2 la integración de sus módulos.
- [ ] Construir la comparación de **tres configuraciones**: original y dos modificaciones, manteniendo los mismos `s` y `t` en esa comparación.
- [ ] Preparar capturas y redactar el análisis de cambios y la descripción de la interfaz para el informe.

**Archivos sugeridos:** `src/interfaz.py`, `src/main.py`, `docs/escenarios.md`.

## 4. Responsabilidades compartidas

- [ ] **Los tres:** acordar la configuración inicial y revisar el cumplimiento de las restricciones.
- [ ] **Los tres:** acordar los contratos entre módulos antes de programar en paralelo.
- [ ] **Los tres:** verificar un **caso independiente pequeño de 4 a 6 vértices** resuelto a mano: camino mínimo, caminos sin arcos compartidos y corte mínimo.
- [ ] **Los tres:** contrastar los resultados manuales con los del programa.
- [ ] **Los tres:** verificar en la red principal y las dos modificaciones la dirección y actividad de los arcos, la independencia por arcos y la igualdad flujo máximo/corte mínimo.
- [ ] **Los tres:** revisar el informe final, las referencias bibliográficas y que el repositorio sea accesible.
- [ ] **Los tres:** practicar la presentación y saber explicar decisiones, código y resultados.

**Reparto sugerido de la presentación (12 minutos como máximo):** David: problema y modelo (3 min); Ailyn: algoritmos y fundamento (4 min); Gabriel: demostración y modificaciones (4 min); 1 min de margen. Cada integrante debe poder responder preguntas sobre las otras partes.

## 5. Contrato de integración propuesto

Para evitar conflictos entre módulos, todos trabajarán sobre una representación acordada:

```python
vertices = {"s", "A", "B", "C", "D", "E", "F", "G", "H", "t"}
arcos = {("s", "A"), ("A", "B")}  # Solo ejemplo de formato, NO es el grafo definitivo
bloqueados = set()
```

**Importante:** calcular siempre sobre los arcos activos: `arcos - bloqueados`. Los arcos nuevos se incorporan a `arcos` después de validarlos. La configuración inicial concreta debe definirse en equipo.

**Interfaces sugeridas** (ajustables de común acuerdo):

```python
# Integrante 1
camino_minimo(vertices, arcos_activos, s, t) -> (camino, longitud)
# Sin conexión: (None, None)

# Integrante 2
rutas_y_corte(vertices, arcos_activos, s, t) -> (caminos, corte)
# caminos: lista de rutas (cada ruta es una lista de vértices)
# corte: conjunto de pares (origen, destino)
# Sin conexión: ([], set())

# Integrante 3
# Obtiene vertices y arcos_activos del modelo, ejecuta ambas funciones
# y presenta los resultados sin implementar algoritmos en la UI.
```

Antes de integrar, decidir también cómo se ordenarán los vecinos para obtener resultados reproducibles. Un camino mínimo o un corte mínimo pueden no ser únicos.

## 6. Estructura sugerida del repositorio

```text
laberintos-rutas/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── grafo.py
│   ├── camino_minimo.py
│   ├── rutas_independientes.py
│   ├── corte_minimo.py
│   ├── interfaz.py
│   └── main.py
├── tests/
│   ├── test_camino_minimo.py
│   ├── test_flujo_corte.py
│   └── test_integracion.py
└── docs/
    ├── escenarios.md
    ├── caso_manual.md
    ├── fuentes.md
    └── informe.pdf              # Al finalizar
```

## 7. Cronograma recomendado

| Fecha | Objetivo | Responsables |
|---|---|---|
| **19–20 nov.** | Definir grafo inicial, contratos, tecnología, repositorio y fuentes | Todos |
| **20–22 nov.** | Programar grafo/BFS, flujo/corte e interfaz base en paralelo | David, Ailyn y Gabriel |
| **23 nov.** | Integrar módulos y ejecutar pruebas funcionales | Todos; coordina 3 |
| **24 nov.** | Probar las tres configuraciones y resolver/verificar el caso manual | Todos |
| **25 nov.** | Cerrar informe PDF, capturas, README de ejecución y ensayar presentación | Todos |
| **26 nov.** | Presentación presencial y entrega del informe antes de las 23:00 | Todos |

## 8. Verificaciones obligatorias antes de entregar

- [ ] Grafo inicial: 10–12 vértices, 14–20 arcos, sin aislados, lazos, duplicados ni recíprocos; al menos dos rutas independientes.
- [ ] El camino mínimo usa el menor **número de arcos**, no pesos ni distancias físicas.
- [ ] Caminos independientes: ninguna pareja de caminos usa el mismo arco.
- [ ] Corte mínimo: al bloquear sus arcos activos, `t` resulta inalcanzable desde `s`.
- [ ] `número de rutas independientes = tamaño del corte mínimo`.
- [ ] La interfaz permite cambios sin editar el código y permite recalcular.
- [ ] Se estudian **tres configuraciones** manteniendo `s` y `t` para la comparación.
- [ ] Se resuelve y contrasta manualmente un caso de **4 a 6 vértices**.
- [ ] Algoritmos implementados con código propio y funciones principales comentadas.
- [ ] Informe PDF con modelo, investigación y fuentes, implementación, resultados, análisis, verificación y capturas.
- [ ] Repositorio accesible con dependencias e instrucciones reales de ejecución.
- [ ] Los tres participan en la presentación presencial y hacen una modificación interactiva.

## 9. Instalación y ejecución

**Pendiente de completar cuando la aplicación esté implementada.** El equipo agregará la versión mínima de Python requerida, los nombres de las bibliotecas utilizadas, la instalación de dependencias y el comando comprobado para iniciar el simulador. No se especifican comandos todavía para evitar instrucciones que no correspondan al código final.

## 10. Modo de trabajo y coordinación

El equipo trabaja de forma **modular y en paralelo** sobre contratos definidos, evitando conflictos de código y duplicación de lógica:

- **Separación por módulos:** cada integrante desarrolla en sus archivos asignados (`src/grafo.py` y `src/camino_minimo.py` para Integrante 1; `src/rutas_independientes.py` y `src/corte_minimo.py` para Integrante 2; `src/interfaz.py` y `src/main.py` para Integrante 3).
- **Contratos fijos:** no modificar la representación compartida (`vertices`, `arcos_activos`, `s`, `t`) ni las firmas acordadas (`camino_minimo`, `rutas_y_corte`) sin avisar al equipo.
- **Orden y reproducibilidad:** todos los cálculos operan sobre `arcos - bloqueados` y respetan el orden canónico de vecinos (`ordenar_vertices`) para obtener resultados reproducibles.
- **Flujo en Git:** trabajar en una rama por responsabilidad (`feature/grafo-bfs`, `feature/flujo-corte`, `feature/interfaz`), crear *pull requests* pequeños y revisar la integración antes de fusionar a `main`.
- **Validación continua:** antes de hacer *merge*, ejecutar la suite de pruebas (`python3 -m unittest discover -s tests -v`) y contrastar contra los escenarios de referencia (`docs/escenarios.md` y `docs/caso_manual.md`).
- **Implementación propia:** los algoritmos se programan desde cero en Python 3 (sin librerías externas que resuelvan camino mínimo, flujo máximo o corte mínimo); cualquier dependencia visual se declara en `requirements.txt`.

## 11. Ejecución del proyecto

> **Pendiente de completar una vez implementada la aplicación.** No se incluyen comandos ni dependencias ficticias.

- Versión de Python utilizada: `Python 3.10+` (probado en `Python 3.14`).
- Instalación de dependencias: `Sin dependencias externas por ahora (biblioteca estándar); pendiente definir librería de UI`.
- Comando de inicio (verificación actual / futura UI): `python3 -m src.main`
- Comando de pruebas: `python3 -m unittest discover -s tests -v`

---

**Base:** «Proyecto 1. Simulador interactivo de laberintos y rutas alternativas», INFO1158. La arquitectura, las asignaciones y el cronograma son propuestas de organización; los requisitos y la fecha proceden del enunciado del proyecto.
