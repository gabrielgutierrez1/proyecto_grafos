"""Interfaz de escritorio; delega todos los cálculos en los módulos del equipo."""
from __future__ import annotations

import math
import tkinter as tk
from tkinter import messagebox, ttk

from .camino_minimo import formatear_resultado_camino
from .escenarios import Resultado, calcular_resultado, crear_escenarios
from .grafo import Arco, POSICIONES_SUGERIDAS, crear_grafo_inicial, ordenar_vertices




class InterfazLaberinto:
    """Ventana principal interactiva del simulador sobre Tkinter, ttk y Canvas."""

    COLORES_RUTAS = ("#007f73", "#a45100", "#8054bd", "#1565c0", "#bd3972")
    MODOS = ("Red", "Camino mínimo", "Rutas independientes", "Corte mínimo")

    def __init__(self, raiz: tk.Tk) -> None:
        """Construye los paneles, selectores, lienzo y pestañas sobre la raíz Tk.

        Args:
            raiz: Instancia raíz `tk.Tk` donde se aloja la interfaz.

        Returns:
            None.
        """
        self.raiz = raiz
        self.grafo = crear_grafo_inicial()
        self.resultado: Resultado | None = None
        raiz.title("Laberinto · Simulador de grafos dirigidos")
        raiz.geometry("1240x900")
        raiz.minsize(1020, 860)
        self.entrada = tk.StringVar(value="s")
        self.salida = tk.StringVar(value="t")
        self.origen = tk.StringVar(value="H")
        self.destino = tk.StringVar(value="t")
        self.modo = tk.StringVar(value="Camino mínimo")
        self.estado = tk.StringVar()
        self.resumen = tk.StringVar()
        self.leyenda = tk.StringVar()
        self.escenario = tk.StringVar(value="G0 · Original")
        self.metricas = [tk.StringVar(value="—") for _ in range(3)]
        self.pasillo = tk.StringVar()
        self._configurar_estilo()
        self._construir_controles()
        for variable in (self.origen, self.destino):
            variable.trace_add("write", lambda *_: self._actualizar_pasillo())
        self._actualizar_pasillo()
        self.calcular()

    def _configurar_estilo(self) -> None:
        self.raiz.configure(background="#edf2f7")
        estilo = ttk.Style(self.raiz)
        estilo.theme_use("clam")
        estilo.configure(".", font=("DejaVu Sans", 10), foreground="#24334b")
        estilo.configure("TFrame", background="#edf2f7")
        estilo.configure("TLabel", background="#edf2f7")
        estilo.configure("Card.TFrame", background="white")
        estilo.configure("Card.TLabel", background="white")
        estilo.configure("Muted.TLabel", background="white", foreground="#617087", font=("DejaVu Sans", 9))
        estilo.configure("Title.TLabel", font=("DejaVu Sans", 22, "bold"))
        estilo.configure("Section.TLabel", background="white", font=("DejaVu Sans", 11, "bold"))
        estilo.configure("Metric.TLabel", background="white", foreground="#176cbd", font=("DejaVu Sans", 22, "bold"))
        estilo.configure("TButton", padding=(12, 8), background="#e9eff6", borderwidth=0)
        estilo.map("TButton", background=[("active", "#dce6f2")])
        estilo.configure("Primary.TButton", background="#176cbd", foreground="white", font=("DejaVu Sans", 10, "bold"))
        estilo.map("Primary.TButton", background=[("active", "#12599c")])
        estilo.configure("View.TRadiobutton", background="white", padding=(8, 7))
        estilo.map("View.TRadiobutton", background=[("selected", "#e5f0fc")], foreground=[("selected", "#12599c")])
        estilo.configure("TCombobox", padding=5)
        estilo.configure("Treeview", rowheight=27, background="white", fieldbackground="white", borderwidth=0)
        estilo.configure("Treeview.Heading", background="#e9eff6", padding=8, font=("DejaVu Sans", 9, "bold"))
        estilo.configure("TNotebook", background="#edf2f7", borderwidth=0)
        estilo.configure("TNotebook.Tab", padding=(18, 8))

    def _selector(self, marco, titulo, variable, columna):
        ttk.Label(marco, text=titulo, style="Muted.TLabel").grid(row=0, column=columna, sticky="w", pady=(0, 5))
        selector = ttk.Combobox(marco, textvariable=variable, width=9, state="readonly",
                                 values=ordenar_vertices(self.grafo.vertices))
        selector.grid(row=1, column=columna, sticky="ew", padx=(0, 10))
        marco.columnconfigure(columna, weight=1)
        return selector

    def _construir_controles(self) -> None:
        panel = ttk.Frame(self.raiz, padding=20)
        panel.pack(fill="both", expand=True)
        cabecera = ttk.Frame(panel)
        cabecera.pack(fill="x", pady=(0, 16))
        ttk.Label(cabecera, text="Laberinto", style="Title.TLabel").pack(anchor="w")
        ttk.Label(cabecera, text="Explora caminos, compara alternativas y descubre qué pasillos son críticos.", foreground="#617087").pack(anchor="w", pady=(4, 0))
        cuerpo = ttk.Frame(panel)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.rowconfigure(0, weight=1)
        lateral = ttk.Frame(cuerpo, style="Card.TFrame", padding=16, width=270)
        lateral.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        ttk.Label(lateral, text="01  Define el recorrido", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        extremos = ttk.Frame(lateral, style="Card.TFrame")
        extremos.pack(fill="x")
        for selector in (self._selector(extremos, "Entrada", self.entrada, 0), self._selector(extremos, "Salida", self.salida, 1)):
            selector.bind("<<ComboboxSelected>>", self._cambiar_extremos)
        ttk.Label(lateral, text="Elige dos vértices distintos.", style="Muted.TLabel").pack(anchor="w", pady=(6, 10))
        ttk.Separator(lateral).pack(fill="x", pady=(0, 10))
        ttk.Label(lateral, text="02  Edita los pasillos", style="Section.TLabel").pack(anchor="w", pady=(0, 12))
        edicion = ttk.Frame(lateral, style="Card.TFrame")
        edicion.pack(fill="x")
        self._selector(edicion, "Desde", self.origen, 0)
        self._selector(edicion, "Hacia", self.destino, 1)
        ttk.Label(lateral, textvariable=self.pasillo, style="Muted.TLabel", wraplength=235).pack(anchor="w", pady=10)
        self.botones_pasillo = {}
        for texto, accion in (("Bloquear pasillo", "bloquear_arco"), ("Restablecer pasillo", "restablecer_arco"), ("Agregar nuevo arco", "agregar_arco")):
            boton = ttk.Button(lateral, text=texto, command=lambda a=accion: self.modificar(a))
            boton.pack(fill="x", pady=3)
            self.botones_pasillo[accion] = boton
        ttk.Label(lateral, text="También puedes hacer clic en una flecha para seleccionar el pasillo.", style="Muted.TLabel", wraplength=230).pack(anchor="w", pady=(8, 10))
        ttk.Separator(lateral).pack(fill="x", pady=(0, 10))
        ttk.Label(lateral, text="03  Consulta los resultados", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Button(lateral, text="Calcular rutas", style="Primary.TButton", command=self.calcular).pack(fill="x")
        ttk.Label(lateral, textvariable=self.estado, style="Muted.TLabel", wraplength=235).pack(anchor="w", pady=12)

        principal = ttk.Frame(cuerpo)
        principal.grid(row=0, column=1, sticky="nsew")
        tarjetas = ttk.Frame(principal)
        tarjetas.pack(fill="x", pady=(0, 12))
        for i, (titulo, unidad) in enumerate((("Camino mínimo", "arcos de entrada a salida"), ("Rutas independientes", "sin compartir pasillos"), ("Corte mínimo", "arcos que desconectan"))):
            tarjetas.columnconfigure(i, weight=1, uniform="tarjeta")
            tarjeta = ttk.Frame(tarjetas, style="Card.TFrame", padding=12)
            tarjeta.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 8, 0))
            ttk.Label(tarjeta, text=titulo, style="Muted.TLabel").pack(anchor="w")
            ttk.Label(tarjeta, textvariable=self.metricas[i], style="Metric.TLabel").pack(anchor="w", pady=3)
            ttk.Label(tarjeta, text=unidad, style="Muted.TLabel").pack(anchor="w")
        mapa = ttk.Frame(principal, style="Card.TFrame", padding=12)
        mapa.pack(fill="both", expand=True)
        vistas = ttk.Frame(mapa, style="Card.TFrame")
        vistas.pack(fill="x")
        for modo in self.MODOS:
            ttk.Radiobutton(vistas, text=modo, value=modo, variable=self.modo, command=self.dibujar, style="View.TRadiobutton").pack(side="left", padx=(0, 3))
        self.canvas = tk.Canvas(mapa, background="#f8fafd", highlightthickness=0, height=260)
        self.canvas.pack(fill="both", expand=True, pady=10)
        self.canvas.bind("<Configure>", lambda evento: self.dibujar())
        leyenda = ttk.Label(mapa, textvariable=self.leyenda, style="Muted.TLabel", wraplength=700)
        leyenda.pack(anchor="w")
        self.canvas.bind("<Configure>", lambda evento: leyenda.configure(wraplength=max(300, evento.width)), add="+")

        pestañas = ttk.Notebook(panel)
        pestañas.pack(fill="x", pady=(14, 0))
        detalles = ttk.Frame(pestañas, style="Card.TFrame", padding=14)
        comparacion = ttk.Frame(pestañas, style="Card.TFrame", padding=10)
        pestañas.add(detalles, text="Detalle de las rutas")
        pestañas.add(comparacion, text="Comparar escenarios")
        etiqueta = ttk.Label(detalles, textvariable=self.resumen, style="Card.TLabel", justify="left", wraplength=1100)
        etiqueta.pack(anchor="nw")
        detalles.bind("<Configure>", lambda evento: etiqueta.configure(wraplength=max(300, evento.width-30)))
        self.tabla = ttk.Treeview(comparacion, columns=("escenario", "arcos", "longitud", "rutas", "corte"), show="headings", height=3)
        for clave, titulo, ancho in (("escenario", "Configuración", 210), ("arcos", "Arcos activos", 100), ("longitud", "Longitud mínima", 120), ("rutas", "Rutas independientes", 150), ("corte", "Corte mínimo", 230)):
            self.tabla.heading(clave, text=titulo)
            self.tabla.column(clave, width=ancho, minwidth=80, anchor="w" if clave in ("escenario", "corte") else "center")
        self.tabla.tag_configure("alternada", background="#f3f7fc")
        self.tabla.pack(fill="x")
        carga = ttk.Frame(comparacion, style="Card.TFrame")
        carga.pack(fill="x", pady=(8, 0))
        ttk.Combobox(carga, textvariable=self.escenario, values=[n for n, _ in crear_escenarios()], state="readonly", width=25).pack(side="left")
        ttk.Button(carga, text="Cargar escenario", command=self.cargar_escenario).pack(side="left", padx=8)
        ttk.Label(carga, text="Reemplaza la red editada. Conserva entrada y salida.", style="Muted.TLabel").pack(side="left")
        ttk.Label(comparacion, text="Referencia: original y dos modificaciones por separado; no incluye tus ediciones libres.", style="Muted.TLabel").pack(anchor="w", pady=(6, 0))

    def _actualizar_pasillo(self) -> None:
        u, v = self.origen.get(), self.destino.get()
        existe = (u, v) in self.grafo.arcos
        bloqueado = (u, v) in self.grafo.bloqueados
        nuevo_valido = u != v and not existe and (v, u) not in self.grafo.arcos
        estado = "Bloqueado" if bloqueado else "Activo" if existe else "Disponible para agregar" if nuevo_valido else "Arco no permitido"
        self.pasillo.set(f"{u} → {v}  ·  {estado}")
        for accion, habilitado in (("bloquear_arco", existe and not bloqueado), ("restablecer_arco", bloqueado), ("agregar_arco", nuevo_valido)):
            self.botones_pasillo[accion].configure(state="normal" if habilitado else "disabled")
        self.dibujar()

    def _cambiar_extremos(self, evento=None) -> None:
        try:
            self.grafo.cambiar_extremos(self.entrada.get(), self.salida.get())
        except ValueError as error:
            self.entrada.set(self.grafo.entrada)
            self.salida.set(self.grafo.salida)
            messagebox.showerror("Extremos inválidos", str(error), parent=self.raiz)
            return
        self._invalidar("Extremos cambiados. Pulsa calcular.")
        self.tabla.delete(*self.tabla.get_children())

    def _invalidar(self, mensaje: str) -> None:
        self.resultado = None
        self.estado.set(mensaje)
        self.resumen.set("La red cambió. Pulsa «Calcular rutas» para actualizar los resultados.")
        for metrica in self.metricas:
            metrica.set("—")
        self._actualizar_pasillo()
        self.dibujar()

    def modificar(self, accion: str) -> None:
        """Ejecuta una acción de edición sobre el pasillo seleccionado e invalida resultados.

        Args:
            accion: Nombre del método de `GrafoLaberinto` (`'bloquear_arco'`,
                `'restablecer_arco'` o `'agregar_arco'`).

        Returns:
            None.
        """
        try:
            getattr(self.grafo, accion)(self.origen.get(), self.destino.get())
        except ValueError as error:
            messagebox.showerror("No se puede modificar el pasillo", str(error), parent=self.raiz)
            return
        self._invalidar("Red modificada. Pulsa calcular.")

    def cargar_escenario(self) -> None:
        """Reemplaza la red activa por el escenario seleccionado manteniendo los extremos.

        Returns:
            None.
        """
        escenarios = dict(crear_escenarios(self.grafo.entrada, self.grafo.salida))
        self.grafo = escenarios[self.escenario.get()]
        self.calcular()

    @staticmethod
    def texto_corte(corte: set[Arco]) -> str:
        """Formatea el conjunto de arcos del corte mínimo para su presentación visual.

        Args:
            corte: Conjunto de pares ordenados `(u, v)` pertenecientes al corte.

        Returns:
            str: Arcos separados por coma o `'∅'` cuando el corte es vacío.
        """
        return ", ".join(f"{u} → {v}" for u, v in sorted(corte)) or "∅"

    def calcular(self) -> None:
        """Recalcula indicadores, detalle de rutas, tabla comparativa y dibujo de la red.

        Returns:
            None.
        """
        self.resultado = calcular_resultado(self.grafo)
        r = self.resultado
        self.metricas[0].set(str(r.longitud) if r.longitud is not None else "Sin camino")
        self.metricas[1].set(str(len(r.rutas)))
        self.metricas[2].set(str(len(r.corte)))
        rutas = "\n".join(f"R{i}: {' → '.join(ruta)}" for i, ruta in enumerate(r.rutas, 1)) or "Ninguna"
        self.resumen.set(
            f"Camino mínimo: {formatear_resultado_camino(r.camino, r.longitud)}\n"
            f"Rutas independientes: {len(r.rutas)} · Corte mínimo: {self.texto_corte(r.corte)} ({len(r.corte)} arcos)\n{rutas}"
        )
        self.estado.set(f"Calculado: {self.grafo.entrada} → {self.grafo.salida} · {len(self.grafo.arcos_activos)} arcos activos")
        self.tabla.delete(*self.tabla.get_children())
        for indice, (nombre, grafo) in enumerate(crear_escenarios(self.grafo.entrada, self.grafo.salida)):
            resultado = calcular_resultado(grafo)
            self.tabla.insert("", "end", tags=("alternada",) if indice % 2 == 0 else (), values=(nombre, len(grafo.arcos_activos), resultado.longitud if resultado.longitud is not None else "Sin camino", len(resultado.rutas), self.texto_corte(resultado.corte)))
        self._actualizar_pasillo()

    def _seleccionar_arco(self, u: str, v: str) -> None:
        self.origen.set(u)
        self.destino.set(v)

    def dibujar(self) -> None:
        """Dibuja direcciones y una sola capa de resultados para evitar ambigüedad."""
        canvas = self.canvas
        canvas.delete("all")
        ancho, alto = max(canvas.winfo_width(), 300), max(canvas.winfo_height(), 200)
        posiciones = {v: (35 + x * (ancho - 70), 30 + (1-y) * (alto - 60)) for v, (x, y) in POSICIONES_SUGERIDAS.items()}
        destacados = {}
        modo = self.modo.get()
        leyenda = "Gris: activo · Gris discontinuo: bloqueado · Entrada: verde · Salida: naranja"
        if self.resultado:
            r = self.resultado
            if modo == "Camino mínimo" and r.camino:
                destacados = {arco: "#1565c0" for arco in zip(r.camino, r.camino[1:])}
                leyenda += " · Azul grueso: camino mínimo"
            elif modo == "Rutas independientes":
                for i, ruta in enumerate(r.rutas):
                    color = self.COLORES_RUTAS[i % len(self.COLORES_RUTAS)]
                    destacados.update({arco: color for arco in zip(ruta, ruta[1:])})
                leyenda += " · R1 verde, R2 ocre, R3 violeta (número sobre cada arco)"
            elif modo == "Corte mínimo":
                destacados = {arco: "#cc2341" for arco in r.corte}
                leyenda += " · Rojo grueso: arcos del corte mínimo"
        self.leyenda.set(leyenda)
        numeros = {}
        if self.resultado and modo == "Rutas independientes":
            numeros = {arco: i for i, ruta in enumerate(self.resultado.rutas, 1) for arco in zip(ruta, ruta[1:])}
        for u, v in sorted(self.grafo.arcos, key=lambda arco: (arco in destacados, arco)):
            x1, y1 = posiciones[u]
            x2, y2 = posiciones[v]
            dx, dy = x2-x1, y2-y1
            distancia = math.hypot(dx, dy)
            ux, uy = dx/distancia, dy/distancia
            # Curvar arcos largos o que pasan sobre vértices de la misma fila.
            curva = 0
            for w, (x, y) in posiciones.items():
                if w not in (u, v):
                    proyeccion = (x-x1)*ux + (y-y1)*uy
                    if 0 < proyeccion < distancia and abs((x-x1)*uy - (y-y1)*ux) < 26:
                        curva = 55
            mx, my = (x1+x2)/2 - uy*curva, (y1+y2)/2 + ux*curva
            inicio = math.hypot(mx-x1, my-y1)
            fin = math.hypot(x2-mx, y2-my)
            puntos = (x1+23*(mx-x1)/inicio, y1+23*(my-y1)/inicio,
                      mx, my, x2-25*(x2-mx)/fin, y2-25*(y2-my)/fin)
            bloqueado = (u, v) in self.grafo.bloqueados
            color = destacados.get((u, v), "#bcc2cc" if bloqueado else "#8994a6")
            tag = f"arco:{u}:{v}"
            if (u, v) == (self.origen.get(), self.destino.get()):
                canvas.create_line(*puntos, smooth=True, fill="#b9d7fa", width=10)
            canvas.create_line(*puntos, smooth=True, arrow=tk.LAST, arrowshape=(13, 15, 6), fill=color, width=4 if (u, v) in destacados else 2, dash=(5, 5) if bloqueado else (), tags=(tag,))
            canvas.tag_bind(tag, "<Enter>", lambda evento: canvas.configure(cursor="hand2"))
            canvas.tag_bind(tag, "<Leave>", lambda evento: canvas.configure(cursor=""))
            canvas.tag_bind(tag, "<Button-1>", lambda evento, a=u, b=v: self._seleccionar_arco(a, b))
            if (u, v) in numeros:
                canvas.create_text(mx, my-10, text=f"R{numeros[u, v]}", fill=color, font=("TkDefaultFont", 10, "bold"))
        for v, (x, y) in posiciones.items():
            color = "#007f73" if v == self.grafo.entrada else "#b85e13" if v == self.grafo.salida else "#253858"
            canvas.create_oval(x-23, y-20, x+23, y+26, fill="#e0e7f0", outline="")
            if v in (self.grafo.entrada, self.grafo.salida):
                canvas.create_text(x, y-34, text="ENTRADA" if v == self.grafo.entrada else "SALIDA", fill=color, font=("DejaVu Sans", 8, "bold"))
            canvas.create_oval(x-22, y-22, x+22, y+22, fill=color, outline="white", width=2)
            canvas.create_text(x, y, text=v, fill="white", font=("TkDefaultFont", 13, "bold"))


def iniciar_interfaz() -> None:
    """Crea la ventana principal de Tkinter e inicia el bucle de eventos interactivo.

    Returns:
        None.
    """
    raiz = tk.Tk()
    InterfazLaberinto(raiz)
    raiz.mainloop()
