import sqlite3
from langgraph.graph import StateGraph, END
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class Estado(dict):
    """Estado con memoria híbrida"""
    def __init__(self):
        super().__init__()
        self["ultimo_input"] = None
        self["ruta"] = None

# --- Inicialización ---
def inicializar_db():
    conn = sqlite3.connect("06_memoria.db")
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
    cursor = conn.cursor()
    cursor.execute("INSERT INTO historial (rol, contenido) VALUES (?, ?)", (rol, contenido))
    conn.commit()

def obtener_historial(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT rol, contenido FROM historial ORDER BY id ASC")
    return cursor.fetchall()

# --- Inicialización de FAISS ---
def inicializar_faiss():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    dimension = model.get_sentence_embedding_dimension()
    index = faiss.IndexFlatL2(dimension)
    return model, index, []

def indexar_texto(model, index, textos, nuevo_texto):
    vector = model.encode([nuevo_texto])
    index.add(np.array(vector).astype("float32"))
    textos.append(nuevo_texto)
    return textos

def buscar_similar(model, index, textos, query, k=2):
    if len(textos) == 0:
        return []
    vector = model.encode([query])
    D, I = index.search(np.array(vector).astype("float32"), k)
    return [textos[i] for i in I[0] if i < len(textos)]

# --- Nodos ---
def nodo_input(state: Estado):
    user_input = input("👤 Usuario: ")
    state["ultimo_input"] = user_input
    guardar_mensaje(state["db"], "usuario", user_input)
    state["textos"] = indexar_texto(state["model"], state["index"], state["textos"], user_input)
    return state

def nodo_llm(state: Estado):
    pregunta = state["ultimo_input"]

    # Búsqueda semántica en memoria
    similares = buscar_similar(state["model"], state["index"], state["textos"], pregunta)
    contexto = " | ".join(similares)

    if "precio" in pregunta.lower():
        respuesta = f"📈 Pregunta detectada: finanzas. Contexto: {contexto}"
        state["ruta"] = "finanzas"
    elif "clima" in pregunta.lower():
        respuesta = f"🌦️ Pregunta detectada: clima. Contexto: {contexto}"
        state["ruta"] = "clima"
    else:
        respuesta = f"💬 Respuesta general. Contexto: {contexto}"
        state["ruta"] = "general"

    guardar_mensaje(state["db"], "agente", respuesta)
    print(respuesta)
    return state

def nodo_finanzas(state: Estado):
    respuesta = "📊 Precio BTC: 42k (ejemplo)."
    guardar_mensaje(state["db"], "agente", respuesta)
    print(respuesta)
    return state

def nodo_clima(state: Estado):
    respuesta = "☀️ Hoy soleado con 25°C (ejemplo)."
    guardar_mensaje(state["db"], "agente", respuesta)
    print(respuesta)
    return state

def nodo_general(state: Estado):
    respuesta = "🤖 Gracias por tu consulta."
    guardar_mensaje(state["db"], "agente", respuesta)
    print(respuesta)
    return state

def nodo_memoria(state: Estado):
    print("\n📜 Historial persistente (SQLite):")
    historial = obtener_historial(state["db"])
    for i, (rol, contenido) in enumerate(historial, 1):
        print(f"{i}. {rol}: {contenido}")
    return state

# --- Grafo ---
workflow = StateGraph(dict)

workflow.add_node("input", nodo_input)
workflow.add_node("llm", nodo_llm)
workflow.add_node("finanzas", nodo_finanzas)
workflow.add_node("clima", nodo_clima)
workflow.add_node("general", nodo_general)
workflow.add_node("memoria", nodo_memoria)

workflow.set_entry_point("input")
workflow.add_edge("input", "llm")

workflow.add_conditional_edges(
    "llm",
    lambda state: state["ruta"],
    {
        "finanzas": "finanzas",
        "clima": "clima",
        "general": "general",
    },
)

workflow.add_edge("finanzas", "memoria")
workflow.add_edge("clima", "memoria")
workflow.add_edge("general", "memoria")
workflow.add_edge("memoria", END)

grafo = workflow.compile()

# --- Ejecución ---
print("=== LangGraph: Memoria híbrida (SQLite + FAISS) ===")
estado = {
    "db": inicializar_db(),
    "model": None,
    "index": None,
    "textos": [],
    "ultimo_input": None,
    "ruta": None
}
estado["model"], estado["index"], estado["textos"] = inicializar_faiss()
grafo.invoke(estado)
