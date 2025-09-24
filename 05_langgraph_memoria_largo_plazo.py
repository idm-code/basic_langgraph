# === LangGraph: Memoria a largo plazo (SQLite) ===
# Este ejemplo muestra cómo usar LangGraph para gestionar memoria persistente
# en una base de datos SQLite y aplicar lógica condicional en un grafo.
# Ideal para tutoriales y aprendizaje.

import sqlite3
from langgraph.graph import StateGraph, END  # Importamos las clases principales de LangGraph

# --- Funciones de memoria persistente ---
def inicializar_db():
    """
    Inicializa la base de datos y la tabla de historial si no existen.
    Devuelve la conexión SQLite.
    """
    conn = sqlite3.connect("05_memoria.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rol TEXT,
            contenido TEXT
        )
    """)
    conn.commit()
    return conn

def guardar_mensaje(conn, rol, contenido):
    """
    Guarda un mensaje en la base de datos.
    """
    cursor = conn.cursor()
    cursor.execute("INSERT INTO historial (rol, contenido) VALUES (?, ?)", (rol, contenido))
    conn.commit()

def obtener_historial(conn):
    """
    Recupera el historial completo de la base de datos.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT rol, contenido FROM historial ORDER BY id ASC")
    return cursor.fetchall()

# --- Nodos del grafo ---
def nodo_llm(state):
    """
    Nodo que guarda el input en la base y decide la ruta.
    """
    pregunta = state.get("ultimo_input", "")  # Recupera el input del usuario
    guardar_mensaje(state["db"], "usuario", pregunta)  # Guarda el input en la base
    # Lógica condicional para decidir la ruta
    if "precio" in pregunta.lower():
        respuesta = "🤖 El agente detecta que preguntas por precios. Te redirige a la ruta de 'consultas financieras'."
        state["ruta"] = "finanzas"
    elif "clima" in pregunta.lower():
        respuesta = "🤖 El agente detecta que preguntas por el clima. Te redirige a la ruta de 'consultas meteorológicas'."
        state["ruta"] = "clima"
    else:
        respuesta = "🤖 El agente no entiende bien la intención. Te responde de forma genérica."
        state["ruta"] = "general"
    print(respuesta)
    return state

def nodo_finanzas(state):
    """
    Nodo que responde a preguntas financieras y guarda la respuesta en la base.
    """
    respuesta = "📈 Respuesta del módulo de finanzas: el precio de BTC está en 42k (ejemplo)."
    print(respuesta)
    guardar_mensaje(state["db"], "agente", respuesta)
    return state

def nodo_clima(state):
    """
    Nodo que responde a preguntas sobre el clima y guarda la respuesta en la base.
    """
    respuesta = "🌦️ Respuesta del módulo de clima: hoy está soleado con 25°C (ejemplo)."
    print(respuesta)
    guardar_mensaje(state["db"], "agente", respuesta)
    return state

def nodo_general(state):
    """
    Nodo que responde de forma genérica y guarda la respuesta en la base.
    """
    respuesta = "💬 Respuesta general: gracias por tu pregunta."
    print(respuesta)
    guardar_mensaje(state["db"], "agente", respuesta)
    return state

def nodo_memoria(state):
    """
    Nodo que muestra el historial completo guardado en la base de datos.
    """
    print("🗂️ Historial completo:")
    for rol, contenido in obtener_historial(state["db"]):
        print(f"{rol}: {contenido}")
    return state

# --- Construcción del grafo ---
workflow = StateGraph(dict)  # Usamos dict estándar como estado
workflow.add_node("llm", nodo_llm)         # Nodo de decisión y memoria
workflow.add_node("finanzas", nodo_finanzas)  # Nodo de finanzas
workflow.add_node("clima", nodo_clima)        # Nodo de clima
workflow.add_node("general", nodo_general)    # Nodo general
workflow.add_node("memoria", nodo_memoria)    # Nodo que muestra el historial
workflow.set_entry_point("llm")  # El grafo empieza en el nodo de decisión
workflow.add_conditional_edges(
    "llm",  # Nodo desde el que se ramifica
    lambda state: state["ruta"],  # Función que decide la ruta según el estado
    {
        "finanzas": "finanzas",  # Si ruta es 'finanzas', va al nodo_finanzas
        "clima": "clima",        # Si ruta es 'clima', va al nodo_clima
        "general": "general",    # Si ruta es 'general', va al nodo_general
    },
)
workflow.add_edge("finanzas", "memoria")  # Todas las ramas terminan mostrando el historial
workflow.add_edge("clima", "memoria")
workflow.add_edge("general", "memoria")
workflow.add_edge("memoria", END)
grafo = workflow.compile()  # Compilamos el grafo para poder ejecutarlo

# --- Ejecución principal ---
print("=== LangGraph: Memoria a largo plazo (SQLite) ===")
db = inicializar_db()  # Inicializa la base y la tabla correctamente
user_input = input("👤 Usuario: ")  # Recoge el input antes de invocar el grafo
estado = {"db": db, "ultimo_input": user_input}  # Estado inicial con conexión y input
grafo.invoke(estado)  # Ejecuta el grafo completo