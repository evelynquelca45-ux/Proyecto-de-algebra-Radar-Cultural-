"""
PROYECTO FINAL DE ÁLGEBRA LINEAL — UNIVERSIDAD ADVENTISTA DE BOLIVIA
Título: Radar Cultural + Alter Ego Social (Sistema de Predicción y Transformaciones 2D)
Interfaz Gráfica: Tkinter + Matplotlib + NumPy + Pandas

Archivos necesarios en la misma carpeta:
    - radar_cultural_tkinter.py
    - datos_radar_cultural.csv
"""

import os
import math
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import matplotlib
try:
    matplotlib.use("TkAgg")
except Exception:
    pass
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==============================================================================
# 1. CONSTANTES, EJES, PREGUNTAS, CATÁLOGO Y ROLES
# ==============================================================================

EJES = ["novedad", "social", "estructura", "analitico", "intensidad"]
NOMBRES_EJES = [
    "Rutina (-) <-> Novedad (+)",
    "Introspección (-) <-> Energía social (+)",
    "Improvisación (-) <-> Estructura (+)",
    "Emocional (-) <-> Analítico (+)",
    "Calma (-) <-> Intensidad (+)"
]

ROLES = [
    {
        "id": "explorador",
        "nombre": "El Explorador",
        "descripcion": "Sueles sentir curiosidad por probar caminos distintos y proponer experiencias nuevas."
    },
    {
        "id": "conector",
        "nombre": "El Conector",
        "descripcion": "Tiendes a favorecer la participación y las conexiones entre las personas."
    },
    {
        "id": "estratega",
        "nombre": "El Estratega",
        "descripcion": "Te resulta cómodo planificar, comparar alternativas y organizar los pasos."
    },
    {
        "id": "observador",
        "nombre": "El Observador",
        "descripcion": "Prefieres analizar el entorno y elegir cuándo y cómo participar."
    }
]

PREGUNTAS = [
    {
        "id": 1,
        "titulo": "Por fin tienes una tarde completamente libre. ¿Qué haces?",
        "contexto": "Un plan cambia a última hora.",
        "opciones": [
            {
                "texto": "Improviso una actividad que nunca he probado",
                "pesos": [
                    2,
                    1,
                    -2,
                    0,
                    1
                ]
            },
            {
                "texto": "Me quedo con algo tranquilo que disfruto",
                "pesos": [
                    -1,
                    -2,
                    1,
                    -1,
                    -2
                ]
            },
            {
                "texto": "Organizo un plan con horarios y objetivos",
                "pesos": [
                    0,
                    1,
                    2,
                    2,
                    0
                ]
            }
        ]
    },
    {
        "id": 2,
        "titulo": "Llegas a una reunión donde casi nadie te conoce.",
        "contexto": "No tienes ninguna obligación de participar.",
        "opciones": [
            {
                "texto": "Inicio una conversación y conozco a varias personas",
                "pesos": [
                    1,
                    2,
                    -1,
                    -1,
                    1
                ]
            },
            {
                "texto": "Observo primero y converso con una persona",
                "pesos": [
                    -1,
                    -2,
                    1,
                    1,
                    -1
                ]
            },
            {
                "texto": "Busco una actividad concreta en la que colaborar",
                "pesos": [
                    0,
                    1,
                    2,
                    2,
                    0
                ]
            }
        ]
    },
    {
        "id": 3,
        "titulo": "Debes resolver un pequeño reto en equipo.",
        "contexto": "Hay poco tiempo para ponerse de acuerdo.",
        "opciones": [
            {
                "texto": "Propongo experimentar hasta hallar algo original",
                "pesos": [
                    2,
                    1,
                    -2,
                    0,
                    2
                ]
            },
            {
                "texto": "Ordeno los pasos y comparo las alternativas",
                "pesos": [
                    -1,
                    0,
                    2,
                    2,
                    0
                ]
            },
            {
                "texto": "Escucho las ideas y ayudo a lograr un acuerdo",
                "pesos": [
                    0,
                    2,
                    0,
                    -2,
                    -1
                ]
            }
        ]
    },
    {
        "id": 4,
        "titulo": "Descubres un lugar nuevo en tu ciudad.",
        "contexto": "Puedes visitarlo hoy o dejarlo para otro día.",
        "opciones": [
            {
                "texto": "Entro de inmediato por pura curiosidad",
                "pesos": [
                    2,
                    0,
                    -2,
                    -1,
                    1
                ]
            },
            {
                "texto": "Primero busco información y reseñas",
                "pesos": [
                    1,
                    -1,
                    2,
                    2,
                    -1
                ]
            },
            {
                "texto": "Prefiero regresar a uno que ya me gusta",
                "pesos": [
                    -2,
                    -1,
                    1,
                    -1,
                    -2
                ]
            }
        ]
    },
    {
        "id": 5,
        "titulo": "En un viaje surge un cambio inesperado.",
        "contexto": "El itinerario original ya no funciona.",
        "opciones": [
            {
                "texto": "Lo veo como una oportunidad de explorar",
                "pesos": [
                    2,
                    1,
                    -2,
                    -1,
                    2
                ]
            },
            {
                "texto": "Reorganizo la agenda para no perder tiempo",
                "pesos": [
                    0,
                    0,
                    2,
                    2,
                    0
                ]
            },
            {
                "texto": "Busco un momento para adaptarme con calma",
                "pesos": [
                    -1,
                    -2,
                    0,
                    -1,
                    -2
                ]
            }
        ]
    },
    {
        "id": 6,
        "titulo": "Un amigo te pide elegir una actividad para el grupo.",
        "contexto": "Todos tienen preferencias distintas.",
        "opciones": [
            {
                "texto": "Elijo algo emocionante y fuera de lo común",
                "pesos": [
                    2,
                    1,
                    -1,
                    -1,
                    2
                ]
            },
            {
                "texto": "Pregunto qué quiere cada uno y busco equilibrio",
                "pesos": [
                    0,
                    2,
                    1,
                    -2,
                    -1
                ]
            },
            {
                "texto": "Propongo una opción segura y fácil de organizar",
                "pesos": [
                    -2,
                    0,
                    2,
                    1,
                    -1
                ]
            }
        ]
    },
    {
        "id": 7,
        "titulo": "Tienes que aprender una habilidad nueva.",
        "contexto": "Nadie te ha dicho cómo empezar.",
        "opciones": [
            {
                "texto": "Pruebo primero y aprendo de mis errores",
                "pesos": [
                    2,
                    0,
                    -2,
                    0,
                    1
                ]
            },
            {
                "texto": "Estudio una guía y sigo un método",
                "pesos": [
                    -1,
                    -1,
                    2,
                    2,
                    -1
                ]
            },
            {
                "texto": "Busco a otras personas para aprender juntos",
                "pesos": [
                    1,
                    2,
                    0,
                    -1,
                    1
                ]
            }
        ]
    },
    {
        "id": 8,
        "titulo": "Al terminar una semana intensa prefieres...",
        "contexto": "El fin de semana es completamente tuyo.",
        "opciones": [
            {
                "texto": "Una salida animada y llena de estímulos",
                "pesos": [
                    1,
                    2,
                    -1,
                    -1,
                    2
                ]
            },
            {
                "texto": "Descansar con una actividad tranquila",
                "pesos": [
                    -1,
                    -2,
                    1,
                    -1,
                    -2
                ]
            },
            {
                "texto": "Adelantar proyectos personales que tengo pendientes",
                "pesos": [
                    0,
                    -1,
                    2,
                    2,
                    0
                ]
            }
        ]
    },
    {
        "id": 9,
        "titulo": "Te muestran dos ideas diferentes para un proyecto.",
        "contexto": "Solo una de ellas se desarrollará.",
        "opciones": [
            {
                "texto": "Me atrae la idea arriesgada y sorprendente",
                "pesos": [
                    2,
                    0,
                    -2,
                    -1,
                    2
                ]
            },
            {
                "texto": "Elijo la que tiene mejores datos y un plan claro",
                "pesos": [
                    -1,
                    -1,
                    2,
                    2,
                    -1
                ]
            },
            {
                "texto": "Elijo la que emociona y une más al grupo",
                "pesos": [
                    0,
                    2,
                    0,
                    -2,
                    1
                ]
            }
        ]
    },
    {
        "id": 10,
        "titulo": "Piensa en cómo te gustaría terminar el día.",
        "contexto": "No existe una respuesta correcta.",
        "opciones": [
            {
                "texto": "Con una historia memorable que contar",
                "pesos": [
                    2,
                    2,
                    -1,
                    -1,
                    2
                ]
            },
            {
                "texto": "Con una sensación de paz y tiempo para mí",
                "pesos": [
                    -1,
                    -2,
                    0,
                    -2,
                    -2
                ]
            },
            {
                "texto": "Con la satisfacción de haber logrado mis metas",
                "pesos": [
                    0,
                    0,
                    2,
                    2,
                    0
                ]
            }
        ]
    }
]

CATALOGO = [
    {
        "categoria": "Música",
        "titulo": "Indie alternativo",
        "descripcion": "Sonidos creativos para descubrir algo diferente.",
        "vector": [
            2,
            -1,
            -1,
            -1,
            1
        ]
    },
    {
        "categoria": "Música",
        "titulo": "Electrónica energética",
        "descripcion": "Ritmos intensos y ambientes dinámicos.",
        "vector": [
            2,
            2,
            -2,
            -1,
            2
        ]
    },
    {
        "categoria": "Música",
        "titulo": "Lo-fi y acústico",
        "descripcion": "Música suave para la concentración o el descanso.",
        "vector": [
            -1,
            -2,
            1,
            0,
            -2
        ]
    },
    {
        "categoria": "Cine",
        "titulo": "Ciencia ficción",
        "descripcion": "Historias de mundos posibles y grandes ideas.",
        "vector": [
            2,
            -1,
            1,
            2,
            1
        ]
    },
    {
        "categoria": "Cine",
        "titulo": "Drama intimista",
        "descripcion": "Relatos profundos y cercanos a las emociones.",
        "vector": [
            -1,
            -2,
            0,
            -2,
            -1
        ]
    },
    {
        "categoria": "Cine",
        "titulo": "Comedia y aventura",
        "descripcion": "Historias ligeras, divertidas y sorprendentes.",
        "vector": [
            1,
            2,
            -1,
            -1,
            2
        ]
    },
    {
        "categoria": "Comida",
        "titulo": "Cocina fusión",
        "descripcion": "Combinaciones de sabores y recetas novedosas.",
        "vector": [
            2,
            1,
            -2,
            -1,
            1
        ]
    },
    {
        "categoria": "Comida",
        "titulo": "Sabores tradicionales",
        "descripcion": "Recetas familiares y sabores conocidos.",
        "vector": [
            -2,
            -1,
            2,
            -1,
            -1
        ]
    },
    {
        "categoria": "Comida",
        "titulo": "Sabores intensos",
        "descripcion": "Preparaciones audaces y llenas de carácter.",
        "vector": [
            1,
            1,
            -1,
            0,
            2
        ]
    },
    {
        "categoria": "Hobbies",
        "titulo": "Fotografía urbana",
        "descripcion": "Explorar y capturar detalles originales.",
        "vector": [
            2,
            -1,
            -1,
            -1,
            1
        ]
    },
    {
        "categoria": "Hobbies",
        "titulo": "Lectura y escritura",
        "descripcion": "Ideas y relatos para disfrutar en tranquilidad.",
        "vector": [
            -1,
            -2,
            1,
            1,
            -2
        ]
    },
    {
        "categoria": "Hobbies",
        "titulo": "Excursiones y aventura",
        "descripcion": "Descubrir rutas y probar nuevos desafíos.",
        "vector": [
            2,
            1,
            -2,
            0,
            2
        ]
    },
    {
        "categoria": "Estética",
        "titulo": "Minimalismo",
        "descripcion": "Formas limpias y espacios equilibrados.",
        "vector": [
            -1,
            -1,
            2,
            2,
            -2
        ]
    },
    {
        "categoria": "Estética",
        "titulo": "Estilo retro",
        "descripcion": "Colores cálidos y referencias nostálgicas.",
        "vector": [
            -2,
            -1,
            0,
            -2,
            -1
        ]
    },
    {
        "categoria": "Estética",
        "titulo": "Experimental y colorido",
        "descripcion": "Contrastes expresivos y combinaciones atrevidas.",
        "vector": [
            2,
            1,
            -2,
            -1,
            2
        ]
    }
]

USUARIOS_REGISTRADOS = {
    "admin": "1234",
    "estudiante": "algebra2026"
}


# ==============================================================================
# 2. MOTOR MATEMÁTICO (ÁLGEBRA LINEAL, REGRESIÓN Y TRANSFORMACIONES 2D)
# ==============================================================================

def cargar_y_entrenar(ruta_csv="datos_radar_cultural.csv"):
    """
    Carga el CSV de 320 registros, divide en 80% entrenamiento (256) y 20% prueba (64),
    y calcula los coeficientes mediante la ecuación normal:
        β = (Xᵀ X)⁺ Xᵀ Y
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidatos = [
        ruta_csv,
        os.path.join(base_dir, ruta_csv),
        "datos_radar_cultural_uab.csv",
        os.path.join(base_dir, "datos_radar_cultural_uab.csv")
    ]
    for cand in candidatos:
        if os.path.exists(cand):
            ruta_csv = cand
            break

    df = pd.read_csv(ruta_csv)
    U = df[EJES].values
    Y = df[[r["id"] for r in ROLES]].values

    # Matriz de diseño X con columna inicial de 1s (intercepto) -> (320 x 6)
    X = np.column_stack([np.ones(len(df)), U])

    X_train, X_test = X[:256], X[256:]
    Y_train, Y_test = Y[:256], Y[256:]

    # Ecuación normal con pseudoinversa: β = (Xᵀ X)⁺ Xᵀ Y
    XT_X = X_train.T @ X_train
    beta = np.linalg.pinv(XT_X) @ X_train.T @ Y_train

    # Predicción sobre conjunto de prueba: Ŷ = X_test @ β
    Y_pred = X_test @ beta

    # Métricas de validación
    mae_roles = np.mean(np.abs(Y_test - Y_pred), axis=0)
    rmse_roles = np.sqrt(np.mean((Y_test - Y_pred) ** 2, axis=0))
    ss_res = np.sum((Y_test - Y_pred) ** 2, axis=0)
    ss_tot = np.sum((Y_test - np.mean(Y_test, axis=0)) ** 2, axis=0)
    r2_roles = 1.0 - (ss_res / ss_tot)

    metricas = {
        "mae_roles": mae_roles,
        "rmse_roles": rmse_roles,
        "r2_roles": r2_roles,
        "mae_prom": float(np.mean(mae_roles)),
        "rmse_prom": float(np.mean(rmse_roles)),
        "r2_prom": float(np.mean(r2_roles))
    }
    return df, beta, X_train, Y_train, X_test, Y_test, Y_pred, metricas


def calcular_vector_normalizado(indices_respuestas):
    """Suma los 10 vectores de pesos y los normaliza al rango [-5, +5]."""
    suma_pesos = np.zeros(5, dtype=float)
    maximos = np.zeros(5, dtype=float)

    for i, preg in enumerate(PREGUNTAS):
        opcion = preg["opciones"][indices_respuestas[i]]
        suma_pesos += np.array(opcion["pesos"], dtype=float)
        for j in range(5):
            maximos[j] += max(abs(op["pesos"][j]) for op in preg["opciones"])

    vector_u = np.round(5.0 * suma_pesos / maximos, 4)
    return suma_pesos, maximos, vector_u


def similitud_coseno(u, c):
    """Calcula cos(θ) = (u · c) / (||u|| ||c||) y escala a 0-100."""
    nu = np.linalg.norm(u)
    nc = np.linalg.norm(c)
    if nu * nc < 1e-12:
        return 50.0
    cos_t = np.dot(u, c) / (nu * nc)
    return float(np.clip(50.0 * (1.0 + cos_t), 0.0, 100.0))


def matriz_transformacion_2d(tx=0.0, ty=0.0, sx=1.0, sy=1.0, angulo_grados=0.0, shx=0.0, shy=0.0):
    """
    Construye las matrices homogéneas 3x3 de transformación lineal en 2D:
      - Traslación T(tx, ty)
      - Escalado S(sx, sy)
      - Rotación R(θ)
      - Sesgado / Cizallamiento H(shx, shy)
    Retorna la matriz compuesta M = T @ R @ H @ S y cada matriz individual.
    """
    T = np.array([
        [1.0, 0.0, tx],
        [0.0, 1.0, ty],
        [0.0, 0.0, 1.0]
    ], dtype=float)

    S = np.array([
        [sx,  0.0, 0.0],
        [0.0, sy,  0.0],
        [0.0, 0.0, 1.0]
    ], dtype=float)

    rad = math.radians(angulo_grados)
    c, s = math.cos(rad), math.sin(rad)
    R = np.array([
        [c,  -s,  0.0],
        [s,   c,  0.0],
        [0.0, 0.0, 1.0]
    ], dtype=float)

    H = np.array([
        [1.0, shx, 0.0],
        [shy, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ], dtype=float)

    # Composición matricial en coordenadas homogéneas
    M = T @ R @ H @ S
    return M, T, S, R, H


def aplicar_transformacion_puntos(puntos_2d, M):
    """
    Aplica una matriz homogénea 3x3 M a un arreglo de puntos (N x 2):
        P'_hom = (M @ P_homᵀ)ᵀ
    """
    n = puntos_2d.shape[0]
    puntos_hom = np.column_stack([puntos_2d, np.ones(n)])
    transformados_hom = (M @ puntos_hom.T).T
    return transformados_hom[:, :2]


def vector_a_poligono_2d(vector_u):
    """
    Proyecta el vector de 5 ejes u ∈ [-5, +5] en un pentágono 2D centrado en (0, 0),
    donde cada vértice corresponde a un eje con radio proporcional a (u_i + 6) / 2.
    """
    puntos = []
    for k in range(5):
        angulo = math.radians(90 + k * 72)
        radio = 1.5 + (vector_u[k] + 5.0) * 0.35  # radio entre 1.5 y 5.0 unidades
        x = radio * math.cos(angulo)
        y = radio * math.sin(angulo)
        puntos.append([x, y])
    return np.array(puntos, dtype=float)


# ==============================================================================
# 3. INTERFAZ GRÁFICA EN TKINTER (LOGIN + SISTEMA PRINCIPAL)
# ==============================================================================

class VentanaLogin(tk.Toplevel):
    """Ventana modal de inicio de sesión y registro de usuarios."""

    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success
        self.title("Inicio de Sesión — Radar Cultural + Alter Ego Social")
        self.geometry("440x430")
        self.resizable(False, False)
        self.configure(bg="#f5f6fb")
        self.protocol("WM_DELETE_WINDOW", master.destroy)

        self.intentos = 3
        self._construir_ui()
        self.grab_set()

    def _construir_ui(self):
        card = tk.Frame(self, bg="white", bd=1, relief="solid", padx=28, pady=24)
        card.pack(fill="both", expand=True, padx=22, pady=22)

        tk.Label(
            card, text="CONTROL DE ACCESO AL SISTEMA",
            font=("Segoe UI", 9, "bold"), fg="#6054df", bg="#ebe9ff", padx=10, pady=4
        ).pack(anchor="w")

        tk.Label(
            card, text="Iniciar Sesión",
            font=("Segoe UI", 18, "bold"), fg="#202344", bg="white"
        ).pack(anchor="w", pady=(10, 2))

        tk.Label(
            card, text="Ingresa tus credenciales para acceder al sistema predictivo.",
            font=("Segoe UI", 9), fg="#6d778f", bg="white"
        ).pack(anchor="w", pady=(0, 14))

        tk.Label(card, text="Usuario:", font=("Segoe UI", 9, "bold"), fg="#333", bg="white").pack(anchor="w")
        self.entry_user = ttk.Entry(card, font=("Segoe UI", 10))
        self.entry_user.pack(fill="x", pady=(3, 10), ipady=4)

        tk.Label(card, text="Contraseña:", font=("Segoe UI", 9, "bold"), fg="#333", bg="white").pack(anchor="w")
        self.entry_pass = ttk.Entry(card, font=("Segoe UI", 10), show="•")
        self.entry_pass.pack(fill="x", pady=(3, 12), ipady=4)
        self.entry_pass.bind("<Return>", lambda e: self._verificar_login())

        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(fill="x", pady=(4, 10))

        ttk.Button(btn_frame, text="Entrar al Sistema →", command=self._verificar_login).pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=4)
        ttk.Button(btn_frame, text="Registrar Usuario", command=self._registrar).pack(side="left", expand=True, fill="x", padx=(5, 0), ipady=4)

        demo_box = tk.Frame(card, bg="#f4f3ff", padx=12, pady=10)
        demo_box.pack(fill="x", pady=(8, 0))

        tk.Label(
            demo_box,
            text="Demo: admin / 1234  |  estudiante / algebra2026",
            font=("Segoe UI", 8, "bold"), fg="#4f42c9", bg="#f4f3ff"
        ).pack(side="left")

        ttk.Button(demo_box, text="Rellenar", command=self._rellenar_demo).pack(side="right")

    def _rellenar_demo(self):
        self.entry_user.delete(0, tk.END)
        self.entry_user.insert(0, "admin")
        self.entry_pass.delete(0, tk.END)
        self.entry_pass.insert(0, "1234")

    def _verificar_login(self):
        u = self.entry_user.get().strip()
        p = self.entry_pass.get().strip()
        if not u or not p:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa usuario y contraseña.", parent=self)
            return

        if u in USUARIOS_REGISTRADOS and USUARIOS_REGISTRADOS[u] == p:
            self.destroy()
            self.on_success(u)
        else:
            self.intentos -= 1
            if self.intentos > 0:
                messagebox.showerror(
                    "Acceso denegado",
                    f"Usuario o contraseña incorrectos.\nTe quedan {self.intentos} intento(s).",
                    parent=self
                )
            else:
                messagebox.showerror("Bloqueado", "Has agotado los 3 intentos permitidos.", parent=self)
                self.master.destroy()

    def _registrar(self):
        u = self.entry_user.get().strip()
        p = self.entry_pass.get().strip()
        if not u or len(p) < 4:
            messagebox.showwarning(
                "Registro inválido",
                "Escribe un usuario y una contraseña de al menos 4 caracteres en los campos de arriba.",
                parent=self
            )
            return
        if u in USUARIOS_REGISTRADOS:
            messagebox.showwarning("Usuario existente", f"El usuario '{u}' ya está registrado.", parent=self)
            return
        USUARIOS_REGISTRADOS[u] = p
        messagebox.showinfo("Registro exitoso", f"Usuario '{u}' creado. Ahora presiona 'Entrar al Sistema'.", parent=self)


class AplicacionRadarCultural(tk.Tk):
    """Ventana principal del sistema con Tkinter."""

    def __init__(self):
        super().__init__()
        self.title("UAB — Álgebra Lineal | Radar Cultural + Alter Ego Social & Transformaciones 2D")
        self.geometry("1160x740")
        self.minsize(1020, 660)
        self.configure(bg="#f5f6fb")

        # Cargar datos y entrenar modelo lineal al iniciar
        self.df, self.beta, self.X_train, self.Y_train, self.X_test, self.Y_test, self.Y_pred, self.metricas = cargar_y_entrenar()

        # Vector inicial (ejemplo Anexo A) para visualizar en transformaciones 2D
        _, _, self.vector_actual = calcular_vector_normalizado([0, 1, 2, 0, 1, 2, 0, 1, 2, 0])
        self.usuario_activo = None

        self._configurar_estilos()
        self.withdraw()  # Ocultar ventana principal hasta iniciar sesión
        VentanaLogin(self, self._al_iniciar_sesion)

    def _configurar_estilos(self):
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("TNotebook", background="#f5f6fb", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[14, 8])
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=24)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def _al_iniciar_sesion(self, usuario):
        self.usuario_activo = usuario
        self.deiconify()
        for w in self.winfo_children():
            w.destroy()
        self._construir_interfaz_principal()

    def _cerrar_sesion(self):
        self.usuario_activo = None
        self.withdraw()
        VentanaLogin(self, self._al_iniciar_sesion)

    def _construir_interfaz_principal(self):
        # Barra superior
        header = tk.Frame(self, bg="white", height=58, bd=1, relief="solid")
        header.pack(fill="x")

        tk.Label(
            header,
            text="◈ RADAR CULTURAL + ALTER EGO SOCIAL  |  ÁLGEBRA LINEAL (UAB)",
            font=("Segoe UI", 12, "bold"), fg="#6054df", bg="white", padx=16
        ).pack(side="left", pady=12)

        right_box = tk.Frame(header, bg="white")
        right_box.pack(side="right", padx=16)

        tk.Label(
            right_box, text=f"Usuario activo: {self.usuario_activo}",
            font=("Segoe UI", 9, "bold"), fg="#202344", bg="#ebe9ff", padx=10, pady=4
        ).pack(side="left", padx=(0, 10))

        ttk.Button(right_box, text="Cerrar Sesión", command=self._cerrar_sesion).pack(side="left")

        # Cuaderno de pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=14, pady=12)

        self.tab_modelo = tk.Frame(self.notebook, bg="#f5f6fb")
        self.tab_grafica = tk.Frame(self.notebook, bg="#f5f6fb")
        self.tab_prediccion = tk.Frame(self.notebook, bg="#f5f6fb")
        self.tab_trans2d = tk.Frame(self.notebook, bg="#f5f6fb")

        self.notebook.add(self.tab_modelo, text="1. Datos CSV y Modelo Lineal (β)")
        self.notebook.add(self.tab_grafica, text="2. Gráfica y Validación (MAE, RMSE, R²)")
        self.notebook.add(self.tab_prediccion, text="3. Predicción y Radar Cultural")
        self.notebook.add(self.tab_trans2d, text="4. Transformaciones Lineales 2D")

        self._construir_tab_modelo()
        self._construir_tab_grafica()
        self._construir_tab_prediccion()
        self._construir_tab_transformaciones_2d()

    # --------------------------------------------------------------------------
    # PESTAÑA 1: DATOS CSV, MATRIZ β Y MÉTRICAS
    # --------------------------------------------------------------------------
    def _construir_tab_modelo(self):
        top_info = tk.Frame(self.tab_modelo, bg="white", padx=16, pady=12, bd=1, relief="solid")
        top_info.pack(fill="x", pady=(4, 10))

        tk.Label(
            top_info,
            text="Propósito del Sistema y Modelo Matemático",
            font=("Segoe UI", 11, "bold"), fg="#202344", bg="white"
        ).pack(anchor="w")

        tk.Label(
            top_info,
            text=(
                "Resuelve el problema de 'inicio en frío' (cold-start) perfilando a un usuario mediante 10 preguntas en 5 ejes "
                "normalizados [-5, +5]. Entrena una regresión lineal múltiple con 320 registros ficticios (256 entrenamiento / 64 prueba) "
                "mediante la Ecuación Normal:  β = (XᵀX)⁺ XᵀY   y predice 4 perfiles sociales con:  Ŷ = Xβ."
            ),
            font=("Segoe UI", 9), fg="#4f566b", bg="white", wraplength=1080, justify="left"
        ).pack(anchor="w", pady=(4, 0))

        # Contenedor dividido: Izquierda (CSV) | Derecha (Matriz Beta + Métricas)
        mid = tk.Frame(self.tab_modelo, bg="#f5f6fb")
        mid.pack(fill="both", expand=True)

        left = tk.LabelFrame(mid, text=" Dataset cargado: datos_radar_cultural.csv (320 filas) ", font=("Segoe UI", 9, "bold"), bg="white", padx=10, pady=8)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        cols_csv = ["id", "novedad", "social", "estructura", "analitico", "intensidad", "explorador", "conector", "estratega", "observador"]
        tree_csv = ttk.Treeview(left, columns=cols_csv, show="headings", height=16)
        for col in cols_csv:
            tree_csv.heading(col, text=col)
            tree_csv.column(col, width=72, anchor="center")
        tree_csv.column("id", width=42)

        for _, row in self.df[cols_csv].head(50).iterrows():
            vals = [int(row["id"])] + [f"{row[c]:.2f}" for c in cols_csv[1:]]
            tree_csv.insert("", "end", values=vals)

        sb_csv = ttk.Scrollbar(left, orient="vertical", command=tree_csv.yview)
        tree_csv.configure(yscrollcommand=sb_csv.set)
        tree_csv.pack(side="left", fill="both", expand=True)
        sb_csv.pack(side="right", fill="y")

        right = tk.Frame(mid, bg="#f5f6fb", width=440)
        right.pack(side="right", fill="both")

        # Matriz Beta
        box_beta = tk.LabelFrame(right, text=" Matriz de Coeficientes β (6 × 4) ", font=("Segoe UI", 9, "bold"), bg="white", padx=10, pady=8)
        box_beta.pack(fill="x", pady=(0, 8))

        cols_beta = ["Variable", "Explorador", "Conector", "Estratega", "Observador"]
        tree_beta = ttk.Treeview(box_beta, columns=cols_beta, show="headings", height=6)
        for c in cols_beta:
            tree_beta.heading(c, text=c)
            tree_beta.column(c, width=82, anchor="center")

        etiquetas = ["Intercepto"] + EJES
        for i, et in enumerate(etiquetas):
            vals = [et] + [f"{self.beta[i, j]:+.4f}" for j in range(4)]
            tree_beta.insert("", "end", values=vals)
        tree_beta.pack(fill="x")

        # Métricas de Validación
        box_met = tk.LabelFrame(right, text=" Validación en Conjunto de Prueba (64 filas) ", font=("Segoe UI", 9, "bold"), bg="white", padx=10, pady=8)
        box_met.pack(fill="both", expand=True)

        cols_met = ["Perfil Social", "MAE", "RMSE", "R²"]
        tree_met = ttk.Treeview(box_met, columns=cols_met, show="headings", height=5)
        for c in cols_met:
            tree_met.heading(c, text=c)
            tree_met.column(c, width=98, anchor="center")

        for j, r in enumerate(ROLES):
            tree_met.insert("", "end", values=[
                r["nombre"],
                f"{self.metricas['mae_roles'][j]:.3f}",
                f"{self.metricas['rmse_roles'][j]:.3f}",
                f"{self.metricas['r2_roles'][j]:.3f}"
            ])
        tree_met.insert("", "end", values=[
            "PROMEDIO",
            f"{self.metricas['mae_prom']:.3f}",
            f"{self.metricas['rmse_prom']:.3f}",
            f"{self.metricas['r2_prom']:.3f}"
        ])
        tree_met.pack(fill="x", pady=(0, 8))

        tk.Label(
            box_met,
            text=(
                "Interpretación de coeficientes β:\n"
                "• Cada valor indica cuánto cambia el puntaje del rol al subir 1 unidad en ese eje.\n"
                "• Ej: 'social' suma +5.20 en Conector y resta -4.56 en Observador."
            ),
            font=("Segoe UI", 9), fg="#42465a", bg="#f4f3ff", padx=10, pady=8, justify="left"
        ).pack(fill="x")

    # --------------------------------------------------------------------------
    # PESTAÑA 2: GRÁFICA DE RESULTADOS (MATPLOTLIB EMBEBIDO)
    # --------------------------------------------------------------------------
    def _construir_tab_grafica(self):
        frame = tk.Frame(self.tab_grafica, bg="white", padx=14, pady=12, bd=1, relief="solid")
        frame.pack(fill="both", expand=True, pady=4)

        top_bar = tk.Frame(frame, bg="white")
        top_bar.pack(fill="x", pady=(0, 6))

        tk.Label(
            top_bar,
            text="Validación Visual: Valores Reales (Y) vs. Valores Predichos (Ŷ = Xβ)",
            font=("Segoe UI", 11, "bold"), fg="#202344", bg="white"
        ).pack(side="left")

        ttk.Button(top_bar, text="Guardar Imagen PNG", command=self._guardar_png_grafica).pack(side="right")

        fig = Figure(figsize=(8.5, 4.4), dpi=100)
        ax = fig.add_subplot(111)

        y_real = self.Y_test.flatten()
        y_est = self.Y_pred.flatten()

        ax.scatter(y_real, y_est, color="#6256e3", alpha=0.78, edgecolors="white", s=48, label="Datos de prueba (Real vs. Estimado)")
        mn = min(y_real.min(), y_est.min()) - 2
        mx = max(y_real.max(), y_est.max()) + 2
        ax.plot([mn, mx], [mn, mx], "--", color="#555555", linewidth=1.6, label="Ajuste ideal (Y = Ŷ)")

        ax.set_title("Dispersión de Predicciones en el Conjunto de Prueba (64 filas × 4 roles)", fontsize=11, fontweight="bold")
        ax.set_xlabel("Valor Real Observado (Y)")
        ax.set_ylabel("Valor Estimado por el Modelo (Ŷ = Xβ)")
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        tk.Label(
            frame,
            text=(
                f"Interpretación de resultados: Los puntos se agrupan estrechamente sobre la línea diagonal Y = Ŷ, "
                f"confirmando un coeficiente de determinación promedio R² = {self.metricas['r2_prom']:.3f} "
                f"y un error absoluto medio MAE = {self.metricas['mae_prom']:.3f} puntos en una escala de 0 a 100."
            ),
            font=("Segoe UI", 9), fg="#333", bg="#f4f3ff", padx=12, pady=8, wraplength=1060, justify="left"
        ).pack(fill="x", pady=(6, 0))

    def _guardar_png_grafica(self):
        fig = Figure(figsize=(8, 5.5), dpi=150)
        ax = fig.add_subplot(111)
        y_real = self.Y_test.flatten()
        y_est = self.Y_pred.flatten()
        ax.scatter(y_real, y_est, color="#6256e3", alpha=0.78, edgecolors="white", s=50, label="Muestras de prueba")
        mn, mx = min(y_real.min(), y_est.min()) - 2, max(y_real.max(), y_est.max()) + 2
        ax.plot([mn, mx], [mn, mx], "--", color="#555555", linewidth=1.8, label="Ajuste ideal (Y = Ŷ)")
        ax.set_title("Valores Reales vs. Estimados (Prueba)")
        ax.set_xlabel("Valor Real Observado (Y)")
        ax.set_ylabel("Valor Estimado (Ŷ = Xβ)")
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend()
        fig.tight_layout()
        fig.savefig("grafica_resultados.png")
        messagebox.showinfo("Gráfica guardada", "Se guardó 'grafica_resultados.png' en la carpeta del proyecto.")

    # --------------------------------------------------------------------------
    # PESTAÑA 3: CUESTIONARIO Y PREDICCIÓN EN VIVO
    # --------------------------------------------------------------------------
    def _construir_tab_prediccion(self):
        cont = tk.Frame(self.tab_prediccion, bg="#f5f6fb")
        cont.pack(fill="both", expand=True, pady=4)

        # Panel izquierdo: 10 preguntas con scroll
        left = tk.LabelFrame(cont, text=" Entrada de Datos: Cuestionario de 10 Preguntas ", font=("Segoe UI", 9, "bold"), bg="white", padx=8, pady=8)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        btn_bar = tk.Frame(left, bg="white")
        btn_bar.pack(fill="x", pady=(0, 6))

        ttk.Button(btn_bar, text="Cargar Datos de Prueba (Anexo A)", command=self._cargar_prueba_anexo_a).pack(side="left", padx=(0, 6))
        ttk.Button(btn_bar, text="Calcular Predicción y Radar →", command=self._ejecutar_prediccion_usuario).pack(side="left")

        canvas_q = tk.Canvas(left, bg="white", highlightthickness=0)
        sb_q = ttk.Scrollbar(left, orient="vertical", command=canvas_q.yview)
        scroll_frame = tk.Frame(canvas_q, bg="white")

        scroll_frame.bind("<Configure>", lambda e: canvas_q.configure(scrollregion=canvas_q.bbox("all")))
        canvas_q.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas_q.configure(yscrollcommand=sb_q.set)

        canvas_q.pack(side="left", fill="both", expand=True)
        sb_q.pack(side="right", fill="y")

        self.vars_preguntas = []
        for idx, preg in enumerate(PREGUNTAS):
            var = tk.IntVar(value=[0, 1, 2, 0, 1, 2, 0, 1, 2, 0][idx])
            self.vars_preguntas.append(var)

            card_q = tk.Frame(scroll_frame, bg="#f9f9fd", padx=10, pady=7, bd=1, relief="groove")
            card_q.pack(fill="x", pady=4, padx=4)

            tk.Label(
                card_q, text=f"{preg['id']}. {preg['titulo']}",
                font=("Segoe UI", 9, "bold"), fg="#202344", bg="#f9f9fd", anchor="w"
            ).pack(fill="x")

            for op_i, op in enumerate(preg["opciones"]):
                letra = "ABC"[op_i]
                tk.Radiobutton(
                    card_q,
                    text=f"[{letra}] {op['texto']}   (pesos: {op['pesos']})",
                    variable=var, value=op_i,
                    font=("Segoe UI", 9), bg="#f9f9fd", anchor="w"
                ).pack(fill="x")

        # Panel derecho: Resultados
        right = tk.LabelFrame(cont, text=" Resultados de la Predicción y Similitud del Coseno ", font=("Segoe UI", 9, "bold"), bg="white", padx=12, pady=10, width=450)
        right.pack(side="right", fill="both")

        self.txt_resultados = tk.Text(right, font=("Consolas", 10), bg="#fafaff", fg="#202344", wrap="word", padx=10, pady=10)
        self.txt_resultados.pack(fill="both", expand=True)

        self._ejecutar_prediccion_usuario()

    def _cargar_prueba_anexo_a(self):
        secuencia = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0]  # A, B, C, A, B, C, A, B, C, A
        for var, val in zip(self.vars_preguntas, secuencia):
            var.set(val)
        self._ejecutar_prediccion_usuario()

    def _ejecutar_prediccion_usuario(self):
        respuestas = [v.get() for v in self.vars_preguntas]
        s, m, u = calcular_vector_normalizado(respuestas)
        self.vector_actual = u

        # Predicción por regresión lineal: Ŷ = [1, u] @ β
        x_ext = np.concatenate([[1.0], u])
        puntajes = np.clip(x_ext @ self.beta, 0.0, 100.0)

        ranking = sorted(
            zip([r["nombre"] for r in ROLES], [r["descripcion"] for r in ROLES], puntajes),
            key=lambda x: x[2], reverse=True
        )

        out = []
        out.append("1) VECTOR DEL USUARIO NORMALIZADO [-5, +5]")
        out.append("-" * 46)
        out.append(f"Suma bruta s   : {s.astype(int).tolist()}")
        out.append(f"Máximos M      : {m.astype(int).tolist()}")
        out.append(f"Vector u       : {u.tolist()}\n")

        out.append("2) ALTER EGO SOCIAL (Regresión Lineal Ŷ = x·β)")
        out.append("-" * 46)
        out.append(f">>> PERFIL DOMINANTE: {ranking[0][0].upper()} ({ranking[0][2]:.2f} pts)")
        out.append(f"{ranking[0][1]}\n")
        for nombre, _, pts in ranking:
            out.append(f"  • {nombre:<15} : {pts:6.2f} / 100")

        out.append("\n3) RADAR CULTURAL (Similitud del Coseno)")
        out.append("-" * 46)
        for cat in ["Música", "Cine", "Comida", "Hobbies", "Estética"]:
            items = [it for it in CATALOGO if it["categoria"] == cat]
            mejor = max(items, key=lambda it: similitud_coseno(u, np.array(it["vector"], dtype=float)))
            score = similitud_coseno(u, np.array(mejor["vector"], dtype=float))
            out.append(f"  • {cat:<9} -> {mejor['titulo']} ({score:.1f}/100)")

        out.append("\n[Nota] El polígono de la pestaña 'Transformaciones Lineales 2D'")
        out.append("se ha actualizado automáticamente con este vector de perfil.")

        self.txt_resultados.delete("1.0", tk.END)
        self.txt_resultados.insert("1.0", "\n".join(out))

        if hasattr(self, "canvas_2d"):
            self._actualizar_transformacion_2d()

    # --------------------------------------------------------------------------
    # PESTAÑA 4: TRANSFORMACIONES LINEALES EN 2D (TRASLACIÓN, ESCALADO, ROTACIÓN, SESGADO)
    # --------------------------------------------------------------------------
    def _construir_tab_transformaciones_2d(self):
        cont = tk.Frame(self.tab_trans2d, bg="#f5f6fb")
        cont.pack(fill="both", expand=True, pady=4)

        # Panel izquierdo: Controles de las 4 transformaciones + presets
        ctrl = tk.LabelFrame(cont, text=" Parámetros de Transformaciones Lineales 2D ", font=("Segoe UI", 9, "bold"), bg="white", padx=12, pady=10, width=360)
        ctrl.pack(side="left", fill="y", padx=(0, 8))

        tk.Label(
            ctrl,
            text="Aplica transformaciones homogéneas 3×3 al polígono 2D del perfil Radar Cultural:",
            font=("Segoe UI", 9), fg="#555", bg="white", wraplength=330, justify="left"
        ).pack(anchor="w", pady=(0, 8))

        self.var_tx = tk.DoubleVar(value=0.0)
        self.var_ty = tk.DoubleVar(value=0.0)
        self.var_sx = tk.DoubleVar(value=1.0)
        self.var_sy = tk.DoubleVar(value=1.0)
        self.var_rot = tk.DoubleVar(value=0.0)
        self.var_shx = tk.DoubleVar(value=0.0)
        self.var_shy = tk.DoubleVar(value=0.0)

        self._crear_slider(ctrl, "1. Traslación X (tx):", self.var_tx, -4.0, 4.0, 0.5)
        self._crear_slider(ctrl, "   Traslación Y (ty):", self.var_ty, -4.0, 4.0, 0.5)
        self._crear_slider(ctrl, "2. Escalado X (sx):", self.var_sx, 0.4, 2.0, 0.1)
        self._crear_slider(ctrl, "   Escalado Y (sy):", self.var_sy, 0.4, 2.0, 0.1)
        self._crear_slider(ctrl, "3. Rotación θ (grados):", self.var_rot, -180.0, 180.0, 15.0)
        self._crear_slider(ctrl, "4. Sesgado X (shx):", self.var_shx, -1.0, 1.0, 0.1)
        self._crear_slider(ctrl, "   Sesgado Y (shy):", self.var_shy, -1.0, 1.0, 0.1)

        # Botones rápidos para demostrar cada transformación por separado en la defensa
        presets = tk.LabelFrame(ctrl, text=" Demostración Rápida (1 clic) ", font=("Segoe UI", 9, "bold"), bg="#f9f9fd", padx=8, pady=6)
        presets.pack(fill="x", pady=(10, 0))

        row1 = tk.Frame(presets, bg="#f9f9fd")
        row1.pack(fill="x", pady=2)
        ttk.Button(row1, text="Traslación", command=lambda: self._preset(2.0, 1.5, 1.0, 1.0, 0.0, 0.0, 0.0)).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(row1, text="Escalado", command=lambda: self._preset(0.0, 0.0, 1.5, 0.7, 0.0, 0.0, 0.0)).pack(side="left", expand=True, fill="x", padx=2)

        row2 = tk.Frame(presets, bg="#f9f9fd")
        row2.pack(fill="x", pady=2)
        ttk.Button(row2, text="Rotación 45°", command=lambda: self._preset(0.0, 0.0, 1.0, 1.0, 45.0, 0.0, 0.0)).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(row2, text="Sesgado", command=lambda: self._preset(0.0, 0.0, 1.0, 1.0, 0.0, 0.5, 0.0)).pack(side="left", expand=True, fill="x", padx=2)

        row3 = tk.Frame(presets, bg="#f9f9fd")
        row3.pack(fill="x", pady=2)
        ttk.Button(row3, text="Combinada", command=lambda: self._preset(1.5, 1.0, 1.2, 1.2, 30.0, 0.3, 0.0)).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(row3, text="Reiniciar", command=lambda: self._preset(0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0)).pack(side="left", expand=True, fill="x", padx=2)

        # Panel central: Plano cartesiano 2D en Canvas
        center = tk.LabelFrame(cont, text=" Plano Cartesiano 2D: Figura Original vs. Transformada ", font=("Segoe UI", 9, "bold"), bg="white", padx=8, pady=8)
        center.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self.canvas_2d = tk.Canvas(center, bg="white", width=440, height=440, highlightthickness=1, highlightbackground="#dfe3ee")
        self.canvas_2d.pack(fill="both", expand=True)
        self.canvas_2d.bind("<Configure>", lambda e: self._actualizar_transformacion_2d())

        # Panel derecho: Matrices y coordenadas calculadas
        right = tk.LabelFrame(cont, text=" Matriz Homogénea M (3×3) y Coordenadas ", font=("Segoe UI", 9, "bold"), bg="white", padx=10, pady=8, width=320)
        right.pack(side="right", fill="y")

        self.txt_matriz_2d = tk.Text(right, font=("Consolas", 9), bg="#fafaff", fg="#202344", width=38, wrap="word", padx=8, pady=8)
        self.txt_matriz_2d.pack(fill="both", expand=True)

        self._actualizar_transformacion_2d()

    def _crear_slider(self, parent, label, var, frm, to, res):
        row = tk.Frame(parent, bg="white")
        row.pack(fill="x", pady=2)
        tk.Label(row, text=label, font=("Segoe UI", 9, "bold"), fg="#333", bg="white", width=20, anchor="w").pack(side="left")
        scale = tk.Scale(
            row, variable=var, from_=frm, to=to, resolution=res,
            orient="horizontal", length=150, bg="white", highlightthickness=0,
            command=lambda val: self._actualizar_transformacion_2d()
        )
        scale.pack(side="right")

    def _preset(self, tx, ty, sx, sy, rot, shx, shy):
        self.var_tx.set(tx)
        self.var_ty.set(ty)
        self.var_sx.set(sx)
        self.var_sy.set(sy)
        self.var_rot.set(rot)
        self.var_shx.set(shx)
        self.var_shy.set(shy)
        self._actualizar_transformacion_2d()

    def _actualizar_transformacion_2d(self):
        tx, ty = self.var_tx.get(), self.var_ty.get()
        sx, sy = self.var_sx.get(), self.var_sy.get()
        rot = self.var_rot.get()
        shx, shy = self.var_shx.get(), self.var_shy.get()

        M, _, _, _, _ = matriz_transformacion_2d(tx, ty, sx, sy, rot, shx, shy)
        pts_orig = vector_a_poligono_2d(self.vector_actual)
        pts_trans = aplicar_transformacion_puntos(pts_orig, M)

        # Dibujar en el Canvas 2D
        c = self.canvas_2d
        c.delete("all")
        w = max(c.winfo_width(), 380)
        h = max(c.winfo_height(), 380)
        cx, cy = w / 2.0, h / 2.0
        escala_px = min(w, h) / 18.0  # Rango visual aproximado [-9, +9]

        def to_px(pt):
            return cx + pt[0] * escala_px, cy - pt[1] * escala_px

        # Cuadrícula y ejes coordenados
        for g in range(-8, 9):
            gx, _ = to_px((g, 0))
            _, gy = to_px((0, g))
            c.create_line(gx, 10, gx, h - 10, fill="#f0f2f8")
            c.create_line(10, gy, w - 10, gy, fill="#f0f2f8")

        c.create_line(10, cy, w - 10, cy, fill="#9aa3b8", width=1.5, arrow=tk.LAST)
        c.create_line(cx, h - 10, cx, 10, fill="#9aa3b8", width=1.5, arrow=tk.LAST)
        c.create_text(w - 20, cy - 12, text="X", font=("Segoe UI", 9, "bold"), fill="#555")
        c.create_text(cx + 12, 18, text="Y", font=("Segoe UI", 9, "bold"), fill="#555")

        # Polígono original (línea punteada gris)
        poly_orig_px = [coord for p in pts_orig for coord in to_px(p)]
        c.create_polygon(poly_orig_px, outline="#7f889c", fill="", width=2, dash=(5, 4))

        # Polígono transformado (línea sólida morada)
        poly_trans_px = [coord for p in pts_trans for coord in to_px(p)]
        c.create_polygon(poly_trans_px, outline="#6054df", fill="#ebe9ff", stipple="gray25", width=2.5)

        # Vértices y etiquetas
        etiquetas_ejes = ["Nov", "Soc", "Est", "Ana", "Int"]
        for i in range(5):
            ox, oy = to_px(pts_orig[i])
            tx_p, ty_p = to_px(pts_trans[i])
            c.create_oval(ox - 3, oy - 3, ox + 3, oy + 3, fill="#7f889c", outline="")
            c.create_oval(tx_p - 4.5, ty_p - 4.5, tx_p + 4.5, ty_p + 4.5, fill="#6054df", outline="white")
            c.create_text(tx_p + 14, ty_p - 8, text=f"{etiquetas_ejes[i]}'", font=("Segoe UI", 8, "bold"), fill="#4f42c9")

        # Leyenda en canvas
        c.create_rectangle(14, 14, 215, 62, fill="white", outline="#dfe3ee")
        c.create_line(24, 28, 52, 28, fill="#7f889c", width=2, dash=(4, 3))
        c.create_text(60, 28, text="Polígono Original (P)", anchor="w", font=("Segoe UI", 8), fill="#555")
        c.create_line(24, 46, 52, 46, fill="#6054df", width=2.5)
        c.create_text(60, 46, text="Transformado (P' = M·P)", anchor="w", font=("Segoe UI", 8, "bold"), fill="#4f42c9")

        # Mostrar matriz M y tabla de vértices en texto
        lines = [
            "ECUACIÓN MATRICIAL:",
            "P' = M · P  (M = T · R · H · S)",
            "",
            "Matriz Compuesta M (3 × 3):",
            f"  [{M[0,0]:+7.3f}  {M[0,1]:+7.3f}  {M[0,2]:+7.3f}]",
            f"  [{M[1,0]:+7.3f}  {M[1,1]:+7.3f}  {M[1,2]:+7.3f}]",
            f"  [{M[2,0]:+7.3f}  {M[2,1]:+7.3f}  {M[2,2]:+7.3f}]",
            "",
            "PARÁMETROS ACTIVOS:",
            f"• Traslación : tx={tx:+.1f}, ty={ty:+.1f}",
            f"• Escalado   : sx={sx:.2f}, sy={sy:.2f}",
            f"• Rotación   : θ={rot:+.0f}°",
            f"• Sesgado    : shx={shx:+.2f}, shy={shy:+.2f}",
            "",
            "VÉRTICES (Original -> Transformado):"
        ]
        for i, et in enumerate(etiquetas_ejes):
            lines.append(
                f"{et}: ({pts_orig[i,0]:+5.2f},{pts_orig[i,1]:+5.2f}) -> "
                f"({pts_trans[i,0]:+5.2f},{pts_trans[i,1]:+5.2f})"
            )

        self.txt_matriz_2d.delete("1.0", tk.END)
        self.txt_matriz_2d.insert("1.0", "\n".join(lines))


if __name__ == "__main__":
    app = AplicacionRadarCultural()
    app.mainloop()
