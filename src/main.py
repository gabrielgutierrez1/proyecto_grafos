from __future__ import annotations

from .camino_minimo import camino_minimo, formatear_resultado_camino
from .grafo import crear_grafo_inicial, crear_grafo_manual
from .interfaz import iniciar_interfaz


def resumen_consola() -> None:
    escenarios = []

    g0 = crear_grafo_inicial()
    escenarios.append(("G0 (Red original)", g0))

    g1 = crear_grafo_inicial()
    g1.bloquear_arco("H", "t")
    escenarios.append(("G1 (Bloqueo H -> t)", g1))

    g2 = crear_grafo_inicial()
    g2.agregar_arco("A", "t")
    escenarios.append(("G2 (Nuevo arco A -> t)", g2))

    gm = crear_grafo_manual()
    escenarios.append(("Gm (Caso manual 5 vértices)", gm))

    print("=== Verificación de Modelación y Camino Mínimo (BFS) ===")
    for nombre, grafo in escenarios:
        camino, longitud = camino_minimo(
            grafo.vertices,
            grafo.arcos_activos,
            grafo.entrada,
            grafo.salida,
        )
        print(
            f"- {nombre}: |V|={len(grafo.vertices)}, "
            f"|E_activos|={len(grafo.arcos_activos)} -> "
            f"{formatear_resultado_camino(camino, longitud)}"
        )


def main() -> None:
    try:
        iniciar_interfaz()
    except NotImplementedError:
        resumen_consola()


if __name__ == "__main__":
    main()
